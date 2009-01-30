# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
""" Data Nodes """

__license__ = "Cecill-C"
__revision__ = " $Id$ "

from os.path import join
from openalea.core import *


class Variable(Node):
    """ Transmit obj to output and display str as caption
    """

    def __call__(self, inputs):
        """
        :param inputs: list of input values
        :returns: Obj
        """
        self.set_caption(str(inputs[0]))
        return (inputs[1], )


class Bool(Node):
    """
    Boolean value

    :param ins: input 1
    :param outs: input 2
    """

    def __init__(self, ins, outs):
        Node.__init__(self, ins, outs)
        self.set_caption(str(False))

    def __call__(self, inputs):
        """ inputs is the list of input values 

        :returns: the value
        """
        res= bool(inputs[0])
        self.set_caption(str(res))
        return (res, )


class Int(Node):
    """
    :param ins: The stored value
    :param outs: todo
    
    """

    def __init__(self, ins, outs):
        Node.__init__(self, ins, outs)
        self.set_caption(str(0))

    def __call__(self, inputs):
        """
        :returns: Transmit the stored value
        """
        v = int(inputs[0])
        self.set_caption(str(v))
        return (v, )


class Float(Node):
    """
    :param ins: The stored value
    :param outs: todo
    """

    def __init__(self, ins, outs):
        Node.__init__(self, ins, outs)
        self.set_caption(str(0.0))

    def __call__(self, inputs):
        """ inputs is the list of input values 

        :returns: Transmit the stored value
        """
        res = float(inputs[0])
        self.set_caption('%.1f'%res)
        return (res, )


class FloatScy(Node):
    """Float Variable

    :param ins: The stored value in string format
    :param outs: todo

    """

    def __init__(self, ins, outs):
        Node.__init__(self, ins, outs)
        self.set_caption(str(0.0))

    def __call__(self, inputs):
        """ inputs is the list of input values 

        :returns: Transmit the stored value
        """
        res = float(inputs[0])
        self.set_caption('%.1e'%res)
        return (res, )


class String(Node):
    """String Variable"""

    def __call__(self, inputs):
        """
        
        :param inputs: list of input values
        :returns: Transmit the stored value
        """
        s = str(inputs[0])
        self.set_caption(repr(s))
        return (s, )


class Text(Node):
    """Text Variable"""

    def __call__(self, inputs):
        """ inputs is the list of input values
        
        :param inputs: list of  input values
        :type inputs: a list with 1 element
        :returns: Transmit the stored value
        """
        return (str(inputs[0]), )


class DateTime(Node):
    """DateTime"""

    def __call__(self, inputs):
        """ inputs is the list of input values
        
        :param inputs: The stored value
        """
        return (inputs[0], )


class List(Node):
    """Python List"""

    def __call__(self, inputs):
        """ inputs is the list of input value
        :param inputs: The stored value
        """
        import copy
        try:
            iter(inputs[0])
            return (copy.copy(inputs[0]), )
        except:
            return ([copy.copy(inputs[0])], )


class Dict(Node):
    """Python Dictionary"""

    def __call__(self, inputs):
        """ inputs is the list of input values
        :param inputs: The stored value
        """
        import copy
        return (copy.copy(inputs[0]), )


class Pair(Node):
    """Python 2-uple generator"""

    def __call__(self, inputs):
        """
        :param inputs: list of 2 values
        :returns: tuple of the 3 inputs
        """
        return ((inputs[0], inputs[1]), )


class Tuple3(Node):
    """
    Python 3-uple generator
    """

    def __call__(self, inputs):
        """ returns 3-tuple

        :param inputs: list of 3 values
        :returns: tuple of the 3 inputs
        """
        return ((inputs[0], inputs[1], inputs[2]), )


def list_select(items, index):
    """ __getitem__ """
    try:
        return items[index]
    except:
        return None


# DEPRECATED


class FileName(Node):
    """A file path

    """

    def __call__(self, inputs):
        """ 
        :param inputs: the list of input values
        :returns:  the file path string
        """

        print "This node is DEPRECATED. Use %s instead"%("Catalog.File.FileName")
        fname, cwd = inputs
        if len(cwd)>0 :
            return (join(str(cwd),str(fname)),)
        else :
            return (str(fname),)


class DirName(Node):
    """A directory path


    """

    def __call__(self, inputs):
        """ 
        :param inputs: the list of input values
        :returns:  the path string
        """

        print "This node is DEPRECATED. Use %s instead"%("Catalog.File.DirName")
        rep, cwd = inputs
        if len(cwd)>0 :
            return ( join(str(cwd),str(rep)), )
        else :
            return ( str(rep), )


class PackageDir(Node):
    """

    """

    def __call__(self, inputs):
        """
        :param inputs: list of input values

        :returns: The Path of the package wralea
        """

        print "This node is DEPRECATED. Use %s instead"%("Catalog.File.PackageDir")
        pname = str(inputs[0])

        from openalea.core.pkgmanager import PackageManager
        pm = PackageManager()
        pkg = pm.get(pname) 
        path = ''

        if pkg :
            path = pkg.path

        return (path, )



