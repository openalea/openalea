#!/usr/bin/python
# Gcc configure environment
# Author: Christophe Pradal ( christophe.pradal@cirad.fr )
# Licence: GPL

import os, sys
from sconsx.config import *


class Gcc:

   def __init__( self, config ):
      self.name= 'gcc'
      self.config= config


   def option(  self, opts ):
      pass

   def update( self, env ):
      """ Update the environment with specific flags """

      t= Tool( 'gcc' )
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
   " Create gcc tool "
   gcc= Gcc( config )

   return gcc

