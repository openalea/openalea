#!/usr/bin/python
# Gnuplot configure environment
# Author: Christophe Pradal ( christophe.pradal@cirad.fr )
# Licence: GPL

import os, sys
from sconsx.config import *


class Gnuplot:
   def __init__( self, config ):
      self.name= 'gnuplot'
      self.config= config
      self._default= {}


   def default( self ):

      if isinstance( platform, Posix ):
         self._default[ 'bin' ]= pj('/usr','bin')
      elif isinstance( platform, Win32 ):
         self._default[ 'bin' ]= 'C:\\'


   def option(  self, opts ):

      self.default()

      opts.Add( PathOption( 'gnuplot_bin', 
                            'Gnuplot binary path', 
                            self._default[ 'bin' ] ) )


   def update( self, env ):
      """ Update the environment with specific flags """
      pass


   def configure( self, config ):
      g= WhereIs( "gnuplot", config.conf.env[ 'gnuplot_bin' ] )

      if not g:
        s="""
        Warning !!! Gnuplot not found !
        Please, install Gnuplot and try again.
        """
        print s
        sys.exit( -1 )


def create( config ):
   " Create gnuplot tool "
   gnuplot= Gnuplot( config )

   return gnuplot

