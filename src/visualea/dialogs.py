# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
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
QT4 Main window 
"""

__license__= "CeCILL v2"
__revision__=" $Id$ "


from PyQt4 import QtCore, QtGui
from openalea.core.setting import get_userpkg_dir
from openalea.core.compositenode import CompositeNodeFactory
from openalea.core.pkgmanager import PackageManager
from openalea.core.settings import Settings

import ui_newgraph
import os
import ui_tofactory
import ui_newpackage
import ui_preferences
import ui_ioconfig



class NewGraph(QtGui.QDialog, ui_newgraph.Ui_NewGraphDialog) :
    """ New network dialog """
    
    def __init__(self, title, packages, categories, parent=None):
        """
        Constructor
        @param packages : the list of packages the graph can be added to
        """
        
        QtGui.QDialog.__init__(self, parent)
        ui_newgraph.Ui_NewGraphDialog.__init__(self)
        self.setWindowTitle(title)

        self.setupUi(self)

        pkgstr = []
        self.pkgmap = {}
        
        for p in packages:
            pkgstr.append(p.name)
            self.pkgmap[p.name] = p

        self.packageBox.addItems(pkgstr)
        self.categoryEdit.addItems(categories)


    def accept(self):

        # Test if name is correct
        name = str(self.nameEdit.text())
        if(not name or self.get_package().has_key(name)):
            mess = QtGui.QMessageBox.warning(self, "Error",
                                            "The Name is already use")
            return
        
        QtGui.QDialog.accept(self)


    def get_package(self):
        """ Return the selected package """

        pkgstr = str(self.packageBox.currentText().toAscii())
        return self.pkgmap[pkgstr]


    def get_data(self):
        """
        Return the dialog data in a tuple
        (name, nin, nout, category, description)
        """

        name = str(self.nameEdit.text())
        category = str(self.categoryEdit.currentText().toAscii())
        description = str(self.descriptionEdit.text().toAscii())
        
        return (name, self.inBox.value(), self.outBox.value(), self.get_package(),
                category, description)


    def get_port_lists(self, nbin, nbout):
        """ Return 2 list of inputs and outpus descriptor """
        inputs = []
        outputs = []
        for i in range(nbin):
            inputs.append(dict(name="IN%i"%(i), interface=None, value=None))
        for i in range(nbout):
            outputs.append(dict(name="OUT%i"%(i), interface=None))

        return (inputs, outputs)



    def create_cnfactory(self, pkgmanager):
        """ Create, register and return a new CompositeNodeFactory """
        
        (name, nin, nout, pkg, cat, desc) = self.get_data()

        (inputs, outputs) = self.get_port_lists(nin, nout)
        newfactory = CompositeNodeFactory( name=name,
                                           description= desc,
                                           category = cat,
                                           inputs=inputs,
                                           outputs=outputs,
                                           )
            
        pkg.add_factory(newfactory)
        
        try:
            pkg.write()
        except:
            print "Cannot Write CompositeNodeFactorty"
                
        pkgmanager.add_package(pkg)

        return newfactory


    def create_nodefactory(self, pkgmanager):
        """ Create, register and return a NodeFactory """

        (name, nin, nout, pkg, cat, desc) = self.get_data()

        (inputs, outputs) = self.get_port_lists(nin, nout)
        ret = pkg.create_user_factory(name=name,
                                      description=desc,
                                      category=cat,
                                      inputs=inputs,
                                      outputs=outputs,
                                      )
            
        pkgmanager.add_package(pkg)

        return ret




class NewPackage(QtGui.QDialog, ui_newpackage.Ui_NewPackageDialog) :
    """ New package dialog """
    
    def __init__(self, pkgs, name="", parent=None):
        """ pkgs : list of existing package name """
        
        QtGui.QDialog.__init__(self, parent)
        ui_newpackage.Ui_NewPackageDialog.__init__(self)
        self.setupUi(self)

        self.pkgs = pkgs
        self.connect(self.pathButton, QtCore.SIGNAL("clicked()"), self.path_clicked)

        self.pathEdit.setText(get_userpkg_dir())


    def path_clicked(self):

        # Test Path
        path = str(self.pathEdit.text())
        result = QtGui.QFileDialog.getExistingDirectory(self, "Select Directory", path)
    
        if(result):
            self.pathEdit.setText(result)
        

    def accept(self):

        # Test if name is correct
        name = str(self.nameEdit.text())
        if(not name or name in self.pkgs):
            mess = QtGui.QMessageBox.warning(self, "Error",
                                            "The Name is already use")
            return

        # Test Path
        path = str(self.pathEdit.text())
        if(not os.path.isdir(path)):
            mess = QtGui.QMessageBox.warning(self, "Error",
                                             "Invalid Path")
            return

        QtGui.QDialog.accept(self)


    def get_data(self):
        """
        Return a tuple (name, metainfo, path)
        metainfo is a dictionnary
        """
        name = str(self.nameEdit.text())
        path = str(self.pathEdit.text())
        metainfo = dict(
            description=str(self.descriptionEdit.text()),
            version=str(self.versionEdit.text()),
            license=str(self.licenseEdit.text()),
            authors=str(self.authorsEdit.text()),
            institutes=str(self.institutesEdit.text()),
            url=str(self.urlEdit.text()),
            )
        
        return (name, metainfo, path)



class EditPackage(QtGui.QDialog, ui_newpackage.Ui_NewPackageDialog) :
    """ Edit package dialog """
    
    def __init__(self, package, parent=None):
        """ package : package object to edit """
        
        QtGui.QDialog.__init__(self, parent)
        ui_newpackage.Ui_NewPackageDialog.__init__(self)
        self.setupUi(self)

        path = None
        if(hasattr(package, "path")):
           path = package.path
         
        self.pathButton.setVisible(False)
        self.nameEdit.setEnabled(False)
        self.pathEdit.setEnabled(False)
        
        self.set_data(package.name, path, package.metainfo)
        

    def accept(self):

        metainfo = dict(
            description=str(self.descriptionEdit.text()),
            version=str(self.versionEdit.text()),
            license=str(self.licenseEdit.text()),
            authors=str(self.authorsEdit.text()),
            institutes=str(self.institutesEdit.text()),
            url=str(self.urlEdit.text()),
            )
        
        self.package.metainfo.update(metainfo)
        
        QtGui.QDialog.accept(self)


    def set_data(self, name, path, metainfo):
        """ Set the dialog data """

        self.nameEdit.setText(name)
        if(path):
            self.pathEdit.setText(path)
        
        self.descriptionEdit.setText(metainfo.get('description', ''))
        self.versionEdit.setText(metainfo.get('version', ''))
        self.licenseEdit.setText(metainfo.get('license', ''))
        self.authorsEdit.setText(metainfo.get('authors', ''))
        self.institutesEdit.setText(metainfo.get('institutes', ''))
        self.urlEdit.setText(metainfo.get('url', ''))
               


class FactorySelector(QtGui.QDialog, ui_tofactory.Ui_FactorySelector) :
    """ New package dialog """
    
    def __init__(self, default_factory=None, parent=None):
        """
        default_factory : default choice
        """
        
        QtGui.QDialog.__init__(self, parent)
        ui_tofactory.Ui_FactorySelector.__init__(self)
        self.setupUi(self)

        self.pkgmanager = PackageManager()
        self.factorymap = {}
        
        cfactories = []
        # Get all composite node factories
        for pkg in self.pkgmanager.values():
            for f in pkg.values():
                if(isinstance(f, CompositeNodeFactory)):
                   cfactories.append(f.name)
                   self.factorymap[f.name] = f
                   

        self.comboBox.addItems(cfactories)

        if(default_factory):
            i = self.comboBox.findText(default_factory.name)
            self.comboBox.setCurrentIndex(i)

        self.connect(self.newFactoryButton, QtCore.SIGNAL("clicked()"), self.new_factory)


    def accept(self):

        # Test if name is correct
        text = self.comboBox.currentText()
        if(not text):
            mess = QtGui.QMessageBox.warning(self, "Error",
                                            "Please choose a valid model.")
            return

        QtGui.QDialog.accept(self)


    def new_factory(self):

        pkgs = self.pkgmanager.get_user_packages()
        
        dialog = NewGraph("New Graph Model", pkgs, self.pkgmanager.category.keys(), self)
        ret = dialog.exec_()

        if(ret>0):
            newfactory = dialog.create_cnfactory(self.pkgmanager)
            self.comboBox.addItem(newfactory.name)
            self.factorymap[newfactory.name] = newfactory
            i = self.comboBox.findText(newfactory.name)
            self.comboBox.setCurrentIndex(i)
        

    def get_factory(self):
        """ Return the selected factory """

        text = self.comboBox.currentText()
        return self.factorymap[str(text)]

        
   


class PreferencesDialog(QtGui.QDialog, ui_preferences.Ui_Preferences) :
    """ Preferences dialog """
    
    def __init__(self, parent):
        
        QtGui.QDialog.__init__(self, parent)
        ui_preferences.Ui_Preferences.__init__(self)
        self.setupUi(self)

        # Read config
        config = Settings()

        # pkgmanager
        try:
            str = config.get("pkgmanager", "path")
            l = eval(str)
            
            for p in l:
                self.pathList.addItem(p)
        except:
            pass

        # UI
        try:
            str = config.get("UI", "DoubleClick")
            l = eval(str)
            if("run" in l and "open" in l):
                self.dbclickBox.setCurrentIndex(0)
            elif("run" in l):
                self.dbclickBox.setCurrentIndex(1)
            elif("open" in l):
                self.dbclickBox.setCurrentIndex(2)
        except:
            pass

        

        self.connect(self.addButton, QtCore.SIGNAL("clicked()"), self.add_search_path)
        self.connect(self.removeButton, QtCore.SIGNAL("clicked()"), self.remove_search_path)


    def add_search_path(self):
        """ Package Manager : Add a path in the list """
        result = QtGui.QFileDialog.getExistingDirectory(self, "Select Directory")
    
        if(result):
            self.pathList.addItem(result)


    def remove_search_path(self):
        """ Package Manager : Remove a path in the list """

        row = self.pathList.currentRow()
        self.pathList.takeItem(row)
        

    def valid_search_path(self):
        """ Set the search path in the package manager """

        pkgmanager = PackageManager()
        pkgmanager.set_default_wraleapath()
        for i in xrange(self.pathList.count()):
            path = self.pathList.item(i).text()
            pkgmanager.add_wraleapath(os.path.abspath(str(path)))

        pkgmanager.write_config()


    def valid_ui(self):
        """ Valid UI Parameters """

        d = [["run", "open"], ["run"], ["open"],]
        index = self.dbclickBox.currentIndex()

        config = Settings()
        config.set("UI", "DoubleClick", repr(d[index]))
        config.write_to_disk()
            

    def accept(self):

        self.valid_search_path()
        self.valid_ui()
        QtGui.QDialog.accept(self)



class IOConfigDialog(QtGui.QDialog, ui_ioconfig.Ui_IOConfig) :
    """ IO Configuration dialog """
    
    def __init__(self, node, parent=None):
        """ node : the node IO to edit """
        
        QtGui.QDialog.__init__(self, parent)
        ui_ioconfig.Ui_IOConfig.__init__(self)
        self.setupUi(self)

        self.inTable.setRowCount(len(node.input_desc))
        for i, d in enumerate(node.input_desc):
            self.inTable.setItem(i, 0, QtGui.QTableWidgetItem(str(d['name'])))
            self.inTable.setItem(i, 1, QtGui.QTableWidgetItem(str(d['interface'])))
            

        self.outTable.setRowCount(len(node.output_desc))
        for i, d in enumerate(node.output_desc):
            self.outTable.setItem(i, 0, QtGui.QTableWidgetItem(str(d['name'])))
            self.outTable.setItem(i, 1, QtGui.QTableWidgetItem(str(d['interface'])))


    def accept(self):
        QtGui.QDialog.accept(self)

