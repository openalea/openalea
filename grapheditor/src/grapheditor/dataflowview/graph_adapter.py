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

import weakref
import openalea.core.node

class GraphAdapter(object):
    """An adapter to openalea.core.compositenode"""
    def __init__(self, graph):
        self.graph = weakref.ref(graph)

    def add_vertex(self, vertex, position=None):
        self.graph().add_node(vertex)
        if(position):
            vertex.get_ad_hoc_dict().set_metadata("position", position)

    def get_vertex(self, vid):
        return self.graph().node(vid)

    def remove_vertex(self, vertex):
        self.graph().remove_node(vertex)

    def remove_vertices(self, vertexList):
        for vert in vertexList:
            self.remove_vertex(vert)

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

    def add_edge(self, src, dst):
        vtxIdSrc, portIdSrc = src[0].get_id(), src[1].get_id()
        vtkIdDst, portIdDst = dst[0].get_id(), dst[1].get_id()
        self.graph().connect(vtxIdSrc, portIdSrc, vtkIdDst, portIdDst)

    def remove_edge(self, src, dst):
        vtxIdSrc, portIdSrc = src[0].get_id(), src[1].get_id()
        vtkIdDst, portIdDst = dst[0].get_id(), dst[1].get_id()
        self.graph().disconnect(vtxIdSrc, portIdSrc, vtkIdDst, portIdDst)

    #type checking
    def is_input(self, input):
        return isinstance(input, openalea.core.node.InputPort)

    def is_output(self, output):
        return isinstance(output, openalea.core.node.OutputPort)

