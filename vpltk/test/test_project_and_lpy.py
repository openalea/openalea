from openalea.vpltk.qt import qt

from openalea.lpy import Lsystem,AxialTree,generateScene
from openalea.lpy_wralea.lpy_nodes import run_lpy
from openalea.vpltk.project.project import ProjectManager
from path import path
import os
import shutil

def test_load_project_1():
    # reference
    fn = "data/noise_branch-2d.lpy"
    tree, lsys = run_lpy(fn)
 
    pm = ProjectManager()
    fn = "data/test_project_lpy/scripts/noise_branch-2d.lpy" # remove python & context
    current_path = path.abspath(path('.'))
    proj = pm.load('test_project_lpy',current_path/'data') # load in globals context and python as startup
    l = Lsystem(fn, proj.ns)
    tree2 = l.iterate()

    assert len(tree) == len(tree2)
    
    
def test_load_project_2():
    fn = "data/noise_branch-2d.lpy"
    tree, lsys = run_lpy(fn)

    pm = ProjectManager()
    fn = "data/test_project_lpy/scripts/noise_branch-2d.lpy" # remove python & context
    current_path = path.abspath(path('.'))
    proj = pm.load('test_project_lpy',current_path/'data') # load in globals context and python as startup
    tree2, lsys2 = run_lpy(fn, parameters=proj.ns)
    
    assert len(tree) == len(tree2)

    
def test_create_project():
    pm = ProjectManager()
    proj = pm.create('my_new_temp_project')
    listdir = os.listdir(proj.path/proj.name)
    
    assert len(listdir) == 3
    
    shutil.rmtree(proj.path/proj.name)