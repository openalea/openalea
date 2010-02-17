#!/usr/bin/python

# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA  
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#                       Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the CeCILL v2 License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL_V2-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################
"""Main Module for graphical interface"""

__license__ = "CeCILL v2"
__revision__ = "$Id$"


import sys, os
from PyQt4 import QtGui
from PyQt4 import QtCore

from openalea.visualea.mainwindow import MainWindow
from openalea.core.session import Session

import time

# Restore default signal handler for CTRL+C
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

import __builtin__
__builtin__.__debug_with_old__ = False

def set_stdout():
    """Disable stdout if using pythonw"""
    if("pythonw" in sys.executable):
        nullfd = open(os.devnull, "w")
        sys.stdout = nullfd
        sys.stderr = nullfd


def main(args):
    global __builtin__

    set_stdout()
    app = QtGui.QApplication(args)

    # Check Version
    version = QtCore.QT_VERSION_STR
    # QT_VERSION_STR implement __le__ operator
    if(version < '4.5.2'):

        mess = QtGui.QMessageBox.warning(None, "Error",
                                         "Visualea need QT library >=4.5.2")

        return 

    #splash screen
    import metainfo

    pix=QtGui.QPixmap(":/icons/splash.png")
    splash = QtGui.QSplashScreen(pix)

    splash.show()
    splash.showMessage(
        metainfo.get_copyrigth() +
        "Version : %s \n"%(metainfo.get_version(),) + 
        "Loading modules...",
        QtCore.Qt.AlignCenter|QtCore.Qt.AlignBottom)

    
    time.clock()

    session = Session()

    t1 = time.clock()

    print 'session build in %f seconds'%t1


    #parse command line
    """
    if(len(args)==2):
        filename = args[1]
        try:
            session.load(filename)
        except Exception, e:
            print e
    """

    QtGui.QApplication.processEvents()    

    win = MainWindow(session)
    win.show()    
    splash.finish(win);
    return app.exec_()



if __name__ == "__main__":
    main(sys.argv)
    
