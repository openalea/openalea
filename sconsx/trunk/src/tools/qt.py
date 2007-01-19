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

__doc__=""" QT configure environment. """
__license__= "Cecill-C"
__revision__="$Id: $"

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
      opts.Add( ( 'QT_BINPATH', 'QT binaries path.', 
                '$QTDIR/bin' ) )
      opts.Add( ( 'QT_CPPPATH', 'QT includes path.', 
                '$QTDIR/include' ) )
      opts.Add( ( 'QT_LIBPATH', 'QT lib path.', 
                '$QTDIR/lib' ) )


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

