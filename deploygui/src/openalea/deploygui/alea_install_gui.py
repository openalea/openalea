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
import shutil
import signal

from PyQt4 import QtGui
from PyQt4 import QtCore

import ui_mainwindow
from openalea.deploy.util import get_repo_list as util_get_repo_list
from setuptools.package_index import PackageIndex
import pkg_resources
from setuptools import setup
from auth import cookie_login

url = "http://openalea.gforge.inria.fr"

def busy_pointer(f):
    """ Decorator to display a busy pointer """

    def wrapped(*args):
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.BusyCursor))
        ret = f(*args)
        QtGui.QApplication.restoreOverrideCursor ()
        return ret
        
    return wrapped



class MainWindow(QtGui.QMainWindow, ui_mainwindow.Ui_MainWindow):
    """ Main configuration window """

    def __init__(self):

        QtGui.QMainWindow.__init__(self)
        ui_mainwindow.Ui_MainWindow.__init__(self)
        self.setupUi(self)

        for i in util_get_repo_list():
            self.locationList.addItem(i)

        self.pi = None # package index
        self.pnamemap = {} # map txt and (pname, dist)
        sys.stdout = self
        sys.stderr = self

        # Signal connection
        self.connect(self.fileButton, QtCore.SIGNAL("clicked()"), self.get_filename)
        self.connect(self.customInstallButton, QtCore.SIGNAL("clicked()"), self.install_egg)
        self.connect(self.action_Quit, QtCore.SIGNAL("activated()"), self.quit)
        self.connect(self.action_About, QtCore.SIGNAL("activated()"), self.about)
        self.connect(self.action_Web, QtCore.SIGNAL("activated()"), self.web)
        self.connect(self.radioAll, QtCore.SIGNAL("clicked()"), self.refresh)
        self.connect(self.radioRecommended, QtCore.SIGNAL("clicked()"), self.refresh)
        self.connect(self.radioUpdate, QtCore.SIGNAL("clicked()"), self.refresh)
        self.connect(self.radioInstalled, QtCore.SIGNAL("clicked()"), self.refresh)
        self.connect(self.proceedButton, QtCore.SIGNAL("clicked()"), self.proceed)
        self.connect(self.refreshButton, QtCore.SIGNAL("clicked()"), self.refresh)
        self.connect(self.addLocButton, QtCore.SIGNAL("clicked()"), self.add_location)
        self.connect(self.removeLocButton, QtCore.SIGNAL("clicked()"), self.remove_location)
        self.connect(self.actionCookie_Session, QtCore.SIGNAL("activated()"), self.inriagforge_authentify)
        
        self.refresh()



    def quit(self):
        self.close()


    def about(self):
         """ Display About Dialog """
        
         mess = QtGui.QMessageBox.about(self, "About OpenAlea Installer",
                                        
                                        u"Copyright \xa9  2006-2007 INRIA - CIRAD - INRA\n"+
                                        "This Software is distributed under the Cecill-V2 License.\n\n"+
                                       
                                        "Visit %s\n\n"%(url,)
                                       )


    def web(self):
        """ Open OpenAlea website """
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(url))



    def get_mode(self):
        """ Return a string corresponding to the package mode:
        ALL, RECOMMENDED, UPDATE, INSTALLED
        """

        if(self.radioAll.isChecked()):
            return "ALL"
        elif(self.radioRecommended.isChecked()):
            return "RECOMMENDED"
        elif(self.radioUpdate.isChecked()):
            return "UPDATE"
        elif(self.radioInstalled.isChecked()):
            return "INSTALLED"

        return None
                

    @busy_pointer
    def refresh(self):
        """ Refresh the list of packages """

        print "Refreshing package list..."

        self.packageList.clear()
        self.pnamemap.clear()

        env = pkg_resources.Environment()

        mode = self.get_mode()

        # select the correct package index
        if(mode == "INSTALLED"):
            self.proceedButton.setText("Remove")
            self.pi = env
           
        else:
            self.proceedButton.setText("Install")
            self.pi = PackageIndex("")
            self.pi.add_find_links(self.get_repo_list())
            self.pi.prescan()


        # Parse each distribution
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
                if(mode != "INSTALLED"):
                    installed_version = [d.version for d in env[project_name]]
                    if(installed_version):
                        if(max(installed_version) < version):
                            update = True
                        else:
                            ignore = True
                            continue
                
                if(ignore) : continue
                if(update): txt += " -- UPDATE --"

                # Filter depending of mode
                if(mode == "ALL" or mode == "INSTALLED"):
                    ok = True
                    
                elif(mode == "RECOMMENDED" and
                     "openalea" in project_name.lower()):
                    ok = True
                    
                elif(mode == "UPDATE" and update):
                    ok = True

                else : ok = False
                     
                
                if(ok):
                    listitem = QtGui.QListWidgetItem(txt, self.packageList)
                    listitem.setFlags(QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsUserCheckable)
                    listitem.setCheckState(QtCore.Qt.Unchecked)
                    pname = "%s==%s"%(project_name, version)
                    self.pnamemap[txt] = (pname, dist)
                            
            
        print "Done\n"



    def get_repo_list(self):
        """ Return the list of the repository """

        ret = set()
        for i in xrange(self.locationList.count()):
            item = self.locationList.item(i)
            ret.add(str(item.text()))

        return list(ret)


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


    def install_egg(self):
        """ Install manually an egg """
        
        loc = str(self.requestEdit.text())
        if(not loc): return
        
        ok = self.install_package(loc, loc)
        self.display_finish_message(ok)
        self.refresh()
   
        
    def proceed(self):
        """ Install selected packages """
        ok = True

        for i in xrange(self.packageList.count()):
            item = self.packageList.item(i)
            
            if(item and item.checkState() == QtCore.Qt.Checked):
                pname, dist = self.pnamemap[str(item.text())]

                if(self.get_mode() == "INSTALLED"):
                    print "Removing ", pname
                    ret = self.remove_package(pname, dist.location)
                    ok = ret and ok
                    
                else:
                    print "Installing ", pname, ok
                    ret = self.install_package(pname, dist.location)
                    ok = ret and ok
                    

        self.display_finish_message(ok)
        self.refresh()
        

    @busy_pointer
    def install_package(self, pname, location):
        """ Start alea_install for a particular project name, given a location
        return True if OK
        """
        
        print "Installing %s\n"%(pname,)
        try:
            repositories = []
            for r in self.get_repo_list():
                repositories += ['-f', r]

            setup(
                script_args = ['-q','alea_install', '-v'] + repositories + [location],
                script_name = 'alea_install',
                )
            return True

        except Exception, e:
            self.write(str(e))
            return False

        except :
            print "Unexpected error:", sys.exc_info()[0]
            print "Please check you have permission to install package in " + \
                  "the destination directory."
            return False


    def display_finish_message(self, ok):
        """ Display finish message depending of ok """
        if(ok):
            mess = QtGui.QMessageBox.information(self, "OpenAlea Installer",
                                                 "Success.")
        else:
            mess = QtGui.QMessageBox.warning(self, "OpenAlea Installer",
                                             "An error occured. Check the log output.")
        
        
    @busy_pointer
    def remove_package(self, pname, location):
        """ Remove a distribution
        return True if OK
        """
        
        try:
            print "Remove ", location
            if(os.path.isdir(location)):
                shutil.rmtree(location)
            else:
                os.remove(location)
            return True

        except Exception, e:
            print e
            self.write(str(e))
            return False

        except :
            print "Unexpected error:", sys.exc_info()[0]
            print "Please check you have permission to remove packages. "
            return False


    def add_location(self):
        """ Add a repository """

        # Read a string
        repo, ok = QtGui.QInputDialog.getText(self, "URL", "Enter a valid URL:",
                                          QtGui.QLineEdit.Normal, "http://")
        if(ok):
            self.locationList.addItem(str(repo))
            self.refresh()


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


    def get_filename(self):
        """ Retrieve a local egg filename """
        
        filename = QtGui.QFileDialog.getOpenFileName(
            self, "Choose an Egg", QtCore.QDir.homePath(), "Egg (*.egg)")

        filename = str(filename)
        if(filename) : self.requestEdit.setText(filename)

        
        

        


                

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
    
