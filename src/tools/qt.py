# -*-python-*-
# QT configure environment
# Author: Christophe Pradal ( christophe.pradal@cirad.fr )
# Licence: CECILL-C

import os, sys
from openalea.sconsx.config import *

class QT:
   def __init__( self, config ):
      self.name= 'qt'
      self.config= config
      self._default= {}


   def default( self ):

      qtdir= os.getenv( "QTDIR" )
      if not qtdir:
         if isinstance( platform, Win32 ):
            qtdir= pj('C:','QT')
         elif isinstance( platform, Posix ):
            qtdir= pj( '/usr', 'lib', 'qt3' )
      self._default[ "QTDIR" ]= qtdir


   def option(  self, opts ):

      self.default()

      opts.Add( PathOption( 'QTDIR', 'QT directory', 
                self._default[ 'QTDIR' ] ) )


   def update( self, env ):
      """ Update the environment with specific flags """

      t= Tool( 'qt' )
      t( env )

      if isinstance( platform, Win32 ):
         qt_lib='qt-mtnc321'
      else:
         qt_lib='qt-mt' 
      
      multithread= exist( qt_lib , pj( env['QTDIR'], 'lib' ) )
      if multithread:
         env.AppendUnique( CPPDEFINES= ['QT_THREAD_SUPPORT'] )
         env.Replace( QT_LIB= qt_lib )

      if isinstance( platform, Win32 ):
         env.AppendUnique( CPPDEFINES= ['QT_DLL'] )
      elif isinstance( platform, Cygwin ):
         env['QT_CPPPATH']='/usr/include/qt3'


   def configure( self, config ):
      if not config.conf.CheckLibWithHeader( 'qt-mt', 
                [ 'qapplication.h', 'qgl.h', 'qthread.h' ], 
                'c++', 
                'QApplication qapp(0,0);', autoadd=0 ):

         print """Error: QT not found ! 
                  Please, install QT and try again."""
         sys.exit( -1 )

      #TODO: Check qgl & qthread support



def create( config ):
   " Create qt tool "
   qt= QT( config )

   return qt

