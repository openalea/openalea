# -*- python -*-
#
#       OpenAlea.image
#
#       Copyright 2012 INRIA - CIRAD - INRA
#
#       File author(s):  Jonathan Legrand <jonathan.legrand@ens-lyon.fr>
#                        Frederic Boudon <frederic.boudon@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite: http://openalea.gforge.inria.fr
#
################################################################################
"""Test creation of PropertyGraph from SpatialImages"""
import numpy as np

from openalea.image.serial.basics import imread
from openalea.image.algo.analysis import SpatialImageAnalysis
from openalea.image.algo.graph_from_image import graph_from_image
from openalea.plantgl.gui import Viewer

def test_graph_from_image(visual = False):
    im =  imread("segmentation.inr.gz")
    graph = graph_from_image(im)
    if visual :
        Viewer.display(graph2pglscene(graph,graph.vertex_property('barycenter'),graph.vertex_property('L1')))

def test_graph_from_simple_image(visual = False):
    im = np.array([[1, 2, 7, 7, 1, 1],
                  [1, 6, 5, 7, 3, 3],
                  [2, 2, 1, 7, 3, 3],
                  [1, 1, 1, 4, 1, 1]])
    borders = SpatialImageAnalysis(im).cells_in_image_margins()
    print '**', SpatialImageAnalysis(im).boundingbox(real=False)
    #~ print borders
    #~ print np.unique(im)
    graph = graph_from_image(im)
    
    #~ print list(graph.vertices())
    #~ print map(graph.edge_vertices,graph.edges())
    #~ print list(graph.vertex_property_names())
    #~ print list(graph.edge_property_names())
    for propname in graph.vertex_property_names():
        print propname
        print graph.vertex_property(propname)

    #~ for propname in graph.edge_property_names():
        #~ print propname
        #~ print [(i,graph.edge_vertices(i),j) for i,j in graph.edge_property(propname).iteritems()]
    if visual :
        Viewer.display(graph2pglscene(graph,graph.vertex_property('barycenter'),graph.vertex_property('border')))

if __name__ == '__main__':
    test_graph_from_simple_image()
    # test_graph_from_image()
