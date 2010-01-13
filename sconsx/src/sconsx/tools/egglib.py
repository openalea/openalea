# -*-python-*-
#--------------------------------------------------------------------------------
#
#       OpenAlea.SConsX: SCons extension package for building platform
#                        independant packages.
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA  
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
#--------------------------------------------------------------------------------
""" OpenAlea configure environment. """

__license__= "Cecill-C"
__revision__="$Id$"

import os, sys
from openalea.sconsx.config import *


class EggLib:

   def __init__(self, name, config):
      
      self.name = name
      self.config = config
      self._default = {}

      _name = name.replace(".", "_")
      self.lib_key = "%s_lib"%(_name)
      self.include_key = "%s_include"%(_name)
      
      
      
   def default( self ):
      """Set default tool values"""

      try:
         from openalea.deploy import get_inc_dirs, get_lib_dirs, get_base_dir

         bdir = get_base_dir(self.name)
         dirs = [os.path.join(bdir, x) for x in get_lib_dirs(self.name)]
         incs = [os.path.join(bdir, x) for x in get_inc_dirs(self.name)]
         
         self._default[self.lib_key] = dirs
         self._default[self.include_key] = incs

      except Exception, e:
         print "Cannot find build parameters for %s : "%(self.name,), e
         self._default[self.lib_key] = ""
         self._default[self.include_key] = ""
      

   def option(self, opts):
      """Add scons options to opts"""
      
      self.default()

      opts.Add( self.lib_key,
                self.lib_key + ' directory', 
                self._default[self.lib_key] )
      
      opts.Add( self.include_key,
                self.include_key + ' directory', 
                self._default[self.include_key])


   def update(self, env):
      """ Update the environment with specific flags """

      env.AppendUnique(CPPPATH=[env[self.include_key]] )
      env.AppendUnique(LIBPATH=[env[self.lib_key]] )

      #env.EnableALEALib= _EnableALEALib

   def configure( self, config ):
      pass



def create(name, config):
   return EggLib(name, config)
