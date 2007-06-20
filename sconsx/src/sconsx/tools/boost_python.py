# -*-python-*-
#--------------------------------------------------------------------------------
#
#       OpenAlea.SConsX: SCons extension package for building platform
#                        independant packages.
#
#       Copyright 2006 INRIA - CIRAD - INRA  
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

__doc__ = """ Boost.Python configure environment. """
__license__ = "Cecill-C"
__revision__ = "$Id$"

import os, sys
from openalea.sconsx.config import *


class Boost_Python:
   def __init__(self, config):
      self.name = 'boost_python'
      self.config = config
      self._default = {}


   def depends(self):
      deps = ['python']

      if isinstance(platform, Posix):
         deps.append('pthread')

      return deps


   def default(self):

      self._default['libs_suffix'] = '$compiler_libs_suffix'

      if isinstance(platform, Win32):
         self._default['flags'] = ''
         self._default['defines'] = ''
         try:
            import openalea.config as conf
            self._default['include'] = conf.include_dir
            self._default['lib'] = conf.lib_dir

         except ImportError, e:
            self._default['include'] = 'C:' + os.sep
            self._default['lib'] = 'C:' + os.sep

      elif isinstance(platform, Posix):
         self._default['include'] = '/usr/include'
         self._default['lib'] = '/usr/lib'
         self._default['flags'] = '-ftemplate-depth-100'
         self._default['defines'] = 'BOOST_PYTHON_DYNAMIC_LIB'


   def option( self, opts):

      self.default()

      opts.AddOptions(
         PathOption('boost_includes', 
                     'Boost_python include files', 
                     self._default['include']),

         PathOption('boost_lib', 
                     'Boost_python libraries path', 
                     self._default['lib']),

         ('boost_flags', 
           'Boost_python compiler flags', 
           self._default['flags']),

         ('boost_defines', 
           'Boost_python defines', 
           self._default['defines']),

         ('boost_libs_suffix', 
           'Boost_python library suffix name like -vc80-mt or -gcc', 
           self._default['libs_suffix'])
     )


   def update(self, env):
      """ Update the environment with specific flags """

      env.AppendUnique(CPPPATH=[env['boost_includes']])
      env.AppendUnique(LIBPATH=[env['boost_lib']])
      env.Append(CPPDEFINES='$boost_defines')
      env.Append(CPPFLAGS='$boost_flags')

      boost_name= 'boost_python'+ env['boost_libs_suffix']
      env.AppendUnique(LIBS=[boost_name])


   def configure(self, config):
      if not config.conf.CheckCXXHeader('boost/python.hpp'):
         print "Error: boost.python headers not found."
         sys.exit(-1)


def create(config):
   " Create boost tool "
   boost = Boost_Python(config)

   deps= boost.depends()
   for lib in deps:
      config.add_tool(lib)

   return boost

