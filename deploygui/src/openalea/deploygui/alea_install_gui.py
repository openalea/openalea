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

from openalea.deploy.command import set_env
from openalea.deploy.util import get_repo_list as util_get_repo_list

from fake_pkg_generation import *

from setuptools.package_index import PackageIndex
import pkg_resources
from pkg_resources import parse_version
from setuptools import setup, find_packages
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
        self.connect(self.action_Quit, QtCore.SIGNAL("triggered()"), self.quit)
        self.connect(self.action_About, QtCore.SIGNAL("triggered()"), self.about)
        self.connect(self.action_Web, QtCore.SIGNAL("triggered()"), self.web)
        
        self.connect(self.checkAll, QtCore.SIGNAL("clicked()"), self.check_all)
        self.connect(self.ClearAll, QtCore.SIGNAL("clicked()"), self.clear_all)
        
        self.connect(self.radioAll, QtCore.SIGNAL("clicked()"), self.refresh)
        self.connect(self.radioRecommended, QtCore.SIGNAL("clicked()"), self.refresh)
        self.connect(self.radioUpdate, QtCore.SIGNAL("clicked()"), self.refresh)
        self.connect(self.radioInstalled, QtCore.SIGNAL("clicked()"), self.refresh)
        self.connect(self.proceedButton, QtCore.SIGNAL("clicked()"), self.proceed)
        self.connect(self.refreshButton, QtCore.SIGNAL("clicked()"), self.refresh)
        self.connect(self.addLocButton, QtCore.SIGNAL("clicked()"), self.add_location)
        self.connect(self.removeLocButton, QtCore.SIGNAL("clicked()"), self.remove_location)
        self.connect(self.actionCookie_Session, QtCore.SIGNAL("triggered()"), self.inriagforge_authentify)
        self.connect(self.requestEdit, QtCore.SIGNAL("returnPressed()"), self.install_egg)
        self.connect(self.customPackageDirButton,QtCore.SIGNAL("clicked()"), lambda : self.get_base_custom_dirname())
        self.connect(self.customPackageIncludeButton,QtCore.SIGNAL("clicked()"), lambda : self.get_custom_dirname(self.customPackageIncludeEdit,self.customPackageDirEdit))
        self.connect(self.customPackageLibButton,QtCore.SIGNAL("clicked()"), lambda : self.get_custom_dirname(self.customPackageLibEdit,self.customPackageDirEdit))
        self.connect(self.customPackageBinButton,QtCore.SIGNAL("clicked()"), lambda : self.get_custom_dirname(self.customPackageBinEdit,self.customPackageDirEdit))
        self.connect(self.customPythonPackageButton,QtCore.SIGNAL("clicked()"), lambda : self.get_custom_dirname(self.customPythonPackageEdit,self.customPackageDirEdit))
        self.connect(self.customCppPackageFrame,QtCore.SIGNAL("toggled(bool)"),self.updateCppFrame)
        self.connect(self.customPythonPackageFrame,QtCore.SIGNAL("toggled(bool)"),self.updatePythonFrame)
        self.connect(self.customResetButton,QtCore.SIGNAL("clicked()"), self.resetCustom)
        self.connect(self.customApplyButton,QtCore.SIGNAL("clicked()"), self.applyCustom)
        try:
            from openalea.deploy.util import get_recommended_prefix
            self.recommended_prefix = get_recommended_prefix()

        except Exception, e:
            self.recommended_prefix = ["openalea"]
        self.namespaceEdit.setText(self.recommended_prefix[0])
        self.refresh()


    def quit(self):
        self.close()


    def about(self):
         """ Display About Dialog """
        
         mess = QtGui.QMessageBox.about(self, "About OpenAlea Installer",
                                        
                                        u"Copyright \xa9  2006-2008 INRIA - CIRAD - INRA\n"+
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


    def check_all(self):
        """ Check all entry in the list """
        
        for i in xrange(self.packageList.count()):
            
            item = self.packageList.item(i)
            item.setCheckState(QtCore.Qt.Checked)

        
    def clear_all(self):
        """ UnCheck all entry in the list """
        
        for i in xrange(self.packageList.count()):
            
            item = self.packageList.item(i)
            item.setCheckState(QtCore.Qt.Unchecked)


    @busy_pointer
    def refresh(self):
        """ Refresh the list of packages """

        print "Refreshing package list..."

        self.packageList.clear()
        self.pnamemap.clear()

        in_list = set() # already added project

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
            
            # Sort list by version
            # Be carefull : use parse_version rather than comparing strings!!
            dist_list = self.pi._distmap[project_name]
            dist_list = dist_list[:]
            dist_list.sort(cmp = (lambda x,y : cmp(parse_version(y.version), parse_version(x.version))))
            
            for dist in dist_list :
                
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
                    if installed_version:
                        if parse_version(max(installed_version, key=parse_version)) < parse_version(version):
                            update = True
                        else:
                            ignore = True
                            continue
                
                if(ignore) : continue
                if(update): txt += " -- UPDATE --"

                # Filter depending of mode
                if(mode == "ALL" or mode == "INSTALLED"):
                    ok = True
                    
                elif(mode == "RECOMMENDED"):

                    # Keep only most recent package
                    if(project_name in in_list): 
                        ok = False
                        continue

                    # Test all prefix
                    n = project_name.lower()
                    ok = False
                    for pref in self.recommended_prefix:
                        if(n.startswith(pref.lower())):
                            ok = True
                            break;

                    if(not ok): continue

                    
                elif(mode == "UPDATE" and update
                     and project_name not in in_list):
                    # Keep only most recent package

                    ok = True

                else : ok = False
                     
                
                if(ok):
                    in_list.add(project_name)
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
                    
        if(ok):
            self.configuration()

        self.display_finish_message(ok)
        self.refresh()


    @busy_pointer
    def configuration(self):
        """ Call alea_config """
        set_env()
        

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


    def get_custom_dirname(self, widget_to_fill = None, widget_to_use_to_start = None):
        """ Select a dirname for local custom package """
        
        init_path = ''
        if not widget_to_fill.text().isEmpty() : 
            init_path = str(widget_to_fill.text())

        if not widget_to_use_to_start is None: 
            init_path = str(widget_to_use_to_start.text())

        if len(init_path) == 0:
            init_path = QtCore.QDir.homePath()

        dirname = QtGui.QFileDialog.getExistingDirectory (
            self, "Local Custom Package Directory", init_path )
        dirname = str(dirname)
        if(dirname) : widget_to_fill.setText(dirname)
        

    def get_base_custom_dirname(self):
        """ select a base dirname for custom package """
        
        self.get_custom_dirname(self.customPackageDirEdit)

        
    def resetCustom(self):
        """ reset custom package form """
        
        self.customPackageNameEdit.clear()
        self.customPackageVersionEdit.clear()
        self.customPackageDirEdit.clear()
        self.customCppPackageFrame.setChecked(False)
        self.customPythonPackageFrame.setChecked(False)
        self.customPackageIncludeEdit.clear()
        self.customPackageLibEdit.clear()
        self.customPythonPackageEdit.clear()
        self.pythonNamespaceFrame.setChecked(False)
        self.namespaceEdit.setText(self.recommended_prefix[0])
        

    def updateCppFrame(self, enabled):
        """ update cpp information frame of custom package """
        
        if enabled:
          if not self.customPackageDirEdit.text().isEmpty():
            self.customPackageIncludeEdit.setText(
                os.path.join(str(self.customPackageDirEdit.text()),'include'))
            self.customPackageLibEdit.setText(
                os.path.join(str(self.customPackageDirEdit.text()),'lib'))
            self.customPackageBinEdit.setText(
                os.path.join(str(self.customPackageDirEdit.text()),'bin'))
        else:
            self.customPackageIncludeEdit.clear()
            self.customPackageLibEdit.clear()
            self.customPackageBinEdit.clear()
        

    def updatePythonFrame(self, enabled):
        """ update python information frame of custom package """
        
        if enabled:
          if self.customPackageDirEdit.text():
            self.customPythonPackageEdit.setText(
                os.path.join(str(self.customPackageDirEdit.text()),'src','openalea'))
        else:
            self.customPythonPackageEdit.clear()
        

    def applyCustom(self):
        """ Apply custom package form """
        
        pkg_name = str(self.customPackageNameEdit.text())
        pkg_version = str(self.customPackageVersionEdit.text())
        pkg_dir = str(self.customPackageDirEdit.text())

        # Test parameters
        if len(pkg_name) == 0 or len(pkg_version) == 0 or len(pkg_dir) == 0:
            QtGui.QMessageBox.warning(self,'Invalid custom package',
                                      'Properties of custom package are not set properly !')
            return

        if not os.path.exists(pkg_dir):
                QtGui.QMessageBox.warning(self,'Invalid package path', 'Invalid path : '+pkg_dir)
                return

        os.chdir(pkg_dir)
        args = { 'name' : pkg_name, 'version':pkg_version,  
                 'zip_safe' : False, 
                 'script_args':['-q', 'develop'], 'script_name':"" }

        # build lib and inc dirs
        if self.customCppPackageFrame.isChecked() :
            # Cpp module arguments
            pkg_lib = os.path.normpath(relative_path(pkg_dir,str(self.customPackageLibEdit.text())))
            if not os.path.exists(str(self.customPackageLibEdit.text())):
                QtGui.QMessageBox.warning(self,'Invalid package path', 
                                          'Invalid path : '
                                          + str(self.customPackageLibEdit.text()))
                return

            args['lib_dirs'] = {'lib' : pkg_lib,}
            pkg_inc = os.path.normpath(
                relative_path(pkg_dir,str(self.customPackageIncludeEdit.text())))
            
            if not os.path.exists(str(self.customPackageIncludeEdit.text())):
                QtGui.QMessageBox.warning(self,
                                          'Invalid package path', 
                                          'Invalid path : ' + 
                                          str(self.customPackageIncludeEdit.text()))
                return

            args['inc_dirs'] = {'include' : pkg_inc,}
            if len(self.customPackageBinEdit.text()) > 0:
                pkg_bin = os.path.normpath(
                    relative_path(pkg_dir,str(self.customPackageBinEdit.text())))

                if not os.path.exists(str(self.customPackageBinEdit.text())):
                    QtGui.QMessageBox.warning(self,'Invalid package path', 
                                              'Invalid path : ' + 
                                              str(self.customPackageBinEdit.text()))
                    return

                args['bin_dirs'] = {'bin' : pkg_bin,}
        
        if self.customPythonPackageFrame.isChecked():
            # Python module arguments
            # module base name and path
            py_base_path = os.path.normpath(str(self.customPythonPackageEdit.text()))
            if not os.path.exists(py_base_path):
                    QtGui.QMessageBox.warning(self,'Invalid package path', 
                                              'Invalid path : '+py_base_path)
                    return

            py_base_relative_path = os.path.normpath(relative_path(pkg_dir,py_base_path))
            py_base_module      = os.path.basename(py_base_path)
            py_base_module_path = os.path.dirname(py_base_relative_path)
            
            # submodule
            submodules = find_packages(py_base_path)

            #including namespace
            if self.pythonNamespaceFrame.isChecked() :
                namespace = str(self.namespaceEdit.text())
                args['namespace_packages'] =  [namespace]
                args['create_namespaces'] = True
                py_base_module = namespace+'.'+py_base_module

            if len(py_base_module) == 0:
                QtGui.QMessageBox.warning(self,'Invalid custom python package',
                                          'python package name for path "' + 
                                          py_base_relative_path+'" is invalid !')
                return

            py_module_map = { py_base_module : py_base_relative_path }

            for submodule in submodules:
                    m = submodule.split('.')
                    py_module_map[ py_base_module+'.'+submodule ] = \
                        os.path.join(py_base_relative_path,*m)

            args['packages'] = py_module_map.keys()

            if len(py_base_module_path) > 0:
                    py_module_map[''] = py_base_module_path
            args['package_dir'] = py_module_map

        os.chdir(pkg_dir)
        ok = True
        print 'setup('+','.join([key+'='+repr(value) for key,value in args.iteritems()])+')\n\n'

        try:
            setup(**args)
        except Exception, e:
            self.write(str(e))
            ok = False

        except :
            print "Unexpected error:", sys.exc_info()[0]
            print "Please check you have permission to install package in " + \
                  "the destination directory."
            ok = False
        print 'Done\n'
        self.display_finish_message(ok)
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
    
