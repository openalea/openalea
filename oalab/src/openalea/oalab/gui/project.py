
class ProjectManager(object):
    def __init__(self):
        self.current_path = None
        self.current_file_name = None
        self.current_extension = None
        self.current_path_and_fname = None
        self.currentProject = None
        self.currentFile = None
        self.projects = []
        
    def new_project(self, fname=None):
        i = len(self.projects)
        self.currentProject = Project()
        self.projects.append(self.currentProject)       


class Project(object):
    def __init__(self):
        pass
        