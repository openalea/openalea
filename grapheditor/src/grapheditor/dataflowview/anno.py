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

from .. import qtgraphview


class GraphicalAnnotation(QtGui.QGraphicsTextItem, qtgraphview.Annotation):
    """ Text annotation on the data flow """

    def __init__(self, annotation, graphadapter, parent=None):
        """ Create a nice annotation """
        QtGui.QGraphicsTextItem.__init__(self, parent)
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
        self.setPlainText(text)


