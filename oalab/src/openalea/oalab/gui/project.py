
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
        self.currentProject = Project(self,i,fname)
        self.projects.append(self.currentProject)
        self.currentProject.currentFile = self.currentProject.new_file()
        


class Project(object):
    # self.currentProjectID = None

    def __init__(self,widget,index = 0, fname = None):
        pass

    def new_file(self):
        self.new_python_script()

    def new_python_script(self):
        pass
        
    def new_lpy_script(self):
        pass

    def new_workflow(self):
        pass
