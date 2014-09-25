
import unittest
from openalea.core.unittest_tools import TestCase, EventTracker

from openalea.core.path import tempdir
from openalea.core.path import path as Path
from openalea.core.project.project import Project
from openalea.oalab.service.data import DataFactory
from openalea.core.observer import AbstractListener
import re


def get_data(filename):
    return Path(__file__).parent.abspath() / 'data' / filename

class TestProject(TestCase):

    def setUp(self):
        self.tmpdir = tempdir()
        self.project = Project(self.tmpdir / 'test', alias='test')
        self.ev = EventTracker()
        self.project.register_listener(self.ev)

    def tearDown(self):
        self.project = None
        self.tmpdir.rmtree()

    def test_path_incompatibility(self):
        model = DataFactory(path=get_data('model.py'))
        model2 = self.project.add('model', model)
        events = self.ev.events
        self.check_events(events, ['data_added', 'project_changed'])

        assert model is not model2
        assert model2.path == self.project.path / 'model' / 'model.py'

    def test_autocreate_category_dir(self):
        # Project exists on disk
        #########################

        # Add data object created from scratch in a project existing on disk
        project = Project(self.tmpdir / 'test1', alias='test')
        project.save()
        d1 = project.add('data', filename='image_1.tiff', content=b'')
        assert d1.path.exists()

        # Add an existing data in a project existing on disk
        project = Project(self.tmpdir / 'test2', alias='test')
        project.save()
        d1 = project.add('data', path=get_data('image_2.tiff'))
        assert d1.path.exists()
        assert d1.path.parent == project.path / 'data'

        # Project don't exists on disk
        ##############################

        # Add data object created from scratch in a project NOT existing on disk
        project = Project(self.tmpdir / 'test3', alias='test')
        d1 = project.add('data', filename='image_1.tiff', content=b'')
        assert d1.path.exists() is False

        # Add an existing data in a project NOT existing on disk
        project = Project(self.tmpdir / 'test4', alias='test')
        d1 = project.add('data', path=get_data('image_2.tiff'))
        assert d1.path.exists() is False
        assert d1.path.parent == project.path / 'data'

    def test_add_item(self):
        # Create new data from scratch
        d1 = self.project.add('data', filename='image_1.tiff', content=b'')
        assert d1.path.name == 'image_1.tiff'
        events = self.ev.events
        self.check_events(events, ['data_added', 'project_changed'])

        # Create new data and get content and name from existing file
        d2 = self.project.add('data', path=get_data('image_2.tiff'))
        assert d2.path.name == 'image_2.tiff'
        events = self.ev.events
        self.check_events(events, ['data_added', 'project_changed'])

        # Create new data with explicit filename and get content from existing file
        # Warning: in this test, extension is changed
        d3 = self.project.add('data', path=get_data('image.jpg'), filename='image_4.jpeg')
        assert d3.path.name == 'image_4.jpeg'
        events = self.ev.events
        self.check_events(events, ['data_added', 'project_changed'])

        for data in [d1, d2, d3]:
            assert data.path.parent == self.project.path / 'data'

        assert len(self.project.data) == 3

    def test_add_exceptions(self):

        # Case of path passed doesn't exist
        with self.assertRaises(ValueError) as cm:
            self.project.add('data', path='/do/not/exist.err')

        msg = "path '/do/not/exist.err' doesn't exists"
        self.assertEqual(cm.exception.message, msg)
        assert(len(self.project.data) == 0)

        # Case nothing is defined
        with self.assertRaises(ValueError) as cm:
            self.project.add('data')

        msg = "path or filename required"
        self.assertEqual(cm.exception.message, msg)
        assert(len(self.project.data) == 0)

        # Case user give an existing path and a content
        with self.assertRaises(ValueError) as cm:
            self.project.add('data', path=get_data('image.jpg'), content=b'')

        msg = "got multiple values for content (parameter and 'image.jpg')"
        self.assertEqual(cm.exception.message, msg)
        assert(len(self.project.data) == 0)

        # Add an object twice
        self.project.add('data', filename='image.png')
        with self.assertRaises(ValueError) as cm:
            self.project.add('data', filename='image.png')

        msg = "data 'image.png' already exists in project 'test'"
        self.assertEqual(cm.exception.message, msg)

    def test_add_model(self):

        m1 = self.project.add('model', filename='model_1.py', datatype='python', content='print 1')
        self.assertEqual(m1.read(), 'print 1')
        assert str(m1.filename) == 'model_1.py'
        assert m1.path == self.project.path / 'model' / 'model_1.py'
        events = self.ev.events
        self.check_events(events, ['data_added', 'project_changed'])

        m2 = self.project.add('model', filename='model_2.py', content='print 2')
        assert m2.read() == 'print 2'
        assert str(m2.filename) == 'model_2.py'
        assert m2.path == self.project.path / 'model' / 'model_2.py'
        events = self.ev.events
        self.check_events(events, ['data_added', 'project_changed'])

        sample = get_data('model.py')
        f = open(sample)
        code = f.read()
        f.close()

        m3 = self.project.add('model', path=sample)
        assert str(m3.filename) == 'model.py'
        assert m3.path == self.project.path / 'model' / 'model.py'
        self.assertEqual(m3.read(), code)
        events = self.ev.events
        self.check_events(events, ['data_added', 'project_changed'])

        m4 = self.project.add('model', filename='model_4.py', datatype='py', content='print 4')
        assert m4.read() == 'print 4'
        assert str(m4.filename) == 'model_4.py'
        assert m4.path == self.project.path / 'model' / 'model_4.py'
        events = self.ev.events
        self.check_events(events, ['data_added', 'project_changed'])

        # Check object is a valid model
        # for model in [m1, m2, m3, m4]:
        #     assert hasattr(model, 'run')
        #     assert model.mimetype == 'text/x-python'

    def test_load(self):
        project = Project(get_data('test_project_lpy'))
        project.register_listener(self.ev)
        assert len(project.model) == 1
        assert len(project.cache) == 4
        assert len(project.startup) == 1
        assert 'noise_branch-2d.lpy' in project.model
        events = self.ev.events
        # self.check_events(events, ['project_loaded', 'project_changed'])

    def test_save(self):
        proj = self.project
        model1 = proj.add("model", filename="plop.py", content="print 'plop world'")
        model2 = proj.add("model", path=get_data('model.py'), mode=proj.MODE_LINK)
        events = self.ev.events # clear events

        proj.save()
        events = self.ev.events
        self.check_events(events, ['project_saved'])
        assert len(proj.model) == 2


        proj2 = Project(self.tmpdir / 'test')
        assert len(proj2.model) == 2
        # assert len(proj2.control) == 2
        # assert proj2.control["my_integer"] == 42
        # assert proj2.control["my_float"] == 3.14
        self.assertEqual(proj2.model["plop.py"].read(), "print 'plop world'")
        self.assertEqual(proj2.model["model.py"].read(), "print 'hello world'\n")

    def test_get_model(self):
        self.project.add("model", filename="1.py",)
        model = self.project.get_model('1')
        assert model.filename == '1.py'

        model = self.project.get_model('1.py')
        assert model.filename == '1.py'

        self.project.add("model", filename="1.lpy")


        # Case datatype is not defined
        with self.assertRaises(ValueError) as cm:
            model = self.project.get_model('1')

        msg = "2 model have basename '1': '1.py', '1.lpy'"
        self.assertEqual(cm.exception.message, msg)

        model = self.project.get_model('1.py')
        assert model.filename == '1.py'




    def test_add_script(self):
        self.project.add("model", filename="1.py", content="blablabla")
        self.project.add("model", filename="2.py", content="blablabla2")
#         self.project.add("model", filename="2.py", content="blablabla2")
        assert len(self.project.model) == 2

    def test_rename_item(self):
        self.project.add("model", filename="1.py", content="blablabla")

        model1_path = self.project.path / 'model' / '1.py'
        self.assertEqual(self.project.get('model', '1.py').path, model1_path)

        events = self.ev.events # clear events
        self.project.rename_item("model", "1.py", "2.py")
        assert len(self.project.model) == 1
        assert "2.py" in self.project.model
        assert self.project.model["2.py"].read() == "blablabla"
        assert self.project.model["2.py"].filename == "2.py"
        events = self.ev.events
        self.check_events(events, ['data_renamed', 'project_changed'])


        # Old bug, path lost extension at rename
        model2_badpath = self.project.path / 'model' / '2'
        assert model2_badpath.exists() is False

        msg = "You must give filename only, not path"

        with self.assertRaises(ValueError) as cm:
            self.project.rename_item("model", self.project.path / "model" / "1.py", "2.py")
        self.assertEqual(cm.exception.message, msg)

        with self.assertRaises(ValueError) as cm:
            self.project.rename_item("model", "1.py", self.project.path / "model" / "2.py")
        self.assertEqual(cm.exception.message, msg)

        with self.assertRaises(ValueError) as cm:
            self.project.rename_item("model", "model/1.py", "2.py")
        self.assertEqual(cm.exception.message, msg)

        with self.assertRaises(ValueError) as cm:
            self.project.rename_item("model", "1.py", "model/2.py")
        self.assertEqual(cm.exception.message, msg)


    def test_move_project(self):
        self.project.add("model", filename="1.py", content="blablabla")
        old_path = self.project.path
        tmpdir2 = tempdir()

        events = self.ev.events # clear events

        self.project.move(tmpdir2/"test2")
        assert old_path.exists() is False
        assert self.project.path != old_path
        assert self.project.name == "test2"
        assert self.project.name == "test2"
        events = self.ev.events
        self.check_events(events, ['project_moved', 'project_changed'])

        old_dir = self.project.projectdir
        self.project.rename("test3")
        assert self.project.name == "test3"
        assert self.project.projectdir == old_dir
        events = self.ev.events
        self.check_events(events, ['project_moved', 'project_changed'])

    def test_set_attr_err(self):
        with self.assertRaises(NameError) as cm:
            self.project.model = dict()

        msg = "cannot change 'model' attribute"
        self.assertEqual(cm.exception.message, msg)

    def test_get_attr(self):
        model1 = self.project.add("model", filename="1.py", content="blablabla")
        model2 = self.project.model
        model2 = model2.values()[0]
        assert model1.read() == model2.read()

    def test_repr(self):
        msg = "Project(%r)" % str(self.project.path)
        self.assertEqual(repr(self.project), msg)

    def test_remove_item(self):
        self.project.add("model", filename="1.py", content="blablabla")
        self.project.save()
        assert len(self.project.model) == 1
        assert (self.project.path / "model" / "1.py").exists()

        events = self.ev.events # clear events
        self.project.remove_item("model", filename="1.py")
        events = self.ev.events
        self.check_events(events, ['data_removed', 'project_changed'])

        assert len(self.project.model) == 0
        assert (self.project.path / "model" / "1.py").exists()

