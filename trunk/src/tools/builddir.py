#!/usr/bin/python
# BuildDir configure environment
# Author: Christophe Pradal ( christophe.pradal@cirad.fr )
# Licence: GPL

import os, sys
from sconsx.config import *


class BuildDir:

    def __init__( self, config ):
        self.name= 'build_dir'
        self.config= config
        self._default= {}


    def default( self ):
        self._default[ 'build_prefix' ]= pj( self.config.dir[ 0 ], "build-" + platform.name ) 

    def option(  self, opts ):

        self.default()
        opts.Add(  BoolOption( 'with_build_dir', 'build files in a separate directory?', True ) )
        opts.Add( 'build_prefix',
                  'local preinstall directory',
                  self._default[ 'build_prefix' ] )


    def update( self, env ):
        """ Update the environment with specific flags """

        if env[ 'with_build_dir' ]:
            prefix= env[ 'build_prefix' ]
        else:
            prefix= self.config.dir[ 0 ]

        build= { 
        'build_bindir': pj( prefix, 'bin' ),
        'build_libdir' : pj( prefix, 'lib' ),
        'build_includedir' : pj( prefix, 'include' ) }

        if env[ 'with_build_dir' ]:
            build[ 'build_dir' ]= pj( prefix, 'src' )

        # Creation of missing directories
        for dir in build:
            path= build[ dir ]
            env[ dir ]= path
            if not os.path.exists( path ):
                os.makedirs(path)

        if not env[ 'with_build_dir' ]:
            env[ 'build_dir' ]= pj( prefix, 'src' )



    def configure( self, config ):
        pass

def create( config ):
    " Create builddir tool "
    builddir= BuildDir( config )

    return builddir

