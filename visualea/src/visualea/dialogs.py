# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2006-2008 INRIA - CIRAD - INRA
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
###############################################################################
"""QT4 Main window"""

__license__ = "CeCILL v2"
__revision__ = " $Id$ "

import os
from subprocess import Popen

from PyQt4 import QtCore, QtGui
from openalea.core.compositenode import CompositeNodeFactory
from openalea.core.pkgmanager import PackageManager
from openalea.core.settings import Settings, get_userpkg_dir
from openalea.core.interface import *
from openalea.core.session import Session


import ui_newgraph
import ui_tofactory
import ui_newpackage
import ui_preferences
import ui_ioconfig
import ui_tableedit
import ui_listedit
import ui_nodechooser
import ui_newdata


class NewGraph(QtGui.QDialog, ui_newgraph.Ui_NewGraphDialog) :
    """ New composite node dialog """
    
    def __init__(self, title, pmanager, parent=None,
                 factory=None, io=True, inputs=(), outputs=(),
                 pkg_id=None, name=""):
        """
        Constructor
        pmanager : the package manager
        factory : if not None, activate edition mode
        io : provide io config
        inputs and output are default inputs and output
        pkg_id : id of selected pkg
        """
        
        QtGui.QDialog.__init__(self, parent)
        ui_newgraph.Ui_NewGraphDialog.__init__(self)
        self.setWindowTitle(title)

        self.setupUi(self)

        self.factory = factory # edition mode

        packages = pmanager.get_user_packages()
        self.pmanager = pmanager

        # Build Map package name -> package
        pkgstr = []
        self.pkgmap = {}

        for p in packages:
            pkgstr.append(p.name)
            self.pkgmap[p.name] = p
        pkgstr.sort()

        # Get category
        cats = pmanager.category.keys()
        cats.sort()
        self.categoryEdit.addItems(cats)

        if(factory): # Edition mode
            self.packageBox.addItem(factory.package.name)
            self.packageBox.setEnabled(False)
            self.inputs = factory.inputs
            self.outputs = factory.outputs
            self.nameEdit.setText(factory.name)
            self.descriptionEdit.setText(factory.description)
            i = self.categoryEdit.findText(factory.category)
            self.categoryEdit.setCurrentIndex(i)

        else:
            self.packageBox.addItems(pkgstr)
            if(pkg_id):
                i = self.packageBox.findText(pkg_id)
            else:
                i = self.packageBox.findText(Session.USR_PKG_NAME)
            self.packageBox.setCurrentIndex(i)
            self.categoryEdit.setCurrentIndex(-1)
            self.inputs = inputs
            self.outputs = outputs
            self.nameEdit.setText(name)

        self.ioButton.setVisible(io)
        self.connect(self.ioButton, QtCore.SIGNAL("clicked()"), self.edit_io)
        

    def accept(self):
        """ Accept Dialog result """

        # Test if name is correct
        name = str(self.nameEdit.text())
        if(not name or
           (not self.factory and self.get_package().has_key(name)) or
           (self.factory and self.factory.name != name and 
            self.get_package().has_key(name))
           ):
            mess = QtGui.QMessageBox.warning(self, "Error",
                                            "The Name is already use")
            return
        
        QtGui.QDialog.accept(self)


    def edit_io(self):
        """ Open IO Config Dialog """

        dialog = IOConfigDialog(self.inputs, self.outputs, parent=self)
        ret = dialog.exec_()

        if(ret):
            self.inputs = dialog.inputs
            self.outputs = dialog.outputs
            

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
        if not category:
            category = 'Unclassified'
        description = str(self.descriptionEdit.text().toAscii())
        
        return (name, self.get_package(), category, description)



    def create_cnfactory(self, pkgmanager):
        """ Create, register and return a new CompositeNodeFactory """
        
        (name, pkg, cat, desc) = self.get_data()

        newfactory = pkg.create_user_compositenode( name=name,
                                                    description= desc,
                                                    category = cat,
                                                    inputs=self.inputs,
                                                    outputs=self.outputs,
                                                    )
                
        pkgmanager.add_package(pkg)

        return newfactory


    def create_nodefactory(self, pkgmanager):
        """ Create, register and return a NodeFactory """

        (name, pkg, cat, desc) = self.get_data()

        ret = pkg.create_user_node(name=name,
                                   description=desc,
                                   category=cat,
                                   inputs=self.inputs,
                                   outputs=self.outputs,
                                   )
            
        pkgmanager.add_package(pkg)

        return ret


    def update_factory(self):
        """ Update factory with value """
        (name, pkg, cat, desc) = self.get_data()

        factory = self.factory
        if(not factory) : return
        
        oldname = factory.name
        factory.name = name
        factory.description = desc
        factory.inputs = self.inputs
        factory.outputs = self.outputs
        oldcat = factory.category
        factory.category = cat
        
        factory.package.update_factory(oldname, factory)
        factory.package.write()

        # update category
        if(oldcat != cat): 
            if oldcat in self.pmanager.category:
                self.pmanager.category[oldcat].remove(factory)
            self.pmanager.update_category(factory.package)



class NewData(QtGui.QDialog, ui_newdata.Ui_NewDataDialog) :
    """ import data dialog """
    
    def __init__(self, title, pmanager, parent=None,
                 pkg_id=None):
        """
        Constructor
        pmanager : the package manager
        pkg_id : id of selected pkg
        """
        
        QtGui.QDialog.__init__(self, parent)
        ui_newdata.Ui_NewDataDialog.__init__(self)
        self.setupUi(self)

        packages = pmanager.get_user_packages()
        self.pmanager = pmanager

        # Build Map package name -> package
        pkgstr = []
        self.pkgmap = {}

        for p in packages:
            pkgstr.append(p.name)
            self.pkgmap[p.name] = p
        pkgstr.sort()

        self.packageBox.addItems(pkgstr)
        if(pkg_id):
            i = self.packageBox.findText(pkg_id)
        else:
            i = self.packageBox.findText(Session.USR_PKG_NAME)
        self.packageBox.setCurrentIndex(i)
        
        self.connect(self.browseButton, QtCore.SIGNAL("clicked()"), self.browse_file)
        

    def accept(self):
        """ Accept Dialog result """

        # Test if name is correct
        name = str(self.nameEdit.text())
        name = os.path.basename(name)
        if(not name or self.get_package().has_key(name)):
            mess = QtGui.QMessageBox.warning(self, "Error",
                                            "The Name is already use")
            return
        
        QtGui.QDialog.accept(self)


    def browse_file(self):
        """ Open File browser """

        filename = QtGui.QFileDialog.getOpenFileName(
            self, "Import file")

        filename = str(filename)
        if(not filename) : return

        self.nameEdit.setText(os.path.abspath(filename))
            

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
        description = str(self.descriptionEdit.text().toAscii())
        
        return (name, self.get_package(), description)


    def create_datafactory(self, pkgmanager):
        """ Create, register and return a new CompositeNodeFactory """
        
        (name, pkg, desc) = self.get_data()
        newfactory = pkg.add_data_file(name, desc)
        pkgmanager.add_package(pkg)

        return newfactory



class NewPackage(QtGui.QDialog, ui_newpackage.Ui_NewPackageDialog) :
    """ New package dialog """
    
    def __init__(self, pkgs, name="", parent=None, metainfo=None):
        """ 
        @param pkgs : list of existing package name
        @param name : defaut name
        @param parent :
        @metainfo : default metainfo
        """
        
        QtGui.QDialog.__init__(self, parent)
        ui_newpackage.Ui_NewPackageDialog.__init__(self)
        self.setupUi(self)

        self.pkgs = pkgs
        self.connect(self.pathButton, QtCore.SIGNAL("clicked()"), self.path_clicked)

        #self.pathEdit.setText(get_userpkg_dir())
        if(metainfo) : self.set_data(name, "", metainfo)

        self.pathEdit.setText(get_userpkg_dir())


    def path_clicked(self):

        # Test Path
        path = str(self.pathEdit.text())
        result = QtGui.QFileDialog.getExistingDirectory(self, "Select Directory", path)
    
        if(result):
            self.pathEdit.setText(result)
        

    def accept(self):
        """ Accept dialog result """
        # Test if name is correct
        name = str(self.nameEdit.text())
        if(not name or name in self.pkgs):
            mess = QtGui.QMessageBox.warning(self, "Error",
                                            "The Name is already use")
            return

        # Test Path
        path = str(self.pathEdit.text())
        if(path and not os.path.isdir(path)):
            mess = QtGui.QMessageBox.warning(self, "Error",
                                             "Invalid Path")
            return

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



class EditPackage(NewPackage) :
    """ Edit package dialog """
    
    def __init__(self, package, parent=None):
        """ @param package : package object to edit """
        
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
        self.package = package
        

    def accept(self):
        """ Accept dialog result """

        metainfo = dict(
            description=str(self.descriptionEdit.text()),
            version=str(self.versionEdit.text()),
            license=str(self.licenseEdit.text()),
            authors=str(self.authorsEdit.text()),
            institutes=str(self.institutesEdit.text()),
            url=str(self.urlEdit.text()),
            )
        
        self.package.metainfo.update(metainfo)
        if(hasattr(self.package, 'write')):
           self.package.write()           
        
        QtGui.QDialog.accept(self)



class FactorySelector(QtGui.QDialog, ui_tofactory.Ui_FactorySelector) :
    """ Dialog to select a particular CompositeNode factory """
    

    def __init__(self, default_factory=None, parent=None):
        """
        Construtor
        @param default_factory : default selected factory
        """
        
        QtGui.QDialog.__init__(self, parent)
        ui_tofactory.Ui_FactorySelector.__init__(self)
        self.setupUi(self)

        self.pkgmanager = PackageManager()
        self.factorymap = {}
        self.default_factory = default_factory

        cfactories = []
        # Get all composite node factories in writable packages
        for pkg in self.pkgmanager.get_user_packages():
            pname = pkg.name
            
            for f in pkg.itervalues():
                if(isinstance(f, CompositeNodeFactory)):
                    name = "%s.%s"%(pname, f.name)
                    cfactories.append(name)
                    self.factorymap[name] = f

        cfactories.sort()
        self.comboBox.addItems(cfactories)

        i = -1
        if(default_factory and default_factory.package):
            name = "%s.%s"%(default_factory.package.name, default_factory.name)
            i = self.comboBox.findText(name)

        self.comboBox.setCurrentIndex(i)

        self.connect(self.newFactoryButton, QtCore.SIGNAL("clicked()"), self.new_factory)


    def accept(self):
        """ Accept dialog result """
        # Test if name is correct
        text = self.comboBox.currentText()
        if(not text):
            mess = QtGui.QMessageBox.warning(self, "Error",
                                            "Invalid Choice.")
            return

        QtGui.QDialog.accept(self)


    def new_factory(self):
        """ Create a new composite node """

        if(self.default_factory and self.default_factory.package):
            pkg_id = self.default_factory.package.name
        else :
            pkg_id = None
        dialog = NewGraph("New Composite Node", self.pkgmanager, self, io=False, pkg_id=pkg_id)
        ret = dialog.exec_()

        if(ret>0):
            newfactory = dialog.create_cnfactory(self.pkgmanager)
            name = "%s.%s"%(newfactory.package.name, newfactory.name)
            self.comboBox.addItem(name)
            self.factorymap[name] = newfactory
            i = self.comboBox.findText(name)
            self.comboBox.setCurrentIndex(i)
            self.accept()
        

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
        self.session = parent.session

        # pkgmanager
        try:
            str = config.get("pkgmanager", "path")
            l = eval(str)
            
            for p in l:
                self.pathList.addItem(p)
        except:
            pass

#        try:
            #str = config.get("pkgmanager", "include_namespace")
            #enabled = bool(eval(str))

#            if(enabled):
#                self.includenmspace.setCheckState(QtCore.Qt.Checked)
#            else:
#                self.includenmspace.setCheckState(QtCore.Qt.Unchecked)
#        except:
#            pass

        # Editor
        try:
            str = config.get("editor", "use_external")
            l = eval(str)
            if(l):
                self.externalBool.setCheckState(QtCore.Qt.Checked)
            else:
                self.externalBool.setCheckState(QtCore.Qt.Unchecked)
        except Exception, e:
            print e

        try:
            str = config.get("editor", "command")
            self.commandStr.setText(str)
        except:
            pass

        self.connect(self.commandPath, QtCore.SIGNAL("clicked()"), self.select_editor)


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
            self.dbclickBox.setCurrentIndex(2)

        try:
            self.edge_style = config.get("UI", "EdgeStyle")
            if(self.edge_style == "Spline"):
                self.comboBox.setCurrentIndex(0)
            elif(self.edge_style == "Polyline"):
                self.comboBox.setCurrentIndex(1)
            elif(self.edge_style == "Line"):
                self.comboBox.setCurrentIndex(2)
        except:
            self.edge_style = "Spline"

        # Dataflow
        try:
            str = config.get("eval", "type")
            str = str.strip('"')
            eval_algo = str.strip("'")
        except:
            eval_algo = "SelectiveEvaluation"

        self.update_eval_algo(eval_algo)

        self.connect(self.addButton, QtCore.SIGNAL("clicked()"), self.add_search_path)
        self.connect(self.removeButton, QtCore.SIGNAL("clicked()"), self.remove_search_path)


    def add_search_path(self):
        """ Package Manager : Add a path in the list """

        result = QtGui.QFileDialog.getExistingDirectory(self, "Select Directory")
        
        if(result):
            self.pathList.addItem(result)


    def select_editor(self):
        """ Select Python Editor command """

        filename = QtGui.QFileDialog.getOpenFileName(
            self, "Select python editor")

        filename = str(filename)
        if(not filename) : return

        if(filename):
            self.commandStr.setText(filename)


    def update_eval_algo(self, algo_str):
        """ Search available evaluation algorithm
        and select algo_str """

        import openalea.core.algo.dataflow_evaluation as evalmodule
        
        # Search class obj in module
        l = lambda x: isinstance(x, type) and evalmodule.AbstractEvaluation in x.mro()
        classlist = filter(l, evalmodule.__dict__.values())
        classlist.remove(evalmodule.AbstractEvaluation)
        
        selectitem = None
        for c in classlist:
            try:
                item = QtGui.QListWidgetItem(c.__name__)
                self.listAlgo.addItem(item)
                if(c.__name__ == algo_str):
                    selectitem = item
            except:
                pass
            
        if(selectitem):
            self.listAlgo.setCurrentItem(selectitem)


    def remove_search_path(self):
        """ Package Manager : Remove a path in the list """

        row = self.pathList.currentRow()
        self.pathList.takeItem(row)
        

    def valid_search_path(self):
        """ Set the search path in the package manager """

        pkgmanager = PackageManager()

        pkgmanager.user_wralea_path.clear()

        for i in xrange(self.pathList.count()):
            path = self.pathList.item(i).text()
            pkgmanager.add_wralea_path(os.path.abspath(str(path)), pkgmanager.user_wralea_path)

        pkgmanager.write_config()


    def valid_ui(self):
        """ Valid UI Parameters """

        d = [["run", "open"], ["run"], ["open"],]
        index = self.dbclickBox.currentIndex()

        styles = ["Spline", "Polyline", "Line"]
        edge_style_index = self.comboBox.currentIndex()
        edge_style = styles[edge_style_index]
        
        config = Settings()
        config.set("UI", "DoubleClick", repr(d[index]))
        config.set("UI", "EdgeStyle", edge_style)
        config.write_to_disk()

        if edge_style != self.edge_style:
            self.edge_style = edge_style
            session = self.session
            session.notify_listeners()
            ws = session.workspaces
            for cn in ws:
                cn.notify_listeners(('graph_modified',))


    def valid_dataflow(self):
        """ Valid dataflow parameter """
        item = self.listAlgo.currentItem()
        if(item):
            algostr = str(item.text())
        
            config = Settings()
            config.set("eval", "type", algostr)
            config.write_to_disk()


    def valid_editor(self):
        """ Valid editor parameter """
        use_ext = bool(self.externalBool.checkState() == QtCore.Qt.Checked)
        command = str(self.commandStr.text())

        config = Settings()
        config.set("editor", "use_external", repr(use_ext))
        config.set("editor", "command", command)
        config.write_to_disk()

        
          

    def accept(self):
        """ Validate dialog results """

        self.valid_search_path()
        self.valid_ui()
        self.valid_dataflow()
        self.valid_editor()
        QtGui.QDialog.accept(self)



class ComboDelegate(QtGui.QItemDelegate):
    """ 
    Tool class used in IO editor 
    It allows to choose an interface from a combobox in a QTable
    """

    def get_interfaces(self):
        """ Return the list of availble interfaces """

        x =  [k.__name__ for k in IInterfaceMetaClass.all]
        x.sort()
        x.append('None')
        return x
        
    
    def createEditor(self, parent, option, index):
        """ Create the editor """
        if index.column() == 1:
            editor = QtGui.QComboBox(parent)
            editor.addItems(self.get_interfaces())
            return editor

        return QtGui.QItemDelegate.createEditor(self, parent, option, index)

    
    def setEditorData(self, editor, index):
        """ Accessor """

        if index.column() == 1:
            value = str(index.data().toString())
            i = editor.findText(value)
            editor.setCurrentIndex (i)
        else:
            QtGui.QItemDelegate.setEditorData(self, editor, index)


    def setModelData(self, editor, model, index):
        """ Accessor """
        if index.column() == 1:
            value = editor.currentText()
            model.setItem(index.row(), index.column(),
                          QtGui.QStandardItem(str(value)))
        else:
            QtGui.QItemDelegate.setModelData(self, editor, model, index)


class IOConfigDialog(QtGui.QDialog, ui_ioconfig.Ui_IOConfig) :
    """ IO Configuration dialog """
    
    def __init__(self, inputs=(), outputs=(), parent=None):
        """ node : the node IO to edit """
        
        QtGui.QDialog.__init__(self, parent)
        ui_ioconfig.Ui_IOConfig.__init__(self)
        self.setupUi(self)
        delegate = ComboDelegate()
        self.__delegate = delegate

        self.inputs = inputs
        self.outputs = outputs
        
        self.inModel = QtGui.QStandardItemModel(len(inputs), 4)
        self.inModel.setHorizontalHeaderLabels(["Name", "Interface", "Value", "Description"])
        self.inTable.setModel(self.inModel)

        self.inTable.setItemDelegate(delegate)

        self.outModel = QtGui.QStandardItemModel(len(outputs), 3)
        self.outModel.setHorizontalHeaderLabels(["Name", "Interface", "Description"])
        self.outTable.setModel(self.outModel)
        
        self.outTable.setItemDelegate(delegate)

        #self.inTable.setItemDelegateForColumn(1, ComboBoxDeletegate())
                                                      
        for i, d in enumerate(inputs):
            self.inModel.setItem(i, 0, QtGui.QStandardItem(str(d['name'])))
            self.inModel.setItem(i, 1, QtGui.QStandardItem(str(d['interface'])))
            self.inModel.setItem(i, 2, QtGui.QStandardItem(str(d.get('value'))))
            self.inModel.setItem(i, 3, QtGui.QStandardItem(str(d.get('desc', ''))))

        for i, d in enumerate(outputs):
            self.outModel.setItem(i, 0, QtGui.QStandardItem(str(d['name'])))
            self.outModel.setItem(i, 1, QtGui.QStandardItem(str(d['interface'])))
            self.outModel.setItem(i, 2, QtGui.QStandardItem(str(d.get('desc', ''))))


        self.connect(self.addInput, QtCore.SIGNAL("clicked()"), self.add_input)
        self.connect(self.delInput, QtCore.SIGNAL("clicked()"), self.del_input)
        self.connect(self.addOutput, QtCore.SIGNAL("clicked()"), self.add_output)
        self.connect(self.delOutput, QtCore.SIGNAL("clicked()"), self.del_output)


    def accept(self):
        """ Valid IO """

        # build input dict
        self.inputs = []
        c = self.inModel.rowCount()
        for i in xrange(c):
            name = str(self.inModel.item(i,0).text())
            interface_str = str(self.inModel.item(i,1).text())
            val_str = str(self.inModel.item(i,2).text())
            desc_str = str(self.inModel.item(i,3).text())

            try:
                interface = eval(interface_str)
            except:
                interface = None

            try:
                val = eval(val_str)
            except:
                val = None

        
            self.inputs.append(dict(name=name, interface=interface, value=val, desc=desc_str))
            

        # build output dict
        self.outputs = []
        c = self.outModel.rowCount()
        for i in xrange(c):
            name = str(self.outModel.item(i,0).text())
            interface_str = str(self.outModel.item(i,1).text())
            desc_str = str(self.outModel.item(i,2).text())

            try:
                interface = eval(interface_str)
            except:
                interface = None

            self.outputs.append(dict(name=name, interface=interface, desc=desc_str))
        
        QtGui.QDialog.accept(self)


    def add_input(self):
        c = self.inModel.rowCount()
        self.inModel.appendRow([QtGui.QStandardItem('IN%i'%(c+1,)),
                                QtGui.QStandardItem('None'),
                                QtGui.QStandardItem('None'),
                                QtGui.QStandardItem('')])


    def add_output(self):
        c = self.outModel.rowCount()
        self.outModel.appendRow([QtGui.QStandardItem('OUT%i'%(c+1,)),
                                QtGui.QStandardItem('None'),
                                 QtGui.QStandardItem('')])

        
    def del_input(self):
        c = self.inModel.rowCount()
        self.inModel.takeRow(c-1)


    def del_output(self):
        c = self.outModel.rowCount()
        self.outModel.takeRow(c-1)
        


class DictEditor(QtGui.QDialog, ui_tableedit.Ui_TableEditor):
    """Dictionnary editor (used for node internals)

    If accepted :
        - self.pdict contains the modified dictionary
        - self.modified_key  contains the list of modified key

    """
    
    def __init__(self, pdict, parent):

        QtGui.QDialog.__init__(self, parent)
        ui_tableedit.Ui_TableEditor.__init__(self)
        self.setupUi(self)

        self.pdict = pdict.copy() # copy the dictionary
        self.modified_key = [] # list of modified key

        # Fill the table
        self.tableWidget.setRowCount(len(pdict.keys()))
        for (i, (k,v)) in enumerate(pdict.items()):

            item = QtGui.QTableWidgetItem(str(k))
            item.setFlags(QtCore.Qt.ItemIsEnabled)
            self.tableWidget.setItem(i, 0, item)
            self.tableWidget.setItem(i, 1, QtGui.QTableWidgetItem(str(v)))
        
        
    def accept(self):

        # Check for modification in each row
        for (i, (k,v)) in enumerate(self.pdict.items()):
            keyitem = self.tableWidget.item(i, 0)
            valueitem = self.tableWidget.item(i, 1)

            if(str(keyitem.text()) != str(k)): continue
            s = str(valueitem.text())
            if(s != str(v)):
                
                self.modified_key.append(k)
                try:
                    self.pdict[k] = eval(s)
                except:
                    self.pdict[k] = s
                    
        QtGui.QDialog.accept(self)


class ShowPortDialog(QtGui.QDialog, ui_listedit.Ui_ListEdit):
    """
    Port show status configuration dialog
    """

    def __init__(self, node, parent):

        QtGui.QDialog.__init__(self, parent)
        ui_listedit.Ui_ListEdit.__init__(self)
        self.setupUi(self)

        self.setWindowTitle("Show/Hide ports")

        self.node = node
        
        for i, desc in enumerate(node.input_desc):

            try:
                interface = desc.get('interface').__name__
            except:
                interface = ""

            
            txt = "%s %s"%(desc['name'], interface)
            listitem = QtGui.QListWidgetItem(txt, self.listWidget)
            
            if(node.input_states[i] is not "connected"):
                listitem.setFlags(QtCore.Qt.ItemIsEnabled|QtCore.Qt.ItemIsUserCheckable)
            else:
                listitem.setFlags(QtCore.Qt.ItemIsUserCheckable)

            #hide = desc.is_hidden()
            hide = node.is_port_hidden(i)

            if(not hide):
                listitem.setCheckState(QtCore.Qt.Checked)
            else:
                listitem.setCheckState(QtCore.Qt.Unchecked)

                
        
    def accept(self):
        """ Set port status in the node """

        for i in xrange(self.listWidget.count()):
            item = self.listWidget.item(i)

            if(self.node.input_states[i] is "connected"):
                self.node.set_port_hidden(i, False)
                
            elif(item and (item.flags() & QtCore.Qt.ItemIsEnabled)):

                if(item.checkState() == QtCore.Qt.Checked):
                    self.node.set_port_hidden(i, False)
                else:
                    self.node.set_port_hidden(i, True)

        self.node.notify_listeners( ("port_modified", ) )

                    
        QtGui.QDialog.accept(self)



   


class NodeChooser(QtGui.QDialog, ui_nodechooser.Ui_NodeChooser):
    """ Dialog allowing to choose a node (package view) """

    def __init__(self, parent):
        from node_treeview import SearchListView, SearchModel

        QtGui.QDialog.__init__(self, parent)
        ui_nodechooser.Ui_NodeChooser.__init__(self)
        self.setupUi(self)

        self.pman = PackageManager()
        self.map = {}


    def search(self, name='', nb_inputs=-1, nb_outputs=-1):
        """ Add node to combo box selector corresponding to request 
        @param name
        @param nb_inputs
        @param nb_outputs
        """

        res = self.pman.search_node(name, nb_inputs, nb_outputs)
        strs = []

        for f in res:
            key = "%s.%s"%(f.package.get_id().lower(), f.name)
            self.map[key] = f
            strs.append(key)
        
        strs.sort()
        self.comboBox.addItems(strs)

    
    def get_selection(self):
        """ Return selected factory """

        s = str(self.comboBox.currentText())
        
        if(self.map.has_key(s)):
            return self.map[s]

        return None


    def accept(self):
        """ Validate result """

        s = str(self.comboBox.currentText())
        
        if(self.map.has_key(s)):
            QtGui.QDialog.accept(self)
        
        else:
            QtGui.QMessageBox.warning(self, "Error", "Unknown component name")

            


