#!/usr/bin/python
# Readline configure environment
# Author: Christophe Pradal ( christophe.pradal@cirad.fr )
# Licence: GPL

import os, sys
from scons_util.config import *


class Readline:
   def __init__( self, config ):
      self.name= 'readline'
      self.config= config
      self._default= {}

   def depends( self ):
       return [ "termcap" ]

   def default( self ):
      if isinstance( platform, Posix ):
         
         self._default[ 'include' ]= '/usr/include'
         self._default[ 'lib' ]= '/usr/lib'
         if isinstance( platform, Cygwin ):
            self._default[ 'include' ]= '/usr/include/readline'


   def option(  self, opts ):

      self.default()

      if isinstance( platform, Posix ):
         opts.AddOptions( 
            PathOption( 'readline_includes', 
                        'readline include files', 
                        self._default[ 'include' ] ),

            PathOption( 'readline_lib', 
                        'readline libraries path', 
                        self._default[ 'lib' ] ) 
            )


   def update( self, env ):
      if isinstance( platform, Posix ):
         env.AppendUnique( CPPPATH= [ env['readline_includes'] ] )
         env.AppendUnique( LIBPATH= [ env['readline_lib'] ] )
         env.AppendUnique( LIBS= [ 'readline' ] )


   def configure( self, config ):
      if isinstance( platform, Posix ):
         if not config.conf.CheckCHeader( [ 'stdio.h', 
                                            'string.h', 
                                            'readline/readline.h' ] ):
            print """Error: readline.h not found !!!
            Please install readline and start again."""
            sys.exit(-1)


def create( config ):
   " Create readline tool "
   readline= Readline( config )

   deps= readline.depends()
   for lib in deps:
      config.add_tool( lib )

   return readline

