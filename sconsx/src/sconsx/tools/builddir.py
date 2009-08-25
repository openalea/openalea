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
""" Build directory configure environment. """
 
__license__ = "Cecill-C"
__revision__ = "$Id$"

import os, sys
from openalea.sconsx.config import *

class BuildDir:

    def __init__(self, config):
        self.name = 'build_dir'
        self.config = config
        self._default = {}


    def default(self):
        #self._default['build_prefix']= pj(self.config.dir[0], "build-" + platform.name) 
        self._default['build_prefix'] = pj(self.config.dir[0], "build-scons") 

    def option( self, opts):

        self.default()
        opts.Add( BoolVariable('with_build_dir', 'build files in a separate directory?', True))
        opts.Add('build_prefix',
                  'local preinstall directory',
                  self._default['build_prefix'])


    def update(self, env):
        """ Update the environment with specific flags """

        if env['with_build_dir']:
            prefix = env['build_prefix']
        else:
            prefix = self.config.dir[0]
        
        build = { 
        'build_prefix': prefix,
        'build_bindir': pj(prefix, 'bin'),
        'build_libdir' : pj(prefix, 'lib'),
        'build_includedir' : pj(prefix, 'include') }

        if env['with_build_dir']:
            build['build_dir'] = pj(prefix, 'src')

        # Creation of missing directories
        for udir in build:
            path = build[udir]
            env[udir] = os.path.abspath(path)
            if not os.path.exists(path):
                os.makedirs(path)

        if not env['with_build_dir']:
            env['build_dir'] = pj(env['build_prefix'], 'src')



    def configure(self, config):
        pass

def create(config):
    " Create builddir tool "
    builddir = BuildDir(config)

    return builddir

