#!/usr/bin/python
# Flex configure environment
# Author: Christophe Pradal ( christophe.pradal@cirad.fr )
# Licence: GPL

import os, sys
from scons_util.config import *


class Flex:
   def __init__( self, config ):
      self.name= 'flex'
      self.config= config
      self._default= {}


   def default( self ):

      if isinstance( platform, Win32 ):
         self._default[ 'bin' ]= pj( 'C:', 'Tools', 'Bin' )
         self._default[ 'lib' ]= pj( 'C:', 'Tools', 'Bin' )
      elif isinstance( platform, Posix ):
         self._default[ 'bin' ]= '/usr/bin'
         self._default[ 'lib' ]= '/usr/lib'


   def option(  self, opts ):

      self.default()

      opts.Add( 'flex_bin', 'Flex binary path', 
                self._default[ 'bin' ] )
      opts.Add( 'flex_lib', 'Flex library path',
                self._default[ 'lib' ] )


   def update( self, env ):
      """ Update the environment with specific flags """

      if not isinstance( platform, Win32 ):
         env.AppendUnique( LIBS= [ 'm', 'fl' ] )
         
      env.AppendUnique( LIBPATH= [ env['flex_lib'] ] )

      t= Tool( 'lex', toolpath=[ getLocalPath() ] )
      t( env )

      flex= env.WhereIs( 'flex', env[ 'flex_bin' ] )
      env.Replace( LEX= flex )


   def configure( self, config ):
      b= WhereIs( "flex", config.conf.env[ 'flex_bin' ] )

      if not b:
        s="""
        Warning !!! Flex not found !
        Please, install Flex and try again.
        """
        print s
        sys.exit( -1 )


def create( config ):
   " Create flex tool "
   flex= Flex( config )

   return flex

