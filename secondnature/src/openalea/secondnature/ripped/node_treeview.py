# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
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
################################################################################
"""Tree Item model for package manager.

Only Package and Category objects are view as a tree item.
Others are view as leaves.
"""

__license__ = "CeCILL v2"
__revision__ = " $Id$ "

import os
from weakref import ref

from PyQt4 import QtCore, QtGui

from openalea.core.observer import AbstractListener
from openalea.core.node import NodeFactory, AbstractFactory
from openalea.core.data import DataFactory
from openalea.core.package import Package, UserPackage
from openalea.core.compositenode import CompositeNodeFactory
from openalea.core.pkgmanager import PackageManager
from openalea.core.pkgmanager import PseudoGroup, PseudoPackage
from openalea.core import cli

from openalea.visualea.dialogs import EditPackage, NewGraph, NewPackage, NewData
from openalea.visualea.util import open_dialog, exception_display, busy_cursor
from openalea.visualea.node_widget import SignalSlotListener
from openalea.visualea.code_editor import get_editor
from openalea.visualea.util import grab_icon

from openalea.visualea import images_rc
import urllib

# Utilities function
icon_dict = None

def init_global_icons():
    global icon_dict
    if(not icon_dict):
        # dict to do a switch
        icon_dict = {
            PseudoGroup : QtGui.QIcon(":/icons/category.png"),
            CompositeNodeFactory : QtGui.QIcon(":/icons/diagram.png"),
            NodeFactory : QtGui.QIcon(":/icons/node.png"),
            DataFactory : QtGui.QIcon(":/icons/data.png"),
            UserPackage : QtGui.QIcon(":/icons/usrpkg.png"),
            Package :  QtGui.QIcon(":/icons/pkg.png"),
            }

def get_icon2(item):
    """ Return Icon object depending of the type of item """
    if(isinstance(item, Package)):
        # Try to load package specific icon
        icon = item.metainfo.get("icon", None)
        if(icon):
            icon = os.path.join(item.path, icon)
            return QtGui.QIcon(icon)
        # Standard icon
        return icon_dict[type(item)]
    # Get icon from dictionary
    elif(icon_dict.has_key(type(item))):
        return icon_dict[type(item)]
    else:
        return QtGui.QIcon(":/icons/pseudopkg.png")


# Qt4 Models/View classes
import collections
TrNode = collections.namedtuple("TrNode", "item children")

class PkgModel(QtGui.QStandardItemModel, AbstractListener):
    pkgmodelRole =  QtCore.Qt.UserRole + 40

    def __init__(self, pkgmanager, parent=None):
        QtGui.QStandardItemModel.__init__(self, parent)
        AbstractListener.__init__(self)
        init_global_icons()
        self.pman = pkgmanager
        self.paths = {}
        self.pkgnames = set()
        self.build_item_tree(pkgmanager)
        self.initialise(pkgmanager)

    def build_item_tree(self, pman):
        # -- sorting is important, it ensures less dotted
        # names are created before more dotted names
        # (parents before children) --
        pkgs = sorted(pman.get_packages(),
                      lambda x,y: cmp(x.name.lower(),y.name.lower()))

        base = par = TrNode(self, self.paths)
        self.remove_obsoletes(pkgs, base)
        self.pkgnames = set(p.name.lower() for p in pkgs)
        for pkg in pkgs:
            self.add_package_items(pkg, base)

    def add_package_items(self, pkg, base):
        dottedPath = pkg.name.split(".")
        par = base
        for pkName in dottedPath:
            #: cpar is the next sub parent
            cpar = par.children.get(pkName.lower())
            if cpar is None:
                item = QtGui.QStandardItem(pkName)
                self.decorate_element(pkg, pkName, item, parent=par.item)
                childrenDict = {}
                newNode = TrNode(item, childrenDict)
                par.children[pkName.lower()] = newNode
                cpar = newNode
            par = cpar

        for fac in pkg.iter_public_values():
            item = par.children.get(fac.name)
            if not item:
                item = QtGui.QStandardItem(fac.name)
                par.children[fac.name] = item
                self.decorate_element(fac, fac.name, item, par.item)

    def get_node(self, base, name, pop=True):
        dottedPath = name.lower().split(".")
        pathLen    = len(dottedPath)
        preleaf = base
        leaf = None

        if pathLen == 1:
            return None, preleaf.children.get(dottedPath[0])
        else:
            for pkName in dottedPath[:-1]:
                if preleaf:
                    preleaf = preleaf.children.get(pkName)

        if len(dottedPath)==1:
            return None, preleaf

        if preleaf:
            if pop:
                leaf = preleaf.children.pop(dottedPath[-1], None)
            else:
                leaf = preleaf.children.get(dottedPath[-1], None)
        return preleaf, leaf

    def remove_package_items(self, pkg, base):
        if isinstance(pkg, Package):
            name = pkg.name
        elif isinstance(pkg, str):
            name = pkg
        preleaf = base
        preleaf, leaf = self.get_node(base=preleaf, name=pkg.name)
        if preleaf and leaf:
            preleaf.item.removeRow(leaf.row())

    def remove_obsoletes(self, pkgs, base):
        # remove factories that don't exist anymore
        for pkg in pkgs:
            preleaf, leaf = self.get_node(base, pkg.name, pop=False)
            if leaf is None:
                continue
            pkgFacs = set(f.name for f in pkg.iter_public_values())
            childCopy = leaf.children.copy()
            for facName, facItem in childCopy.iteritems():
                if facName not in pkgFacs:
                    if isinstance(facItem, TrNode):
                        #a package can contain Factories AND sub packages (represented by TrNode)
                        continue
                    leaf.item.removeRow(facItem.row())
                    del leaf.children[facName]

        # remove packages that don't exist anymore
        pkgnames = set(p.name for p in pkgs)
        obsoletes = self.pkgnames - pkgnames
        for pname in obsoletes:
            pass#self.remove_package_items(pname, base)

    def notify(self, sender, event):
        if event=="update":
            self.build_item_tree(sender)

    def decorate_element(self, elt, name, newItem, parent=None):
        icon = get_icon2(elt)
        newItem.setIcon(icon)
        newItem.setToolTip(elt.get_tip())
        newItem.setData(QtCore.QVariant(elt), self.pkgmodelRole)
        if parent:
            parent.appendRow(newItem)
        return newItem

    def mimeData(self, modelIndexes):
        item       = self.itemFromIndex(modelIndexes[0])
        mimeData   = QtGui.QStandardItemModel.mimeData(self, modelIndexes)
        (pkg_id, factory_id, mimetype) = self.get_item_info(item)

        # -- marshall package and factory to the data stream, needed later --
        itemData   = QtCore.QByteArray()
        dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.WriteOnly)
        dataStream << QtCore.QString(pkg_id) << QtCore.QString(factory_id)
        mimeData.setData(mimetype, itemData)

        # -- build an url --
        factory = PackageManager()[pkg_id][factory_id]
        if isinstance(factory, DataFactory):
            url = QtCore.QUrl.fromLocalFile(factory.get_pkg_data().repr)
        else:
            query   = ["fac="+factory_id]
            ftname  = type(factory).__name__
            query.append("ft="+ftname)
            query = reduce(lambda x,y:"&".join((x,y)), query)
            url = QtCore.QUrl("oa://local/"+pkg_id+"?"+query)

        mimeData.setUrls([url])
        return mimeData

    def mimeTypes(self):
        return QtGui.QStandardItemModel.mimeTypes(self) + \
               [DataFactory.mimetype, NodeFactory.mimetype, CompositeNodeFactory.mimetype]


    def headerData(self, section, orientation, role):
        return QtCore.QVariant()

    @classmethod
    def get_item_info(cls, item):
        """
        Return (package_id, factory_id, mimetype) corresponding to item.
        """
        # put in the Mime Data pkg id and factory id
        var = item.data(cls.pkgmodelRole)
        obj = var.toPyObject()

        if obj.mimetype in [NodeFactory.mimetype, CompositeNodeFactory.mimetype]:
            factory_id = obj.get_id()
            pkg_id = obj.package.get_id()
            return (pkg_id, factory_id, obj.mimetype)
        return ("","", "openalea/notype")





class DataPoolModel (QtCore.QAbstractListModel) :
    """ QT4 data model (model/view pattern) to support Data Pool """

    def __init__(self, datapool, parent=None):

        QtCore.QAbstractListModel.__init__(self, parent)
        self.datapool = datapool


    def reset(self):
        QtCore.QAbstractItemModel.reset(self)


    def data(self, index, role):

        if (not index.isValid()):
            return QtCore.QVariant()

        if (index.row() >= len(self.datapool.keys())):
            return QtCore.QVariant()

        if (role == QtCore.Qt.DisplayRole):
            l = self.datapool.keys()
            l.sort()
            name = l[index.row()]
            #classname = self.datapool[name].__class__
            value = repr(self.datapool[name])
            if(len(value) > 30) : value = value[:30] + "..."
            return QtCore.QVariant("%s ( %s )"%(name, value))

        # Icon
        elif( role == QtCore.Qt.DecorationRole ):
            return QtCore.QVariant(QtGui.QPixmap(":/icons/ccmime.png"))

        # Tool Tip
        elif( role == QtCore.Qt.ToolTipRole ):
            l = self.datapool.keys()
            l.sort()
            name = l[index.row()]

            tips = [name]

            tips.append("%s\n"%(str(self.datapool[name]),))
            tips.append("Dir :")

            temp = ""
            for i, n in enumerate(dir(self.datapool[name])):
                s = str(n)
                if(len(s) > 20): s = s[:20]
                temp += s + "\t\t"
                # 2 column view
                if(i%2):
                    tips.append(temp)
                    temp = ""

            if(temp) : tips.append(temp)
            tipstr = '\n'.join(tips)

            return QtCore.QVariant(str(tipstr))

        else:
            return QtCore.QVariant()


    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled

        return QtCore.Qt.ItemIsEnabled | \
               QtCore.Qt.ItemIsSelectable | \
               QtCore.Qt.ItemIsDragEnabled


    def headerData(self, section, orientation, role):
        return QtCore.QVariant()


    def rowCount(self, parent):
        return len(self.datapool.keys())




################################################################################
# Views

class NodeFactoryView(object):

    def __init__(self, siblings=[]):
        self.__siblings = siblings

    @staticmethod
    def get_item_info(item):
        """
        Return (package_id, factory_id, mimetype) corresponding to item.
        """

        # put in the Mime Data pkg id and factory id
        obj = item.internalPointer()

        if obj.mimetype in [NodeFactory.mimetype, CompositeNodeFactory.mimetype]:

            factory_id = obj.get_id()
            pkg_id = obj.package.get_id()

            return (pkg_id, factory_id, obj.mimetype)

        return ("","", "openalea/notype")


    def contextMenuEvent(self, event):
        """ Context menu event : Display the menu"""

        index = self.indexAt(event.pos())
        obj   = self.model().data(index, PkgModel.pkgmodelRole).toPyObject()
        menu  = None

        if(isinstance(obj, AbstractFactory)): # Factory
            menu = QtGui.QMenu(self)
            action = menu.addAction("Open")
            self.connect(action, QtCore.SIGNAL("triggered()"), self.open_node)

            action = menu.addAction("Edit")
            self.connect(action, QtCore.SIGNAL("triggered()"), self.edit_node)

            action = menu.addAction("Properties")
            self.connect(action, QtCore.SIGNAL("triggered()"), self.edit_properties)

            menu.addSeparator()

            action = menu.addAction("Remove")
            self.connect(action, QtCore.SIGNAL("triggered()"), self.remove_node)

        elif(isinstance(obj, Package)): # Package

            enabled = True#obj.is_real_package()
            pkg = obj

            menu = QtGui.QMenu(self)

            action = menu.addAction("Open URL")
            action.setEnabled(enabled)
            self.connect(action, QtCore.SIGNAL("triggered()"), self.open_node)

            action = menu.addAction("Meta informations")
            action.setEnabled(enabled)
            self.connect(action, QtCore.SIGNAL("triggered()"), self.edit_package)

            action = menu.addAction("Edit Code")
            action.setEnabled(enabled and pkg.is_editable())
            self.connect(action, QtCore.SIGNAL("triggered()"), self.edit_pkg_code)

            menu.addSeparator()

            action = menu.addAction("Add Python Node")
            action.setEnabled(enabled and pkg.is_editable())
            self.connect(action, QtCore.SIGNAL("triggered()"), self.add_python_node)

            action = menu.addAction("Add Composite Node")
            action.setEnabled(enabled and pkg.is_editable())
            self.connect(action, QtCore.SIGNAL("triggered()"), self.add_composite_node)

            action = menu.addAction("Add Data File")
            action.setEnabled(enabled and pkg.is_editable())
            self.connect(action, QtCore.SIGNAL("triggered()"), self.add_data)

            menu.addSeparator()

            action = menu.addAction("Grab Icon")
            action.setEnabled(enabled)
            self.connect(action, QtCore.SIGNAL("triggered()"), self.grab_icon)

            menu.addSeparator()

            action = menu.addAction("Move/Rename Package")
            action.setEnabled(enabled and pkg.is_editable())
            self.connect(action, QtCore.SIGNAL("triggered()"), self.move_package)

            action = menu.addAction("Copy Package")
            action.setEnabled(enabled)
            self.connect(action, QtCore.SIGNAL("triggered()"), self.duplicate_package)

            action = menu.addAction("Remove Package")
            action.setEnabled(enabled and pkg.is_editable())
            self.connect(action, QtCore.SIGNAL("triggered()"), self.remove_package)


            menu.addSeparator()

            action = menu.addAction("Reload Package")
            action.setEnabled(enabled)
            self.connect(action, QtCore.SIGNAL("triggered()"), self.reload_package)

        if(menu):
            menu.popup(event.globalPos())



    def get_current_pkg(self):
        """ Return the current package """
        index = self.currentIndex()
        obj   = self.model().data(index, PkgModel.pkgmodelRole).toPyObject()
        return obj


    def add_python_node(self):
        """ """
        pman = self.model().pman # pkgmanager
        pkg = self.get_current_pkg()

        dialog = NewGraph("New Python Node", pman, self, pkg_id=pkg.name)
        ret = dialog.exec_()

        if(ret>0):
            dialog.create_nodefactory(pman)


    def add_composite_node(self):
        """ """
        pman = self.model().pman # pkgmanager
        pkg = self.get_current_pkg()

        dialog = NewGraph("New Composite Node", pman, self, pkg_id=pkg.name)
        ret = dialog.exec_()

        if(ret>0):
            newfactory = dialog.create_cnfactory(pman)


    def add_data(self):
        """ """
        pman = self.model().pman # pkgmanager
        pkg = self.get_current_pkg()

        dialog = NewData("Import Data", pman, self, pkg_id=pkg.name)
        ret = dialog.exec_()

        if(ret>0):
            newfactory = dialog.create_datafactory(pman)



    def remove_package(self):
        """ Remove selected package """

        pkg = self.get_current_pkg()
        pman = self.model().pman # pkgmanager

        if(not pkg.is_directory()):
            QtGui.QMessageBox.warning(self, "Error",
                                             "Cannot Remove old style package\n")
            return

        if(not pkg.is_editable()): return

        ret = QtGui.QMessageBox.question(self, "Remove package",
                                         "Remove %s?\n"%(pkg.name,),
                                         QtGui.QMessageBox.Yes, QtGui.QMessageBox.No,)

        if(ret == QtGui.QMessageBox.No):
            return

        try:
            pkg.remove_files()
        except AssertionError:
            return

        del pman[pkg.get_id()]



    def grab_icon(self):
        """ Set the package icon """

        pkg = self.get_current_pkg()
        pix = grab_icon(self)

        fname = os.path.join(pkg.path, "icon.png")
        pix.save(fname)
        pkg.set_icon(fname)


    def edit_pkg_code(self):
        """ Edit __wralea__ """

        pkg = self.get_current_pkg()
        pman = self.model().pman # pkgmanager

        if(not pkg.is_directory()):
            QtGui.QMessageBox.warning(self, "Error",
                                             "Cannot edit code of old style package\n")
            return

        filename = pkg.get_wralea_path()
        widget = get_editor()(self)
        widget.edit_file(filename)
        if(widget.is_widget()) : open_dialog(self, widget, pkg.name)


    def reload_package(self):
        """ Reload package """

        pkg = self.get_current_pkg()
        pman = self.model().pman # pkgmanager

        if(not pkg.is_directory()):
            QtGui.QMessageBox.warning(self, "Error",
                                             "Cannot reload old style package\n")
            return

        pman.reload(pkg)


    def duplicate_package(self):
        """ Duplicate a package """

        pkg = self.get_current_pkg()
        pman = self.model().pman # pkgmanager

        if(not pkg.is_directory()):
            QtGui.QMessageBox.warning(self, "Error",
                                             "Cannot duplicate old style package\n")
            return


        dialog = NewPackage(pman.keys(), parent = self, metainfo=pkg.metainfo)
        ret = dialog.exec_()

        if(ret>0):
            (name, metainfo, path) = dialog.get_data()

            newpkg = pman.create_user_package(name, metainfo, path)
            newpkg.clone_from_package(pkg)
            pman.add_package(newpkg)


    def move_package(self):
        """ Move a package """

        pkg = self.get_current_pkg()
        pman = self.model().pman # pkgmanager

        if(not pkg.is_directory()):
            QtGui.QMessageBox.warning(self, "Error",
                                      "Cannot move old style package\n")
            return


        (result, ok) = QtGui.QInputDialog.getText(self, "Move/Rename Package",
                                                  "Full new name (ex: openalea.data)",
                                                  QtGui.QLineEdit.Normal, )

        if(ok):
            new_name = str(result)
            old_name = pkg.name
            pman.rename_package(old_name, new_name)


    def edit_package(self):
        """ Edit package Metadata """

        obj = self.get_current_pkg()

        dialog = EditPackage(obj, parent = self)
        ret = dialog.exec_()


    def mouseDoubleClickEvent(self, event):

        index = self.currentIndex()
        obj   = self.model().data(index, PkgModel.pkgmodelRole).toPyObject()

        msg = """You are trying to open a composite node that has already been opened.
        Doing this might cause confusion later on.
        Do you want to continue?"""

        if(isinstance(obj, CompositeNodeFactory)):
            for ws in self.__siblings:
                if obj == ws.factory:
                    res = QtGui.QMessageBox.warning(self, "Other instances are already opened!",
                                                    msg,
                                                    QtGui.QMessageBox.Ok | \
                                                    QtGui.QMessageBox.Cancel)
                    if res == QtGui.QMessageBox.Cancel:
                        return
                    else:
                        break
            self.edit_node()

        elif (not isinstance(obj, Package)):
            self.open_node()


    @busy_cursor
    @exception_display
    def open_node(self):
        """ Instantiate Node : open a dialog """
        index = self.currentIndex()
        obj   = self.model().data(index, PkgModel.pkgmodelRole).toPyObject()

        if(isinstance(obj, AbstractFactory)):
            widget = obj.instantiate_widget(autonomous=True)
            open_dialog(self, widget, obj.get_id())

        elif(isinstance(obj, Package)):
            # Display URL
            urlstr = obj.get_metainfo('url')
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(urlstr))

    @busy_cursor
    @exception_display
    def edit_node(self):
        """ Edit Node in tab workspace"""

        index = self.currentIndex()
        obj   = self.model().data(index, PkgModel.pkgmodelRole).toPyObject()

        if isinstance(obj, CompositeNodeFactory):
            self.compositeFactoryOpenRequest.emit(obj)
        elif isinstance(obj, NodeFactory) or \
             isinstance(obj, DataFactory):
            widget = obj.instantiate_widget(edit=True)
            if(widget.is_widget()) :
                open_dialog(self, widget, obj.get_id())


    def edit_properties(self):
        """ Edit Node info"""

        index = self.currentIndex()
        obj   = self.model().data(index, PkgModel.pkgmodelRole).toPyObject()

        if(isinstance(obj, DataFactory)):
            QtGui.QMessageBox.information(self, "Properties", "Data : %s"%(obj.name))
            return

        d = NewGraph("Node Properties", PackageManager(), self, obj)
        ret = d.exec_()
        if(ret):
            d.update_factory()


    def remove_node(self):
        """ Remove the node from the package """
        pman  = self.model().pman
        index = self.currentIndex()
        obj   = self.model().data(index, PkgModel.pkgmodelRole).toPyObject()

        ret = QtGui.QMessageBox.question(self, "Remove Model",
                                         "Remove %s?\n"%(obj.name,),
                                         QtGui.QMessageBox.Yes, QtGui.QMessageBox.No,)

        if(ret == QtGui.QMessageBox.Yes):

            try:
                obj.package[obj.name].clean_files()
            except Exception, e:
                print e

            del(obj.package[obj.name])
            obj.package.write()
            pman.emit_update()



class PackageManagerView(QtGui.QWidget):
    def __init__(self, siblings=[], parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.__lay = QtGui.QVBoxLayout()
        self.__lay.setContentsMargins(2,2,2,2)
        self.__searchField = QtGui.QLineEdit()
        self.__treeView    = NodeFactoryTreeView(siblings)
        self.__lay.addWidget(self.__searchField)
        self.__lay.addWidget(self.__treeView)
        self.__searchField.hide()
        self.__searchField.installEventFilter(self)
        self.setLayout(self.__lay)

    def setModel(self, model):
        self.__treeView.setModel(model)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_F and \
           event.modifiers()==QtCore.Qt.ControlModifier:
            self.__searchField.show()
            self.__searchField.setFocus(QtCore.Qt.ShortcutFocusReason)

    def eventFilter(self, watched, event):
        if watched == self.__searchField and \
           event.type() == QtCore.QEvent.KeyPress and \
           event.key() == QtCore.Qt.Key_Escape:
            self.__searchField.hide()
            return True
        return False

class NodeFactoryTreeView(QtGui.QTreeView, NodeFactoryView):

    compositeFactoryOpenRequest = QtCore.pyqtSignal(CompositeNodeFactory)

    def __init__(self, siblings=[], parent=None):
        QtGui.QTreeView.__init__(self, parent)
        NodeFactoryView.__init__(self, siblings)
        self.setDragEnabled(True)
        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.setIconSize(QtCore.QSize(25,25))
        self.setHeaderHidden(True)


























class SearchListView(NodeFactoryView, QtGui.QTreeView):
    """ Specialized QListView to display search results with Drag and Drop support """

    def __init__(self, main_win, parent=None):
        """
        @param main_win : main window
        @param parent : parent widget
        """

        QtGui.QListView.__init__(self, parent)
        NodeFactoryView.__init__(self, main_win, parent)
        self.setRootIsDecorated(False)


    def reset(self):
        QtGui.QTreeView.reset(self)
        for i in range(self.model().columnCount(None)):
            self.resizeColumnToContents(i)



class DataPoolListView(QtGui.QListView, SignalSlotListener):
    """ Specialized QListView to display data pool contents """

    def __init__(self, datapool, parent=None):
        """
        @param datapool : datapool instance
        @param parent : parent widget
        """

        QtGui.QListView.__init__(self, parent)
        SignalSlotListener.__init__(self)

        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setAcceptDrops(True)

        self.initialise(datapool)


    def notify(self, sender, event):
        """ Notification by observed """

        self.reset()


    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("openalea/data_instance"):
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("openalea/data_instance"):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):

        event.ignore()


    def startDrag(self, supportedActions):

        item = self.currentIndex()

        itemData = QtCore.QByteArray()
        dataStream = QtCore.QDataStream(itemData, QtCore.QIODevice.WriteOnly)
        pixmap = QtGui.QPixmap(":/icons/ccmime.png")

        l = self.model().datapool.keys()
        l.sort()
        name = l[item.row()]

        dataStream << QtCore.QString(name)

        mimeData = QtCore.QMimeData()
        mimeData.setData("openalea/data_instance", itemData)

        linecode = cli.get_datapool_code(name)
        mimeData.setText(linecode)

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(QtCore.QPoint(pixmap.width()/2, pixmap.height()/2))
        drag.setPixmap(pixmap)

        drag.start(QtCore.Qt.MoveAction)


    def contextMenuEvent(self, event):
        """ Context menu event : Display the menu"""


        menu = QtGui.QMenu(self)
        action = menu.addAction("Remove")
        self.connect(action, QtCore.SIGNAL("triggered()"), self.remove_element)

        menu.move(event.globalPos())
        menu.show()


    def remove_element(self):
        """ Remove an element from the datapool"""

        item = self.currentIndex()

        model = item.model()
        if(not model) : return

        datapool = model.datapool

        l = self.model().datapool.keys()
        l.sort()
        name = l[item.row()]

        del(datapool[name])







