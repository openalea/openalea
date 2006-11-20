# -*-python-*-
# MinGW configure environment
# Author: Christophe Pradal ( christophe.pradal@cirad.fr )
# Licence: CECILL-C

import os, sys
from openalea.sconsx.config import *


class MinGW:

   def __init__( self, config ):
      self.name= 'mingw'
      self.config= config


   def option(  self, opts ):
      pass

   def update( self, env ):
      """ Update the environment with specific flags """

      t= Tool( 'mingw' )
      t( env )

      CXXFLAGS= []
      if env["warnings"]:
         CXXFLAGS += [ '-W', '-Wall' ]

      if env["debug"]:
         CXXFLAGS.extend(['-g'])
      else:
         CXXFLAGS.extend(['-DNDEBUG', '-O2'])

      LINKFLAGS=["-enable-stdcall-fixup",
                 "-enable-auto-import",
                 "-enable-runtime-pseudo-reloc",
                 "-s"]

      env.AppendUnique(CXXFLAGS = CXXFLAGS)
      #env.AppendUnique(LINKFLAGS = LINKFLAGS )


   def configure( self, config ):
      pass

def create( config ):
   " Create mingw tool "
   mingw= MinGW( config )

   return mingw

