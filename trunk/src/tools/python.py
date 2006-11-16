# -*-python-*-
# Python configure environment
# Author: Christophe Pradal ( christophe.pradal@cirad.fr )
# Licence: GPL

import os, sys
from sconsx.config import *
from distutils.sysconfig import *
pj= os.path.join

class Python:
   def __init__( self, config ):
      self.name= 'python'
      self.config= config
      self._default= {}


   def default( self ):

      self._default[ 'include' ]= get_python_inc(plat_specific=1)

      if isinstance( platform, Win32 ):
         self._default[ 'lib' ]= pj(PREFIX,"libs")
      else:
         try:
            self._default[ 'lib' ]= get_config_vars('LIBPL')
         except:
            self._default[ 'lib' ]= '/usr/lib'


   def option(  self, opts ):

      self.default()

      opts.AddOptions(
         PathOption( 'python_includes', 'Python include files', 
          self._default[ 'include' ]),

         PathOption( 'python_lib', 'Python library path', 
         self._default[ 'lib' ] )
         )


   def update( self, env ):
      """ Update the environment with specific flags """

      env.AppendUnique( CPPPATH= [ env['python_includes'] ] )
      env.AppendUnique( LIBPATH= [ env['python_lib'] ] )

      if isinstance( platform, Win32 ):
         version= "%d%d"%sys.version_info[0:2]
         python_lib= 'python' + version
      else:
         python_lib= 'python' + get_config_var( 'VERSION' )

      env.AppendUnique( LIBS= python_lib )


   def configure( self, config ):
      if not config.conf.CheckCHeader('Python.h','<>'):
         print "Error: Python.h not found, probably failure in automatic python detection"
         sys.exit(-1)


def create( config ):
   " Create python tool "
   python= Python( config )

   return python

