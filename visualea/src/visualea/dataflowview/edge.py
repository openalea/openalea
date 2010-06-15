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

import weakref
from PyQt4 import QtCore, QtGui

from openalea.grapheditor import qtgraphview
from openalea.grapheditor import edgefactory
import vertex
from openalea.grapheditor import baselisteners

from math import sqrt

class FloatingEdge(QtGui.QGraphicsPathItem, qtgraphview.FloatingEdge):
    """
    Represents an edge during its creation
    It is connected to one connector only
    and deleted at the end of the user
    interaction
    """

    def __init__(self, srcPoint, graph):
        QtGui.QGraphicsPathItem.__init__(self, None)
        qtgraphview.FloatingEdge.__init__(self, srcPoint, graph)

    def get_connections(self):
        boxsize = 10.0
        #find the port items that were activated
        srcPortItem = self.scene().itemAt( self.srcPoint )
        dstPortItem = self.scene().find_closest_connectable(self.dstPoint, boxsize)
        if not dstPortItem: return None, None

        #find the vertex items that were activated
        srcVertexItem = srcPortItem.parentItem()
        dstVertexItem = dstPortItem.parentItem()

        if(not hasattr(dstPortItem, "port")): return None, None

        #if the input and the output are on the same vertex...
        if(srcPortItem.port().vertex() == dstPortItem.port().vertex()):
            raise Exception("Nonsense connection : plugging self to self.")

        #actually, the source might not be an output, and the target
        #might not be an input, so we sort:
        if( self.graph().is_output(srcPortItem.port()) and
            self.graph().is_input(dstPortItem.port())):
            return (srcVertexItem.vertex(), srcPortItem.port()), \
                (dstVertexItem.vertex(), dstPortItem.port()), \
                srcPortItem, dstPortItem
        elif( self.graph().is_input(srcPortItem.port()) and
              self.graph().is_output(dstPortItem.port())):
            return (dstVertexItem.vertex(), dstPortItem.port()), \
                (srcVertexItem.vertex(), srcPortItem.port()), \
                srcPortItem, dstPortItem
        else:
            raise Exception("Nonsense connection : " + \
                                "plugging input to input or output to output")


class GraphicalEdge(QtGui.QGraphicsPathItem, qtgraphview.Edge):
    """ An edge between two graphical vertices """

    def __init__(self, edgeModel, graphadapter, port1, port2, parent=None):
        """ """
        QtGui.QGraphicsPathItem.__init__(self, parent)
        qtgraphview.Edge.__init__(self, edgeModel, graphadapter, port1, port2)
        self.__edge_creator = self.set_edge_creator(edgefactory.SplineEdgePath())
        self.initialise_from_model()

    def initialise_from_model(self):
        self.srcBBox().get_ad_hoc_dict().simulate_full_data_change(self, self.srcBBox())
        self.dstBBox().get_ad_hoc_dict().simulate_full_data_change(self, self.dstBBox())

    def remove(self):
        self.graph().remove_edge( (self.srcBBox().vertex(), self.srcBBox()),
                                  (self.dstBBox().vertex(), self.dstBBox()) )

    store_view_data = None
    get_view_data   = None
