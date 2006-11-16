# -*-python-*-
# MinGW configure environment
# Author: Christophe Pradal ( christophe.pradal@cirad.fr )
# Licence: GPL

import os, sys
from sconsx.config import *


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

      env.AppendUnique(CXXFLAGS = CXXFLAGS)


   def configure( self, config ):
      pass

def create( config ):
   " Create mingw tool "
   mingw= MinGW( config )

   return mingw

