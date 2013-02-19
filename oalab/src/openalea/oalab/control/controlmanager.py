from collections import OrderedDict

class ControlManager(object):
    """ Manage controls """
    def __init__(self):
        # Initialize the dictionnary wich contain the controls registered
        self.controls = OrderedDict()

    def new_control(self, name):
        # Create and register a default empty control with the name 'name'
        control=''
        self.controls[name]=control
        
    def add_control(self, name, control):
        # Register a control 'control' with name 'name' in the ControlManager
        name = self._check_if_name_is_unique(name)
        self.controls[name]=control

    def get_controls(self):
        # Return all controls registers in the ControlManager
        return self.controls

    def get_control(self, name):
        # Return control by name
        # If they are no controls named "name" registered, return '-1'
        if name in self.controls:
            return self.controls[name]
        else:
            return -1   

    def list_possibilities(self):
        pass        
        
    def load(self):
        pass

    def save(self):
        pass        

    def _check_if_name_is_unique(self, name):
        # Check if a control with the same name 'name' is alreadey register
        # in the control manager.
        # If it is the case, the name is changed ("_1" is append).
        # This is realize until the name becomes unique.
        while name in self.controls:
            try:
                end = name.split("_")[-1]
                l = len(end)
                end = int(end)
                end += 1
                name = name[0:-l] + str(end)
            except:    
                name += "_1"
        return name    
        
        
class ControlABC(object):
    """ Abstract Base Class for controls """
    def __init__(self):
        pass

    def edit(self):
        pass
        
    def copy(self, control):
        pass
        
    def display(self):
        pass
 
 
def main():

    class ControlExample(ControlABC):
        # Empty class Control for test
        def __init__(self):
            pass

    CM = ControlManager()
    CM.new_control("test1")
    C = ControlExample()
    CM.add_control("test2",C)
    
    print "We must have 2 controls registered in control manager"
    print "Here, we have:"
    for c in CM.get_controls(): print c,  CM.get_controls()[c]

    
if( __name__ == "__main__"):
    main()
 