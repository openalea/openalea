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

import sys, numpy, weakref
from PyQt4 import QtCore, QtGui

from .. import gengraphview
from .. import qtgraphview
from .. import edgefactory

import openalea.core.node


class AleaQFloatingEdge(QtGui.QGraphicsPathItem, qtgraphview.QtGraphViewFloatingEdge):
    """
    Represents an edge during its creation
    It is connected to one connector only
    and deleted at the end of the user
    interaction
    """

    def __init__(self, srcPoint):
        QtGui.QGraphicsPathItem.__init__(self, None)
        qtgraphview.QtGraphViewFloatingEdge.__init__(self, srcPoint)

    def consolidate(self, model):
        try:
            srcNode, idSrc, dstNode, idDst = self.get_connections()
            model.connect(srcNode.get_id(), idSrc, dstNode.get_id(), idDst)
        except Exception, e:
            print "consolidation failed :", e
        return
        
    def get_connections(self):
        #find the port items that were activated
        srcPortItem = self.scene().itemAt( self.sourcePoint )
        dstPortItem = self.scene().itemAt( self.destPoint   )

        #find the node items that were activated
        srcNodeItem = srcPortItem.parentItem()
        dstNodeItem = dstPortItem.parentItem()

        #if the input and the output are on the same node...
        if(srcPortItem.observed().node() == dstPortItem.observed().node()):
            raise Exception("Nonsense connection : plugging self to self.")            

        #actually, the source might not be an output, and the target
        #might not be an input, so we sort:
        if( isinstance(srcPortItem.observed(), openalea.core.node.OutputPort) and
            isinstance(dstPortItem.observed(), openalea.core.node.InputPort)):
            print "right side"
            return srcNodeItem.observed(), srcPortItem.get_index(), \
                dstNodeItem.observed(), dstPortItem.get_index()
        elif( isinstance(srcPortItem.observed(), openalea.core.node.InputPort) and
              isinstance(dstPortItem.observed(), openalea.core.node.OutputPort)):
            print "opposite side"
            return dstNodeItem.observed(), dstPortItem.get_index(), \
                srcNodeItem.observed(), srcPortItem.get_index()
        else:
            raise Exception("Nonsense connection : " + \
                                "plugging input to input or output to output")


class AleaQGraphicalEdge(QtGui.QGraphicsPathItem, qtgraphview.QtGraphViewEdge):
    """ An edge between two graphical nodes """
        
    def __init__(self, edgeModel, port1, port2, parent=None):
        """ """
        QtGui.QGraphicsPathItem.__init__(self, parent)
        qtgraphview.QtGraphViewEdge.__init__(self, edgeModel, port1, port2)
        self.initialise_from_model()


    def contextMenuEvent(self, event):
        """ Context menu event : Display the menu"""

        menu = QtGui.QMenu(self.scene().views()[0])

        action = menu.addAction("Delete connection")
        self.scene().connect(action, QtCore.SIGNAL("triggered()"), self.remove)
        
        menu.move(event.screenPos())
        menu.show()

        event.accept()
        
