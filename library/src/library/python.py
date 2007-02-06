# -*- python -*-
#
#       OpenAlea.Core.Library: OpenAlea Core Library module
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
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
Data Node
"""

__license__= "Cecill-C"
__revision__=" $Id: simple_models.py 331 2007-02-02 15:50:47Z dufourko $ "


from openalea.core import *



class SetItem(Node):
    """
    Python __setitem__
    """

    def __init__(self):

        Node.__init__(self)
        self.add_input( name = "obj", interface = None, value = None)
        self.add_input( name = "param1", interface = None, value = None)
        self.add_input( name = "param2", interface = None, value = None) 
        self.add_output( name = "obj", interface = None) 
                

    def __call__(self, inputs):
        """ inputs is the list of input values """

        obj = inputs[0]
        p1 = inputs[1]
        p2 = inputs[2]
        ret = obj.__setitem__(p1,p2)
        return (obj , )


class GetItem(Node):
    """
    Python __getitem__
    """

    def __init__(self):

        Node.__init__(self)
        self.add_input( name = "obj", interface = None, value = None)
        self.add_input( name = "param1", interface = None, value = None)
        self.add_output( name = "result", interface = None) 

    def __call__(self, inputs):
        """ inputs is the list of input values """

        obj = inputs[0]
        p1 = inputs[1]
        ret = obj.__getitem__(p1)
        return (ret, )



class Append(Node):
    """
    Python append
    """

    def __init__(self):

        Node.__init__(self)
        self.add_input( name = "obj", interface = ISequence, value = [])
        self.add_input( name = "append", interface = None, value = None)
        self.add_output( name = "result", interface = None) 

    def __call__(self, inputs):
        """ inputs is the list of input values """

        obj = inputs[0]
        p1 = inputs[1]
        obj.append(p1)
        return (obj, )
