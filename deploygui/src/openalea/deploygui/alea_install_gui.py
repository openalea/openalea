#!/usr/bin/python

# -*- python -*-
#
#       OpenAlea.DeployGui: OpenAlea installation frontend
#
#       Copyright 2006-2007 INRIA - CIRAD - INRA  
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
Main Module for installation graphical frontend
"""

__license__= "CeCILL v2"
__revision__=" $Id$"


import sys, os
import signal

from PyQt4 import QtGui
from PyQt4 import QtCore

import ui_mainwindow
from openalea.deploy import OPENALEA_PI
from setuptools.package_index import PackageIndex
import pkg_resources
from setuptools import setup
from auth import cookie_login



class MainWindow(QtGui.QMainWindow, ui_mainwindow.Ui_MainWindow):
    """ Main configuration window """

    def __init__(self):

        QtGui.QMainWindow.__init__(self)
        ui_mainwindow.Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.locationList.addItem(OPENALEA_PI)

        self.pi = None # package index
        self.pnamemap = {} # map txt and (pname, dist)
        sys.stdout = self
        sys.stderr = self

        # Signal connection
        self.connect(self.proceedButton, QtCore.SIGNAL("clicked()"), self.proceed)
        self.connect(self.refreshButton, QtCore.SIGNAL("clicked()"), self.refresh)
        self.connect(self.addLocButton, QtCore.SIGNAL("clicked()"), self.add_location)
        self.connect(self.removeLocButton, QtCore.SIGNAL("clicked()"), self.remove_location)
        self.connect(self.actionCookie_Session, QtCore.SIGNAL("activated()"), self.inriagforge_authentify)
        
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
            for dist in self.pi._distmap[project_name]:
                
                version = dist._version or ""
                platform = dist.platform or ""
            
                txt = "%s %s %s"%(project_name, version, platform,)

                ignore = False
                update = False
                
                # Filter
                # Select only egg
                if(dist.precedence != pkg_resources.EGG_DIST):
                    ignore = True
                    continue

                # compare with already installed egg
                installed_version = [d.version for d in env[project_name]]
                if(installed_version):
                    if(max(installed_version) < version):
                        update = True
                    else:
                        ignore = True

                if(update): txt += " (UPDATE)"
                if(not ignore):
                    self.packageList.addItem(txt)
                    pname = "%s==%s"%(project_name, version)
                    self.pnamemap[txt] = (pname, dist)
                            
            
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
                pname, dist = self.pnamemap[str(item.text())]
                print "Installing ", pname
                self.install_package(pname, dist)
            
        self.refresh()
        

    def install_package(self, pname, dist):
        """ Start alea_install for a particular project name """
        
        print "Installing %s from %s\n"%(pname, dist.location)
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


    def inriagforge_authentify(self):
        """ Cookie based authentification """

        login, ok = QtGui.QInputDialog.getText(self, "Login", "Enter your login name:",
                                          QtGui.QLineEdit.Normal, "")
        if not ok : return
        
        password, ok = QtGui.QInputDialog.getText(self, "Password", "Enter your password:",
                                               QtGui.QLineEdit.Password, "")

        if not ok :
            password = None
            return

        # Create login/password values
        values = {'form_loginname':login,
                  'form_pw':password,
                  'return_to' : '',
                  'login' : "Connexion avec SSL" }

        url = "https://gforge.inria.fr/account/login.php"

        cookie_login(url, values)
        self.refresh()
        
        


                

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
    
