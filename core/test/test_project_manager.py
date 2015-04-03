
from openalea.core.unittest_tools import TestCase, EventTracker
from openalea.core.path import tempdir
from openalea.core.path import path as Path
from openalea.core.project.project import Project
from openalea.core.project.manager import ProjectManager

pm = ProjectManager()
ev = EventTracker()
# ev.debug = True
pm.register_listener(ev)


def get_data(filename):
    return Path(__file__).parent.abspath() / 'data' / filename


class TestProjectManager(TestCase):

    def setUp(self):
        self.tmpdir = tempdir()
        self.tmpdir2 = tempdir()

        pm.clear()
        # Force to ignore default repositories
        pm.repositories = [self.tmpdir]
        ev.events  # clear events

    def tearDown(self):
        self.tmpdir.rmtree()
        self.tmpdir2.rmtree()

    def create_projects(self):
        """
        tmp1
          - p1
          - p2
          - link -> p2
        tmp2
          - p1
          - p3
          - link -> p4
        """
        project = Project(self.tmpdir / 'p1', alias="p1")
        project.save()

        project = Project(self.tmpdir / 'p2')
        project.save()

        project.path.symlink(self.tmpdir / 'link')

        project = Project(self.tmpdir2 / 'p1', alias="Project 1")
        project.save()

        project = Project(self.tmpdir2 / 'p3')
        project.save()

        project.path.symlink(self.tmpdir2 / 'link')

    def test_create_project_from_manager(self):
        proj = pm.create('new_temp_project', projectdir=self.tmpdir)
        assert proj.projectdir == self.tmpdir
        assert proj.path.name == 'new_temp_project'

    def test_discover(self):
        pm.discover()
        self.assertEqual(pm.projects, [])

        self.create_projects()
        pm.discover()

        directories = sorted([str(path.name) for path in self.tmpdir.listdir()])
        project_dirs = sorted([str(project.path.name) for project in pm.projects])

        # Check that we discover projects in the right repository (tmpdir)
        for project in pm.projects:
            self.assertEqual(project.projectdir, self.tmpdir)

        # Check all directory have been created
        self.assertListEqual(directories, ['link', 'p1', 'p2'])

        # Check symlink has been replaced by right path
        # And check projects are not appended twice
        self.assertListEqual(project_dirs, ['p1', 'p2'])

    def test_repository_added_twice(self):
        # Check if a repository is added twice, projects are discovered only one time
        self.create_projects()
        assert len(pm.repositories) == 1
        pm.repositories.append(self.tmpdir)
        pm.discover()

        assert len(pm.projects) == 2

    def test_search(self):
        self.create_projects()
        pm.repositories.append(self.tmpdir2)
        pm.discover()

        p1a = self.tmpdir / 'p1'
        p2a = self.tmpdir / 'p2'
        p1b = self.tmpdir2 / 'p1'
        p3b = self.tmpdir2 / 'p3'

        assert len(pm.search()) == 4
        proj_p1 = pm.search(name='p1')
        name_p1 = sorted([str(project.path) for project in proj_p1])

        assert len(proj_p1) == 2
        assert len(pm.search(name='p2')) == 1
        self.assertListEqual(name_p1, sorted([str(p1a), str(p1b)]))

        alias_p1 = pm.search(alias='p1')
        self.assertEqual(len(alias_p1), 1)
        self.assertEqual(alias_p1[0].path, self.tmpdir / 'p1')

    def test_load(self):
        self.create_projects()
        pm.repositories.append(self.tmpdir2)
        pm.discover()
        project = pm.load('p2')
        assert project.path == self.tmpdir / 'p2'
        project = pm.load('p1')
        assert project.name == 'p1'
        assert isinstance(project, Project)

    def test_default(self):
        project = pm.default()
        assert str(project.name) == "temp"

    def test_project_updated_event(self):
        project = pm.create('TestProject', self.tmpdir)
        project.save()
        pm.cproject = project
        ev.events  # clear
        project.add('model', filename='newfile.py')
        self.check_events(ev.events, ['project_updated'])

    def test_namespace(self):
        proj = pm.create('new_temp_project', projectdir=self.tmpdir)
        pm.cproject = proj
        user_ns = pm.shell.user_ns

        assert 'project' in user_ns
        assert user_ns['project'].path == proj.path
        assert user_ns['data'] == proj.path / 'data'

        pm.cproject = None
        assert 'project' not in user_ns
        assert 'data' not in user_ns

    def test_world_namespace(self):
        from openalea.core.service.run import namespace
        from openalea.core.model import Model

        proj = pm.create('new_temp_project', projectdir=self.tmpdir)
        user_ns = pm.shell.user_ns

        assert 'world' in user_ns
        w = user_ns['world']
        assert w.keys() == []

        code = "world.add(1, name='i');a=1"
        model = Model()
        proj.add('model', model)
        model.set_code(code)
        model.run(**namespace())

        assert w.keys() == ['i']
        assert w['i'].obj == 1

        pm.cproject = None
        assert 'world' not in user_ns
        assert w.keys() == []
