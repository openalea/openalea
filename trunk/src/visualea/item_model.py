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

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

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
