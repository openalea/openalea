from openalea.vpltk.project.manager import ProjectManager


def test_project_manager_discover():
    pm = ProjectManager()
    pm.discover()
    
    assert len(pm.projects) > 0

def test_project_manager_discover_not_add_twice():
    pm = ProjectManager()
    pm.discover()
    
    projects_nb = len(pm.projects)
    pm.discover()
    
    assert len(pm.projects) == projects_nb
  

    
