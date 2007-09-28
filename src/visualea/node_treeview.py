# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2006 - 2007 INRIA - CIRAD - INRA  
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
Tree Item model for package manager.
Only Package and Category objects are view as a tree item.
Others are view as leaves.
"""

__license__= "CeCILL v2"
__revision__=" $Id$ "

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QAbstractItemModel,QModelIndex, QVariant
from PyQt4.QtCore import QAbstractListModel

from openalea.core.node import NodeFactory, AbstractFactory
from openalea.core.package import Package
from openalea.core.compositenode import CompositeNodeFactory
from openalea.core.pkgmanager import PackageManager, Category
from openalea.core.observer import AbstractListener

from dialogs import EditPackage, NewGraph
from util import open_dialog

import images_rc


# Utilities function

def get_icon(item):
    """ Return Icon object depending of the type of item """
    if(isinstance(item, Package)):
        return QVariant(QtGui.QPixmap(":/icons/package.png"))

    elif(isinstance(item, Category)):
        return QVariant(QtGui.QPixmap(":/icons/category.png"))

    elif( isinstance(item, CompositeNodeFactory)):
        return QVariant(QtGui.QPixmap(":/icons/diagram.png"))
           
    elif( isinstance(item, NodeFactory)):
        return QVariant(QtGui.QPixmap(":/icons/node.png"))

    else:
        return QVariant()


# Qt4 Models/View classes

class PkgModel (QAbstractItemModel) :
    """ QT4 data model (model/view pattern) to support pkgmanager """

    def __init__(self, pkgmanager, parent=None):
        
        QAbstractItemModel.__init__(self, parent)
        self.rootItem = pkgmanager

        self.parent_map = {}
        self.row_map = {}

        
    def reset(self):
        self.parent_map = {}
        self.row_map = {}
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
                if( len (item) ) : lenstr = " ( %i )"%(len(item),)
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


    def index(self, row, column, parent):

        if (not parent.isValid()):
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        l = parentItem.values()
        l.sort((lambda x,y : cmp(x.get_id(), y.get_id())))
        childItem = l[row]

        # save parent and row
        self.parent_map[id(childItem)] = parentItem
        self.row_map[id(childItem)] = row
        
        return self.createIndex(row, column, childItem)
        

    def parent(self, index):

        if (not index.isValid()):
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        
        parentItem = self.parent_map[id(childItem)]
        
        if (parentItem == self.rootItem):
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

        return len(parentItem)
        


class CategoryModel (PkgModel) :
    """ QT4 data model (model/view pattern) to view category """

    def __init__(self, pkgmanager, parent=None):
        
        PkgModel.__init__(self, pkgmanager, parent)
    

    def index(self, row, column, parent):

        if (not parent.isValid()):
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        if( isinstance(parentItem, PackageManager)):
            l = parentItem.category.values()
            l.sort(key = Category.get_id)
            childItem = l[row]

        elif( isinstance(parentItem, Category)):
            l= list(parentItem)
            l.sort(key = AbstractFactory.get_id)
            childItem = l[row]
        else:
            childItem = None
        

        if (childItem):
            # save parent and row
            self.parent_map[ id(childItem) ] = parentItem
            self.row_map[ id(childItem) ] = row
                
            return self.createIndex(row, column, childItem)
        
        else:
            return QtCore.QModelIndex()


    def rowCount(self, parent):

        if (not parent.isValid()):
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        if( isinstance(parentItem, PackageManager)):
            return len(parentItem.category.keys())

        elif( isinstance(parentItem, Category)):
            return len(parentItem)

        else :
            return 0

       

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
            tipstr = "%s\n\n"%(str(self.datapool[name]),)
            tipstr +="Dir :\n  "
            tip = filter( lambda x : not x.startswith('__'),
                          dir(self.datapool[name]))
            tipstr += '\n  '.join(tip)

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

        
    def reset(self):
        QAbstractItemModel.reset(self)
        

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
            return QVariant(str(item.name))

        # Icon
        elif( role == QtCore.Qt.DecorationRole ):
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
        return len(self.searchresult)


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
        
        self.main_win = main_win

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
    
        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(QtCore.QPoint(pixmap.width()/2, pixmap.height()/2))
        drag.setPixmap(pixmap)

        drag.start(QtCore.Qt.MoveAction)

        
    def get_item_info(self, item):
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
            self.connect(action, QtCore.SIGNAL("activated()"), self.open_node)

            action = menu.addAction("Edit")
            self.connect(action, QtCore.SIGNAL("activated()"), self.edit_node)

            action = menu.addAction("Properties")
            self.connect(action, QtCore.SIGNAL("activated()"), self.edit_properties)

            action = menu.addAction("Remove")
            self.connect(action, QtCore.SIGNAL("activated()"), self.remove_node)

        elif(isinstance(obj, Package)): # Package
            menu = QtGui.QMenu(self)
            action = menu.addAction("Open URL")
            self.connect(action, QtCore.SIGNAL("activated()"), self.open_node)

            action = menu.addAction("Infos")
            self.connect(action, QtCore.SIGNAL("activated()"), self.edit_package)


        if(menu):
            menu.move(event.globalPos())
            menu.show()


    def edit_package(self):
        """ Edit package Metadata """

        item = self.currentIndex()
        obj =  item.internalPointer()

        dialog = EditPackage(obj, parent = self)
        ret = dialog.exec_()
        

    def mouseDoubleClickEvent(self, event):

        item = self.currentIndex()
        obj =  item.internalPointer()

        if(isinstance(obj, CompositeNodeFactory)):
            self.edit_node()
        elif (not isinstance(obj, Package)):
            self.open_node()


    def open_node(self):
        """ Instantiate Node : open a dialog """

        item = self.currentIndex()
        obj =  item.internalPointer()
        
        if(isinstance(obj, AbstractFactory)):
            widget = obj.instantiate_widget()
            open_dialog(self, widget, obj.get_id())
        

        elif(isinstance(obj, Package)):
            # Display URL
            urlstr = obj.get_metainfo('url')
            QtGui.QDesktopServices.openUrl(QtCore.QUrl(urlstr))


    def edit_node(self):
        """ Edit Node in tab workspace"""

        item = self.currentIndex()
        obj =  item.internalPointer()
        
        if(isinstance(obj, CompositeNodeFactory)):
            self.main_win.open_compositenode(obj)

        elif(isinstance(obj, NodeFactory)):
            widget = obj.instantiate_widget(edit=True)
            open_dialog(self, widget, obj.get_id())


    def edit_properties(self):
        """ Edit Node info"""

        item = self.currentIndex()
        obj =  item.internalPointer()
        
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
            del(obj.package[obj.name])
            self.main_win.reinit_treeview()
        
       

class NodeFactoryTreeView(NodeFactoryView, QtGui.QTreeView):
    """ Specialized TreeView to display node factory in a tree with Drag and Drop support  """

    def __init__(self, main_win, parent=None):
        """
        @param main_win : main window
        @param parent : parent widget
        """

        QtGui.QTreeView.__init__(self, parent)
        NodeFactoryView.__init__(self, main_win, parent)



class SearchListView(NodeFactoryView, QtGui.QListView):
    """ Specialized QListView to display search results with Drag and Drop support """
    
    def __init__(self, main_win, parent=None):
        """
        @param main_win : main window
        @param parent : parent widget
        """

        QtGui.QListView.__init__(self, parent)
        NodeFactoryView.__init__(self, main_win, parent)
        

class DataPoolListView(QtGui.QListView, AbstractListener):
    """ Specialized QListView to display data pool contents """
    
    def __init__(self, main_win, datapool, parent=None):
        """
        @param main_win : main window
        @param datapool : datapool instance
        @param parent : parent widget
        """
        
        QtGui.QListView.__init__(self, parent)
        AbstractListener.__init__(self)

        self.main_win = main_win

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
    
        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(QtCore.QPoint(pixmap.width()/2, pixmap.height()/2))
        drag.setPixmap(pixmap)

        drag.start(QtCore.Qt.MoveAction)


    def contextMenuEvent(self, event):
        """ Context menu event : Display the menu"""

        
        menu = QtGui.QMenu(self)
        action = menu.addAction("Remove")
        self.connect(action, QtCore.SIGNAL("activated()"), self.remove_element)

        menu.move(event.globalPos())
        menu.show()
        

    def remove_element(self):
        """ Remove an element from the datapool"""

        item = self.currentIndex()
        datapool = item.model().datapool

        l = self.model().datapool.keys()
        l.sort()
        name = l[item.row()]

        del(datapool[name])

        

       



