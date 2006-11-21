# -*-python-*-
# OpenAlea configure environment
# Author: Christophe Pradal ( christophe.pradal@cirad.fr )
# Licence: CECILL-C

import os, sys
from openalea.sconsx.config import *

class Alea:
   def __init__( self, config ):
      self.name= 'alea'
      self.config= config
      self._default= {}
      
      
   def default( self ):
      """Set default tool values"""
      try:
         import openalea.config as alea_conf
         self._default[ "openalea_lib" ]= alea_conf.lib_dir
         self._default[ "openalea_include" ]= alea_conf.include_dir

      except ImportError, e :

         if isinstance( platform, Win32 ):
            self._default[ "openalea_lib" ]= 'C:\\openalea\\lib'
            self._default[ "openalea_include" ]= 'C:\\openalea\\include'
         elif isinstance( platform, Posix ):
            self._default[ "openalea_lib" ]= '/usr/local/openalea/lib'
            self._default[ "openalea_include" ]= '/usr/local/openalea/include'


   def option(  self, opts ):
      """Add scons options to opts"""
      
      self.default()

      opts.Add( PathOption( 'openalea_lib', 'OpenAlea lib directory', 
                            self._default[ 'openalea_lib' ] ) )
      opts.Add( PathOption( 'openalea_include', 'OpenAlea include directory', 
                            self._default[ 'openalea_include' ] ) )


   def update( self, env ):
      """ Update the environment with specific flags """

      env.AppendUnique( CPPPATH= [ env['openalea_include'] ] )
      env.AppendUnique( LIBPATH= [ env['openalea_lib'] ] )

      #env.EnableALEALib= _EnableALEALib

   def configure( self, config ):
      try:
         import openalea.config as alea_conf
      except ImportError, e :
         print '!!Warning : OpenAlea config not found.'
         print 'You can download it from http://openalea.gforge.inria.fr'


# def _EnableALEALib(env, libs, *args, **kwds ):
#    """Add libraries to compiler"""
#    env.AppendUnique( LIBS= libs )
   

def create( config ):
   " Create alea tool "
   oa= Alea( config )

   return oa

