from openalea.vpltk.project.manager import ProjectManager
from openalea.vpltk.project.project import Project
from openalea.core.path import path
import shutil
import os

def test_load():
    pm = ProjectManager()
    fn = path("data")/"test_project_lpy"/"scripts"/"noise_branch-2d.lpy" # remove python & context
    current_path = path('.')
    proj = pm.load('test_project_lpy',current_path/'data') # load in globals context and python as startup

    for category in ["scripts", "cache", "controls", "ns", "scene", "startup", "shell"]:
        assert hasattr(proj,category) 
    
    for category in ["name", "path", "icon", "authors", "description", "version", "license", "dependencies"]:
        assert hasattr(proj,category) 

    assert len(proj.scripts) == 1
    assert len(proj.cache) == 4
    assert len(proj.controls) == 0
    assert len(proj.scene) == 0
    assert len(proj.startup) == 1

    assert isinstance(proj.ns["radius"], int)
    
def test_manifest():
    pm = ProjectManager()
    proj = pm.load('test_project_lpy','data')
    manifest = proj._load_manifest()
    assert len(manifest["scripts"]) == 1
    assert len(manifest["cache"]) == 4
    assert len(manifest["controls"]) == 0
    assert len(manifest["scene"]) == 0
    assert len(manifest["startup"]) == 1
    assert len(manifest) == 5
    
def test_save_project():
    pm = ProjectManager()
    name = path("data")/"my_new_temp_project"
    
    if name.exists():
        shutil.rmtree(name)
        
    proj = pm.create('my_new_temp_project', path("data"))
    proj.scripts["plop.py"] = "print 'hello world'"
    proj.controls["my_integer"] = 42
    proj.controls["my_float"] = 3.14
    proj.save()
    
    assert len(proj.ns) == 0
    assert len(proj.scripts) == 1
    assert len(proj.controls) == 2
    
    pm.close('my_new_temp_project')
    proj2 = pm.load('my_new_temp_project', path("data"))
    
    assert len(proj2.ns) == 0
    assert len(proj2.scripts) == 1
    assert len(proj2.controls) == 2
    assert proj2.controls["my_integer"] == 42
    assert proj2.controls["my_float"] == 3.14
    assert proj2.scripts["plop.py"] == "print 'hello world'"
    
    pm.close('my_new_temp_project')
    shutil.rmtree(name)

def test_add_script():
    name = path("data")/"my_new_temp_project"
    pm = ProjectManager()
    proj = pm.create('my_new_temp_project', path("data"))
    proj.add_script("1", "blablabla")
    proj.add_script("2", "blablabla2")
    proj.add_script("3", "blablabla3")
    proj.add_script("4", "blablabla4")
    assert len(proj.scripts) == 4
    assert proj.is_project() is True
    assert proj.is_script() is False
	
def test_rename():
    pm = ProjectManager()
    proj = pm.create('my_new_temp_project', path("data"))
    proj.add_script("1", "blablabla")
    proj.rename("scripts", "1","2")
    assert len(proj.scripts) == 1
    assert proj.scripts["2"] == "blablabla"

#######################################################
# New API
#######################################################

def test_create_project_from_manager():
    pm = ProjectManager()
    name = path("data")/"my_new_temp_project"
    proj = pm.create('my_new_temp_project', path("data"))

    for category in ["name", "path", "icon", "authors", "description", "version", "license", "dependencies"]:
        assert hasattr(proj,category) 
    
def test_create_project():
    proj = Project('my_new_temp_project', path("data"))
    
    for category in ["name", "path", "icon", "authors", "description", "version", "license", "dependencies"]:
        assert hasattr(proj,category)     

def test_add():
    name = path("data")/"my_new_temp_project"
    proj = Project('my_new_temp_project', path("data"))
    proj.add("fake_category", "fake_name", "fake_value")
    
    assert hasattr(proj,"fake_category")   
    assert proj.fake_category["fake_name"] == "fake_value"    

def test_get():
    proj = Project('my_new_temp_project', path("data"))
    
    proj.add(category="scripts", name="test_name", value="test_value")
    proj.add(category="answer", name="the Ultimate Question of Life, the Universe, and Everything", value=42)
    
    assert proj.get(category="scripts", name="test_name") == "test_value"
    assert proj.get(category="answer", name="the Ultimate Question of Life, the Universe, and Everything") == 42
