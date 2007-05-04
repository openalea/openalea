class DebugNode (object) :
    """
    visualea adapter to debug code
    """
    def __call__(self, value) :
        #print self.label,inputs[0]
        print "deb",value
        return value


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


