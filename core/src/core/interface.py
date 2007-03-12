# -*- python -*-
#
#       OpenAlea.Core: OpenAlea Core
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
This module defines Interface classes (I/O types)
"""

__license__= "Cecill-C"
__revision__=" $Id$ "
    

class Interface(object):
    """ Abstract base class for all interfaces """
    pass

class IFileStr(Interface):
    """ File Path interface """
    pass


class IStr(Interface):
    """ String interface """
    pass


class IFloat(Interface):
    """ Float interface """
    
    def __init__(self, min = -2.**24, max = 2.**24):

        self.min = min
        self.max = max
    


class IInt(Interface):
    """ Int interface """
    
    def __init__(self, min = -2**24, max = 2**24):

        self.min = min
        self.max = max


class IBool(Interface):
    """ Bool interface """
    pass


class IEnumStr(Interface):
    """ String enumeration """

    def __init__(self, enum = []):
        self.enum = enum


class IRGBColor(Interface):
    """ RGB Color """
    pass

class ITuple3(Interface):
    """ Tuple3 """
    def __init__(self):
        pass

class IFunction(Interface):
    """ Function interface """
    pass

class ISequence(Interface):
    """ Sequence interface (list, tuple, ...) """
    pass

class IDict(Interface):
    """ Dictionary interface """
    pass
