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

__doc__ = """ OpenGL configure environment. """
__license__ = "Cecill-C"
__revision__ = "$Id$"


import os, sys
from openalea.sconsx.config import *

exists = os.path.exists

class OpenGL:
   def __init__(self, config):
      self.name = 'opengl'
      self.config = config
      self._default = {}


   def default(self):

        if isinstance(platform, Win32):
            #MVSdir = r'C:\Program Files\Microsoft Visual Studio\VC98'
            MVSdir = r'C:\Program Files\Microsoft Platform SDK'
            self._default['msvc_include'] = pj(MVSdir, 'Include')
            self._default['msvc_lib'] = pj(MVSdir, 'Lib')
            
            mgw_dir = r'C:\MinGW'
            self._default['mgw_include'] = pj(mgw_dir, 'include')
            self._default['mgw_lib'] = pj(mgw_dir, 'lib', 'GL')
            
            self._default['include'] = self._default['msvc_include']
            self._default['lib'] = self._default['msvc_lib']
            
        elif isinstance(platform, Posix):
            if exists ('/usr/include/GL/gl.h'):
                self._default['include'] = '/usr/include'
                self._default['lib'] = '/usr/lib'
            else: 
                self._default['include'] = '/usr/X11R6/include'
                self._default['lib'] = '/usr/X11R6/lib'


   def option( self, opts):

      self.default()
                
      opts.AddOptions(
         ('gl_includes', 'GL include files', 
          self._default['include']),

         ('gl_lib', 'GL library path', 
         self._default['lib'])
        )


   def update(self, env):
      """ Update the environment with specific flags """
      if env.get('compiler', 'mingw') == 'mingw':
        if env['gl_includes'] == self._default['mgw_include']:
            env['gl_includes'] = self._default['msvc_include']
        if env['gl_lib'] == self._default['mgw_lib']:
            env['gl_lib'] = self._default['msvc_lib']

      env.AppendUnique(CPPPATH=[env['gl_includes']])
      env.AppendUnique(LIBPATH=[env['gl_lib']])

      if isinstance(platform, Cygwin):
         env.AppendUnique(LIBS=['opengl32','glu32', 'glut32'])
      elif isinstance(platform, Posix):
         env.AppendUnique(LIBS=['GLU', 'glut'])
      elif isinstance(platform, Win32):
         env.AppendUnique(LIBS=['opengl32','GLU32'])


   def configure(self, config):
      if not config.conf.CheckLibWithHeader('GL',['GL/gl.h', 'GL/glu.h'], 'c++', autoadd = 0):
         print "Error: gl.h not found, probably failure in automatic opengl detection"
         sys.exit(-1)


def create(config):
   " Create opengl tool "
   opengl = OpenGL(config)

   return opengl

