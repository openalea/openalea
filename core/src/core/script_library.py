# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#                       Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
"""This module defines the ScriptLibrary class
to register objects with their names"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

from singleton import Singleton

class ScriptLibrary(object):
    """The ScriptLibrary is a library that register
    python objects with their names
    """
    
    __metaclass__ = Singleton
    
    def __init__ (self) :
        self._registered = {}
        self._used_names = set()
    
    def clear (self) :
        """Clear all registered names.
        """
        self._registered.clear()
        self._used_names.clear()
    
    def find_free_name (self, prefix) :
        name = prefix
        i = 0
        while name in self._used_names :
            name = "%s%d" % (prefix,i)
            i += 1
        return name
    
    def name (self, obj, script) :
        """Retrieves the name associated with
        a python object
        """
        try :
            return self._registered[id(obj)],script
        except KeyError :
            script += "assert False #obj '%s' not defined\n" % str(obj)
            return None,script
    
    def register (self, obj, suggested_name = "obj") :
        """Register a python object
        This method will try to use suggested_name
        if it is available.
        """
        name = self.find_free_name(suggested_name)
        self._registered[id(obj)] = name
        self._used_names.add(name)
        return name

