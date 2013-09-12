# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2013 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
__revision__ = "$Id: $"

import abc

class ControlABC:
    __metaclass__ = abc.ABCMeta
    def __init__(self):
        self.default()
        
    @abc.abstractmethod
    def default(self):
        """
        Create a default control
        """
        self.name = "default"
        self.value = 0
  
    def rename(self, name):
        self.name = name
        
    @abc.abstractmethod    
    def edit(self):
        pass
        
    @abc.abstractmethod    
    def thumbnail(self):
        pass

    @abc.abstractmethod
    def save(self):
        pass


