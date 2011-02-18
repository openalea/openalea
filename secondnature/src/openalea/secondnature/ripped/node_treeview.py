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
from PyQt4.QtCore import QAbstractItemModel,QModelIndex, QVariant
from PyQt4.QtCore import QAbstractListModel

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


# Utilities function

icon_dict = None

def get_icon(item):
    """ Return Icon object depending of the type of item """

    global icon_dict
    if(not icon_dict):
        # dict to do a switch
        icon_dict = {
            PseudoGroup : QVariant(QtGui.QPixmap(":/icons/category.png")),
            CompositeNodeFactory : QVariant(QtGui.QPixmap(":/icons/diagram.png")),
            NodeFactory : QVariant(QtGui.QPixmap(":/icons/node.png")),
            DataFactory : QVariant(QtGui.QPixmap(":/icons/data.png")),
            UserPackage : QVariant(QtGui.QPixmap(":/icons/usrpkg.png")),
            Package :  QVariant(QtGui.QPixmap(":/icons/pkg.png")),
            }

    # Get icon from dictionary
    if(icon_dict.has_key(type(item))):
        return icon_dict[type(item)]

    elif(isinstance(item, PseudoPackage)):

        if(item.is_real_package()):

            # Try to load package specific icon
            icon = item.item.metainfo.get("icon", None)
            if(icon):
                icon = os.path.join(item.item.path, icon)
                pix = QtGui.QPixmap(icon)
                if(not pix.isNull()):
                    return QVariant(pix)

            # Standard icon
            return icon_dict[type(item.item)]

        return QVariant(QtGui.QPixmap(":/icons/pseudopkg.png"))

    else:
        return QVariant()


# Qt4 Models/View classes

class PkgModel (QAbstractItemModel) :
    """ QT4 data model (model/view pattern) to support pkgmanager """

    def __init__(self, pkgmanager, parent=None):

        QAbstractItemModel.__init__(self, parent)
        self.pman = pkgmanager
        self.rootItem = self.pman.get_pseudo_pkg()

        self.parent_map = {}
        self.row_map = {}
        self.index_map = {} # map between name and Index object


    def reset(self):

        self.rootItem = self.pman.get_pseudo_pkg()
        QAbstractItemModel.reset(self)


    def columnCount(self, parent):
        return 1


    def data(self, index, role):

        if not index.isValid():
            return QtCore.QVariant()

        item = index.internalPointer()

        # Text
        if (role == QtCore.Qt.DisplayRole):

            # Add size info
            lenstr=''
            try:
                l = item.nb_public_values()
                if(l) : lenstr = " ( %i )"%(l,)
            except: pass

            return QtCore.QVariant(str(item.get_id()) + lenstr)

        # Tool Tip
        elif( role == QtCore.Qt.ToolTipRole ):
            return QtCore.QVariant(str(item.get_tip()))

        # Icon
        elif(role == QtCore.Qt.DecorationRole):
            return get_icon(item)

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


    def get_full_name (self, item) :
        """construct a full unique name from item
        using parent.parent.item syntax
        """
        if item is None :
            return None
        try :
            if item.item is not None :
                return item.item.name
        except AttributeError :
            pass
        return item.name

    def index(self, row, column, parent):

        if (not parent.isValid()):
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        l = list(parentItem.iter_public_values())
        l.sort((lambda x,y : cmp(x.get_id(), y.get_id())))
        childItem = l[row]

        # save parent and row
        self.parent_map[id(childItem)] = parentItem
        self.row_map[id(childItem)] = row

        i = self.createIndex(row, column, childItem)

        name = self.get_full_name(childItem)
        #self.index_map[childItem.name] = i
        self.index_map[name] = i

        return i


    def parent(self, index):

        if (not index.isValid()):
            return QtCore.QModelIndex()

        childItem = index.internalPointer()

        parentItem = self.parent_map[id(childItem)]

        # Test if it is the root
        if (not self.parent_map.has_key(id(parentItem)) ):
            return QtCore.QModelIndex()

        else:
            row = self.row_map[id(parentItem)]
            return self.createIndex(row, 0, parentItem)


    def rowCount(self, parent):

        if (not parent.isValid()):
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        if isinstance(parentItem, AbstractFactory):
            return 0

        # Return the number of DIFFERENT OBJECTS
        l = parentItem.nb_public_values()

        return l



class CategoryModel (PkgModel) :
    """ QT4 data model (model/view pattern) to view category """

    def __init__(self, pkgmanager, parent=None):

        QAbstractItemModel.__init__(self, parent)
        self.pman = pkgmanager
        self.rootItem = self.pman.get_pseudo_cat()

        self.parent_map = {}
        self.row_map = {}
        self.index_map = {}


    def reset(self):
        self.rootItem = self.pman.get_pseudo_cat()
        # self.parent_map = {}
        # self.row_map = {}
        QAbstractItemModel.reset(self)



class DataPoolModel (QAbstractListModel) :
    """ QT4 data model (model/view pattern) to support Data Pool """

    def __init__(self, datapool, parent=None):

        QAbstractListModel.__init__(self, parent)
        self.datapool = datapool


    def reset(self):
        QAbstractItemModel.reset(self)


    def data(self, index, role):

        if (not index.isValid()):
            return QVariant()

        if (index.row() >= len(self.datapool.keys())):
            return QVariant()

        if (role == QtCore.Qt.DisplayRole):
            l = self.datapool.keys()
            l.sort()
            name = l[index.row()]
            #classname = self.datapool[name].__class__
            value = repr(self.datapool[name])
            if(len(value) > 30) : value = value[:30] + "..."
            return QVariant("%s ( %s )"%(name, value))

        # Icon
        elif( role == QtCore.Qt.DecorationRole ):
            return QVariant(QtGui.QPixmap(":/icons/ccmime.png"))

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
            return QVariant()


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



class SearchModel (QAbstractListModel) :
    """ QT4 data model (model/view pattern) to support Search result"""

    def __init__(self, parent=None):

        QAbstractListModel.__init__(self, parent)
        self.searchresult = []


    def set_results(self, results):
        """ Set the search results : results is a list of factory """
        self.searchresult = results
        self.reset()


    def index(self, row, column, parent):

        if (row < len(self.searchresult)):
            factory = self.searchresult[row]
            return self.createIndex(row, column, factory)

        else:
            return QtCore.QModelIndex()


    def data(self, index, role):

        if (not index.isValid()):
            return QVariant()

        if (index.row() >= len(self.searchresult)):
            return QVariant()

        item = self.searchresult[index.row()]

        if (role == QtCore.Qt.DisplayRole):
            if(index.column() == 1):
                return QVariant(str(item.package.get_id()))
            return QVariant(str(item.name+ " ("+item.package.name+")"))

        # Icon
        elif( role == QtCore.Qt.DecorationRole ):
            if(index.column()>0) : return QVariant()
            return get_icon(item)

        # Tool Tip
        elif( role == QtCore.Qt.ToolTipRole ):
            return QtCore.QVariant(str(item.get_tip()))

        else:
            return QVariant()


    def flags(self, index):
        if not index.isValid():
            return QtCore.Qt.ItemIsEnabled

        return QtCore.Qt.ItemIsEnabled | \
               QtCore.Qt.ItemIsSelectable | \
               QtCore.Qt.ItemIsDragEnabled


    def headerData(self, section, orientation, role):
        return QtCore.QVariant()


    def rowCount(self, parent):

        if (not parent.isValid()):
            return len(self.searchresult)
        else :
            return 0


    def columnCount(self, index):
        return 2


################################################################################
# Views

class NodeFactoryView(object):
    """
    Base class for all view which display node factories.
    Implements Drag and Drop facilities.
    """

    def __init__(self, main_win, parent=None):
        """
        @param main_win : main window
        @param parent : parent widget
        """

        self.main_win = None#ref(main_win)

        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setAcceptDrops(True)
        try:
            h = self.header().hide()
        except:
            pass


    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("openalea/nodefactory"):
            event.accept()
        else:
            event.ignore()


    def dragMoveEvent(self, event):
        if event.mimeData().hasFormat("openalea/nodefactory"):
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
        pixmap = QtGui.QPixmap(item.data(QtCore.Qt.DecorationRole))

        (pkg_id, factory_id, mimetype) = self.get_item_info(item)

        dataStream << QtCore.QString(pkg_id) << QtCore.QString(factory_id)

        mimeData = QtCore.QMimeData()

        mimeData.setData(mimetype, itemData)

        #build an url
        factory = PackageManager()[pkg_id][factory_id]
        if isinstance(factory, DataFactory):
            url = QtCore.QUrl("file://"+factory.get_pkg_data().repr)
        else:
            query   = ["fac="+factory_id]

            ftname  = type(factory).__name__
            query.append("ft="+ftname)

            query = reduce(lambda x,y:"&".join((x,y)), query)
            url = QtCore.QUrl("oa://local/"+pkg_id+"?"+query)

        mimeData.setUrls([url])

        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(QtCore.QPoint(pixmap.width()/2, pixmap.height()/2))
        drag.setPixmap(pixmap)

        drag.start(QtCore.Qt.MoveAction)


    @staticmethod
    def get_item_info(item):
        """
        Return (package_id, factory_id, mimetype) corresponding to item.
        """

        # put in the Mime Data pkg id and factory id
        obj = item.internalPointer()

        if(obj.mimetype == "openalea/nodefactory"):

            factory_id = obj.get_id()
            pkg_id = obj.package.get_id()

            return (pkg_id, factory_id, obj.mimetype)

        return ("","", "openalea/notype")


    def contextMenuEvent(self, event):
        """ Context menu event : Display the menu"""

        item = self.currentIndex()
        obj =  item.internalPointer()
        menu = None

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

        elif(isinstance(obj, PseudoPackage)): # Package

            enabled = obj.is_real_package()
            pkg = obj.item

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
            menu.move(event.globalPos())
            menu.show()


    def get_current_pkg(self):
        """ Return the current package """
        item = self.currentIndex()
        obj =  item.internalPointer()
        # obj is necessary a pseudo package (menu disbled in other case)
        obj = obj.item

        return obj


    def add_python_node(self):
        """ """
        pman = self.model().pman # pkgmanager
        pkg = self.get_current_pkg()

        dialog = NewGraph("New Python Node", pman, self, pkg_id=pkg.name)
        ret = dialog.exec_()

        if(ret>0):
            dialog.create_nodefactory(pman)
            self.main_win().reinit_treeview()


    def add_composite_node(self):
        """ """
        pman = self.model().pman # pkgmanager
        pkg = self.get_current_pkg()

        dialog = NewGraph("New Composite Node", pman, self, pkg_id=pkg.name)
        ret = dialog.exec_()

        if(ret>0):
            newfactory = dialog.create_cnfactory(pman)
            self.main_win().reinit_treeview()


    def add_data(self):
        """ """
        pman = self.model().pman # pkgmanager
        pkg = self.get_current_pkg()

        dialog = NewData("Import Data", pman, self, pkg_id=pkg.name)
        ret = dialog.exec_()

        if(ret>0):
            newfactory = dialog.create_datafactory(pman)
            self.main_win().reinit_treeview()



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
        self.main_win().reinit_treeview()



    def grab_icon(self):
        """ Set the package icon """

        pkg = self.get_current_pkg()
        pix = grab_icon(self.main_win())

        fname = os.path.join(pkg.path, "icon.png")
        pix.save(fname)
        pkg.set_icon(fname)

        self.main_win().reinit_treeview()


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
        if(widget.is_widget()) : open_dialog(self.main_win(), widget, pkg.name)


    def reload_package(self):
        """ Reload package """

        pkg = self.get_current_pkg()
        pman = self.model().pman # pkgmanager

        if(not pkg.is_directory()):
            QtGui.QMessageBox.warning(self, "Error",
                                             "Cannot reload old style package\n")
            return

        pman.reload(pkg)
        self.main_win().reinit_treeview()


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
            self.main_win().reinit_treeview()


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
            self.main_win().reinit_treeview()




    def edit_package(self):
        """ Edit package Metadata """

        obj = self.get_current_pkg()

        dialog = EditPackage(obj, parent = self)
        ret = dialog.exec_()


    def mouseDoubleClickEvent(self, event):

        item = self.currentIndex()
        obj =  item.internalPointer()

        if(isinstance(obj, CompositeNodeFactory)):
            session = self.main_win().session
            for ws in session.workspaces:
                if obj == ws.factory:
                    res = QtGui.QMessageBox.warning(self.main_win(), "Other instances are already opened!",
                                                    """You are trying to open a composite node that has already been opened.
Doing this might cause confusion later on.
Do you want to continue?""",
                                                    QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
                    if res == QtGui.QMessageBox.Cancel:
                        return
                    else:
                        break
            self.edit_node()
        # elif isinstance(obj, DataFactory):
        #     f=obj.get_pkg_data().repr
        #     self.edit_data(f)
        elif (not isinstance(obj, Package)):
            self.open_node()


    # @busy_cursor
    # @exception_display
    # def edit_node(self):


    @busy_cursor
    @exception_display
    def open_node(self):
        """ Instantiate Node : open a dialog """

        item = self.currentIndex()
        obj =  item.internalPointer()

        if(isinstance(obj, AbstractFactory)):
            widget = obj.instantiate_widget(autonomous=True)
            open_dialog(self.main_win(), widget, obj.get_id())


        elif(isinstance(obj, PseudoPackage)):
            # Display URL
            urlstr = obj.get_metainfo('url')
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(urlstr))


    @busy_cursor
    @exception_display
    def edit_node(self):
        """ Edit Node in tab workspace"""

        item = self.currentIndex()
        obj =  item.internalPointer()

        if(isinstance(obj, CompositeNodeFactory)):
            self.main_win().open_compositenode(obj)

        elif(isinstance(obj, NodeFactory)
             or isinstance(obj, DataFactory)
             ):
            widget = obj.instantiate_widget(edit=True)
            if(widget.is_widget()) :
                open_dialog(self.main_win(), widget, obj.get_id())


    def edit_properties(self):
        """ Edit Node info"""

        item = self.currentIndex()
        obj =  item.internalPointer()

        if(isinstance(obj, DataFactory)):
            QtGui.QMessageBox.information(self, "Properties", "Data : %s"%(obj.name))
            return

        d = NewGraph("Node Properties", PackageManager(), self, obj)
        ret = d.exec_()
        if(ret):
            d.update_factory()



    def remove_node(self):
        """ Remove the node from the package """

        item = self.currentIndex()
        obj =  item.internalPointer()

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
            self.main_win().reinit_treeview()




class NodeFactoryTreeView(NodeFactoryView, QtGui.QTreeView):
    """ Specialized TreeView to display node factory in a tree with Drag and Drop support  """

    def __init__(self, main_win, parent=None):
        """
        @param main_win : main window
        @param parent : parent widget
        """

        QtGui.QTreeView.__init__(self, parent)
        NodeFactoryView.__init__(self, main_win, parent)

        self.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        #self.setAnimated(True)

        self.connect(self, QtCore.SIGNAL("expanded (const QModelIndex &)"), self.expanded)
        self.connect(self, QtCore.SIGNAL("collapsed (const QModelIndex &)"), self.collapsed)

        self.expanded_items = set()


    def collapsed(self, index):
        name = self.model().get_full_name(index.internalPointer() )
        #self.expanded_items.remove(index.internalPointer().name)
        self.expanded_items.remove(name)


    def expanded(self, index):
        name = self.model().get_full_name(index.internalPointer() )
        #self.expanded_items.add(index.internalPointer().name)
        self.expanded_items.add(name)


    def reset(self):
        QtGui.QTreeView.reset(self)

        for n in list(self.expanded_items):
            i = self.model().index_map[n]
            self.setExpanded(i, True)


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

    def __init__(self, main_win, datapool, parent=None):
        """
        @param main_win : main window
        @param datapool : datapool instance
        @param parent : parent widget
        """

        QtGui.QListView.__init__(self, parent)
        SignalSlotListener.__init__(self)

        self.main_win = ref(main_win)

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







