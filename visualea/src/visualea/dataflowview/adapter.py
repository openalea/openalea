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
from openalea.core import node
from openalea.core import compositenode
import openalea.grapheditor.base as grapheditorbase

class GraphAdapter(grapheditorbase.GraphAdapterBase):
    """An adapter to openalea.core.compositenode"""
    def __init__(self, graph):
        grapheditorbase.GraphAdapterBase.__init__(self, graph)

    def __getattr__(self, name):
        "shortcut to access to methods of the real graph that we don't implement"""
        return getattr( self.graph(), name )

    def set_graph(self, graph):
        self.graph = weakref.ref(graph)

    def get_vertex(self, vid):
        return self.graph().node(vid)

    def add_vertex(self, vertex, position=None):
        try:
            vid = self.graph().add_node(vertex)
            if(position):
                vertex.get_ad_hoc_dict().set_metadata("position", position)
            return vid
        except node.RecursionError:
            mess = QtGui.QMessageBox.warning(self, "Error",
                                             "A graph cannot be contained in itself.")

    def remove_vertex(self, vertex):
        self.graph().remove_node(vertex.get_id())

    def add_edge(self, src, dst):
        if(type(src[0])==int):
            vtxIdSrc, portIdSrc = src[0], src[1]
            vtxIdDst, portIdDst = dst[0], dst[1]
        else:
            vtxIdSrc, portIdSrc = src[0].get_id(), src[1].get_id()
            vtxIdDst, portIdDst = dst[0].get_id(), dst[1].get_id()
        self.graph().connect(vtxIdSrc, portIdSrc, vtxIdDst, portIdDst)

    def remove_edge(self, src, dst):
        vtxIdSrc, portIdSrc = src[0].get_id(), src[1].get_id()
        vtkIdDst, portIdDst = dst[0].get_id(), dst[1].get_id()
        self.graph().disconnect(vtxIdSrc, portIdSrc, vtkIdDst, portIdDst)

    # -- Utility methods, not always useful/relevant.


    def replace_vertex(self, oldVertex, newVertex):
        self.graph().replace_node(oldVertex.get_id(), newVertex)

    def get_vertex_inputs(self, vid):
        return self.graph().node(vid).input_desc

    def get_vertex_outputs(self, vid):
        return self.graph().node(vid).output_desc

    def get_vertex_input(self, vid, pid):
        return self.graph().node(vid).input_desc[pid]

    def get_vertex_output(self, vid, pid):
        return self.graph().node(vid).output_desc[pid]


    #type checking
    def is_input(self, input):
        return isinstance(input, node.InputPort)

    def is_output(self, output):
        return isinstance(output, node.OutputPort)

    #other checks
    def is_vertex_protected(self, vertex):
        if (isinstance(vertex, compositenode.CompositeNodeInput) or \
                isinstance(vertex, compositenode.CompositeNodeOutput)):
            return True
        return False

    def is_legal_connection(self, src, dst):
        pass

    @classmethod
    def get_vertex_types(cls):
        return ["annotation", "vertex"]

    @classmethod
    def get_edge_types(cls):
        return ["default"]
