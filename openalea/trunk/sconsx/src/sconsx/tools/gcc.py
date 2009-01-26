# -*-python-*-
#--------------------------------------------------------------------------------
#
#       OpenAlea.SConsX: SCons extension package for building platform
#                        independant packages.
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA  
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

__doc__ = """ Gcc configure environment. """
__license__ = "Cecill-C"
__revision__ = "$Id$"

import os, sys
from openalea.sconsx.config import *


class Gcc:

   def __init__(self, config):
      self.name = 'gcc'
      self.config = config


   def option( self, opts):
      pass

   def update(self, env):
      """ Update the environment with specific flags """

      t = Tool('gcc')
      t(env)

      CXXFLAGS = []
      if env["warnings"]:
         CXXFLAGS += ['-W', '-Wall']

      if env["debug"]:
         CXXFLAGS.extend(['-g'])
      else:
         CXXFLAGS.extend(['-DNDEBUG', '-O2'])

      env.AppendUnique(CXXFLAGS=CXXFLAGS)


   def configure(self, config):
      pass

def create(config):
   " Create gcc tool "
   gcc = Gcc(config)

   return gcc

