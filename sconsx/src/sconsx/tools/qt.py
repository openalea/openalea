# -*-python-*-
#-------------------------------------------------------------------------------
#
#   OpenAlea.SConsX: SCons extension package for building platform
#                    independant packages.
#
#   Copyright 2006 INRIA - CIRAD - INRA  
#
#   File author(s): Christophe Pradal <christophe.prada@cirad.fr>
#
#   Distributed under the Cecill-C License.
#   See accompanying file LICENSE.txt or copy at
#       http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#   OpenAlea WebSite : http://openalea.gforge.inria.fr
#
#-------------------------------------------------------------------------------

__doc__ = """ QT configure environment. """
__license__ = "Cecill-C"
__revision__ = "$Id: $"

import os, sys
from openalea.sconsx.config import *

exists = os.path.exists

class QT:
    def __init__(self, config):
        self.name = 'qt'
        self.config = config
        self._default = {}


    def default(self):

        qt_dir = os.getenv("QTDIR")
        qt_lib = '$QTDIR/lib'
        qt_bin = '$QTDIR/bin'
        qt_inc = '$QTDIR/include'

        if not qt_dir:
            if isinstance(platform, Win32):
                qt_dir = pj('C:','QT')
            elif isinstance(platform, Posix):
                qt_dir = pj('/usr', 'lib', 'qt3')
                if not exists(pj(qt_dir, 'bin')):
                    # Use LSB spec
                    qt_dir = '/usr'
                    qt_bin = '/usr/bin'
                    qt_inc = '/usr/include/qt3'
                    qt_lib = '/usr/lib'

        self._default["QTDIR"] = qt_dir
        self._default["QT_BINPATH"] = qt_bin
        self._default["QT_CPPPATH"] = qt_inc
        self._default["QT_LIBPATH"] = qt_lib


    def option( self, opts):

        self.default()

        opts.Add(('QTDIR', 'QT directory', 
                    self._default['QTDIR']))
        opts.Add(('QT_BINPATH', 'QT binaries path.', 
                    self._default['QT_BINPATH']))
        opts.Add(('QT_CPPPATH', 'QT includes path.', 
                    self._default['QT_CPPPATH']))
        opts.Add(('QT_LIBPATH', 'QT lib path.', 
                    self._default['QT_LIBPATH']))


    def update(self, env):
      """ Update the environment with specific flags """

      t = Tool('qt')
      t(env)

      if isinstance(platform, Win32):
         qt_lib ='qt-mtnc321'
      else:
         qt_lib ='qt-mt' 
      
      libpath = str(env.subst(env['QT_LIBPATH']))
      multithread = exist(qt_lib , libpath)
      if multithread:
         env.AppendUnique(CPPDEFINES=['QT_THREAD_SUPPORT'])
         env.Replace(QT_LIB=qt_lib)

      if isinstance(platform, Win32):
         env.AppendUnique(CPPDEFINES=['QT_DLL'])

    def configure(self, config):
      if not config.conf.CheckLibWithHeader('qt-mt', 
                ['qapplication.h', 'qgl.h', 'qthread.h'], 
                'c++', 
                'QApplication qapp(0,0);', autoadd=0):

         print """Error: QT not found ! 
                  Please, install QT and try again."""
         sys.exit(-1)


def create(config):
   " Create qt tool "
   qt = QT(config)

   return qt

