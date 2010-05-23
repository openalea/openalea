# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Daniel Barbeau <daniel.barbeau@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

__license__ = "Cecill-C"
__revision__ = " $Id$ "

from PyQt4 import QtGui, QtCore

from openalea.grapheditor import qtgraphview, baselisteners
from openalea.grapheditor.qtutils import mixin_method

class GraphicalAnnotation(QtGui.QGraphicsTextItem, qtgraphview.Vertex):
    """ Text annotation on the data flow """
    
    __def_string__ = u"Double-click to edit"

    def __init__(self, annotation, graphadapter, parent=None):
        """ Create a nice annotation """
        QtGui.QGraphicsTextItem.__init__(self, self.__def_string__, parent)
        qtgraphview.Vertex.__init__(self, annotation, graphadapter)

        # ---Qt Stuff---        
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(0x800) #SIP doesn't know about the ItemSendsGeometryChanges flag yet
        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.setZValue(2.0)

        font = self.font()
        font.setBold(True)
        font.setPointSize(12)
        self.setFont(font)
        
        self.initialise_from_model()
        return

    annotation = baselisteners.GraphElementObserverBase.get_observed        

    #####################
    # ----Qt World----  #
    #####################
    itemChange = mixin_method(qtgraphview.Vertex, QtGui.QGraphicsTextItem,
                              "itemChange")
                              
    paint = mixin_method(None, QtGui.QGraphicsTextItem,
                              "paint")                              
                              
    mousePressEvent = mixin_method( QtGui.QGraphicsTextItem, qtgraphview.Vertex,
                                   "mousePressEvent")
        
    def mouseDoubleClickEvent(self, event):
        self.setTextInteractionFlags(QtCore.Qt.TextEditorInteraction)
        self.setSelected(True)
        self.setFocus() #setting selection doesn't set the focus
        QtGui.QGraphicsTextItem.mouseDoubleClickEvent(self, event)

    def keyPressEvent(self, event):
        QtGui.QGraphicsTextItem.keyPressEvent(self, event)              
        
    def focusOutEvent(self, event):
        text = unicode(self.toPlainText())
        if(text != self.__def_string__):
            self.store_view_data('text', text)
        self.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        QtGui.QGraphicsTextItem.focusOutEvent(self, event)
        
        
    #########################
    # ----Other things----  #
    #########################
    def notify(self, sender, event):
        if event:
            if event[0] == "metadata_changed":
                if event[1] == "text":
                    self.set_text(event[2])
                    return
        qtgraphview.Vertex.notify(self, sender, event)
    
    def set_text(self, text):
        if text == u"" :
            text = self.__def_string__
        self.setPlainText(text)

    def store_view_data(self, key, value, notify=True):
        self.annotation().get_ad_hoc_dict().set_metadata(key, value)

    def get_view_data(self, key):
        return self.annotation().get_ad_hoc_dict().get_metadata(key)

    def announce_view_data(self, exclusive=False):
        if not exclusive:
            self.annotation().get_ad_hoc_dict().simulate_full_data_change()
        else:
            self.annotation().exclusive_command(exclusive,
                                                self.annotation().get_ad_hoc_dict().simulate_full_data_change)
