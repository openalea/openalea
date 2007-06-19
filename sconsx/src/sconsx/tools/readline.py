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

__doc__ = """ Readline configure environment. """
__license__ = "Cecill-C"
__revision__ = "$Id: $"

import os, sys
from openalea.sconsx.config import *


class Readline:
   def __init__(self, config):
      self.name = 'readline'
      self.config = config
      self._default = {}

   def depends(self):
       return ["termcap"]

   def default(self):
      if isinstance(platform, Posix):
         
         self._default['include'] = '/usr/include'
         self._default['lib'] = '/usr/lib'
         if isinstance(platform, Cygwin):
            self._default['include'] = '/usr/include/readline'


   def option( self, opts):

      self.default()

      if isinstance(platform, Posix):
         opts.AddOptions(
            PathOption('readline_includes', 
                        'readline include files', 
                        self._default['include']),

            PathOption('readline_lib', 
                        'readline libraries path', 
                        self._default['lib']) 
           )


   def update(self, env):
      if isinstance(platform, Posix):
         env.AppendUnique(CPPPATH=[env['readline_includes']])
         env.AppendUnique(LIBPATH=[env['readline_lib']])
         env.AppendUnique(LIBS=['readline'])


   def configure(self, config):
      if isinstance(platform, Posix):
         if not config.conf.CheckCHeader(['stdio.h', 
                                            'string.h', 
                                            'readline/readline.h']):
            print """Error: readline.h not found !!!
            Please install readline and start again."""
            sys.exit(-1)


def create(config):
   " Create readline tool "
   readline = Readline(config)

   deps= readline.depends()
   for lib in deps:
      config.add_tool(lib)

   return readline

