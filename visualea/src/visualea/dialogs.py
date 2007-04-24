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
import ui_newgraph
import os



class NewGraph(QtGui.QDialog, ui_newgraph.Ui_NewGraphDialog) :
    """ New network dialog """
    
    def __init__(self, title, packages, categories, parent=None):
        """
        Constructor
        @param pacakges : the list of packages the graph can be added to
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


    def create_cnfactory(self, pkgmanager):
        """ Create, register and return a new CompositeNodeFactory """
        
        (name, nin, nout, pkg, cat, desc) = self.get_data()
            
        newfactory = CompositeNodeFactory( name=name,
                                           description= desc,
                                           category = cat, )
            
        newfactory.set_nb_input(nin)
        newfactory.set_nb_output(nout)
            
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

        ret = pkg.create_user_factory(name=name,
                                      description=desc,
                                      category=cat,
                                      nbin=nin,
                                      nbout=nout,
                                      )
            
        pkgmanager.add_package(pkg)

        return ret



import ui_newpackage

class NewPackage(QtGui.QDialog, ui_newpackage.Ui_NewPackageDialog) :
    """ New package dialog """
    
    def __init__(self, pkgs, name="", metainfo={}, parent=None):
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




import ui_tofactory

class FactorySelector(QtGui.QDialog, ui_tofactory.Ui_FactorySelector) :
    """ New package dialog """
    
    def __init__(self, pkgmanager, default_factory=None, parent=None):
        """
        pkgmanager : package manager
        default_factory : default choice
        """
        
        QtGui.QDialog.__init__(self, parent)
        ui_tofactory.Ui_FactorySelector.__init__(self)
        self.setupUi(self)

        self.pkgmanager = pkgmanager
        self.factorymap = {}
        
        cfactories = []
        # Get all composite node factories
        for pkg in pkgmanager.values():
            for f in pkg.values():
                if(isinstance(f, CompositeNodeFactory)):
                   cfactories.append(f.name)
                   self.factorymap[f.name] = f
                   

        self.comboBox.addItems(cfactories)

        if(default_factory):
            i = self.comboBox.findText(default_factory.name)
            self.comboBox.setCurrentIndex(i)

        self.connect(self.newFactoryButton, QtCore.SIGNAL("clicked()"), self.new_factory)



    def new_factory(self):

        pkgs = self.pkgmanager.get_user_packages()
        
        dialog = NewGraph("New Dataflow", pkgs, self.pkgmanager.category.keys(), self)
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

        
   
