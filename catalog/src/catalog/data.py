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
Data Node
"""

__license__= "Cecill-C"
__revision__=" $Id$ "


from openalea.core import *


class InputFile(Node):
    """
A file path
Out :  the file path string
    """

    def __call__(self, inputs):
        """ inputs is the list of input values """

        return ( str(inputs[0]),  )



class Bool(Node):
    """
Boolean value
Out :  the value
    """

    def __init__(self, ins, outs):
        Node.__init__(self, ins, outs)
        self.set_caption(str(False))


    def __call__(self, inputs):
        """ inputs is the list of input values """
        res= bool(inputs[0])
        self.set_caption(str(res))
        return ( res,  )



class Int(Node):
    """
Variable
Input 0 : The stored value
Ouput 0 : Transmit the stored value
    """

    def __init__(self, ins, outs):
        Node.__init__(self, ins, outs)
        self.set_caption(str(0))


    def __call__(self, inputs):
        v = int(inputs[0])
        self.set_caption(str(v))
        return ( v, )


class Float(Node):
    """
Variable
Input 0 : The stored value
Ouput 0 : Transmit the stored value
    """

    def __init__(self, ins, outs):
        Node.__init__(self, ins, outs)
        self.set_caption(str(0.0))
       

    def __call__(self, inputs):
        """ inputs is the list of input values """
        res = float(inputs[0])
        self.set_caption('%.1f'%res)
        return ( res, )


class String(Node):
    """
String Variable
Input 0 : The stored value
Ouput 0 : Transmit the stored value
    """


    def __call__(self, inputs):
        """ inputs is the list of input values """
        return ( str(inputs[0]), )



class EnumTest(Node):
    """
String enumeration Test
    """

    def __call__(self, inputs):
        return ( inputs[0], )


class RGB(Node):
    """
RGB Color
    """

    def __call__(self, inputs):
        """ inputs is the list of input values """
        return ( inputs[0], )


class List(Node):
    """
Python List
    """

    def __call__(self, inputs):
        """ inputs is the list of input values """
        import copy
        return (copy.copy(inputs[0]), )


class Dict(Node):
    """
Python Dictionary
    """

    def __call__(self, inputs):
        """ inputs is the list of input values """
        import copy
        return (copy.copy(inputs[0]), )


class Pair(Node):
    """
    Python 2-uple generator
    """

    def __call__(self, inputs):
        return ( (inputs[0], inputs[1]), )


class List9(Node):
    """
    Python list with 8 entries.
    """

    def __init__(self):

        Node.__init__(self)
        self.add_input( name = "i0", interface = None)
        self.add_input( name = "i1", interface = None)
        self.add_input( name = "i2", interface = None)
        self.add_input( name = "i3", interface = None)
        self.add_input( name = "i4", interface = None)
        self.add_input( name = "i5", interface = None)
        self.add_input( name = "i6", interface = None)
        self.add_input( name = "i7", interface = None)
        self.add_input( name = "i8", interface = None)
        self.add_output( name = "list", interface = ISequence) 

    def __call__(self, inputs):
        """ inputs is the list of input values """
        l= filter(None,inputs)
        return ( l, )


from openalea.core.datapool import DataPool

class PoolReader(Node):
    """
In : Name (String)
Out : Object (Any)
    """

    def __init__(self, inputs, outputs):

        Node.__init__(self, inputs, outputs)
        self.pool = DataPool()


    def __call__(self, inputs):
        """ inputs is the list of input values """

        key = str(inputs[0])
        obj = self.pool[key]
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

        key = str(inputs[0])
        obj = str(inputs[1])
        self.pool[key] = obj



def list_select(items, index):
    """ __getitem__ """
    try:
        return items[index]
    except:
        return None



from openalea.core.core import NodeWidget
from PyQt4 import QtGui, QtCore

class ListSelectorWidget(QtGui.QListWidget, NodeWidget):

    def __init__(self, node, parent):
        """
        @param node
        @param parent
        """
        
        QtGui.QListWidget.__init__(self, parent)
        NodeWidget.__init__(self, node)

        self.updating = False
        self.notify(node, ("input_modified", 0))
        self.notify(node, ("input_modified", 1))


    def notify(self, sender, event):
        """ Notification sent by node """

        if(event[0] != "input_modified"): return
        
        seq = self.node.get_input("List")
        index = self.node.get_input("Index")

        if(event[1] == 0):
            self.update_list(seq)

        elif(index >= 0):
            self.updating = True
            self.setCurrentRow(index)
            self.updating = False


    def update_list(self, seq):
        """ Rebuild the list """
        
        self.clear()
        for elt in seq :

            item = QtGui.QListWidgetItem(str(elt))
            item.setFlags(QtCore.Qt.ItemIsEnabled|
                          QtCore.Qt.ItemIsSelectable)
            self.addItem(item)
    

    def currentRowChanged(self, row):
        """ Update the index"""
        
        print row
        if(not self.updating and row >= 0): 
            self.node.set_input("Index", row)


