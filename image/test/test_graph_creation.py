from openalea.image.algo.graph_from_image import *
from openalea.image.all import *
import numpy as np

def test_graph_from_image():
    im =  read_inrimage("segmentation.inr.gz")
    graph = graph_from_image(im)

def test_graph_from_simple_image():
    import numpy as np
    im = np.array([[1, 2, 7, 7, 1, 1],
                  [1, 6, 5, 7, 3, 3],
                  [2, 2, 1, 7, 3, 3],
                  [1, 1, 1, 4, 1, 1]])
    graph = graph_from_image(im)
    print list(graph.vertices())
    print map(graph.edge_vertices,graph.edges())
    print list(graph.vertex_property_names())
    print list(graph.edge_property_names())
    for propname in graph.vertex_property_names():
        print propname
        print graph.vertex_property(propname)
    
    for propname in graph.edge_property_names():
        print propname
        print graph.edge_property(propname)
    
if __name__ == '__main__':
    test_graph_from_simple_image()
    #test_graph_from_image()
    