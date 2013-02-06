class ProjectManager(object):
    def __init__(self):
        self.projects=[]
        self.currentProject=None

    def new_project(self, fname=None):
        i = len(self.projects)
        self.currentProject = Project(fname)
        self.currentProject.id(i)
        self.projects.append(self.currentProject)
        
    def open_project(self, fname=None):
        pass
        
    def current(self, id=0):
        self.currentProject = self.get_by_id(id)
        
    def get_current(self):  
        return self.currentProject

    def get_all(self):  
        return self.projects
        
    def get_by_id(self, id):    
        for i in self.projects:
            if i.get_id() == id:
                return i
        return -1  

    def del_current(self):
        i = self.get_current().get_id()
        print i
        self.del_by_id(id=i)
    
    def del_by_id(self, id):
        del self.projects[id]
        
        
        
class Project(object):
    def __init__(self, fname=None):
        # New Project
        self.name(fname)

    def name(self, fname):
        self.name = fname
        
    def id(self, id):
        self.id = id
        
    def get_id(self):
        return self.id

    def open(self, fname=None):
        pass
                
    def save(self):
        pass
        
    def close(self):
        del self
        
        
        
        
def main():
    PM = ProjectManager()       # Create Project Manager
    
    PM.new_project("proj1")     # Add 3 projects in PM
    PM.new_project("proj5")
    PM.new_project("proj2")

    PM.current(id=1)            # Set proj5 current
    PM.del_current()            # Close current project
    
    print("We have %i projects in project manager" %len(PM.get_all()))  
    print "Normally, we have proj1 and proj2"
    for n in PM.get_all():
        print n.name   

    
if( __name__ == "__main__"):
    main()
        