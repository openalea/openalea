# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2013 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
__revision__ = ""


from openalea.vpltk.qt import QtGui, QtCore

from session import Session
from mainwindow import MainWindow

from openalea.oalab.gui import resources_rc
from openalea.oalab import metainfo

import sys


class OALab(QtGui.QApplication):
    def __init__(self, args):
        QtGui.QApplication.__init__(self, args)

        # -- show the splash screen --
        self.splash = show_splash_screen()
        
        #self.setStyle('cleanlooks')
        # -- main window --
        session = Session()
        self.win = MainWindow(session)
        self.win.setMinimumSize(800,400)
        self.win.showMaximized()
        self.win.setWindowTitle("OpenAlea Laboratory")
        self.win.setWindowIcon(QtGui.QIcon(":/images/resources/openalea_icon2.png"))
        self.win.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        
        QtCore.QObject.connect(self, QtCore.SIGNAL('focusChanged(QWidget*, QWidget*)'),self.win.changeMenuTab)

        self.win.setEnabled(False)
        self.win.show()
        self.win.raise_()
        self.splash.finish(self.win)
        self.win.setEnabled(True)
        
        
def show_splash_screen():
    """Show a small splash screen to make people wait for OpenAleaLab to startup"""
    
    pix = QtGui.QPixmap(":/images/resources/splash.png")
    splash = QtGui.QSplashScreen(pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.show()
    message = "" + metainfo.get_copyright() +\
              "Version : %s\n"%(metainfo.get_version(),) +\
              "Loading modules..."
    splash.showMessage(message, QtCore.Qt.AlignCenter|QtCore.Qt.AlignBottom)
    # -- make sure qt really display the message before importing the modules.--
    QtGui.QApplication.processEvents()
    return splash        
        
        
if( __name__ == "__main__"):
    app = OALab(sys.argv)
    app.exec_()
