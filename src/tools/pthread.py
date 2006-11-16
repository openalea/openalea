# -*-python-*-
# Pthread configure environment
# Author: Christophe Pradal ( christophe.pradal@cirad.fr )
# Licence: GPL

import os, sys
from sconsx.config import *


class Pthread:
   def __init__( self, config ):
      self.name= 'pthread'
      self.config= config
      self._default= {}


   def default( self ):

      self._default[ 'include' ]= '/usr/include'
      self._default[ 'lib' ]= '/usr/lib'



   def option(  self, opts ):

      self.default()

      opts.AddOptions( 
         PathOption( 'pthread_includes', 'pthread include files', 
                     self._default[ 'include' ] ),
         PathOption( 'pthread_lib', 'pthread libraries path', 
                     self._default[ 'lib' ] ) 
      )



   def update( self, env ):
      """ Update the environment with specific flags """

      env.AppendUnique( CPPPATH= [ env['pthread_includes'] ] )
      env.AppendUnique( LIBPATH= [ env['pthread_lib'] ] )
      env.AppendUnique( LIBS= [ 'pthread' ] )



   def configure( self, config ):
      if not config.conf.CheckCHeader('pthread.h'):
         print """Error: pthread.h not found !!!
         Please install pthread and start again."""
         sys.exit(-1)


def create( config ):
   " Create pthread tool "
   pthread= Pthread( config )

   return pthread

