from openalea.vpltk.project.manager import ProjectManager


def test_project_manager_discover():
    pm = ProjectManager()
    pm.discover()
    
    assert len(pm.projects) > 0

    
  

    
