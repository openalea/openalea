# -*-python-*-
#--------------------------------------------------------------------------------
#
#       OpenAlea.SConsX: SCons extension package for building platform
#                        independant packages.
#
#       Copyright or © or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
#--------------------------------------------------------------------------------

__doc__=""" MinGW configure environment. """
__license__= "Cecill-C"
__revision__="$Id: $"


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
      env.Replace(RCINCPREFIX = '--include-dir=')
      #env.AppendUnique(LINKFLAGS = LINKFLAGS )


   def configure( self, config ):
      pass

def create( config ):
   " Create mingw tool "
   mingw= MinGW( config )

   return mingw

