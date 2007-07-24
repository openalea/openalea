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

__doc__ = """ Install configure environment. """
__license__ = "Cecill-C"
__revision__ = "$Id$"


import os, sys
from openalea.sconsx.config import *


class Install:

    def __init__(self, config):
        self.name = 'install'
        self.config = config
        self._default = {}


    def default(self):

        if isinstance(platform, Win32):
            self._default['prefix'] = 'C:' + os.sep + 'local'

        elif isinstance(platform, Posix):
            self._default['prefix'] = '/usr/local'



    def option( self, opts):
        # TODO: check if dirs exist on windows
        self.default()

        # Installation Directories
        opts.Add(('prefix', 
                  'install architecture-independent files', 
                  self._default['prefix']))

        opts.Add(('exec_prefix', 
                  'install architecture-dependent files', 
                  '$prefix'))

        # Fine tunning of the installation directory
        opts.Add(('bindir', 
                  'user executables', 
                  pj('$prefix', 'bin')))

        opts.Add(('libdir', 
                  'object code libraries', 
                  pj('$prefix', 'lib')))

        opts.Add(('includedir', 
                  'header files', 
                  pj('$prefix', 'include')))

        opts.Add(('datadir', 
                  'data', 
                  pj('$prefix', 'share')))

        # Program & Library names

        opts.Add('program_prefix', 
                  'prepend prefix to installed program names', '')

        opts.Add('program_suffix', 
                  'append suffix to installed program names', '')

        opts.Add('lib_prefix', 
                  'prepend prefix to installed library names', '')

        opts.Add('lib_suffix', 
                  'append suffix to installed library names', '')




    def update(self, env):
        """ Update the environment with specific flags """
        pass


    def configure(self, config):
        pass

def create(config):
   " Create install tool "

   install = Install(config)
   return install

