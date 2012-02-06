from analysis import SpatialImageAnalysis
from openalea.image.spatial_image import SpatialImage
from openalea.container import PropertyGraph

default_properties = ['volume','barycenter','boundingbox','border','L1','epidermis_wall_surface','wall_surface','inertia']

def generate_graph_topology(labels, neigborhood):
    graph = PropertyGraph()
    vertex2label = {}
    for l in labels: vertex2label[graph.add_vertex(l)] = l
    label2vertex = dict([(j,i) for i,j in vertex2label.iteritems()])
    
    labelset = set(labels)
    edges = {}
    
    for source,targets in neigborhood.iteritems():
        if source in labelset :
            for target in targets:
                if source < target and target in labelset:
                    edges[(source,target)] = graph.add_edge(label2vertex[source],label2vertex[target])
    
    graph.add_vertex_property('label')
    graph.vertex_property('label').update(vertex2label)
    
    return graph, label2vertex, edges

def graph_from_image(image, 
                     labels = None, 
                     background = 1, 
                     default_properties = default_properties,
                     default_real_property = True,
                     bbox_as_real = False):
    """ 
        Construct a PropertyGraph from a SpatialImage (or equivalent) representing a segmented image.

        :Parameters:
         - `labels` (list) - sequence of label numbers of the objects to be measured.
            If labels is None, all labels are used.
         - `background` (int) - label representing background.
         - `default_properties` (list) - the list of name of properties to create. It should be in default_properties.
         - `default_real_property` (bool) - If default_real_property = True, property is in real-world units else in voxels.
         - `bbox_as_real` (bool) - If bbox_as_real = True, bounding boxes are in real-world units else in voxels.

        :rtype: PropertyGraph

        :Examples:

        >>> import numpy as np
        >>> image = np.array([[1, 2, 7, 7, 1, 1],
                          [1, 6, 5, 7, 3, 3],
                          [2, 2, 1, 7, 3, 3],
                          [1, 1, 1, 4, 1, 1]])

        >>> from openalea.image.algo.graph_from_image import graph_from_image
        >>> graph = graph_from_image(image)

    """
    
    analysis = SpatialImageAnalysis(image)
    
    if labels is None: 
        filter_label = False
        labels = list(analysis.labels())
        if background in labels : del labels[labels.index(background)]
        neigborhood = analysis.neighbors(labels)
    else:
        filter_label = True
        neigborhood = analysis.neighbors(labels)
    labelset = set(labels)
    
    graph, label2vertex, edges = generate_graph_topology(labels, neigborhood)
    
    if 'boundingbox' in default_properties : 
        add_vertex_property_from_label_and_value(graph,'boundingbox',labels,analysis.boundingbox(labels,real=bbox_as_real),mlabel2vertex=label2vertex)
    
    if 'volume' in default_properties : 
        add_vertex_property_from_label_and_value(graph,'volume',labels,analysis.volume(labels,real=default_real_property),mlabel2vertex=label2vertex)
    
    barycenters = None
    if 'barycenter' in default_properties :
        barycenters = analysis.center_of_mass(labels,real=default_real_property)
        add_vertex_property_from_label_and_value(graph,'barycenter',labels,barycenters,mlabel2vertex=label2vertex)

    if 'L1' in default_properties :         
        background_neighbors = set(analysis.neighbors(background)[background])
        add_vertex_property_from_label_and_value(graph,'L1',labels,[(l in background_neighbors) for l in labels],mlabel2vertex=label2vertex)
        
    if 'border' in default_properties : 
        border_cells = analysis.border_cells()
        try: border_cells.remove(background)
        except: pass
        border_cells = set(border_cells)
        add_vertex_property_from_label_and_value(graph,'border',labels,[(l in border_cells) for l in labels],mlabel2vertex=label2vertex)
        
    if 'inertia_axis' in default_properties : 
        inertia_axis, inertia_values = analysis.inertia_axis(labels,barycenters)
        add_vertex_property_from_label_and_value(graph,'inertia_axis',labels,zip(inertia_axis,inertia_value),mlabel2vertex=label2vertex)
        
    
    if 'wall_surface' in default_properties : 
        filtered_edges = {}
        for source,targets in neigborhood.iteritems():
            if source in labelset :
                filtered_edges[source] = [ target for target in targets if source < target and target in labelset ]
        wall_surfaces = analysis.wall_surfaces(filtered_edges,real=default_real_property)
        add_edge_property_from_label_property(graph,'wall_surface',wall_surfaces,mlabelpair2edge=edges)
        
    if 'epidermis_surface' in default_properties :
        background_edges = {}
        for source,targets in neigborhood.iteritems():
            if source == background :
                background_edges[source] = targets
            elif source < background and background in targets:
                background_edges[source] = [background]
    
        epidermis_surfaces = analysis.wall_surfaces(background_edges,real=default_real_property)
        epidermis_surfaces = dict([(sum(indices)-background,value) for indices,value in epidermis_surfaces.iteritems()])
        add_vertex_property_from_label_property(graph,'epidermis_surface',epidermis_surfaces,mlabel2vertex=label2vertex)
    
    return graph       

def label2vertex_map(graph):
    """
        Compute a dictionary that map label to vertex id.
        It requires the existence of a 'label' vertex property
        
        :rtype: dict
    """
    return dict([(j,i) for i,j in graph.vertex_property('label').iteritems()])

def label2vertex(graph,labels):
    """
        Translate label as vertex id.
        It requires the existence of a 'label' vertex property
        
        :rtype: dict
    """
    label2vertexmap = label2vertex_map(graph)
    if isinstance(labels,list):
        return [label2vertexmap[label] for label in labels]
    else : return label2vertexmap[labels]

def labelpair2edge_map(graph):
    """
        Compute a dictionary that map pair of labels to edge id.
        It requires the existence of a 'label' property
        
        :rtype: dict
    """
    mlabel2vertex = label2vertex_map(graph)
    return dict([((mlabel2vertex[graph.source(eid)],mlabel2vertex[graph.target(eid)]),eid) for eid in graph.edges()])


def add_vertex_property_from_label_and_value(graph, name, labels, property_values, mlabel2vertex = None):
    """ 
        Add a vertex property with name 'name' to the graph build from an image. 
        The values of the property are given as two lists. 
        First one gives the label in the image and second gives the value of the property.
        Labels are first translated in id of the graph and values are assigned to these ids in the graph
    """
        
    if mlabel2vertex is None:    
        mlabel2vertex = label2vertex_map(graph)
    
    graph.add_vertex_property(name)
    graph.vertex_property(name).update(dict([(mlabel2vertex[i], v) for i,v in zip(labels,property_values)]))

def add_vertex_property_from_label_property(graph, name, label_property, mlabel2vertex = None):
    """ 
        Add a vertex property with name 'name' to the graph build from an image. 
        The values of the property are given as a dictionnary associating a label and a value. 
        Labels are first translated in id of the graph and values are assigned to these ids in the graph
    """
    if mlabel2vertex is None:    
        mlabel2vertex = label2vertex_map(graph)
    
    graph.add_vertex_property(name)
    graph.vertex_property(name).update(dict([(mlabel2vertex[i], v) for i,v in label_property.iteritems]))

def add_edge_property_from_label_and_value(graph, name, label_pairs, property_values, mlabelpair2edge = None):
    """ 
        Add an edge property with name 'name' to the graph build from an image. 
        The values of the property are given as two lists. 
        First one gives the pair of labels in the image that are connected and the second list gives the value of the property.
        Pairs of labels are first translated in edge ids of the graph and values are assigned to these ids in the graph
    """
        
    if mlabelpair2edge is None:
        mlabelpair2edge = labelpair2edge_map(graph)
    
    graph.add_edge_property(name)
    graph.edge_property(name).update(dict([(mlabelpair2edge[i], v) for labelpair,value in zip(label_pairs,property_values)]))

def add_edge_property_from_label_property(graph, name, labelpair_property, mlabelpair2edge = None):
    """ 
        Add an edge property with name 'name' to the graph build from an image. 
        The values of the property are given as a dictionnary associating a pair of label and a value. 
        Pairs of labels are first translated in edge ids of the graph and values are assigned to these ids in the graph
    """
    if mlabelpair2edge is None:
        mlabelpair2edge = labelpair2edge_map(graph)
    
    graph.add_edge_property(name)
    graph.edge_property(name).update(dict([(mlabelpair2edge[labelpair], value) for labelpair,value in labelpair_property.iteritems()]))    