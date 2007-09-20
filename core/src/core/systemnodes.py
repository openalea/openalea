# -*- python -*-
#
#       OpenAlea.Core.Library: OpenAlea Core Library module
#
#       Copyright 2006 INRIA - CIRAD - INRA  
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
__revision__=" $Id: python.py 604 2007-06-21 17:30:12Z dufourko $ "


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
        self.iterable = None

        
    def eval(self):
        """
        Return True if the node need a reevaluation
        """
        try:
            if(not self.iterable):
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
            self.iterable = None
            return False



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
            self.set_caption(str(key))
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
        self.set_caption(str(key)+' : '+str(obj))
        self.pool[key] = obj



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
            self.pool[varname] = list()

        self.pool[varname].append(value)
        

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

        self.pool[varname] += float(value)


