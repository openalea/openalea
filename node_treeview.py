# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#                       Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the GPL License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.gnu.org/licenses/gpl.txt
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

__doc__="""
Tree Item model for package manager
"""

__license__= "GPL"
__revision__=" $Id$ "

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import QAbstractItemModel,QModelIndex, QVariant

from aleacore.core import NodeFactory, Package

import images_rc



class PkgModel (QAbstractItemModel) :
    """ QT4 data model (model/view pattern) to support pkgmanager """

    def __init__(self, pkgmanager, parent=None):
        
        QAbstractItemModel.__init__(self, parent)
        self.rootItem = pkgmanager

        self.parent_map = {}


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
        elif( role == QtCore.Qt.DecorationRole ):

            if( isinstance( item, Package) ):
                return QVariant(QtGui.QPixmap(":/icons/package.png"))
            elif( isinstance( item, NodeFactory) ):
                return QVariant(QtGui.QPixmap(":/icons/node.png"))
        

        
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
        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        childItem = parentItem[ parentItem.keys()[row] ]
        if childItem:

            # save parent position
            self.parent_map[ id(childItem) ] = (parentItem, row)
            return self.createIndex(row, column, childItem)
        
        else:
            return QtCore.QModelIndex()

    def parent(self, index):

        if not index.isValid():
            return QtCore.QModelIndex()

        childItem = index.internalPointer()
        
        (parentItem, row) = self.parent_map[ id(childItem) ]

        if parentItem == self.rootItem:
            return QtCore.QModelIndex()

        return self.createIndex(row, 0, parentItem)

    def rowCount(self, parent):

        if not parent.isValid():
            parentItem = self.rootItem
        else:
            parentItem = parent.internalPointer()

        try:
            return len(parentItem)
        except:
            return 0




class NodeTreeView(QtGui.QTreeView):
    """ Specialized TreeView to display node in a tree which support Drag and Drop """
    
    def __init__(self, main_win, parent=None):
        """
        @param main_win : main window
        @param parent : parent widget
        """
        QtGui.QTreeView.__init__(self, parent)

        self.main_win = main_win

        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        
        
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

        # put in the Mime Data pkg id and factory id
        obj = item.internalPointer()

        if(obj.mimetype == "openalea/nodefactory"):

            factory_id = obj.get_id()
            pkg_id = item.parent().internalPointer().get_id()
            
            dataStream << QtCore.QString(pkg_id) << QtCore.QString(factory_id)

        mimeData = QtCore.QMimeData()
        
        mimeData.setData(obj.mimetype, itemData)
    
        drag = QtGui.QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(QtCore.QPoint(pixmap.width()/2, pixmap.height()/2))
        drag.setPixmap(pixmap)

        drag.start(QtCore.Qt.MoveAction)
        
    def mouseDoubleClickEvent(self, event):

        item = self.currentIndex()
        obj =  item.internalPointer()
        
        if(isinstance(obj, NodeFactory)):
            self.main_win.open_widget(obj)
            
