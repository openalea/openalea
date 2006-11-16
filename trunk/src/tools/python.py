# -*-python-*-
# Python configure environment
# Author: Christophe Pradal ( christophe.pradal@cirad.fr )
# Licence: GPL

import os, sys
from sconsx.config import *
from distutils.sysconfig import get_python_inc, get_config_var



class Python:
   def __init__( self, config ):
      self.name= 'python'
      self.config= config
      self._default= {}


   def default( self ):

      self._default[ 'include' ]= get_python_inc()
      try:
         self._default[ 'lib' ]= get_config_var( 'LIBDIR' )
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

      python_lib= 'python' + get_config_var( 'VERSION' )
      env.Append( LIBS= python_lib )


   def configure( self, config ):
      if not config.conf.CheckCHeader('Python.h','<>'):
         print "Error: Python.h not found, probably failure in automatic python detection"
         sys.exit(-1)


def create( config ):
   " Create python tool "
   python= Python( config )

   return python

