#!/usr/bin/python
# Compiler configure environment
# Author: Christophe Pradal ( christophe.pradal@cirad.fr )
# Licence: GPL

import os, sys
from scons_util.config import *


class Compiler:

   def __init__( self, config ):
      self.name= 'compiler'
      self.config= config
      self._default= {}


   def depends( self ):
      deps= []

      if isinstance( platform, Posix ):
         deps.append( 'gcc' )
      elif isinstance( platform, Win32 ):
         deps.append( 'msvc' )
      else:
         raise "Add a compiler support for your os !!!"

      return deps


   def default( self ):

      self._default[ 'debug' ]= False
      self._default[ 'warnings' ]= False
      self._default[ 'static' ]= False


   def option(  self, opts ):

      self.default()

      opts.Add( BoolOption( 'debug', 
                            'compilation in a debug mode',
                            self._default[ 'debug' ] ) )
      opts.Add( BoolOption( 'warnings',
                            'compilation with -Wall and similar',
                            self._default[ 'warnings' ] ) )
      opts.Add( BoolOption( 'static',
                            '',
                            self._default[ 'static' ] ) )

      opts.Add( 'EXTRA_CXXFLAGS', 'Specific user flags for c++ compiler', '')
      opts.Add( 'EXTRA_CXXDEFINES', 'Specific c++ defines', '')
      opts.Add( 'EXTRA_LINKFLAGS', 'Specific user flags for c++ linker', '')
      opts.Add( 'EXTRA_CPPPATH', 'Specific user iinclude path', '')
      opts.Add( 'EXTRA_LIBPATH', 'Specific user library path', '')
      opts.Add( 'EXTRA_LIBS', 'Specific user libraries', '')


   def update( self, env ):
      """ Update the environment with specific flags """

      env.Append( CXXFLAGS= Split( env['EXTRA_CXXFLAGS'] ) )
      env.Append( CXXDEFINES= Split( env['EXTRA_CXXDEFINES'] ) )
      env.Append( LINKFLAGS= Split( env['EXTRA_LINKFLAGS'] ) )
      env.Append( CPPPATH= Split( env['EXTRA_CPPPATH'] ) )
      env.Append( LIBPATH= Split( env['EXTRA_LIBPATH'] ) )
      env.Append( LIBS= Split( env['EXTRA_LIBS'] ) )


   def configure( self, config ):
      pass

def create( config ):
   " Create compiler tool "
   compiler= Compiler( config )

   deps= compiler.depends()
   for lib in deps:
      config.add_tool( lib )

   return compiler

