from openalea.core import Node

class DebugNode (Node) :
    """
    visualea adapter to debug code
    """
    def __init__ (self) :
        Node.__init__(self)
        self.add_input( name = "in", interface = None, value=None)
        self.add_output( name = "out", interface = None)
        #self.label="deb"
        #self.set_caption(self.label)
    
    def __call__(self, inputs) :
        #print self.label,inputs[0]
        print "deb", inputs[0]
        return inputs


class CidNode (object) :
    """
    visualea adapter to send cell scale
    """
    def __call__ (self) :
        return 0

class WidNode (object) :
    """
    visualea adapter to send wall scale
    """
    def __call__ (self) :
        return 1

class EidNode (object) :
    """
    visualea adapter to send edge scale
    """
    def __call__ (self) :
        return 2


