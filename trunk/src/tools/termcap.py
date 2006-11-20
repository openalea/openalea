# -*-python-*-
# Termcap configure environment
# Author: Christophe Pradal ( christophe.pradal@cirad.fr )
# Licence: CECILL-C

import os, sys
from openalea.sconsx.config import *


class Termcap:
   def __init__( self, config ):
      self.name= 'termcap'
      self.config= config
      self._default= {}


   def default( self ):
      if isinstance( platform, Posix ):
         self._default[ 'include' ]= pj('/usr','include')
         self._default[ 'lib' ]= pj(  '/usr', 'lib' )


   def option(  self, opts ):
      if isinstance( platform, Posix ):
         self.default()
         
         opts.AddOptions( 
            PathOption( 'termcap_includes', 'termcap include files', 
                        self._default[ 'include' ] ),
            PathOption( 'termcap_lib', 'termcap libraries path', 
                        self._default[ 'lib' ] ) 
            )


   def update( self, env ):
      if isinstance( platform, Posix ):
         env.AppendUnique( CPPPATH= [ env['termcap_includes'] ] )
         env.AppendUnique( LIBPATH= [ env['termcap_lib'] ] )
         env.AppendUnique( LIBS= [ 'termcap' ] )


   def configure( self, config ):
      if isinstance( platform, Posix ):
         if not config.conf.CheckCHeader('termcap.h'):
            print """Error: termcap.h not found !!!
            Please install termcap and start again."""
            sys.exit(-1)


def create( config ):
   " Create termcap tool "
   termcap= Termcap( config )

   return termcap

