# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2006 - 2008 INRIA - CIRAD - INRA  
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


__doc__="""
Annotation node
"""

__license__= "CeCILL v2"
__revision__=" $Id$ "



import sys
import math

from PyQt4 import QtCore, QtGui

from openalea.core.observer import lock_notify
from openalea.core.observer import AbstractListener


def is_available():
    """ Return True if annotation are available """

    version = QtCore.PYQT_VERSION
    if(version <= 262401):
        return False
    return True






class Annotation(QtGui.QGraphicsTextItem, AbstractListener):
    """ Text annotation on the data flow """
    
    def __init__(self, graphview, elt_id):

        scene = graphview.scene()
        QtGui.QGraphicsTextItem.__init__(self)
        
        # members
        self.elt_id = elt_id
        self.subnode = graphview.node.node(elt_id)

        self.initialise(self.subnode)

        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)

        font = self.font()
        font.setBold(True)
        font.setPointSize(12)
        self.setFont(font)

        self.notify(None, ("data_modified",))

        scene.addItem(self)

        
        
    def mouseDoubleClickEvent(self, event):

        self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.setSelected(True)
        self.setFocus()
        cursor = self.textCursor()
        cursor.select(QtGui.QTextCursor.Document)
        self.setTextCursor(cursor)
        

    def focusOutEvent(self, event):

        self.setFlag(QtGui.QGraphicsItem.ItemIsFocusable, False)
        #self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)

        # unselect text
        cursor = self.textCursor ()
        if(cursor.hasSelection()):
            cursor.clearSelection()
            self.setTextCursor(cursor)

        return QtGui.QGraphicsTextItem.focusOutEvent(self, event)



    @lock_notify
    def itemChange(self, change, value):
        """ Callback when item has been modified (move...) """

        if (change == QtGui.QGraphicsItem.ItemPositionChange):
            
            point = value.toPointF()
            self.subnode.set_data('posx', point.x())
            self.subnode.set_data('posy', point.y())
         
            #self.graphview.itemMoved(self, value)
        else:
            self.subnode.set_data('txt', str(self.toPlainText()))

        return QtGui.QGraphicsItem.itemChange(self, change, value)

    
    def notify(self, sender, event):
        """ Notification sended by the node associated to the item """

        if(not event or event[0] != "data_modified"):
            return

        try:
            x = self.subnode.internal_data['posx']
            y = self.subnode.internal_data['posy']
        except:
            (x,y) = (10,10)

        try:
            txt = self.subnode.internal_data['txt']
        except:
            txt = "Comments..."

        self.setPlainText(txt)
        self.setPos(QtCore.QPointF(x,y))
        

        



