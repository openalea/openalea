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
#       This code is inspired from the puzzle QT4 example

__doc__="""
SubGraph widget inspired.

"""

__license__= "GPL"
__revision__=" $Id$"


import sys
import random
from PyQt4 import QtCore, QtGui


class NodeWidget(QtGui.QWidget):
    """
    Base class for all node widget
    This class provides default dialog for editing declared parameters
    """

    def __init__(self, node, factory, parent=None):

        QtGui.QWidget.__init__(self, parent)

        self.node = node
        self.factory = factory

    

    
class SubGraphWidget(NodeWidget):
    """ Subgraph widget allowing to edit the network """
    
    def __init__(self, node, factory, parent=None):

        NodeWidget.__init__(self, node, factory, parent)
    
        self.piecePixmaps = []
        self.pieceRects = []
        self.highlightedRect = QtCore.QRect()
        self.inPlace = 0

        self.setAcceptDrops(True)

    def clear(self):
        self.piecePixmaps = []
        self.pieceRects = []
        self.highlightedRect = QtCore.QRect()
        self.inPlace = 0
        self.update()

    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("openalea/nodefactory"):
            event.accept()
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        updateRect = self.highlightedRect
        self.highlightedRect = QtCore.QRect()
        self.update(updateRect)
        event.accept()

    def dragMoveEvent(self, event):
        updateRect = self.highlightedRect.unite(self.targetSquare(event.pos()))

        if ( event.mimeData().hasFormat("openalea/nodefactory") ):
            self.highlightedRect = self.targetSquare(event.pos())
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            self.highlightedRect = QtCore.QRect()
            event.ignore()

        self.update(updateRect)

    def dropEvent(self, event):

        if (event.mimeData().hasFormat("openalea/nodefactory")):
            pieceData = event.mimeData().data("openalea/nodefactory")
            dataStream = QtCore.QDataStream(pieceData, QtCore.QIODevice.ReadOnly)
            square = self.targetSquare(event.pos())
            pixmap = QtGui.QPixmap()
            dataStream >> pixmap 

            self.piecePixmaps.append(pixmap)
            self.pieceRects.append(square)

            self.hightlightedRect = QtCore.QRect()
            self.update(square)

            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()

        else:
            self.highlightedRect = QtCore.QRect()
            event.ignore()



    def paintEvent(self, event):
        painter = QtGui.QPainter()
        painter.begin(self)
        painter.fillRect(event.rect(), QtCore.Qt.white)

        if self.highlightedRect.isValid():
            painter.setBrush(QtGui.QColor(255, 0, 0, 127))
            painter.setPen(QtCore.Qt.NoPen)
            painter.drawRect(self.highlightedRect.adjusted(0, 0, -1, -1))

        for i in range(len(self.pieceRects)):
  
            painter.setBrush(QtGui.QColor(0, 0, 255, 127))
            painter.setPen(QtCore.Qt.NoPen)
            painter.drawRect(self.pieceRects[i].adjusted(0, 0, -1, -1))
            painter.drawPixmap(self.pieceRects[i], self.piecePixmaps[i])


        painter.end()


    def targetSquare(self, position):
        """ Return the rectangle associated to position """
        
        return QtCore.QRect(position.x()- 40/2, position.y()- 40/2, 40, 40)
    

