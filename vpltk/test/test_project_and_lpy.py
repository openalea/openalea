from openalea.lpy import Lsystem,AxialTree,generateScene
from openalea.lpy_wralea.lpy_nodes import run_lpy
from openalea.vpltk.project.manager import ProjectManager
from openalea.core.path import path
import os

# def test_load_project_1():
#     # reference
#     fn = path("data")/"noise_branch-2d.lpy"
#     tree, lsys = run_lpy(str(fn))
#
#     pm = ProjectManager()
#     fn = path("data")/"test_project_lpy"/"src"/"noise_branch-2d.lpy" # remove python & context
#     proj = pm.load('test_project_lpy','data') # load in globals context and python as startup
#     l = Lsystem(str(fn), proj.ns)
#     tree2 = l.iterate()
#
#     assert len(tree) == len(tree2)
#

# def test_load_project_2():
#     fn = "data/noise_branch-2d.lpy"
#     tree, lsys = run_lpy(fn)
#
#     pm = ProjectManager()
#     fn = path("data")/"test_project_lpy"/"src"/"noise_branch-2d.lpy" # remove python & context
#     proj = pm.load('test_project_lpy','data') # load in globals context and python as startup
#     tree2, lsys2 = run_lpy(str(fn), parameters=proj.ns)
#
#     assert len(tree) == len(tree2)
#
#
# def test_load_project_3():
#     fn = "data/noise_branch-2d.lpy"
#     tree, lsys = run_lpy(fn)
#
#     pm = ProjectManager()
#     proj = pm.load('test_project_lpy','data') # load in globals context and python as startup
#
#     for s in proj.src:
#         script_filename = proj.projectdir/proj.name/'src'/s
#     tree2, lsys2 = run_lpy(str(script_filename), parameters=proj.ns)
#
#     assert len(tree) == len(tree2)
    
    
# def test_load_and_open_project():
#     fn = "data/noise_branch-2d.lpy"
#     tree, lsys = run_lpy(fn)
#
#     pm = ProjectManager()
#     proj = pm.load('test_project_lpy','data')
#
#     for s in proj.src:
#         script_filename = proj.projectdir/proj.name/'src'/s
#
#     code = open(script_filename).read()
#
#     file = open('mytemp.lpy', "w")
#     file.write(code)
#     file.close()
#
#     tree2, lsys2 = run_lpy('mytemp.lpy', parameters=proj.ns)
#
#     os.remove('mytemp.lpy')
#
#
#     assert len(tree) == len(tree2)
