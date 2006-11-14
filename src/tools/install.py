#!/usr/bin/python
# Install configure environment
# Author: Christophe Pradal ( christophe.pradal@cirad.fr )
# Licence: GPL

import os, sys
from sconsx.config import *


class Install:

    def __init__( self, config ):
        self.name= 'install'
        self.config= config
        self._default= {}


    def default( self ):

        if isinstance( platform, Win32 ):
            self._default[ 'prefix' ]= 'C:' + os.sep + 'local'

        elif isinstance( platform, Posix ):
            self._default[ 'prefix' ]= '/usr/local'



    def option(  self, opts ):
        # TODO: check if dirs exist on windows
        self.default()

        # Installation Directories
        opts.Add(PathOption( 'prefix', 
                             'install architecture-independent files', 
                             self._default[ 'prefix' ]))

        opts.Add(PathOption( 'exec_prefix', 
                             'install architecture-dependent files', 
                             '$prefix'))

        # Fine tunning of the installation directory
        opts.Add(PathOption( 'bindir', 
                             'user executables', 
                             pj( '$prefix', 'bin' ) ))

        opts.Add(PathOption( 'libdir', 
                             'object code libraries', 
                             pj( '$prefix', 'lib' ) ))

        opts.Add(PathOption( 'includedir', 
                             'header files', 
                             pj( '$prefix', 'include' ) ))

        opts.Add(PathOption( 'datadir', 
                             'data', 
                             pj( '$prefix', 'share' ) ))

        # Program & Library names

        opts.Add( 'program_prefix', 
                  'prepend prefix to installed program names', '' )

        opts.Add( 'program_suffix', 
                  'append suffix to installed program names', '' )

        opts.Add( 'lib_prefix', 
                  'prepend prefix to installed library names', '' )

        opts.Add( 'lib_suffix', 
                  'append suffix to installed library names', '' )




    def update( self, env ):
        """ Update the environment with specific flags """
        pass


    def configure( self, config ):
        pass

def create( config ):
   " Create install tool "

   install= Install( config )
   return install

