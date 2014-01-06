from openalea.vpltk.project.project import ProjectManager
from path import path
import shutil
import os

def test_load():
    pm = ProjectManager()
    fn = path("data")/"test_project_lpy"/"scripts"/"noise_branch-2d.lpy" # remove python & context
    current_path = path('.')
    proj = pm.load('test_project_lpy',current_path/'data') # load in globals context and python as startup

    assert hasattr(proj,"scripts") 
    assert hasattr(proj,"cache") 
    assert hasattr(proj,"controls") 
    assert hasattr(proj,"ns") 
    assert hasattr(proj,"scene") 
    assert hasattr(proj,"startup") 
    assert hasattr(proj,"shell") 
    assert len(proj.scripts) == 1
    assert len(proj.cache) == 4
    assert len(proj.controls) == 0
    assert len(proj.scene) == 0
    assert len(proj.startup) == 1

    assert isinstance(proj.ns["radius.py"], int)
    
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

def test_create_project():
    pm = ProjectManager()
    name = path("data")/"my_new_temp_project"
    if name.exists():
        shutil.rmtree(name)
    proj = pm.create('my_new_temp_project', path("data"))
    listdir = os.listdir(proj.path/proj.name)
    assert len(listdir) == 5
    
    shutil.rmtree(name)     
    
    
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
    shutil.rmtree( path("data")/"my_new_temp_project")  
	
def test_rename():
    pm = ProjectManager()
    proj = pm.create('my_new_temp_project', path("data"))
    proj.add_script("1", "blablabla")
    proj.rename("scripts", "1","2")
    assert len(proj.scripts) == 1
    assert proj.scripts["2"] == "blablabla"
    
    shutil.rmtree( path("data")/"my_new_temp_project")  

    
