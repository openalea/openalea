from analysis import SpatialImageAnalysis
from openalea.image.spatial_image import SpatialImage
from openalea.container import PropertyGraph

default_properties = ['volume','barycenter','boundingbox','wall_surface']

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
                     default_real_property = True):
    
    analysis = SpatialImageAnalysis(image)
    
    if labels is None: 
        filter_label = False
        labels = list(analysis.labels())
        if background in labels : del labels[labels.index(background)]
        neigborhood = analysis.neighbors()
    else:
        filter_label = True
        neigborhood = analysis.neighbors(labels)
    labelset = set(labels)
    
    graph, label2vertex, edges = generate_graph_topology(labels, neigborhood)
    
    if 'boundingbox' in default_properties : 
        add_vertex_property_from_label_and_value(graph,'boundingbox',labels,analysis.boundingbox(labels,real=default_real_property),mlabel2vertex=label2vertex)
    
    if 'volume' in default_properties : 
        add_vertex_property_from_label_and_value(graph,'volume',labels,analysis.volume(labels,real=default_real_property),mlabel2vertex=label2vertex)
    
    if 'barycenter' in default_properties : 
        add_vertex_property_from_label_and_value(graph,'barycenter',labels,analysis.center_of_mass(labels,real=default_real_property),mlabel2vertex=label2vertex)

    default_edge_properties = [i for i in default_properties if i in ['wall_surface']]
    if not default_edge_properties is None:
        filtered_edges = {}
        for source,targets in neigborhood.iteritems():
            if source in labelset :
                filtered_edges[source] = [ target for target in targets if source < target and target in labelset ]
            
        if 'wall_surface' in default_edge_properties : 
            wall_surfaces = analysis.wall_surfaces(filtered_edges,real=default_real_property)
            add_edge_property_from_label_property(graph,'wall_surface',wall_surfaces,mlabelpair2edge=edges)
    
    return graph       

def label2vertex(graph):
    return dict([(j,i) for i,j in graph.property('label')])

def labelpair2edge(graph):
    mlabel2vertex = label2vertex(graph)
    return dict([((mlabel2vertex[graph.source(eid)],mlabel2vertex[graph.target(eid)]),eid) for eid in graph.edges()])


def add_vertex_property_from_label_and_value(graph, name, labels, property_values, mlabel2vertex = None):
    """ 
        Add a property with name 'name' to the graph build from an image. 
        The values of the property are given as two lists. 
        First one gives the label in the image and second gives the value of the property.
        Labels are first translated in id of the graph and values are assigned to these ids in the graph
    """
        
    if mlabel2vertex is None:    
        mlabel2vertex = label2vertex(graph)
    
    graph.add_vertex_property(name)
    graph.vertex_property(name).update(dict([(mlabel2vertex[i], v) for i,v in zip(labels,property_values)]))

def add_vertex_property_from_label_property(graph, name, label_property, mlabel2vertex = None):
    """ 
        Add a property with name 'name' to the graph build from an image. 
        The values of the property are given as a dictionnary associating a label and a value. 
        Labels are first translated in id of the graph and values are assigned to these ids in the graph
    """
    if mlabel2vertex is None:    
        mlabel2vertex = label2vertex(graph)
    
    graph.add_vertex_property(name)
    graph.vertex_property(name).update(dict([(mlabel2vertex[i], v) for i,v in label_property.iteritems]))

def add_edge_property_from_label_and_value(graph, name, label_pairs, property_values, mlabelpair2edge = None):
    """ 
        Add a property with name 'name' to the graph build from an image. 
        The values of the property are given as two lists. 
        First one gives the label in the image and second gives the value of the property.
        Labels are first translated in id of the graph and values are assigned to these ids in the graph
    """
        
    if mlabelpair2edge is None:
        mlabelpair2edge = labelpair2edge(graph)
    
    graph.add_edge_property(name)
    graph.edge_property(name).update(dict([(mlabelpair2edge[i], v) for labelpair,value in zip(label_pairs,property_values)]))

def add_edge_property_from_label_property(graph, name, labelpair_property, mlabelpair2edge = None):
    """ 
        Add a property with name 'name' to the graph build from an image. 
        The values of the property are given as a dictionnary associating a label and a value. 
        Labels are first translated in id of the graph and values are assigned to these ids in the graph
    """
    if mlabelpair2edge is None:
        mlabelpair2edge = labelpair2edge(graph)
    
    graph.add_edge_property(name)
    graph.edge_property(name).update(dict([(mlabelpair2edge[labelpair], value) for labelpair,value in labelpair_property.iteritems()]))    