#!/usr/bin/python

# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2006 INRIA - CIRAD - INRA  
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

__doc__="""
Main Module for graphical interface
"""

__license__= "CeCILL v2"
__revision__=" $Id: visualeagui.py 606 2007-06-25 12:55:41Z dufourko $"


import sys, os
import signal

from PyQt4 import QtGui
from PyQt4 import QtCore

import ui_mainwindow
from openalea.deploy import OPENALEA_PI
from setuptools.package_index import PackageIndex
import pkg_resources
from setuptools import setup



class MainWindow(QtGui.QMainWindow, ui_mainwindow.Ui_MainWindow):
    """ Main configuration window """

    def __init__(self):

        QtGui.QMainWindow.__init__(self)
        ui_mainwindow.Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.locationList.addItem(OPENALEA_PI)

        self.pi = None # package index
        self.pnamemap = {}
        sys.stdout = self
        sys.stderr = self

        # Signal connection
        self.connect(self.proceedButton, QtCore.SIGNAL("clicked()"), self.proceed)
        self.connect(self.refreshButton, QtCore.SIGNAL("clicked()"), self.refresh)
        self.connect(self.addLocButton, QtCore.SIGNAL("clicked()"), self.add_location)
        self.connect(self.removeLocButton, QtCore.SIGNAL("clicked()"), self.remove_location)

        self.refresh()



    def refresh(self):
        """ Refresh the list of packages """

        print "Refreshing package list..."
        self.pi = PackageIndex("")
        self.pi.add_find_links(self.get_repo_list())
        self.pi.prescan()

        self.packageList.clear()
        self.pnamemap.clear()

        env = pkg_resources.Environment()

        for project_name in self.pi:

            dist = self.pi._distmap[project_name][0]
            version = dist.py_version or ""
            platform = dist.platform or ""
            
            txt = "%s %s %s"%(project_name, version, platform,)
            self.pnamemap[txt] = project_name

            # Filter
            if(dist.precedence != pkg_resources.EGG_DIST
               or project_name in env
               or env[project_name] == version  ):
                continue

            self.packageList.addItem(txt)
            
        print "Done\n"


    def get_repo_list(self):
        """ Return the list of the repository """

        ret = []
        for i in xrange(self.locationList.count()):
            item = self.locationList.item(i)
            ret.append(str(item.text()))

        return ret


    def write(self, text):
        """ Write to log """
        
        cursor = self.logText.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.logText.setTextCursor(cursor)
        self.logText.ensureCursorVisible()

        QtGui.QApplication.processEvents()
        

    def flush(self):
        pass


    def isatty(self):
        return 1


    def proceed(self):
        """ Install selected packages """

        for i in xrange(self.packageList.count()):
            item = self.packageList.item(i)
            
            if(item.isSelected()):
                pname = self.pnamemap[str(item.text())]
                print "Installing ", pname
                dist = self.pi[pname][0]
                self.install_package(dist)
            
        self.refresh()
        

    def install_package(self, dist):
        """ Start alea_install for a particular dist """
        
        print "Installing %s from %s\n"%(dist.project_name, dist.location)
        try:
            setup(
                script_args = ['-q','alea_install', '-v'] + [dist.location],
                script_name = 'alea_install',
                )
        except Exception, e:
            print e
            self.write(str(e))


    def add_location(self):
        """ Add a repository """

        # Read a string
        repo, ok = QtGui.QInputDialog.getText(self, "URL", "Enter a valid URL:",
                                          QtGui.QLineEdit.Normal, "http://")
        if(ok):
            self.locationList.addItem(str(repo))


    def remove_location(self):
        """ Remove a repository """
        
        for i in xrange(self.locationList.count()):
            item = self.locationList.item(i)
            if(item and item.isSelected()):
                self.locationList.takeItem(i)



                

def main(args=None):

    if args is None : args = sys.argv
    
    # Restore default signal handler for CTRL+C
    signal.signal(signal.SIGINT, signal.SIG_DFL)
       
    app = QtGui.QApplication(args)

    win = MainWindow()
    win.show()
    
    return app.exec_()



if __name__ == "__main__":
    main(sys.argv)
    
