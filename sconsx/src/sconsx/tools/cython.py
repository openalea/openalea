# -*-python-*-
#--------------------------------------------------------------------------------
#
#       OpenAlea.SConsX: SCons extension package for building platform
#                        independant packages.
#
#       Copyright 2006-2010 INRIA - CIRAD - INRA  
#
#       File author(s): Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
#--------------------------------------------------------------------------------
""" cython environment. """

__license__ = "Cecill-C"
__revision__ = "$Id: $"

import os, sys
from openalea.sconsx.config import *


class Cython:
   def __init__(self, config):
      self.name = 'cython'
      self.config = config
      self._default = {}


   def default(self):
        pass


   def option( self, opts):
      pass

   def update(self, env):
      """ Update the environment with specific flags """

      t = Tool('cython', toolpath=[getLocalPath()])
      t(env)


   def configure(self, config):
        pass


def create(config):
   " Create flex tool "
   cython = Cython(config)

   return cython

