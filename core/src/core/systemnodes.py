# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2007 INRIA - CIRAD - INRA  
#
#       File author(s): Christophe Pradal <christophe.prada@cirad.fr>
#                       Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#


__doc__="""
System Nodes
"""

__license__= "Cecill-C"
__revision__=" $Id$ "


from openalea.core.node import AbstractNode, Node


class AnnotationNode(AbstractNode):
    """ A DummyNode is a fake node."""

    __graphitem__ = "annotation.Annotation"

    def get_nb_input(self):
        """ Return the nb of input ports """
        return 0

    
    def get_nb_output(self):
        """ Return the nb of output ports """
        return 0

    def eval(self):
        return False


class IterNode(Node):
    """ Iteration Node """

    def __init__(self, *args):
        """ Constructor """

        Node.__init__(self, *args)
        self.iterable = "Empty"

        
    def eval(self):
        """
        Return True if the node need a reevaluation
        """
        try:
            if self.iterable == "Empty":
                self.iterable = iter(self.inputs[0])

            if(hasattr(self, "nextval")):
               self.outputs[0] = self.nextval
            else:
                self.outputs[0] = self.iterable.next()

            self.nextval = self.iterable.next()
            return True

            
        except TypeError, e:
            self.outputs[0] = self.inputs[0]
            return False
        
        except StopIteration, e:
            self.iterable = "Empty"
            if(hasattr(self, "nextval")):
                del self.nextval
            return False



class RDVNode(Node):
    """
    Rendez Vous node (synchronisation)
    In1 : Value
    In2 : Unused (control flow)
    Out : Value
    """

    def __call__(self, inputs):
        """ inputs is the list of input values """
        return inputs


from openalea.core.datapool import DataPool

class PoolReader(Node):
    """
In : Name (key)
Out : Object (value)
    """

    def __init__(self, inputs, outputs):

        Node.__init__(self, inputs, outputs)
        self.pool = DataPool()


    def __call__(self, inputs):
        """ inputs is the list of input values """

        key = inputs[0]
        obj = self.pool.get(key)
        if key in self.pool:
            self.set_caption("pool [%s]"%(repr(key),))
        return (obj, )


class PoolWriter(Node):
    """
In :  Name (String), Object (Any)
    """

    def __init__(self, inputs, outputs):

        Node.__init__(self, inputs, outputs)
        self.pool = DataPool()


    def __call__(self, inputs):
        """ inputs is the list of input values """

        key = inputs[0]
        obj = inputs[1]
        self.set_caption("pool [%s]=%s"%(repr(key),str(obj)))
        self.pool[key] = obj


class InitNode(Node):
    """
In0 : Init value
In1 : Current Value
In2 : State (Bool)

If state is true, return In0, else return In1
state is set to false in the first execution.
    """


    def __call__(self, inputs):
        """ inputs is the list of input values """

        state = inputs[2]

        if(state):
            ret = inputs[0]
        else :
            ret = inputs[1]

        self.set_input(2, False)
        return (ret,)


    def reset(self):
        Node.reset(self)
        self.set_input(2, True)
        
            



class AccuList(Node):
    """ List Accumulator
    Add to a list (in datapool) the receive value
    Inputs : value : value to append
             var_name : name of the datapool variable
    """

    def __init__(self, inputs, outputs):

        Node.__init__(self, inputs, outputs)
        self.pool = DataPool()


    def __call__(self,inputs):

        varname = inputs[1]
        value = inputs[0]
        if(not varname):
            varname = "AccuList_%i"%(id(self))
            
        # Create datapool variable if necessary
        if(not self.pool.has_key(varname) or
           not isinstance(self.pool[varname], list)):
            l = list()
            self.pool[varname] = l
        else:
            l = self.pool[varname]

        self.set_caption("list accumulator : %s"%(repr(str(varname))))
        l.append(value)
        
        return (l,)
        

class AccuFloat(Node):
    """ Float Accumulator
    Add to a Float (in datapool) the receive value
    Inputs : value : value to append
             var_name : name of the datapool variable
    """

    def __init__(self, inputs, outputs):

        Node.__init__(self, inputs, outputs)
        self.pool = DataPool()


    def __call__(self,inputs):

        varname = inputs[1]
        value = inputs[0]
        if(not varname):
            varname = "AccuFloat_%i"%(id(self))
            
        # Create datapool variable if necessary
        if(not self.pool.has_key(varname) or
           not isinstance(self.pool[varname], float)):
            self.pool[varname] = 0.

        self.set_caption("float accumulator : %s"%(repr(str(varname))))
        self.pool[varname] += float(value)
        return (self.pool[varname],)


