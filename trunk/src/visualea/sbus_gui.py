# -*- python -*-
#
#       OpenAlea.SoftwareBusGui: OpenAlea software bus graphical user interface
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#                       Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the GPL License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.gnu.org/licenses/gpl.txt
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

__doc__="""
Main Module for graphical interface
"""

__license__= "GPL"
__revision__=" $Id"


import sys
from PyQt4 import QtGui
from PyQt4 import QtCore

from mainwindow import MainWindow

from pkgmanager import PackageManager
from item_model import PkgModel



def main(args):
    
    app = QtGui.QApplication(args)


    #splash screen
    # pix=QtGui.QPixmap(":/splash/icons/splash.png")
    #     splash = QtGui.QSplashScreen(pix)
    #     splash.show()
    
    #    filename=None
    #     #parse command line
    #     if(len(args)>1):
    #         filename=args[1]



    pkgman = PackageManager()
    pkgman.init("../test/wralea.py")

    
    model = PkgModel(pkgman)

    
    win = MainWindow(model, globals())
    win.show()
    
    #    splash.finish(win);
    
    return app.exec_()






if __name__ == "__main__":
    main(sys.argv)
