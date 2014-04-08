from openalea.vpltk.project.manager import ProjectManager


def test_project_manager_discover():
    pm = ProjectManager()
    pm.discover()
    
    assert len(pm.projects) > 0

def test_project_manager_discover_not_add_twice_by_discover_twice():
    pm = ProjectManager()
    pm.discover()
    
    projects_nb = len(pm.projects)
    pm.discover()
    
    assert len(pm.projects) == projects_nb
  
def test_project_manager_discover_not_add_twice():
    pm = ProjectManager()
    pm.discover()
    
    nb = len(pm.projects)
    nb2 = int(nb/2)
    assert nb > 1
    assert nb2 > 0
    assert str(pm.projects[nb-1].name) != str(pm.projects[nb2-1].name)

    
