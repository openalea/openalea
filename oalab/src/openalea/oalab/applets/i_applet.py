

class IApplet(object):

    identifier = '' # Unique identifier
    name = '' # Human readable name
    
    def __init__(self):
        pass
       
    def actions(self):
        """
        Returns a list ["Tab name", [list of actions] ]
        Where "list of action" is a 3-item list : groupname(unicode), action(QAction), button_type(bool: 0 big button, 1 small button)
        
        Example::
        
            def actions(self):
                return self._actions = ["Python IDE", [
                                           ["Text Edit", self.actionUndo,0],
                                           ["Text Edit", self.actionRedo,0]
                                       ]
                                    ]
        """