# -*- python -*-
#
#       OpenAlea.image.algo
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
"""This module helps to create PropertyGraph from SpatialImages."""

from openalea.image.algo.analysis import SpatialImageAnalysis, AbstractSpatialImageAnalysis, DICT
from openalea.image.spatial_image import is2D
from openalea.container import PropertyGraph
import numpy as np

#~ default_properties2D = ['barycenter','boundingbox','border','L1','epidermis_surface','wall_surface','inertia_axis']
default_properties2D = ['barycenter','boundingbox','border','L1','epidermis_surface','inertia_axis']
default_properties3D = ['volume','barycenter','boundingbox','border','L1','epidermis_surface','wall_surface','inertia_axis', 'projected_anticlinal_wall_median', 'wall_median', 'all_walls_orientation', 'epidermis_local_principal_curvature']

def generate_graph_topology(labels, neighborhood):
    """
    Function generating a topological/spatial graph based on neighbors detection.

    :Parameters:
     - `labels` (list) - list of labels to be found in the image and added to the topological graph.
     - `neighborhood` (dict) - dictionary giving neighbors of each object.

    :Returns:
     - `graph` (PropertyGraph) - the topological/spatial graph.
     - `label2vertex` (dict) - dictionary translating labels into vertex ids (vids).
     - `edges` (dict) - dictionary associating an edge id to a couple of topologically/spatially related vertex.
    """
    graph = PropertyGraph()
    vertex2label = {}
    for l in labels: vertex2label[graph.add_vertex(l)] = l
    label2vertex = dict([(j,i) for i,j in vertex2label.iteritems()])

    labelset = set(labels)
    edges = {}

    for source,targets in neighborhood.iteritems():
        if source in labelset :
            for target in targets:
                if source < target and target in labelset:
                    edges[(source,target)] = graph.add_edge(label2vertex[source],label2vertex[target])

    graph.add_vertex_property('label')
    graph.vertex_property('label').update(vertex2label)

    return graph, label2vertex, edges


def _graph_from_image(image, labels, background, default_properties, 
                     default_real_property, bbox_as_real, 
                     ignore_cells_at_stack_margins, min_contact_surface):
    """ 
    Construct a PropertyGraph from a SpatialImage (or equivalent) representing a segmented image.

    :Parameters:
     - `image` (SpatialImage|AbstractSpatialImageAnalysis) - image containing labeled objects | analysis of an image.
     - `labels` (list) - list of labels to be found in the image.
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

    if isinstance(image, AbstractSpatialImageAnalysis):
        analysis = image
        image = analysis.image
    else:
        try:
            analysis = SpatialImageAnalysis(image, ignoredlabels = 0, return_type = DICT, background = 1)
        except:
            analysis = SpatialImageAnalysis(image, ignoredlabels = 0, return_type = DICT)
    if ignore_cells_at_stack_margins:
        analysis.add2ignoredlabels( analysis.cells_in_image_margins() )

    if labels is None: 
        filter_label = False
        labels = list(analysis.labels())
        if background in labels : del labels[labels.index(background)]
    else:
        filter_label = True
        if isinstance(labels,int) : labels = [labels]
        # -- We don't want to have the "outer cell" (background) and "removed cells" (0) in the graph structure.
        # if 0 in labels: labels.remove(0)
        if background in labels: labels.remove(background)
        # -- If labels are provided, we ignore all others by default:
        analysis.add2ignoredlabels( set(analysis.labels()) - set(labels) )

    neighborhood = analysis.neighbors(labels, min_contact_surface = min_contact_surface)
    labelset = set(labels)

    graph, label2vertex, edges = generate_graph_topology(labels, neighborhood)

    # -- We want to keep the unit system of each variable
    graph.add_graph_property("units",dict())

    if ("wall_orientation" in default_properties) and ('all_wall_orientation' in default_properties):
        default_properties.remove("wall_orientation")

    if 'boundingbox' in default_properties : 
        print 'Extracting boundingbox...'
        add_vertex_property_from_dictionary(graph,'boundingbox',analysis.boundingbox(labels,real=bbox_as_real),mlabel2vertex=label2vertex)
        #~ graph._graph_property("units").update( {"boundingbox":(u'\u3bcm'if bbox_as_real else 'voxels')} )

    if 'volume' in default_properties and analysis.is3D(): 
        print 'Computing volume property...'
        add_vertex_property_from_dictionary(graph,'volume',analysis.volume(labels,real=default_real_property),mlabel2vertex=label2vertex)
        #~ graph._graph_property("units").update( {"volume":('\u03bcm\u00B3'if default_real_property else 'voxels')} )

    barycenters = None
    if 'barycenter' in default_properties :
        print 'Computing barycenter property...'
        barycenters = analysis.center_of_mass(labels,real=default_real_property)
        add_vertex_property_from_dictionary(graph,'barycenter',barycenters,mlabel2vertex=label2vertex)
        #~ graph._graph_property("units").update( {"barycenter":('\u03bcm'if default_real_property else 'voxels')} )

    background_neighbors = set(analysis.neighbors(background))
    background_neighbors.intersection_update(labelset)
    if 'L1' in default_properties :         
        print 'Generating the list of cells belonging to the first layer...'
        add_vertex_property_from_label_and_value(graph,'L1',labels,[(l in background_neighbors) for l in labels],mlabel2vertex=label2vertex)

    if 'border' in default_properties : 
        print 'Generating the list of cells at the margins of the stack...'
        border_cells = analysis.cells_in_image_margins()
        try: border_cells.remove(background)
        except: pass
        border_cells = set(border_cells)
        add_vertex_property_from_label_and_value(graph,'border',labels,[(l in border_cells) for l in labels],mlabel2vertex=label2vertex)

    if 'inertia_axis' in default_properties : 
        print 'Computing inertia_axis property...'
        inertia_axis, inertia_values = analysis.inertia_axis(labels,barycenters)
        add_vertex_property_from_dictionary(graph,'inertia_axis',inertia_axis,mlabel2vertex=label2vertex)
        add_vertex_property_from_dictionary(graph,'inertia_values',inertia_values,mlabel2vertex=label2vertex)

    if 'wall_surface' in default_properties : 
        print 'Computing wall_surface property...'
        filtered_edges, unlabelled_target, unlabelled_wall_surfaces = {}, {}, {}
        for source,targets in neighborhood.iteritems():
            if source in labelset :
                filtered_edges[source] = [ target for target in targets if source < target and target in labelset ]
                unlabelled_target[source] = [ target for target in targets if target not in labelset and target != background]
        wall_surfaces = analysis.wall_surfaces(filtered_edges,real=default_real_property)
        add_edge_property_from_label_property(graph,'wall_surface',wall_surfaces,mlabelpair2edge=edges)

        graph.add_vertex_property('unlabelled_wall_surface')
        for source in unlabelled_target:
            unlabelled_wall_surface = analysis.wall_surfaces({source:unlabelled_target[source]},real=default_real_property)
            graph.vertex_property('unlabelled_wall_surface')[label2vertex[source]] = sum(unlabelled_wall_surface.values())

        #~ graph._graph_property("units").update( {"wall_surface":('\u03bcm\u00B2'if default_real_property else 'voxels')} )

    if 'epidermis_surface' in default_properties :
        print 'Computing epidermis_surface property...'
        def not_background(indices):
            a,b = indices
            if a == background: 
                if b == background: raise ValueError(indices)
                else : return b
            elif b == background: return a
            else: raise ValueError(indices)
        epidermis_surfaces = analysis.cell_wall_surface(background,list(background_neighbors) ,real=default_real_property)
        epidermis_surfaces = dict([(not_background(indices),value) for indices,value in epidermis_surfaces.iteritems()])
        add_vertex_property_from_label_property(graph,'epidermis_surface',epidermis_surfaces,mlabel2vertex=label2vertex)
        #~ graph._graph_property("units").update( {"epidermis_surface":('um2'if default_real_property else 'voxels')} )


    if 'projected_anticlinal_wall_median' in default_properties:
        print 'Computing projected_anticlinal_wall_median property...'
        wall_median = {}
        dict_anticlinal_wall_voxels = analysis.wall_voxels_per_cells_pairs( analysis.layer1(), neighborhood, only_epidermis = True, ignore_background = True )
        for label_1, label_2 in dict_anticlinal_wall_voxels:
            if label_1 == 0: continue # if 0 means that it wasn't in the labels list provided, so we skip it.
            x,y,z = dict_anticlinal_wall_voxels[(label_1, label_2)]
            # compute geometric median:
            from openalea.image.algo.analysis import geometric_median, closest_from_A
            neighborhood_origin = geometric_median( np.array([list(x),list(y),list(z)]) )
            integers = np.vectorize(lambda x : int(x))
            neighborhood_origin = integers(neighborhood_origin)
            # closest points:
            pts = [tuple([int(x[i]),int(y[i]),int(z[i])]) for i in xrange(len(x))]
            min_dist = closest_from_A(neighborhood_origin, pts)
            wall_median[(label_1, label_2)] = min_dist

        add_edge_property_from_dictionary(graph, 'projected_anticlinal_wall_median', wall_median)


    if 'wall_median' in default_properties:
        print 'Computing wall_median property...'
        dict_wall_voxels = analysis.wall_voxels_per_cells_pairs(labels, neighborhood, ignore_background=False )

        wall_median = {}
        for label_1, label_2 in dict_wall_voxels:
            #~ if dict_wall_voxels[(label_1, label_2)] == None:
                #~ if label_1 != 0:
                    #~ print "There might be something wrong between cells %d and %d" %label_1  %label_2
                #~ continue # if None we can use it.
            x,y,z = dict_wall_voxels[(label_1, label_2)]
            # compute geometric median:
            from openalea.image.algo.analysis import geometric_median, closest_from_A
            neighborhood_origin = geometric_median( np.array([list(x),list(y),list(z)]) )
            integers = np.vectorize(lambda x : int(x))
            neighborhood_origin = integers(neighborhood_origin)
            # closest points:
            pts = [tuple([int(x[i]),int(y[i]),int(z[i])]) for i in xrange(len(x))]
            min_dist = closest_from_A(neighborhood_origin, pts)
            wall_median[(label_1, label_2)] = min_dist

        edge_wall_median, unlabelled_wall_median, vertex_wall_median = {},{},{}
        for label_1, label_2 in dict_wall_voxels.keys():
            if (label_1 in graph.vertices()) and (label_2 in graph.vertices()):
                edge_wall_median[(label_1, label_2)] = wall_median[(label_1, label_2)]
            if (label_1 == 0): # no need to check `label_2` because labels are sorted in keys returned by `wall_voxels_per_cells_pairs`
                unlabelled_wall_median[label_2] = wall_median[(label_1, label_2)]
            if (label_1 == 1): # no need to check `label_2` because labels are sorted in keys returned by `wall_voxels_per_cells_pairs`
                vertex_wall_median[label_2] = wall_median[(label_1, label_2)]

        add_edge_property_from_dictionary(graph, 'wall_median', edge_wall_median)
        add_vertex_property_from_dictionary(graph, 'epidermis_wall_median', vertex_wall_median)
        add_vertex_property_from_dictionary(graph, 'unlabelled_wall_median', unlabelled_wall_median)


    if 'all_walls_orientation' in default_properties:
        print 'Computing wall_orientation property...'
        # -- First we have to extract the voxels defining the frontier between two objects:
        # - Extract wall_orientation property for 'unlabelled' and 'epidermis' walls as well:
        try:
            dict_wall_voxels
        except:
            dict_wall_voxels = analysis.wall_voxels_per_cells_pairs(labels, neighborhood, ignore_background=False )

        if 'wall_median' in graph.edge_properties():
            medians_coords = dict( (graph.edge_vertices(eid), coord) for eid,coord in graph.edge_property('wall_median').iteritems() )
            medians_coords.update(dict( (0,vid) for vid in graph.vertex_property('unlabelled_wall_median') ))
            medians_coords.update(dict( (1,vid) for vid in graph.vertex_property('epidermis_wall_median') ))
            pc_values, pc_normal, pc_directions, pc_origin = analysis.wall_orientation( dict_wall_voxels, fitting_degree = 2, plane_projection = False, dict_coord_points_ori = medians_coords )
        else:
            pc_values, pc_normal, pc_directions, pc_origin = analysis.wall_orientation( dict_wall_voxels, fitting_degree = 2, plane_projection = False )

        # -- Now we can compute the orientation of the frontier between two objects:
        edge_pc_values, edge_pc_normal, edge_pc_directions, edge_pc_origin = {},{},{},{}
        vertex_pc_values, vertex_pc_normal, vertex_pc_directions, vertex_pc_origin = {},{},{},{}
        epidermis_pc_values, epidermis_pc_normal, epidermis_pc_directions, epidermis_pc_origin = {},{},{},{}
        for label_1, label_2 in dict_wall_voxels.keys():
            if (label_1 in graph.vertices()) and (label_2 in graph.vertices()):
                edge_pc_values[(label_1, label_2)] = pc_values[(label_1, label_2)]
                edge_pc_normal[(label_1, label_2)] = pc_normal[(label_1, label_2)]
                edge_pc_directions[(label_1, label_2)] = pc_directions[(label_1, label_2)]
                edge_pc_origin[(label_1, label_2)] = pc_origin[(label_1, label_2)]
            if (label_1 == 0): # no need to check `label_2` because labels are sorted in keys returned by `wall_voxels_per_cells_pairs`
                vertex_pc_values[label_2] = pc_values[(label_1, label_2)]
                vertex_pc_normal[label_2] = pc_normal[(label_1, label_2)]
                vertex_pc_directions[label_2] = pc_directions[(label_1, label_2)]
                vertex_pc_origin[label_2] = pc_origin[(label_1, label_2)]
            if (label_1 == 1): # no need to check `label_2` because labels are sorted in keys returned by `wall_voxels_per_cells_pairs`
                epidermis_pc_values[label_2] = pc_values[(label_1, label_2)]
                epidermis_pc_normal[label_2] = pc_normal[(label_1, label_2)]
                epidermis_pc_directions[label_2] = pc_directions[(label_1, label_2)]
                epidermis_pc_origin[label_2] = pc_origin[(label_1, label_2)]

        add_edge_property_from_dictionary(graph, 'wall_principal_curvature_values', edge_pc_values)
        add_edge_property_from_dictionary(graph, 'wall_principal_curvature_normal', edge_pc_normal)
        add_edge_property_from_dictionary(graph, 'wall_principal_curvature_directions', edge_pc_directions)
        if not 'wall_median' in graph.edge_properties():
            add_edge_property_from_dictionary(graph, 'wall_principal_curvature_origin', edge_pc_origin)
        if vertex_pc_values != {}:
            add_vertex_property_from_dictionary(graph, 'unlabelled_wall_principal_curvature_values', vertex_pc_values)
            add_vertex_property_from_dictionary(graph, 'unlabelled_wall_principal_curvature_normal', vertex_pc_normal)
            add_vertex_property_from_dictionary(graph, 'unlabelled_wall_principal_curvature_directions', vertex_pc_directions)
            if not 'wall_median' in graph.edge_properties():
                add_vertex_property_from_dictionary(graph, 'unlabelled_wall_principal_curvature_origin', vertex_pc_origin)
        if epidermis_pc_values != {}:
            add_vertex_property_from_dictionary(graph, 'epidermis_wall_principal_curvature_values', epidermis_pc_values)
            add_vertex_property_from_dictionary(graph, 'epidermis_wall_principal_curvature_normal', epidermis_pc_normal)
            add_vertex_property_from_dictionary(graph, 'epidermis_wall_principal_curvature_directions', epidermis_pc_directions)
            if not 'wall_median' in graph.edge_properties():
                add_vertex_property_from_dictionary(graph, 'epidermis_wall_principal_curvature_origin', epidermis_pc_origin)


    if 'epidermis_local_principal_curvature' in default_properties:
        index_radius = default_properties.index('epidermis_local_principal_curvature')+1
        if isinstance(default_properties[index_radius],int):
            radius = [default_properties[index_radius]]
        elif isinstance(default_properties[index_radius],list):
            radius = default_properties[index_radius]
        else:
            radius = [60]

        graph.add_graph_property('radius_local_principal_curvature_estimation',radius)
        for radius in graph.graph_property('radius_local_principal_curvature_estimation'):
            print 'Computing local_principal_curvature property with radius = {}voxels...'.format(radius)
            print r"This represent a local curvature estimation area of {}$\mu.m^{2}$".format(math.pi*(radius*analysis.image.resolution[0])*(radius*analysis.image.resolution[1]))
            analysis.compute_principal_curvatures(radius=radius,verbose=True)
            add_vertex_property_from_dictionary(graph, 'epidermis_local_principal_curvature_values_r'+str(radius), analysis.principal_curvatures)
            add_vertex_property_from_dictionary(graph, 'epidermis_local_principal_curvature_normal_r'+str(radius), analysis.principal_curvatures_normal)
            add_vertex_property_from_dictionary(graph, 'epidermis_local_principal_curvature_directions_r'+str(radius), analysis.principal_curvatures_directions)
        if not 'wall_median' in graph.edge_properties():
            add_vertex_property_from_dictionary(graph, 'epidermis_local_principal_curvature_origin', analysis.principal_curvatures_origin)

    #~ if 'local_gaussian_curvature' in default_properties:
        #~ print 'Computing local_gaussian_curvature with radius = {}voxels...'.format(radius)
        #~ gaussian_curvature = analysis.gaussian_curvature_CGAL(radius=radius,verbose=True)
        #~ add_vertex_property_from_dictionary(graph, 'local_gaussian_curvature_r'+str(radius), gaussian_curvature)
#~ 
    #~ if 'local_mean_curvature' in default_properties:
        #~ print 'Computing local_mean_curvature property with radius = {}voxels...'.format(radius)
        #~ mean_curvature = analysis.mean_curvature_CGAL(radius=radius,verbose=True)
        #~ add_vertex_property_from_dictionary(graph, 'local_mean_curvature_r'+str(radius), mean_curvature)
#~ 
    #~ if 'local_curvature_ratio' in default_properties:
        #~ print 'Computing local_curvature_ratio property with radius = {}voxels...'.format(radius)
        #~ curvature_ratio = analysis.curvature_ratio_CGAL(radius=radius,verbose=True)
        #~ add_vertex_property_from_dictionary(graph, 'local_curvature_ratio_r'+str(radius), curvature_ratio)
#~ 
    #~ if 'local_curvature_anisotropy' in default_properties:
        #~ print 'Computing local_curvature_anisotropy property with radius = {}voxels...'.format(radius)
        #~ curvature_anisotropy = analysis.curvature_anisotropy_CGAL(radius=radius,verbose=True)
        #~ add_vertex_property_from_dictionary(graph, 'local_curvature_anisotropy_r'+str(radius), curvature_anisotropy)

    return graph


def graph_from_image2D(image, labels, background, default_properties, 
                     default_real_property, bbox_as_real, 
                     ignore_cells_at_stack_margins, min_contact_surface):
    return _graph_from_image(image, labels, background, default_properties,
                            default_real_property, bbox_as_real, ignore_cells_at_stack_margins, min_contact_surface)

def graph_from_image3D(image, labels, background, default_properties, 
                     default_real_property, bbox_as_real, 
                     ignore_cells_at_stack_margins, min_contact_surface):
    return _graph_from_image(image, labels, background, default_properties,
                            default_real_property, bbox_as_real, ignore_cells_at_stack_margins, min_contact_surface)

def graph_from_image(image, 
                     labels = None, 
                     background = 1, 
                     default_properties = None,
                     default_real_property = True,
                     bbox_as_real = False,
                     ignore_cells_at_stack_margins = True,
                     min_contact_surface = None):

    if isinstance(image, AbstractSpatialImageAnalysis):
        real_image = image.image
        if labels is None:
            labels = image.labels()
    else:
        real_image = image

    if is2D(real_image):
        if default_properties == None:
            default_properties = default_properties2D
        return graph_from_image2D(image, labels, background, default_properties,
                            default_real_property, bbox_as_real, ignore_cells_at_stack_margins, min_contact_surface)
    else:
        if default_properties == None:
            default_properties = default_properties3D
        return graph_from_image3D(image, labels, background, default_properties,
                            default_real_property, bbox_as_real, ignore_cells_at_stack_margins, min_contact_surface)

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

def vertexpair2edge_map(graph):
    """
        Compute a dictionary that map pair of labels to edge id.
        It requires the existence of a 'label' property
        
        :rtype: dict
    """
    return dict([((graph.source(eid),graph.target(eid)),eid) for eid in graph.edges()])


def add_vertex_property_from_dictionary(graph, name, dictionary, mlabel2vertex = None):
    """ 
        Add a vertex property with name 'name' to the graph build from an image. 
        The values of the property are given as by a dictionary where keys are vertex labels. 
    """
        
    if mlabel2vertex is None:    
        mlabel2vertex = label2vertex_map(graph)

    if name in graph.vertex_properties():
        raise ValueError('Existing vertex property %s' % name)

    graph.add_vertex_property(name)
    graph.vertex_property(name).update( dict([(mlabel2vertex[k], dictionary[k]) for k in dictionary]) )

def add_vertex_property_from_label_and_value(graph, name, labels, property_values, mlabel2vertex = None):
    """ 
        Add a vertex property with name 'name' to the graph build from an image. 
        The values of the property are given as two lists. 
        First one gives the label in the image and second gives the value of the property.
        Labels are first translated in id of the graph and values are assigned to these ids in the graph
    """
        
    if mlabel2vertex is None:    
        mlabel2vertex = label2vertex_map(graph)

    if name in graph.vertex_properties():
        raise ValueError('Existing vertex property %s' % name)

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

    if name in graph.vertex_properties():
        raise ValueError('Existing vertex property %s' % name)

    graph.add_vertex_property(name)
    graph.vertex_property(name).update(dict([(mlabel2vertex[i], v) for i,v in label_property.iteritems()]))

def add_edge_property_from_dictionary(graph, name, dictionary, mlabelpair2edge = None):
    """ 
        Add an edge property with name 'name' to the graph build from an image. 
        The values of the property are given as by a dictionary where keys are vertex labels. 
    """
        
    if mlabelpair2edge is None:    
        mlabelpair2edge = labelpair2edge_map(graph)

    if name in graph.edge_properties():
        raise ValueError('Existing edge property %s' % name)

    graph.add_edge_property(name)
    graph.edge_property(name).update( dict([(mlabelpair2edge[k], dictionary[k]) for k in dictionary]) )

def add_edge_property_from_label_and_value(graph, name, label_pairs, property_values, mlabelpair2edge = None):
    """ 
        Add an edge property with name 'name' to the graph build from an image. 
        The values of the property are given as two lists. 
        First one gives the pair of labels in the image that are connected and the second list gives the value of the property.
        Pairs of labels are first translated in edge ids of the graph and values are assigned to these ids in the graph
    """
        
    if mlabelpair2edge is None:
        mlabelpair2edge = labelpair2edge_map(graph)

    if name in graph.edge_properties():
        raise ValueError('Existing edge property %s' % name)

    graph.add_edge_property(name)
    graph.edge_property(name).update(dict([(mlabelpair2edge[labelpair], value) for labelpair,value in zip(label_pairs,property_values)]))

def add_edge_property_from_label_property(graph, name, labelpair_property, mlabelpair2edge = None):
    """ 
        Add an edge property with name 'name' to the graph build from an image. 
        The values of the property are given as a dictionnary associating a pair of label and a value. 
        Pairs of labels are first translated in edge ids of the graph and values are assigned to these ids in the graph
    """
    if mlabelpair2edge is None:
        mlabelpair2edge = labelpair2edge_map(graph)

    if name in graph.edge_properties():
        raise ValueError('Existing edge property %s' % name)

    graph.add_edge_property(name)
    graph.edge_property(name).update(dict([(mlabelpair2edge[labelpair], value) for labelpair,value in labelpair_property.iteritems()]))    
