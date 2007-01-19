#!/usr/bin/python

# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
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
__revision__=" $Id$"


import sys
from PyQt4 import QtGui
from PyQt4 import QtCore

from openalea.visualea.mainwindow import MainWindow

from openalea.core.pkgmanager import PackageManager
from openalea.core.core import Package
from openalea.core.subgraph import SubGraphFactory



# Restore default signal handler for CTRL+C
import signal; signal.signal(signal.SIGINT, signal.SIG_DFL)


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


    from openalea.core.pkgmanager import PackageManager

    # initilize package manager
    pkgman = PackageManager()

    pkg_metainfo={}
    pkg=Package("MyObjects", pkg_metainfo)

    rootfactory = SubGraphFactory(pkgman, name="Workspace",
                                description= "",
                                category = "",
                                )

    pkg.add_factory(rootfactory)
    pkgman.add_package(pkg)
    pkgman.find_and_register_packages()

    
    win = MainWindow(pkgman, rootfactory, locals())
    win.show()
    
    #    splash.finish(win);
    
    return app.exec_()



if __name__ == "__main__":
    main(sys.argv)
