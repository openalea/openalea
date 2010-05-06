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

from openalea.grapheditor import qtgraphview
from openalea.grapheditor.qtutils import mixin_method


class GraphicalAnnotation(QtGui.QGraphicsTextItem, qtgraphview.Annotation):
    """ Text annotation on the data flow """

    def __init__(self, annotation, graphadapter, parent=None):
        """ Create a nice annotation """
        print "Graphical Annotation"
        QtGui.QGraphicsTextItem.__init__(self, "Click to edit", parent)
        qtgraphview.Annotation.__init__(self, annotation, graphadapter)

        # ---Qt Stuff---
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
        self.setZValue(2.0)

        font = self.font()
        font.setBold(True)
        font.setPointSize(12)
        self.setFont(font)
        
        self.initialise_from_model()
        return

    def set_text(self, text):
        print "set text ", text
        
        self.setPlainText(text)
        #self.store_view_data('text', text, notify=False)

    itemChange = mixin_method(qtgraphview.Annotation, QtGui.QGraphicsTextItem,
                              "itemChange")

#    def sceneEvent(self, event):
#        if( event.type() == QtCore.QEvent.GraphicsSceneMouseMove ):
#            self.deaf()
#            point = event.scenePos() - event.pos()
#            self.store_view_data('position', [point.x(), point.y()])
#            self.deaf(False)
#        return QtGui.QGraphicsTextItem.sceneEvent(self, event)

    def store_view_data(self, key, value, notify=True):
        print "store view data", key, value
        self.annotation().get_ad_hoc_dict().set_metadata(key, value)

    def get_view_data(self, key):
        print "get view data", key
        return self.annotation().get_ad_hoc_dict().get_metadata(key)

    def announce_view_data(self, exclusive=False):
        print 'announce_view_data ' 
        if not exclusive:
            self.annotation().get_ad_hoc_dict().simulate_full_data_change()
        else:
            self.annotation().exclusive_command(exclusive,
                                                self.annotation().get_ad_hoc_dict().simulate_full_data_change)
