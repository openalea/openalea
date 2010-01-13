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
""" QHull configure environment. """

__license__ = "Cecill-C"
__revision__ = "$Id$"

import os, sys
from openalea.sconsx.config import *


class Qhull:
   def __init__(self, config):
      self.name = 'qhull'
      self.config = config
      self._default = {}


   def default(self):

      self._default['libs_suffix'] = '$compiler_libs_suffix'

      if isinstance(platform, Win32):
         try:
            # Try to use openalea egg
            from openalea.deploy import get_base_dir
            base_dir = get_base_dir("qhull")
            self._default['include'] = os.path.join(base_dir, 'include')
            self._default['lib'] = os.path.join(base_dir, 'lib')
            
         except:
            try:
                import openalea.config as conf
                self._default['include'] = conf.include_dir
                self._default['lib'] = conf.lib_dir

            except ImportError, e:
                self._default['include'] = 'C:'+os.sep
                self._default['lib'] = 'C:'+os.sep

      elif isinstance(platform, Posix):
         self._default['include'] = '/usr/include'
         self._default['lib'] = '/usr/lib'


   def option( self, opts):

      self.default()

      opts.AddVariables(
         ('qhull_includes', 
           'Qhull include files', 
           self._default['include']),

         ('qhull_lib', 
           'Qhull library path', 
           self._default['lib']),

         ('qhull_libs_suffix', 
           'Qhull library suffix name like -vc80 or -mgw', 
           self._default['libs_suffix'])
     )


   def update(self, env):
      """ Update the environment with specific flags """

      env.AppendUnique(CPPPATH=[env['qhull_includes']])
      env.AppendUnique(LIBPATH=[env['qhull_lib']])

      qhull_name = 'qhull'+env['qhull_libs_suffix']
      env.AppendUnique(LIBS=[qhull_name])


   def configure(self, config):
      if not config.conf.CheckCHeader('qhull/qhull_a.h'):
         print "Error: qhull headers not found."
         sys.exit(-1)


def create(config):
   " Create qhull tool "
   qhull = Qhull(config)

   return qhull

