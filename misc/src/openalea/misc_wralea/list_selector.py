from openalea.core import Node

class Select(Node):
    def __init__(self, in_list, out_list):
        Node.__init__(self, in_list, out_list)        
        self.out_indices = []    
        
    def __call__(self, inputs):
        # The out_list has been modified by the widget
        # If in_list have been changed, or there is no widget, the return in_list 
        in_list = inputs[0]

        if len(in_list) != len(self.out_indices):
            print 'ERROR: out', self.out_indices
            print 'in ', in_list
            return in_list
        return [in_list[i] for i, select in enumerate(self.out_indices) if select],

 
