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


from SCons.Variables import PathVariable 
from SCons.Variables import BoolVariable 
from SCons.Variables import EnumVariable 
from SCons.Options import Options
from SCons.Variables import Variables
from SCons.Util import Split, WhereIs

import os, sys
from openalea.sconsx.config import *

class Compiler:

    def __init__(self, config):
        self.name = 'compiler'
        self.config = config
        self._default = {}


    def default(self):

        self._default['debug'] = False
        self._default['warnings'] = False
        self._default['static'] = False

        if isinstance(platform, Posix):
            compilers = ['gcc']
            libs_suffix = ''
        elif isinstance(platform, Win32):
            compilers = ['mingw', 'msvc']
            libs_suffix = '-vc80'
        else:
            raise "Add a compiler support for your os !!!"

        self._default['compilers'] = compilers
        self._default['libs_suffix'] = libs_suffix


    def option( self, opts):

        self.default()

        opts.Add(BoolVariable('debug', 
                          'compilation in a debug mode',
                          self._default['debug']))
        opts.Add(BoolVariable('warnings',
                          'compilation with -Wall and similar',
                          self._default['warnings']))
        opts.Add(BoolVariable('static',
                          '',
                          self._default['static']))

        compilers = self._default['compilers']
        default_compiler = compilers[0]
        opts.Add(EnumVariable('compiler',
                          'compiler tool used for the build',
                          default_compiler,
                          compilers))
        opts.Add('compiler_libs_suffix', 
               'Library suffix name like -vc80 or -mgw',
               self._default['libs_suffix'])
                           
        opts.Add('rpath', 'A list of paths to search for shared libraries')

        opts.Add('EXTRA_CXXFLAGS', 'Specific user flags for c++ compiler', '')
        opts.Add('EXTRA_CPPDEFINES', 'Specific c++ defines', '')
        opts.Add('EXTRA_LINKFLAGS', 'Specific user flags for c++ linker', '')
        opts.Add('EXTRA_CPPPATH', 'Specific user include path', '')
        opts.Add('EXTRA_LIBPATH', 'Specific user library path', '')
        opts.Add('EXTRA_LIBS', 'Specific user libraries', '')

    def update(self, env):
        """ Update the environment with specific flags """

        # Set the compiler
        compiler_name = env['compiler']
        self.config.add_tool(compiler_name)
      
        if isinstance(platform, Cygwin):
            env.AppendUnique(CPPDEFINES = 'SYSTEM_IS__CYGWIN')
        elif isinstance(platform, Win32):
            env.AppendUnique(CPPDEFINES = 'WIN32')
            libs_suffix = env['compiler_libs_suffix']
            if compiler_name == 'mingw' and '-vc' in libs_suffix:
                env['compiler_libs_suffix'] = '-mgw'

        env.Append(RPATH=Split('$rpath'))
        env.Append(CXXFLAGS=Split(env['EXTRA_CXXFLAGS']))
        env.Append(CPPDEFINES=Split(env['EXTRA_CPPDEFINES']))
        env.Append(LINKFLAGS=Split(env['EXTRA_LINKFLAGS']))
        env.Append(CPPPATH=Split(env['EXTRA_CPPPATH']))
        env.Append(LIBPATH=Split(env['EXTRA_LIBPATH']))
        env.Append(LIBS=Split(env['EXTRA_LIBS']))


    def configure(self, config):
        pass

def create(config):
     " Create compiler tool "
     compiler = Compiler(config)

     return compiler

