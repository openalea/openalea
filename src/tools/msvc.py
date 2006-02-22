#!/usr/bin/python

# Msvc configure environment
# Author: Christophe Pradal ( christophe.pradal@cirad.fr )
# Licence: GPL

import os, sys
from scons_util.config import *


class Msvc:

   def __init__( self, config ):
      self.name= 'msvc'
      self.config= config

   def option(  self, opts ):
      pass

   def update( self, env ):
      """ Update the environment with specific flags """

      t= Tool( 'msvc' )
      t( env )

      CXXFLAGS= []
      CPPPATH= [r'C:\PROGRAM FILES\MICROSOFT VISUAL STUDIO\VC98\INCLUDE\STLPORT']
      CPPDEFINES= [ 'WIN32' ]
      if env["warnings"]:
         # TODO add warnings flags
         CXXFLAGS += [ '/W3' ]

      if env["debug"]:
         # TODO add debug flags
         CXXFLAGS.extend(['/MLd','/DEBUG','/Z7','/Od','/Ob0'])
         CPPDEFINES= [ '_DEBUG' ]
      else:
         # TODO add optimized flags
         CXXFLAGS.extend(['/ML','/O2','/Ob2','/Gy','/GF','/GA','/GB' ])
         CPPDEFINES= [ 'NDEBUG' ]

      env.AppendUnique(CPPPATH = CPPPATH)
      env.AppendUnique(CXXFLAGS = CXXFLAGS)
      env.AppendUnique(CPPDEFINES = CPPDEFINES)


   def configure( self, config ):
      pass

def create( config ):
   " Create msvc tool "
   msvc= Msvc( config )

   return msvc

