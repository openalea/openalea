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
""" MinGW configure environment. """

__license__ = "Cecill-C"
__revision__ = "$Id$"


import os, sys
import types
from openalea.sconsx.config import *


class MinGW:

   def __init__(self, config):
      self.name = 'mingw'
      self.config = config


   def option(self, opts):
      pass

   def update(self, env):
      """ Update the environment with specific flags """

      CCFLAGS = env['CCFLAGS']
      if '/nologo' in CCFLAGS:
        CCFLAGS.remove('/nologo') 
        env['CCFLAGS'] = CCFLAGS
        #del env['SHLIBEMITTER'][0]

      # Big HACK, sorry...
      # delete all function unlike qt4 emmiter which is an instance.
      env['SHLIBEMITTER'] = [f for f in env['SHLIBEMITTER'] if type(f) is types.InstanceType]

      t = Tool('mingw')
      t(env)
     
      env['RCCOM'] = '$RC $_CPPDEFFLAGS $RCINCFLAGS ${RCINCPREFIX}${SOURCE.dir} $RCFLAGS -i $SOURCE -o $TARGET'
      CXXFLAGS = []
      if env["warnings"]:
         CXXFLAGS += ['-W', '-Wall']

      if env["debug"]:
         CXXFLAGS.extend(['-g'])
      else:
         CXXFLAGS.extend(['-DNDEBUG', '-O2'])

      LINKFLAGS = ["-enable-stdcall-fixup",
                 "-enable-auto-import",
                 "-enable-runtime-pseudo-reloc",
                 "-s"]

      env.AppendUnique(CXXFLAGS=CXXFLAGS)
      env.Replace(RCINCPREFIX='--include-dir=')
      #env.AppendUnique(LINKFLAGS=LINKFLAGS)


   def configure(self, config):
      pass

def create(config):
   " Create mingw tool "
   mingw = MinGW(config)

   return mingw

