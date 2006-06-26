#!/usr/bin/python
# Boost configure environment
# Author: Christophe Pradal ( christophe.pradal@cirad.fr )
# Licence: GPL

import os, sys
from scons_util.config import *


class Boost_Python:
   def __init__( self, config ):
      self.name= 'boost_python'
      self.config= config
      self._default= {}


   def depends( self ):
      deps= []

      if isinstance( platform, Posix ):
         deps.append( 'python' )
         deps.append( 'pthread' )

      return deps


   def default( self ):

      if isinstance( platform, Win32 ):
         self._default[ 'include' ]= 'C:' + os.sep
         self._default[ 'lib' ]= 'C:' + os.sep
         self._default[ 'flags' ]= ''
         self._default[ 'defines' ]= ''

      elif isinstance( platform, Posix ):
         self._default[ 'include' ]= '/usr/include'
         self._default[ 'lib' ]= '/usr/lib'
         self._default[ 'flags' ]= '-ftemplate-depth-100'
         self._default[ 'defines' ]= 'BOOST_PYTHON_DYNAMIC_LIB'


   def option(  self, opts ):

      self.default()

      opts.AddOptions( 
         PathOption( 'boost_includes', 
                     'Boost_python include files', 
                     self._default[ 'include' ] ),

         PathOption( 'boost_lib', 
                     'Boost_python libraries path', 
                     self._default[ 'lib' ] ),

         ( 'boost_flags', 
           'Boost_python compiler flags', 
           self._default[ 'flags' ] ),

         ( 'boost_defines', 
           'Boost_python defines', 
           self._default[ 'defines' ] )
      )


   def update( self, env ):
      """ Update the environment with specific flags """

      env.AppendUnique( CPPPATH= [ env['boost_includes'] ] )
      env.AppendUnique( LIBPATH= [ env['boost_lib'] ] )
      env.AppendUnique( LIBS= [ 'boost_python' ] )
      env.Append( CPPDEFINES= '$boost_defines' )
      env.Append( CPPFLAGS= '$boost_flags' )


   def configure( self, config ):
      if not config.conf.CheckCXXHeader( 'boost/python.hpp' ):
         print "Error: boost.python headers not found."
         sys.exit( -1 )


def create( config ):
   " Create boost tool "
   boost= Boost_Python( config )

   deps= boost.depends()
   for lib in deps:
      config.add_tool( lib )

   return boost

