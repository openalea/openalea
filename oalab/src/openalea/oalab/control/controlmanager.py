from collections import OrderedDict

class ControlManager(object):
    """ Manage controls """
    def __init__(self):
        self.controls = OrderedDict()

    def new_control(self, name):
        """ Create and register a default empty control
        
        :param name:  name of the control to register (must be a string)
        """
        control=''
        self.controls[name]=control
        
    def add_control(self, name, control):
        """ Register a control in the ControlManager 
        
        :param name: name of the control to register (must be a string)
        :param control: control to register
        """
        name = self._check_if_name_is_unique(name)
        self.controls[name]=control

    def get_controls(self):
        """ Return all controls registers in the ControlManager 
        
        :returns: OrderedDict of all controls
        """
        return self.controls

    def get_control(self, name):
        """ Return control by name
        
        :param name: name of the control that you are searching
        :return: the control if it exists in the control manager. Else, returns '-1'
        """
        if name in self.controls:
            return self.controls[name]
        else:
            return -1   
        
    def load(self):
        """ Not implemented yet 
        
        .. todo:: Implement
        """
        pass

    def save(self):
        """ Not implemented yet 
        
        .. todo:: Implement
        """
        pass        

    def _check_if_name_is_unique(self, name):
        """ Check if a control with the same name 'name' is alreadey register
        in the control manager.
        If it is the case, the name is changed ("_1" is append).
        This is realize until the name becomes unique."""
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
    """ Fake Abstract Base Class for controls
        
    .. todo:: Realize a real ABC
    """
    def __init__(self):
        pass

    def edit(self):
        """ Not implemented yet 
        
        .. todo:: Implement
        """
        pass
        
    def copy(self, control):
        """ Not implemented yet 
        
        .. todo:: Implement
        """
        pass
        
    def display(self):
        """ Not implemented yet 
        
        .. todo:: Implement
        """
        pass
 
 
def main():
    """ Example of how to use control manager """ 
    class ControlExample(ControlABC):
        """ Empty class Control for test """
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
 