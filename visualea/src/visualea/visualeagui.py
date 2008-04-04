#!/usr/bin/python

# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2006 - 2007 INRIA - CIRAD - INRA  
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

__doc__="""
Main Module for graphical interface
"""

__license__= "CeCILL v2"
__revision__=" $Id$"


import sys, os
from PyQt4 import QtGui
from PyQt4 import QtCore

from openalea.visualea.mainwindow import MainWindow
from openalea.core.session import Session

# Restore default signal handler for CTRL+C
import signal; signal.signal(signal.SIGINT, signal.SIG_DFL)


def set_stdout():
    """Disable stdout if using pythonw"""
    if("pythonw" in sys.executable):
        nullfd = open(os.devnull, "w")
        sys.stdout = nullfd
        sys.stderr = nullfd


def main(args):

    set_stdout()
    app = QtGui.QApplication(args)

    # Check Version
    version = int(QtCore.QT_VERSION_STR.replace('.', ''))
    if(version < 420):

        mess = QtGui.QMessageBox.warning(None, "Error",
                                         "Visualea need QT library >=4.2")

        return 

    #splash screen
    pix=QtGui.QPixmap(":/icons/splash.png")
    splash = QtGui.QSplashScreen(pix)
    splash.show()
    QtGui.QApplication.processEvents()
    
    session = Session()

    win = MainWindow(session)

    #parse command line
    if(len(args)>1):
        filename = args[1]
        try:
            session.load(filename)
        except Exception, e:
            print e

    
    win.show()
    
    splash.finish(win);

    return app.exec_()



if __name__ == "__main__":
    main(sys.argv)
    
