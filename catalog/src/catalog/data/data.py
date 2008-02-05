# -*- python -*-
#
#       OpenAlea.Catalog
#
#       Copyright 2006 - 2007 INRIA - CIRAD - INRA  
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################


__doc__=""" Data Nodes """
__license__= "Cecill-C"
__revision__=" $Id$ "

from os.path import join
from openalea.core import *

class Variable(Node):
    """
    In : Caption, Obj
    Out: Obj
    Transmit obj to output
    Display str as caption
    """

    def __call__(self, inputs):
        """ inputs is the list of input values """

        self.set_caption(str(inputs[0]))
        return (inputs[1],  )


    


class RGB(Node):
    """
RGB Color
    """

    def __call__(self, inputs):
        """ inputs is the list of input values """
        return ( inputs[0], )


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


class FloatScy(Node):
    """
Variable
Input 0 : The stored value in string format
Ouput 0 : Transmit the stored value
    """

    def __init__(self, ins, outs):
        Node.__init__(self, ins, outs)
        self.set_caption(str(0.0))
       

    def __call__(self, inputs):
        """ inputs is the list of input values """
        res = float(inputs[0])
        self.set_caption('%.1e'%res)
        return ( res, )


class String(Node):
    """
String Variable
Input 0 : The stored value
Ouput 0 : Transmit the stored value
    """


    def __call__(self, inputs):
        """ inputs is the list of input values """
        s = str(inputs[0])
        self.set_caption(repr(s))
        return ( s, )


class Text(Node):
    """
Text Variable
Input 0 : The stored value
Ouput 0 : Transmit the stored value
    """


    def __call__(self, inputs):
        """ inputs is the list of input values """
        return ( str(inputs[0]), )



class DateTime(Node):
    """
DateTime
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
        try:
            iter( inputs[0] )
            return (copy.copy(inputs[0]), )
        except:
            return ([copy.copy(inputs[0])], )
            


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


class Tuple3(Node):
    """
    Python 2-uple generator
    """

    def __call__(self, inputs):
        return ( (inputs[0], inputs[1], inputs[2]), )


def list_select(items, index):
    """ __getitem__ """
    try:
        return items[index]
    except:
        return None


# DEPRECATED
class FileName(Node):
    """
A file path
Out :  the file path string
    """

    def __call__(self, inputs):
        """ inputs is the list of input values """

        print "This node is DEPRECATED. Use %s instead"%("Catalog.File.FileName")
        fname, cwd = inputs
        if len(cwd)>0 :
            return (join(str(cwd),str(fname)),)
        else :
            return (str(fname),)


class DirName(Node):
    """
A directory path
Out :  the path string
    """

    def __call__(self, inputs):
        """ inputs is the list of input values """

        print "This node is DEPRECATED. Use %s instead"%("Catalog.File.DirName")
        rep, cwd = inputs
        if len(cwd)>0 :
            return ( join(str(cwd),str(rep)),  )
        else :
            return ( str(rep),  )


class PackageDir(Node):
    """
    In : A Package Name
    Out : The Path of the package wralea
    """

    def __call__(self, inputs):
        """ inputs is the list of input values """

        print "This node is DEPRECATED. Use %s instead"%("Catalog.File.PackageDir")
        pname = str(inputs[0])

        from openalea.core.pkgmanager import PackageManager
        pm = PackageManager()
        pkg = pm.get(pname) 
        path = ''

        if pkg :
            path = pkg.path

        return (path,  )



