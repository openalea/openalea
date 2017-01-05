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

from Qt import QtWidgets, QtGui, QtCore

from openalea.oalab import metainfo

def show_splash_screen():
    """Show a small splash screen to make people wait for OpenAleaLab to startup"""

    pix = QtGui.QPixmap(":/images/resources/splash.png")
    splash = QtWidgets.QSplashScreen(pix, QtCore.Qt.WindowStaysOnTopHint)
    splash.show()
    message = "" + metainfo.get_copyright() + \
              "Version : %s\n" % (metainfo.get_version(),) + \
              "Loading modules..."
    splash.showMessage(message, QtCore.Qt.AlignCenter | QtCore.Qt.AlignBottom)
    # -- make sure qt really display the message before importing the modules.--
    QtWidgets.QApplication.processEvents()
    return splash
