from openalea.vpltk.project.manager import ProjectManager
from openalea.vpltk.project.project import Project
from openalea.core.path import path, tempdir
import shutil


def test_import_project():
    from openalea.vpltk.project import Project, ProjectManager
    assert Project is not None
    assert ProjectManager is not None


def test_load():
    pm = ProjectManager()
    current_path = path('.')
    proj = pm.load(name='test_project_lpy', path=current_path / 'data') # load in globals context and python as startup

    for category in ["src", "cache", "scene", "startup"]:
        assert hasattr(proj, category)

    for metadata in ["name", "icon", "author", "description", "version", "license", "dependencies"]:
        assert metadata in proj.metadata

    assert len(proj.src.keys()) == 1
    assert len(proj.cache.keys()) == 4
    assert len(proj.startup.keys()) == 1


def test_manifest():
    pm = ProjectManager()
    proj = pm.load('test_project_lpy', 'data')
    proj.load_manifest()
    assert len(proj.src) == 1
    assert len(proj.cache) == 4
    assert len(proj.startup) == 1


def test_save_project():
    pm = ProjectManager()

    # Work in temporary directory
    tmpprojectdir = tempdir()

    proj = pm.create('my_new_temp_project', tmpprojectdir)
    proj.add("model", "plop.py", "print 'hello world'")
    # proj.control["my_integer"] = 42
    # proj.control["my_float"] = 3.14
    proj.save()

    assert len(proj.src) == 1
    # assert len(proj.control) == 2

    pm.close('my_new_temp_project')
    proj2 = pm.load('my_new_temp_project', tmpprojectdir)

    assert len(proj2.src) == 1
    # assert len(proj2.control) == 2
    # assert proj2.control["my_integer"] == 42
    # assert proj2.control["my_float"] == 3.14
    assert proj2.src["plop"].code == "print 'hello world'"

    pm.close('my_new_temp_project')

    # Delete temporary dir
    tmpprojectdir.rmtree()


def test_add_script():
    pm = ProjectManager()
    proj = pm.create('my_new_temp_project', path("data"))
    proj.add("model", "1.py", "blablabla")
    proj.add("model", "2.py", "blablabla2")
    proj.add("model", "3.py", "blablabla3")
    proj.add("model", "4.py", "blablabla4")
    assert len(proj.models()) == 4
    assert proj.is_project() is True
    assert proj.is_script() is False


def test_rename():
    tmpprojectdir = tempdir()

    pm = ProjectManager()
    proj = pm.create('my_new_temp_project', tmpprojectdir)
    proj.add("model", "1.py", "blablabla")

    model1_path = proj.path / 'model' / '1.py'
    model2_path = proj.path / 'model' / '2.py'

    assert model1_path.isfile()

    proj.rename("model", "1", "2")
    assert len(proj.src) == 1
    assert proj.src["2"].repr_code() == "blablabla"

    # Old bug, path lost extension at rename
    model2_badpath = proj.path / 'model' / '2'
    assert model2_badpath.exists() is False
    assert model2_path.isfile()


    tmpprojectdir.rmtree()

def test_rename_project():
    pm = ProjectManager()
    proj = pm.create('my_new_temp_project', path("data"))
    proj.add("model", "1.py", "blablabla")
    proj.rename("project", "my_new_temp_project", "new_name")
    assert proj.name == "new_name"

#######################################################
# New API
#######################################################



def test_create_project():
    proj = Project('my_new_temp_project', path("data"))

    for category in ["name", "icon", "author", "description", "version", "license", "dependencies"]:
        assert proj.metadata.has_key(category)


def test_add():
    proj = Project('my_new_temp_project', path("data"))
    proj.add("fake_category", "fake_name", "fake_value")

    assert hasattr(proj, "fake_category")
    assert proj.fake_category["fake_name"] == "fake_value"


def test_get():
    proj = Project('my_new_temp_project', path("data"))

#     proj.add(category="src", name="test_name", value="test_value")
#     proj.add(category="answer", name="the Ultimate Question of Life, the Universe, and Everything", value=42)

#     assert proj.get(category="src", name="test_name") == "test_value"
#     assert proj.get(category="answer", name="the Ultimate Question of Life, the Universe, and Everything") == 42
