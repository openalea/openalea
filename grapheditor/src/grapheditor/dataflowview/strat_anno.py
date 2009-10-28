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

from PyQt4 import QtGui, QtCore

import sys
from .. import gengraphview
from .. import qtgraphview
from openalea.core.observer import lock_notify


class GraphicalAnnotation(QtGui.QGraphicsTextItem, qtgraphview.QtGraphViewAnnotation):
    """ Text annotation on the data flow """

    def __init__(self, annotation, parent=None):
        """ Create a nice annotation """
        QtGui.QGraphicsTextItem.__init__(self, parent)
        qtgraphview.QtGraphViewAnnotation.__init__(self, annotation)

        # ---Qt Stuff---
        self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)

        font = self.font()
        font.setBold(True)
        font.setPointSize(12)
        self.setFont(font)
        
        self.initialise_from_model()
        return

    def set_text(self, text):
        self.setPlainText(text)
            
    ############
    # QT WORLD #
    ############
    def itemChange(self, change, value):
        """ Callback when item has been modified (move...) """
        if (change == QtGui.QGraphicsItem.ItemPositionChange):
            point = value.toPointF()
            self.observed().get_ad_hoc_dict().set_metadata("position" ,
                                                        [point.x(), point.y(), 1], 
                                                        False)

        return QtGui.QGraphicsItem.itemChange(self, change, value)

    def paint(self, painter, options, widget):
        QtGui.QGraphicsTextItem.paint(self, painter, options, widget)


