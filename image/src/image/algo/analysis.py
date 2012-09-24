# -*- python -*-
#
#       OpenAlea.Image
#
#       Copyright 2006 - 2012 INRIA - CIRAD - INRA
#
#       File author(s): Eric MOSCARDI <eric.moscardi@sophia.inria.fr>
#                       Jonathan LEGRAND <jonathan.legrand@ens-lyon.fr>
#                       Frederic BOUDON <frederic.boudon@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
################################################################################

__license__ = "Cecill-C"
__revision__ = " $Id$ "

import warnings
import math
import copy
from os.path import exists
import gzip
import pickle

import numpy as np
import numpy.linalg as ln
import scipy.ndimage as nd

from openalea.image.spatial_image import SpatialImage

def dilation(slices):
    """
    Function dilating slices: extend the boundingbox of one voxel.
    """
    return [ slice(max(0,s.start-1), s.stop+1) for s in slices ]

def wall(mask_img, label_id):
    """
    TODO
    """
    img = (mask_img == label_id)
    dil = nd.binary_dilation(img)
    contact = dil - img
    return mask_img[contact]


def contact_surface(mask_img, label_id):
    """
    TODO
    """
    img = wall(mask_img,label_id)
    return set( np.unique(img) )


def real_indices(slices, resolutions):
    """
    TODO
    """
    return [ (s.start*r, s.stop*r) for s,r in zip(slices,resolutions) ]


def hollow_out_cells(image, background, verbose = True):
    """
    Laplacian filter used to dectect and return an Spatial Image containing only cell walls.
    (The Laplacian of an image highlights regions of rapid intensity change.)

    :Parameters:
     - `image` (SpatialImage) - Segmented image (tissu).
     - `background` (int) - label representing the background (to remove).

    :Return:
     - `m` (SpatialImage) - Spatial Image containing hollowed out cells (only walls).
    """
    if verbose: print 'Hollowing out cells...'
    b = nd.laplace(image)
    m = image.copy()
    m[b==0] = 0
    m[np.where(m==background)] = 0
    if verbose: print 'Done !!'
    return m


def cells_walls_coords(image, background = 1, hollow_out = True, verbose = True):
    """
    Return coordinates of the voxels belonging to the cell wall.
    
    .. warning :: Apply only to full 3D image, and not if only the first layer of voxel is provided (external envelope).

    :Parameters:
     - image (SpatialImage) - Segmented image (tissu)

    :Return:
     - x,y,z (list) - coordinates of the voxels defining the cell boundaries (walls).
    """
    if hollow_out:
        image = hollow_out_cells(image, background)
    else:
        image[np.where(image==background)] = 0

    if verbose and hollow_out: print 'Extracting cell walls coordinates...'

    if len(image.shape) == 3:
        x,y,z = np.where(image!=0)
        return list(x), list(y), list(z)

    if len(image.shape) == 2:
        x,y = np.where(image!=0)
        return list(x), list(y)


def cell_vertex_extraction(image, hollow_out = True, verbose = False):
    """
    Calculates cell's vertices positions according to the rule: a vertex is the point where you can find 4 differents cells (in 3D!!)
    For the surface, the outer 'cell' #1 is considered as a cell.

    :Parameters:
     - image (SpatialImage) - Segmented image (tissu). Can be a full spatial image or an extracted surface.

    :Return:
     - barycentric_vtx (dict) -
            *keys = the 4 cells ids associated with the vertex position(values);
            *values = 3D coordinates of the vertex in the Spatial Image;
    """
    x, y, z = cells_walls_coords(image, hollow_out)
    ## Compute vertices positions by findind the voxel belonging to each vertex.
    if verbose: print 'Compute cell vertex positions...'
    vertex_voxel = {}
    dim = len(x)
    for n in xrange(dim):
        if verbose and n%20000 == 0:
            print n,'/',dim
        i, j, k = x[n], y[n], z[n]
        sub_image = image[(i-1):(i+2),(j-1):(j+2),(k-1):(k+2)] # we generate a sub_image-matrix...
        sub_image = tuple(np.unique(sub_image))
        # -- Now we detect voxels defining cells' vertices.
        if ( len(sub_image) == 4 ): # ...in which we search for 4 different labels
            if vertex_voxel.has_key(sub_image):
                vertex_voxel[sub_image] = np.vstack( (vertex_voxel[sub_image], np.array((i,j,k)).T) ) # we group voxels defining the same vertex by the IDs of the 4 cells.
            else:
                vertex_voxel[sub_image] = np.ndarray((0,3))
    ## Compute the barycenter of the voxels associated to each vertex (correspondig to the 3 cells detected previously).
    barycentric_vtx = {}
    for i in vertex_voxel.keys():
        barycentric_vtx[i] = np.mean(vertex_voxel[i],0)
    if verbose: print 'Done !!'

    return barycentric_vtx


def cells_vertices_relations(cells2coord):
    """
    Creates vtx2cells, vtx2coord & cell2vertices dictionaries.
    
    :INPUT:
    - `cells2coord` (dict) *keys=the 4 cells ids at the vertex position ; *values=3D coordinates of the vertex in the Spatial Image.
    
    :OUPTUTS:
    - `vtx2cells` (dict) - *keys= vertex NEW id ; *values= ids of the 4 associated cells.
    - `vtx2coord` (dict) - *keys= vertex NEW id ; *values= 3D coordinates of the vertex in the SpatialImage.
    - `cell2vertices` (dict) - *keys= cell id ; *values= ids of the vertices defining the cell.
    """
    vtx2cells = {} #associated cells to each vertex;
    cell2vertices = {} #associated vertex to each cells;
    vtx2coord = {}
    for n, i in enumerate(cells2coord.keys()):
        vtx2cells[n] = list(i)
        vtx2coord[n] = list(cells2coord[i])
        for j in list(i):
            #check if cell j is already in the dict
            if cell2vertices.has_key(j): 
                cell2vertices[j] = cell2vertices[j]+[n] #if true, keep the previous entry (vertex)and give the value of the associated vertex
            else:
                cell2vertices[j] = [n] #if false, create a new one and give the value of the associated vertex
    #~ del(cell2vertices[1]) #cell #1 doesn't really exist...
    return vtx2cells, vtx2coord, cell2vertices


#~ def OLS_wall(xyz):
    #~ """
    #~ Compute OLS (Ordinary Least Square) fitting of a plane in a 3D space.
    #~ 
    #~ :Parameters:
        #~ - `xyz` voxels coordinate (3xN or Nx3 matrix)
    #~ """
    #~ if xyz.shape()[0] == 3: #if the matrix is 3xN, we convert it to a Nx3 matrix.
        #~ xyz = xyz.transpose()
    #~ 
    #~ ols_fit = ln.lstsq( xyz[:,0:2], xyz[:,2] )
        #~ 
    #~ return ols_fit


def distance(ptsA, ptsB):
    """
    Function computing the Euclidian distance between two points A & B.
    Can be 2D or 3D coordinates.

    :Parameters:
     - `ptsA` (list/numpy.array) - 2D/3D coordinates
     - `ptsB` (list/numpy.array) - 2D/3D coordinates
    """
    if len(ptsA) != len(ptsB):
        warnings.warn("It seems that the points are not in the same space!")
        return None

    if len(ptsA) == 2:
        return math.sqrt( (ptsA[0]-ptsB[0])**2+(ptsA[1]-ptsB[1])**2 )
    
    if len(ptsA) == 3:
        return math.sqrt( (ptsA[0]-ptsB[0])**2+(ptsA[1]-ptsB[1])**2+(ptsA[2]-ptsB[2])**2 )


def closest_from_A(A, pts2search):
    """
    Find the closest point from A in a list of points 'pts2search'.
    Return the 3D coordinates of the closest point from A.
    
    :Parameters:
     - `A` (list/numpy.array) - 2D/3D coordinates of the point of interest (xA, yA)/(xA, yA, zA);
     - `pts2search` (list) - list of 2D/3D coordinates
    """
    dist_1 = float('inf')
    for k in pts2search:
        dist_2 = distance( A, k)
        if dist_2 < dist_1:
            pts_min_dist = k
            dist_1 = copy.copy(dist_2)

    return pts_min_dist



NPLIST, LIST, DICT = range(3)
 
class AbstractSpatialImageAnalysis(object):
    """
    This object can extract a number of 2D or 3D geometric estimator from a SpatialImage 
    (cells volume...) and the neighborhood structure (also the shared surface area of two neighboring cells).
    """
    
    def __init__(self, image, ignoredlabels = [], return_type = NPLIST):
        """
        ..warning :: Label features in the images are an arithmetic progression of continous integers.
        
        By default, we create cache of a property only if it can be used by several functions.
        """
        if not isinstance(image, SpatialImage):
            self.image = SpatialImage(image)
        else:
            self.image = image

        # -- We use this to avoid (when possible) computation of properties on background and other cells (ex: cell in image margins)
        if isinstance(ignoredlabels, int):
            ignoredlabels = [ignoredlabels]
        self._ignoredlabels = set(ignoredlabels) 

        # -- Variables for caching information:
        self._labels = None
        self._bbox = None
        self._kernels = None
        self._neighbors = None
        self._layer1 = None

        # -- Variables for meta-informations:
        try:
            self.filename = image.info["filename"] # Jonathan : 14.05.2012
        except:
            self.filename = None

        self.return_type = return_type


    def is3D(self): return False


    def add2ignoredlabels(self, list2add, verbose = False):
        """
        Add labels to the ignoredlabels list (set) and update the self._labels cache.
        """
        if isinstance(list2add, int):
            list2add = [list2add]

        if verbose: print 'Adding labels', list2add,'to the list of labels to ignore...'
        self._ignoredlabels.update(list2add)
        if verbose: print 'Updating labels list...'
        self._labels = self.__labels()


    def save(self, filename = ""):
        """
        Save an 'analysis' object, under the name 'name'. One can choose to keep only ceretains attributes.
        
        :Parameters:
         - `filename` (str) - name of the file to create WITHOUT extension.
        """

        # If no filename is given, we create one based on the name of the SpatialImage (if possible).
        if ( filename == "" ) and ( self.filename != None ):
            filename = self.filename
            if filename.endswith(".inr.gz"):
                filename = filename[:-7]
            if filename.endswith(".inr"):
                filename = filename[:-4]
            filename.join([filename+"_analysis.pklz"])
        else:
            warnings.warn("The filename is missing, and there's no information about it in "+str(self)+". Saving process ABORTED.")
            return None

        # -- We make sure the file doesn't already exist !
        if exists(filename):
            warnings.warn("The file "+filename+" already exist. Saving process ABORTED.")
            return None

        # -- We save a binary compresed version of the file:
        f = gzip.open( filename , 'wb')
        pickle.dump( self, f )
        f.close()
        print "File " + filename + " succesfully created !!"


    def convert_return(self, values, labels = None):
        """
        This function convert outputs of analysis functions.
        """
        # -- In case of unique label, just return the result for this label
        #~ if not labels is None and isinstance(labels,int): return values[0]
        if not labels is None and isinstance(labels,int): return values
        # -- return a numpy array
        elif self.return_type == NPLIST: return values
        # -- return a standard python list
        elif self.return_type == LIST: return values.tolist()
        # -- return a dictionary 
        else: return dict(zip(labels,values))


    def labels(self):
        """
        Return the list of labels used.

        :Examples:

        >>> import numpy as np
        >>> a = np.array([[1, 2, 7, 7, 1, 1],
                          [1, 6, 5, 7, 3, 3],
                          [2, 2, 1, 7, 3, 3],
                          [1, 1, 1, 4, 1, 1]])

        >>> from openalea.image.algo.analysis import SpatialImageAnalysis
        >>> analysis = SpatialImageAnalysis(a)

        >>> analysis.labels()
        [1,2,3,4,5,6,7]
        """
        if self._labels is None: self._labels = self.__labels()
        return self._labels

    def __labels(self):
        """ Compute the actual list of labels """
        labels = set(np.unique(self.image))-self._ignoredlabels
        integers = np.vectorize(lambda x : int(x))
        return integers(list(labels)).tolist()

    def nb_labels(self):
        """
        Return the number of labels.

        :Examples:

        >>> import numpy as np
        >>> a = np.array([[1, 2, 7, 7, 1, 1],
                          [1, 6, 5, 7, 3, 3],
                          [2, 2, 1, 7, 3, 3],
                          [1, 1, 1, 4, 1, 1]])

        >>> from openalea.image.algo.analysis import SpatialImageAnalysis
        >>> analysis = SpatialImageAnalysis(a)

        >>> analysis.nb_labels()
        7
        """
        if self._labels is None : self._labels = self.__labels()
        return len(self._labels)


    def center_of_mass(self, labels=None, real=True):
        """
            Return the center of mass of the labels.

        :Parameters:
         - `labels` (int) - single label number or a sequence of
            label numbers of the objects to be measured.
            If labels is None, all labels are used.

         - `real` (bool) - If real = True, center of mass is in real-world units else in voxels.

        :Examples:

        >>> import numpy as np
        >>> a = np.array([[1, 2, 7, 7, 1, 1],
                          [1, 6, 5, 7, 3, 3],
                          [2, 2, 1, 7, 3, 3],
                          [1, 1, 1, 4, 1, 1]])

        >>> from openalea.image.algo.analysis import SpatialImageAnalysis
        >>> analysis = SpatialImageAnalysis(a)

        >>> analysis.center_of_mass(7)
        [0.75, 2.75, 0.0]

        >>> analysis.center_of_mass([7,2])
        [[0.75, 2.75, 0.0], [1.3333333333333333, 0.66666666666666663, 0.0]]

        >>> analysis.center_of_mass()
        [[1.8, 2.2999999999999998, 0.0],
         [1.3333333333333333, 0.66666666666666663, 0.0],
         [1.5, 4.5, 0.0],
         [3.0, 3.0, 0.0],
         [1.0, 2.0, 0.0],
         [1.0, 1.0, 0.0],
         [0.75, 2.75, 0.0]]
        """
        if labels is None:
            labels = self.labels()

        # img_as_float = self.image.astype(np.float)
        # center = nd.center_of_mass(img_as_float, img_as_float, index=labels)

        center = np.array(nd.center_of_mass(self.image, self.image, index=labels))

        if real is True:
            center = np.multiply(center,self.image.resolution)
        return self.convert_return(center, labels)


    def boundingbox(self, labels = None, real = False):
        """
        Return the bounding box of a label.

        :Examples:

        >>> import numpy as np
        >>> a = np.array([[1, 2, 7, 7, 1, 1],
                          [1, 6, 5, 7, 3, 3],
                          [2, 2, 1, 7, 3, 3],
                          [1, 1, 1, 4, 1, 1]])

        >>> from openalea.image.algo.analysis import SpatialImageAnalysis
        >>> analysis = SpatialImageAnalysis(a)

        >>> analysis.boundingbox(7)
        (slice(0, 3), slice(2, 4), slice(0, 1))

        >>> analysis.boundingbox([7,2])
        [(slice(0, 3), slice(2, 4), slice(0, 1)), (slice(0, 3), slice(0, 2), slice(0, 1))]

        >>> analysis.boundingbox()
        [(slice(0, 4), slice(0, 6), slice(0, 1)),
        (slice(0, 3), slice(0, 2), slice(0, 1)),
        (slice(1, 3), slice(4, 6), slice(0, 1)),
        (slice(3, 4), slice(3, 4), slice(0, 1)),
        (slice(1, 2), slice(2, 3), slice(0, 1)),
        (slice(1, 2), slice(1, 2), slice(0, 1)),
        (slice(0, 3), slice(2, 4), slice(0, 1))]
        """
        if self._bbox is None:
            self._bbox = nd.find_objects(self.image)
        if labels is None:
            if real: return [real_indices(bbox,self.image.resolution) for bbox in self._bbox]
            else :   return self._bbox

        # bbox of object labelled 1 to n are stored into self._bbox. To access i-th element, we have to use i-1 index
        if isinstance (labels, list):
            bboxes = [self._bbox[i-1] for i in labels]
            if real : return [real_indices(bbox,self.image.resolution) for bbox in bboxes]
            else : return bboxes

        else :
            try:
                if real:  return real_indices(self._bbox[labels-1],self.image.resolution)
                else : return self._bbox[labels-1]
            except:
                return None


    def neighbors(self, labels=None, **kwd ):
        """
        Return the list of neighbors of a label.

        :Examples:

        >>> import numpy as np
        >>> a = np.array([[1, 2, 7, 7, 1, 1],
                          [1, 6, 5, 7, 3, 3],
                          [2, 2, 1, 7, 3, 3],
                          [1, 1, 1, 4, 1, 1]])

        >>> from openalea.image.algo.analysis import SpatialImageAnalysis
        >>> analysis = SpatialImageAnalysis(a)

        >>> analysis.neighbors(7)
        [1, 2, 3, 4, 5]

        >>> analysis.neighbors([7,2])
        {7: [1, 2, 3, 4, 5], 2: [1, 6, 7] }

        >>> analysis.neighbors()
        {1: [2, 3, 4, 5, 6, 7],
         2: [1, 6, 7],
         3: [1, 7],
         4: [1, 7],
         5: [1, 6, 7],
         6: [1, 2, 5],
         7: [1, 2, 3, 4, 5] }
        """
        if labels is None:
            return self._all_neighbors()
        elif not isinstance (labels , list):
            return self._neighbors_with_mask(labels)
        else:
            return self._neighbors_from_list_with_mask(labels)

    def _neighbors_with_mask(self,label):
        if not self._neighbors is None:
            return self._neighbors[label] 

        slices = self.boundingbox(label)

        ex_slices = dilation(slices)
        mask_img = self.image[ex_slices]
        return list(contact_surface(mask_img,label))

    def _neighbors_from_list_with_mask(self,labels):
        if not self._neighbors is None:
            return dict([(i,self._neighbors[i]) for i in labels])

        edges = {}
        for label in labels:

            slices = self.boundingbox(label)

            if slices is None: continue

            ex_slices = dilation(slices)
            mask_img = self.image[ex_slices]

            neigh = list(contact_surface(mask_img,label))

            edges[label]=neigh

        return edges

    def _all_neighbors(self):
        if not self._neighbors is None:
            return self._neighbors

        edges = {} # store src, target

        slice_label = self.boundingbox()
        for label, slices in enumerate(slice_label):
            # label_id = label +1 because the label_id begin at 1
            # and the enumerate begin at 0.
            label_id = label+1

            # sometimes, the label doesn't exist ans slices is None
            if slices is None:
               continue

            ex_slices = dilation(slices)
            mask_img = self.image[ex_slices]
            neigh = list(contact_surface(mask_img,label_id))

            edges[label_id]=neigh

        self._neighbors = edges
        return edges


    def neighbor_kernels(self):
        if self._kernels is None:
            if self.is3D():
                X1kernel = np.zeros((3,3,3),np.bool)
                X1kernel[:,1,1] = True
                X1kernel[0,1,1] = False
                X2kernel = np.zeros((3,3,3),np.bool)
                X2kernel[:,1,1] = True
                X2kernel[2,1,1] = False
                Y1kernel = np.zeros((3,3,3),np.bool)
                Y1kernel[1,:,1] = True
                Y1kernel[1,0,1] = False
                Y2kernel = np.zeros((3,3,3),np.bool)
                Y2kernel[1,:,1] = True
                Y2kernel[1,2,1] = False
                Z1kernel = np.zeros((3,3,3),np.bool)
                Z1kernel[1,1,:] = True
                Z1kernel[1,1,0] = False
                Z2kernel = np.zeros((3,3,3),np.bool)
                Z2kernel[1,1,:] = True
                Z2kernel[1,1,2] = False
                self._kernels = (X1kernel,X2kernel,Y1kernel,Y2kernel,Z1kernel,Z2kernel)
            else:
                X1kernel = np.zeros((3,3),np.bool)
                X1kernel[:,1] = True
                X1kernel[0,1] = False
                X2kernel = np.zeros((3,3),np.bool)
                X2kernel[:,1] = True
                X2kernel[2,1] = False
                Y1kernel = np.zeros((3,3),np.bool)
                Y1kernel[1,:] = True
                Y1kernel[1,0] = False
                Y2kernel = np.zeros((3,3),np.bool)
                Y2kernel[1,:] = True
                Y2kernel[1,2] = False
                self._kernels = (X1kernel,X2kernel,Y1kernel,Y2kernel)
                
        return self._kernels


    def get_voxel_face_surface(self):
        a = self.image.resolution
        if len(a)==3:
            return np.array([a[1] * a[2],a[2] * a[0],a[0] * a[1] ])
        if len(a)==2:
            return np.array([a[0],a[1]])


    def wall_voxels(self, label_1, label_2):
        """
        Return the voxels coordinates defining the contact wall between two labels.

        :Parameters:
            - `label_1` cell id #1.
            - `label_2` cell id #2.

        :Return:
            -`coord` a dictionnary of *keys= (labels_1,label_2); *values= xyz 3xN array.
        """
        # -- We first make sure that labels are neighbors:
        if label_2 not in self.neighbors(label_1):
            warnings.warn("You got it wrong dude,"+str(label_1)+"and"+str(label_2)+"are not neighbors!!")

        dilated_bbox = dilation( self.boundingbox(label_1) )
        dilated_bbox_img = self.image[dilated_bbox]

        mask_img_1 = (dilated_bbox_img == label_1)
        mask_img_2 = (dilated_bbox_img == label_2)

        struct = nd.generate_binary_structure(3, 1)

        dil_1 = nd.binary_dilation(mask_img_1, structure=struct)
        dil_2 = nd.binary_dilation(mask_img_2, structure=struct)
        x,y,z = np.where( ( (dil_1 & mask_img_2) | (dil_2 & mask_img_1) ) == 1 )
        
        coord={}
        coord[min(label_1,label_2),max(label_1,label_2)]=np.array((x+dilated_bbox[0].start,y+dilated_bbox[1].start,z+dilated_bbox[2].start))

        return coord


    def all_wall_voxels(self, label_1, verbose = False):
        """
        Return the voxels coordinates defining the contact wall between two labels, the given one and its neighbors.

        :Parameters:
            - `label_1` cell id #1.

        :Return:
            -`coord` a dictionnary of *keys= [min(labels_1,neighbors[n]), max(labels_1,neighbors[n])]; *values= xyz 3xN array.
        """
        coord={}
        
        dilated_bbox = dilation( self.boundingbox(label_1) )
        dilated_bbox_img = self.image[dilated_bbox]

        mask_img_1 = (dilated_bbox_img == label_1)
        struct = nd.generate_binary_structure(3, 1)
        dil_1 = nd.binary_dilation(mask_img_1, structure=struct)

        neighbors=self.neighbors(label_1)
        if 0 in neighbors: neighbors.remove(0)
        len_neighbors=len(neighbors)
        if verbose: print 'Extracting cell walls coordinates between',label_1,'and its neighbors:',neighbors
        for n,label_2 in enumerate(neighbors):
            if verbose and (label_1!=1) and n%2==0: print n,'/',len_neighbors
            if label_1 == 1:
                dilated_bbox_2 = dilation( self.boundingbox(label_2) )
                #~ dilated_bbox_img_2 = self.image[dilated_bbox_2]
                #~ mask_img_2 = (dilated_bbox_img_2 == label_2)
                #~ dil_2 = nd.binary_dilation(mask_img_2, structure=struct)
                #~ x,y,z = np.where( ( (dil_1[dilated_bbox_2] & mask_img_2) | (dil_2 & mask_img_1[dilated_bbox_2]) ) == 1 )
                x,y,z = np.where( self.image[dilated_bbox_2]*dil_1[dilated_bbox_2] == label_2 )
                coord[1,label_2]=np.array((x+dilated_bbox_2[0].start,y+dilated_bbox_2[1].start,z+dilated_bbox_2[2].start))
            else:
                mask_img_2 = (dilated_bbox_img == label_2)
                dil_2 = nd.binary_dilation(mask_img_2, structure=struct)
                x,y,z = np.where( ( (dil_1 & mask_img_2) | (dil_2 & mask_img_1) ) == 1 )
                coord[min(label_1,label_2),max(label_1,label_2)]=np.array((x+dilated_bbox[0].start,y+dilated_bbox[1].start,z+dilated_bbox[2].start))

        return coord


    def cell_wall_surface( self, label_id, neighbors, real = True):
        """
        Return the surface of contact between a label and its neighbors.
        A list or a unique id can be given as neighbors.

        :Examples:

        >>> import numpy as np
        >>> a = np.array([[1, 2, 7, 7, 1, 1],
                          [1, 6, 5, 7, 3, 3],
                          [2, 2, 1, 7, 3, 3],
                          [1, 1, 1, 4, 1, 1]])

        >>> from openalea.image.algo.analysis import SpatialImageAnalysis
        >>> analysis = SpatialImageAnalysis(a)

        >>> analysis.cell_wall_surface(7,2)
        1.0
        >>> analysis.cell_wall_surface(7,[2,5])
        {(2, 7): 1.0, (5, 7): 2.0}
        """

        resolution = self.get_voxel_face_surface()
        dilated_bbox =  dilation(self.boundingbox(label_id))
        dilated_bbox_img = self.image[dilated_bbox]

        mask_img = (dilated_bbox_img == label_id)

        xyz_kernels = self.neighbor_kernels()

        unique_neighbor = not isinstance(neighbors,list)
        if unique_neighbor:
            neighbors = [neighbors]

        wall = {}
        for a in xrange(len(xyz_kernels)):
            dil = nd.binary_dilation(mask_img, structure=xyz_kernels[a])
            frontier = dilated_bbox_img[dil-mask_img]

            for n in neighbors:
                nb_pix = len(frontier[frontier==n])
                if real:  surface = float(nb_pix*resolution[a//2])
                else : surface = nb_pix
                i,j = min(label_id,n), max(label_id,n)
                wall[(i,j)] = wall.get((i,j),0.0) + surface

        if unique_neighbor: return wall.itervalues().next()
        else : return wall


    def wall_surfaces(self, neighbors = None, real = True):
        """
        Return the surface of contact between all neighbor labels.
        If neighbors is not given, it is computed first.

        :Examples:

        >>> import numpy as np
        >>> a = np.array([[1, 2, 7, 7, 1, 1],
                          [1, 6, 5, 7, 3, 3],
                          [2, 2, 1, 7, 3, 3],
                          [1, 1, 1, 4, 1, 1]])

        >>> from openalea.image.algo.analysis import SpatialImageAnalysis
        >>> analysis = SpatialImageAnalysis(a)

        >>> analysis.wall_surfaces({ 1 : [2, 3], 2 : [6] })
       {(1, 2): 5.0, (1, 3): 4.0, (2, 6): 2.0 }

        >>> analysis.wall_surfaces()
        {(1, 2): 5.0, (1, 3): 4.0, (1, 4): 2.0, (1, 5): 1.0, (1, 6): 1.0, (1, 7): 2.0, (2, 6): 2.0, (2, 7): 1.0, (3, 7): 2, (4, 7): 1, (5, 6): 1.0, (5, 7): 2.0 }
        """
        if neighbors is None : neighbors = self._all_neighbors()
        surfaces = {}
        for label_id, lneighbors in neighbors.iteritems():
            # To avoid computing 2 times the same wall surface, we select wall between i and j with j > i.
            neigh = [n for n in lneighbors if n > label_id]
            if len(neigh) > 0:
                lsurfaces = self.cell_wall_surface(label_id, neigh, real = real)
                for i,j in lsurfaces.iterkeys():
                    surfaces[(i,j)] = surfaces.get((i,j),0.0) + lsurfaces[(i,j)]
        return surfaces 


    #~ def __L1(self, background = 1):
        #~ return self.neighbors(background)
    def __layer1(self, background = 1):
        return list( set(self.neighbors(background))-self._ignoredlabels )

    #~ def L1(self, background = 1):
        #~ if self._L1 is None : self._L1 = self.__L1(background)
        #~ if 0 in self._L1: self._L1.remove(0)
        #~ return self._L1
    def layer1(self, background = 1):
        """
        Extract a list of labels corresponding to a layer of cell.
        It start from the cell in contact with the outer surface to the inner parts of the segemented tissu.
        """
        if self._layer1 is None :
            self._layer1 = self.__layer1(background)
        return self._layer1


    def __first_voxel_layer(self, background = 1, keep_background = True):
        """
        Extract the first layer of voxels at the surface of the biological object.
        """
        print "Extracting the first layer of voxels..."
        mask_img_1 = (self.image == 1)
        struct = nd.generate_binary_structure(3, 1)
        dil_1 = nd.binary_dilation(mask_img_1, structure=struct)
        
        layer = dil_1 - mask_img_1
        
        if keep_background:
            return self.image * layer + mask_img_1
        else:
            return self.image * layer

    def first_voxel_layer(self, background = 1, keep_background = False):
        """
        Function extracting the first layer of voxels detectable from the outer surface.
        """
        if self._first_voxel_layer is None :
            self._first_voxel_layer = self.__first_voxel_layer(background, keep_background)
        return self._first_voxel_layer


    def remove_cells(self, vids, erase_value = 0, verbose = True):
        """
        Use remove_cell to iterate over a list of cell to remove if there is more cells to keep than to remove.
        If there is more cells to remove than to keep, we fill a "blank" image with those to keep.
        !!!!WARNING!!!!
        This function modify the SpatialImage on self.image
        !!!!WARNING!!!!
        """

        if isinstance(vids,int):
            vids= [vids]

        try:
            isinstance(vids,list)
        except TypeError:
            return None

        N=len(vids)
        if verbose: print "Removing", N, "cells."
        for n, vid in enumerate(vids):
            if verbose and n%20 == 0: print n,'/',N
            xyz = np.where( (self.image[self.boundingbox(vid)]) == vid )
            self.image[tuple((xyz[0]+self.boundingbox(vid)[0].start, xyz[1]+self.boundingbox(vid)[1].start, xyz[2]+self.boundingbox(vid)[2].start))]=erase_value

        self.__init__(self.image)

        if verbose: print 'Done !!'


    def remove_margins_cells(self, erase_value = 0, verbose = False):
        """
        !!!!WARNING!!!!
        This function modify the SpatialImage on self.image
        !!!!WARNING!!!!
        Function removing cells at the margins, because most probably cut during stack aquisition.
        
        :INPUTS:
            .save: text (if present) indicating under which name to save the Spatial Image containing the cells of the first layer;
            .display: boolean indicating if we should display the previously computed image;
        
        :OUPUT:
            Spatial Image without the cell's at the margins.
        """
        
        if verbose: print "Removing cells at the margins of the stack..."

        # -- We start by making sure that there is not only one cell in the image (appart from 0 and 1)
        labels = copy.copy(list(self.labels()))
        if 0 in labels: labels.remove(0)
        if 1 in labels: labels.remove(1)
        if len(labels)==1:
            warnings.warn("Only one cell left in your image, we won't take it out !")
            return self.__init__(self.image)

        # -- Then we recover the list of border cells and delete the from the image:
        cells_in_image_margins = self.cells_in_image_margins()
        if 0 in cells_in_image_margins: cells_in_image_margins.remove(0)
        if 1 in cells_in_image_margins: cells_in_image_margins.remove(1)
        N = len(cells_in_image_margins)
        for n,c in enumerate(cells_in_image_margins):
            if verbose and n%20 == 0: print n,'/',N
            xyz = np.where( (self.image[self.boundingbox(c)]) == c )
            self.image[tuple((xyz[0]+self.boundingbox(c)[0].start,xyz[1]+self.boundingbox(c)[1].start,xyz[2]+self.boundingbox(c)[2].start))]=erase_value
        
        if verbose: print 'Done !!'
        
        self.__init__(self.image)


class SpatialImageAnalysis2D (AbstractSpatialImageAnalysis):
    """
    Class dedicated to 2D objects.
    """
    
    def __init__(self, image, ignoredlabels = [], return_type = NPLIST):
        AbstractSpatialImageAnalysis.__init__(self, image, ignoredlabels, return_type)


    def cells_in_image_margins(self):
        """
        Return a list of cells in contact with the margins of the stack (SpatialImage).
        
        :Parameters:
         - `update_ignoredlabels` (boolean) - if True it will update the list of cell labels to ignore when computing properties.
        """
        margins = set()
        for l in [np.unique(self.image[0,:]),np.unique(self.image[-1,:]),np.unique(self.image[:,0]),np.unique(self.image[:,-1])]:
            margins.update(l)

        return list(margins)

    def inertia_axis(self, labels = None, center_of_mass = None, real = True):
        """
        Return the inertia axis of cells, also called the shape main axis.
        Returns 2 (2D-oriented) vectors and 2 (length) values.
        """
        unique_label = False
        if labels is None : labels = self.labels()
        elif not isinstance(labels,list) :
            labels = [labels]
            unique_label = True

        # results
        inertia_eig_vec = []
        inertia_eig_val = []

        # if center of mass is not specified
        if center_of_mass is None:
            center_of_mass = self.center_of_mass(labels)
        for i,label in enumerate(labels):
            slices = self.boundingbox(label)
            if len(labels) == 1:
                center = center_of_mass
            elif isinstance(center_of_mass, dict):
                center = center_of_mass[label]
            else:
                center = center_of_mass[i]
            # project center into the slices sub_image coordinate
            for i,slice in enumerate(slices):
                center[i] = center[i] - slice.start
            label_image = (self.image[slices] == label)

            # compute the indices of voxel with adequate label
            x,y = label_image.nonzero()

            # difference with the center
            x = x - center[0]
            y = y - center[1]
            coord = np.array([x,y])

            # compute P.P^T
            cov = np.dot(coord,coord.T)

            # Find the eigen values and vectors.
            eig_val, eig_vec = np.linalg.eig(cov)

            inertia_eig_vec.append(eig_vec)

            if real:
                for i in xrange(2):
                    eig_val[i] *= np.linalg.norm( np.multiply(eig_vec[i],self.image.resolution) )

            inertia_eig_val.append(eig_val)

        if unique_label :
            return inertia_eig_vec[0], inertia_eig_val[0]
        else:
            return inertia_eig_vec, inertia_eig_val



class SpatialImageAnalysis3DS (AbstractSpatialImageAnalysis):
    """
    Class dedicated to surfacic 3D objects. 
    Only one layer of voxel is extracted (representing the external envelope of the biological object to analyse).
    """
    
    def __init__(self, image, ignoredlabels = [], return_type = NPLIST):
        AbstractSpatialImageAnalysis.__init__(self, image, ignoredlabels, return_type)



class SpatialImageAnalysis3D(AbstractSpatialImageAnalysis):
    """
    Class dedicated to 3D objects.
    """

    def __init__(self, image, ignoredlabels = [], return_type = NPLIST):
        AbstractSpatialImageAnalysis.__init__(self, image, ignoredlabels, return_type)
        self._first_voxel_layer = None
        self.principal_curvatures = {}
        self.principal_curvatures_normal = {}
        self.principal_curvatures_directions = {}
        self.principal_curvatures_origin = {}
        self.curvatures_tensor = {}
        self.external_wall_geometric_median = {}

    def is3D(self): return True
    
    def volume(self, labels = None, real = True):
        """
        Return the volume of the labels.

        :Parameters:
         - `labels` (int) - single label number or a sequence of
            label numbers of the objects to be measured.
            If labels is None, all labels are used.

         - `real` (bool) - If real = True, volume is in real-world units else in voxels.

        :Examples:

        >>> import numpy as np
        >>> a = np.array([[1, 2, 7, 7, 1, 1],
                          [1, 6, 5, 7, 3, 3],
                          [2, 2, 1, 7, 3, 3],
                          [1, 1, 1, 4, 1, 1]])

        >>> from openalea.image.algo.analysis import SpatialImageAnalysis
        >>> analysis = SpatialImageAnalysis(a)

        >>> analysis.volume(7)
        4.0

        >>> analysis.volume([7,2])
        [4.0, 3.0]

        >>> analysis.volume()
        [10.0, 3.0, 4.0, 1.0, 1.0, 1.0, 4.0]
        """
        if labels is None:
            labels  = self.labels()

        volume = nd.sum(np.ones_like(self.image), self.image, index=np.int16(labels))

        if real is True:
            if self.image.ndim == 2:
                volume = np.multiply(volume,(self.image.resolution[0]*self.image.resolution[1]))
            elif self.image.ndim == 3:
                volume = np.multiply(volume,(self.image.resolution[0]*self.image.resolution[1]*self.image.resolution[2]))
            volume.tolist()
        
        if not isinstance(labels, int):
            return self.convert_return(volume, labels)
        else:
            return volume


    def inertia_axis(self, labels = None, center_of_mass = None, real = True):
        """
        Return the inertia axis of cells, also called the shape main axis.
        Return 3 (3D-oriented) vectors and 3 (length) values.
        """
        unique_label = False
        if labels is None : labels = self.labels()
        elif not isinstance(labels,list) :
            labels = [labels]
            unique_label = True

        # results
        inertia_eig_vec = []
        inertia_eig_val = []

        # if center of mass is not specified
        if center_of_mass is None:
            center_of_mass = self.center_of_mass(labels)
        for i,label in enumerate(labels):
            slices = self.boundingbox(label)
            if len(labels) == 1:
                center = center_of_mass
            elif isinstance(center_of_mass, dict):
                center = center_of_mass[label]
            else:
                center = center_of_mass[i]
            # project center into the slices sub_image coordinate
            for i,slice in enumerate(slices):
                center[i] = center[i] - slice.start
            label_image = (self.image[slices] == label)

            # compute the indices of voxel with adequate label
            x,y,z = label_image.nonzero()

            # difference with the center
            x = x - center[0]
            y = y - center[1]
            z = z - center[2]
            coord = np.array([x,y,z])

            # compute P.P^T
            cov = np.dot(coord,coord.T)

            # Find the eigen values and vectors.
            eig_val, eig_vec = np.linalg.eig(cov)

            inertia_eig_vec.append(eig_vec)

            if real:
                for i in xrange(3):
                    eig_val[i] *= np.linalg.norm( np.multiply(eig_vec[i],self.image.resolution) )

            inertia_eig_val.append(eig_val)

        if unique_label :
            return inertia_eig_vec[0], inertia_eig_val[0]
        else:
            return inertia_eig_vec, inertia_eig_val


    def cells_in_image_margins(self):
        """
        Return a list of cells in contact with the margins of the stack (SpatialImage).
        """
        margins = set()
        for l in [np.unique(self.image[0,:,:]),np.unique(self.image[-1,:,:]),np.unique(self.image[:,0,:]),np.unique(self.image[:,-1,:])]:
            margins.update(l)

        margins.update(np.unique(self.image[:,:,0]))
        margins.update(np.unique(self.image[:,:,-1]))

        return list(margins)


    def __principal_curvature_parameters_CGAL(func):
        def wrapped_function(self, vids = None, radius = 60, fitting_degree = 2, monge_degree = 2, background = 1, verbose = False):
            """
            Decorator wrapping function `compute_principal_curvatures` allowing use of various input for `vids` and preparing the necessary variables for the wrapped function.
            """
            # -- If 'vids' is an integer... 
            if isinstance(vids,int):
                if (vids not in self.layer1()): # - ...but not in the L1 list, there is nothing to do!
                    warnings.warn("Cell "+str(vids)+" is not in the L1. We won't compute it's curvature.")
                    return 0
                else: # - ... and in the L1 list, we make it iterable.
                    vids=[vids]

            # -- If 'vids' is a list, we make sure to keep only its 'vid' present in the L1 list!
            if isinstance(vids,list):
                tmp = copy.deepcopy(vids) # Ensure to scan all the elements of 'vids'
                for vid in tmp:
                    if vid not in self.layer1():
                        warnings.warn("Cell "+str(vid)+" is not in the L1. We won't compute it's curvature.")
                        vids.remove(vid)
                if len(vids) == 0: # if there is no element left in the 'vids' list, there is nothing to do!
                    warnings.warn('None of the cells you provided bellonged to the L1.')
                    return 0

            # -- If 'vids' is `None`, we apply the function to all L1 cells:
            if vids == None:
                vids = self.layer1()

            # -- Now we need the SpatialImage of the first layer of voxels without the background.
            if self._first_voxel_layer == None:
                self.first_voxel_layer(background, keep_background = False)
            else:
                # - If the first layer of voxels has been extracted already, we make sure that we have exluded the background.
                if background in self._first_voxel_layer:
                    self._first_voxel_layer[self._first_voxel_layer == background]=0

            # -- We make sure the radius hasn't been changed and if not defined, we save the value for further evaluation and information.
            try:
                self.used_radius_for_curvature
            except:
                self.used_radius_for_curvature = radius
                recalculate_all = True
            else:
                if self.used_radius_for_curvature == radius:
                    recalculate_all = False
                else:
                    recalculate_all = True

            # -- We create voxels adjacencies
            curvature={}
            x,y,z = np.where(self.first_voxel_layer() != 0)
            pts = [tuple([int(x[i]),int(y[i]),int(z[i])]) for i in xrange(len(x))]
            from openalea.plantgl.all import k_closest_points_from_ann
            adjacencies = k_closest_points_from_ann(pts, k=10)

            # -- Now we can compute the principal curvatures informations
            from openalea.image.algo.analysis import geometric_median
            if verbose: print 'Computing curvature :'
            for n,vid in enumerate(vids):
                if (recalculate_all) or (not self.principal_curvatures.has_key(vid)):
                    if verbose: print n,'/',len(vids)
                    func( self, vid, pts, adjacencies, fitting_degree, monge_degree )

        return wrapped_function


    @__principal_curvature_parameters_CGAL
    def compute_principal_curvatures( self, vid, pts, adjacencies, fitting_degree, monge_degree ):
        """
        Function computing principal curvature using a CGAL c++ wrapped function: 'principal_curvatures'.
        It's only doable for cells of the first layer.
        """
        from openalea.plantgl.all import (r_neighborhood,
                                          principal_curvatures)

        x_vid, y_vid, z_vid = np.where(self.first_voxel_layer() == vid)

        if self.external_wall_geometric_median.has_key(vid):
            neighborhood_origin = self.external_wall_geometric_median[vid]
        else:
            neighborhood_origin = geometric_median( np.array([list(x_vid),list(y_vid),list(z_vid)]) )
            self.external_wall_geometric_median[vid] = neighborhood_origin

        integers = np.vectorize(lambda x : int(x))
        neighborhood_origin = integers(neighborhood_origin)
        pts_vid = [tuple([int(x_vid[i]),int(y_vid[i]),int(z_vid[i])]) for i in xrange(len(x_vid))]

        min_dist = closest_from_A(neighborhood_origin, pts_vid)
        id_min_dist = pts.index(min_dist)

        neigborids = r_neighborhood(id_min_dist, pts, adjacencies, self.used_radius_for_curvature)

        neigbor_pts=[]
        for i in neigborids:
            neigbor_pts.append(pts[i])

        #~ pc = principal_curvatures(pts,id_min_dist,neigborids)
        pc = principal_curvatures(pts,id_min_dist,neigborids, fitting_degree, monge_degree)
        k1 = pc[1][1]
        k2 = pc[2][1]
        self.principal_curvatures[vid] = [k1, k2]
        self.principal_curvatures_normal[vid] = pc[3]
        self.principal_curvatures_directions[vid] = [pc[1][0], pc[2][0]]
        self.principal_curvatures_origin[vid] = pc[0]
        R = np.array( [pc[1][0], pc[2][0], pc[0]] ).T
        D = [ [k1,0,0], [0,k2,0], [0,0,0] ]
        self.curvatures_tensor[vid] = np.dot(np.dot(R,D),R.T)

    def __curvature_parameters_CGAL(func):
        def wrapped_function(self, vids = None, verbose = False):
            """
            """
            # -- If 'vids' is `None`, we apply the function to all L1 cells:
            if vids == None:
                vids = self.layer1()

            # -- If 'vids' is an integer... 
            if isinstance(vids,int):
                if (vids not in self.layer1()): # - ...but not in the L1 list, there is nothing to do!
                    warnings.warn("Cell"+str(vids)+"is not in the L1. We won't compute it's curvature.")
                    return 0
                else: # - ... and in the L1 list, we make it iterable.
                    vids=[vids]

            try:
                self.principal_curvatures
            except:
                warnings.warn('Principal curvature not defined...')
                self.compute_principal_curvatures(vids, verbose = True)

            curvature = {}
            for vid in vids:
                if not self.principal_curvatures.has_key(vid):
                    c = self.compute_principal_curvatures(vid)
                else:
                    c = self.principal_curvatures[vid]
                if c != 0: # 'compute_principal_curvatures' return a 0 when one of the vids is not in the L1.
                    curvature[vid] = func( self, vid )

            return curvature
        return wrapped_function


    @__curvature_parameters_CGAL
    def gaussian_curvature_CGAL( self, vid ):
        """
        Gaussian curvature is the product of principal curvatures 'k1*k2'.
        """
        return self.principal_curvatures[vid][0] * self.principal_curvatures[vid][1]

    @__curvature_parameters_CGAL
    def mean_curvature_CGAL( self, vid ):
        """
        Mean curvature is the product of principal curvatures '1/2*(k1+k2)'.
        """
        return 0.5*(self.principal_curvatures[vid][0] + self.principal_curvatures[vid][1])

    @__curvature_parameters_CGAL
    def curvature_ratio_CGAL( self, vid ):
        """
        Curvature ratio is the ratio of principal curvatures 'k1/k2'.
        """
        return float(self.principal_curvatures[vid][0])/float(self.principal_curvatures[vid][1])

    @__curvature_parameters_CGAL
    def curvature_anisotropy_CGAL( self, vid ):
        """
        Curvature Anisotropy is defined as '(k1-k2)/(k1+k2)'.
        Where k1 is the max value of principal curvature and k2 the min value.
        """
        return float(self.principal_curvatures[vid][0] - self.principal_curvatures[vid][1])/float(self.principal_curvatures[vid][0] + self.principal_curvatures[vid][1])


    def moment_invariants(self, vids = None, order = [], verbose = True):
        """
        Calcul of 3D invariant moment to translation, rotation and scale.
        
        2nd order moments are calculated from:
         - Sadjadi, F. A. & Hall, E. L. Three-Dimensional Moment Invariants. IEEE Transactions on Pattern Analysis and Machine Intelligence, 1980, PAMI-2, 127-136.
        
        3rd and 4th order moments are calculated from:
         - Xu, D. & Li, H. Geometric moment invariants. Pattern Recognition, 2008, 41, 240-249 
        """
        # -- If 'vids' is an integer... 
        if isinstance(vids,int):
            vids=[vids]

        # -- If 'vids' is `None`, we apply the function to all L1 cells:
        if vids == None:
            vids = self.labels()

        central_moments = {}
        I1, I2, I3, I4, I5, I6 = {}, {}, {}, {}, {}, {}

        usefull_combinations = [ [4, 0, 0], [0, 4, 0], [0, 0, 4], [2, 2, 0], [2, 0, 2], [0, 2, 2], [0, 0, 0], \
        [1, 0, 3], [3, 0, 1], [1, 3, 0], [3, 1, 0], [0, 1, 3], [0, 3, 1], [1, 2, 1], \
        [1, 1, 2], [2, 1, 1], [3, 0, 0], [0, 3, 0], [0, 0, 3], [1, 2, 0], [1, 0, 2], \
        [0, 1, 2], [2, 1, 0], [0, 2, 1], [2, 0, 1], [1, 1, 1], [2, 0, 0], [0, 2, 0], \
        [0, 0, 2], [1, 1, 0], [1, 0, 1], [0, 1, 1] ]

        for n,vid in enumerate(vids):
            if verbose and n%5 == 0: print "Cell #",n,"/",len(vids)
            x,y,z = np.where( (self.image[self.boundingbox(vid)]) == vid )
            x_mean,y_mean,z_mean = self.center_of_mass(vid,False)
            x_res, y_res, z_res = self.image.resolution

            x_bar = x+self.boundingbox(vid)[0].start-x_mean
            y_bar = y+self.boundingbox(vid)[1].start-y_mean
            z_bar = z+self.boundingbox(vid)[2].start-z_mean

            #~ for l in xrange(5):
                #~ for m in xrange(5):
                    #~ for n in xrange(5):
                        #~ central_moments[l,m,n] = sum( (x_bar*x_res)**l * (y_bar*y_res)**m * (z_bar*z_res)**n )
            for l, m, n in usefull_combinations:
                central_moments[l,m,n] = sum( (x_bar*x_res)**l * (y_bar*y_res)**m * (z_bar*z_res)**n )

            I1[vid] = ( 1/(central_moments[0,0,0])**(7/3) ) * \
             ( central_moments[4,0,0] + central_moments[0,4,0] + central_moments[0,0,4] + 2*central_moments[2,2,0] + 2*central_moments[2,0,2] + 2*central_moments[0,2,2] )

            I2[vid] = ( 1/(central_moments[0,0,0])**(14/3) ) * \
             ( central_moments[4,0,0]*central_moments[0,4,0] + central_moments[4,0,0]*central_moments[0,0,4] + central_moments[0,0,4]*central_moments[0,4,0] \
             + 3*central_moments[2,2,0]**2 + 3*central_moments[2,0,2]**2 + 3*central_moments[0,2,2]**2 \
             - 4*central_moments[1,0,3]*central_moments[3,0,1] - 4*central_moments[1,3,0]*central_moments[3,1,0] - 4*central_moments[0,1,3]*central_moments[0,3,1] \
             + 2*central_moments[0,2,2]*central_moments[2,0,2] + 2*central_moments[0,2,2]*central_moments[2,2,0] + 2*central_moments[2,2,0]*central_moments[2,0,2] \
             + 2*central_moments[0,2,2]*central_moments[4,0,0] + 2*central_moments[0,0,4]*central_moments[2,2,0] + 2*central_moments[0,4,0]*central_moments[2,0,2] \
             - 4*central_moments[1,0,3]*central_moments[1,2,1] - 4*central_moments[1,3,0]*central_moments[1,1,2] - 4*central_moments[0,1,3]*central_moments[2,1,1] \
             - 4*central_moments[1,2,1]*central_moments[3,0,1] - 4*central_moments[1,1,2]*central_moments[3,1,0] - 4*central_moments[2,1,1]*central_moments[0,3,1] \
             + 4*central_moments[2,1,1]**2 + 4*central_moments[1,1,2]**2 + 4*central_moments[1,2,1]**2 )

            I3[vid] = ( 1/(central_moments[0,0,0])**(14/3) ) * \
             ( central_moments[4,0,0]**2 + central_moments[0,4,0]**2 + central_moments[0,0,4]**2 \
             + 4*central_moments[1,3,0]**2 + 4*central_moments[1,0,3]**2 + 4*central_moments[0,1,3]**2 + 4*central_moments[0,3,1]**2 + 4*central_moments[3,0,1]**2 \
             + 4*central_moments[3,0,1]**2 + 6*central_moments[2,2,0]**2 + 6*central_moments[2,0,2]**2 \
             + 6*central_moments[0,2,2]**2 + 12*central_moments[1,1,2]**2 + 12*central_moments[1,2,1]**2 + 12*central_moments[2,1,1]**2 )

            I4[vid] = ( 1/(central_moments[0,0,0])**4 ) * \
             ( central_moments[3,0,0]**2 + central_moments[0,3,0]**2 + central_moments[0,0,3]**2 + 3*central_moments[1,2,0]**2 + 3*central_moments[1,0,2]**2 \
             + 3*central_moments[0,1,2]**2 + 3*central_moments[2,1,0]**2 + 3*central_moments[0,2,1]**2 + 3*central_moments[2,0,1]**2 + 6*central_moments[1,1,1]**2 )

            I5[vid] = ( 1/(central_moments[0,0,0])**4 ) * \
             ( central_moments[3,0,0]**2 + central_moments[0,3,0]**2 + central_moments[0,0,3]**2 + central_moments[1,2,0]**2 + central_moments[1,0,2]**2 + central_moments[0,1,2]**2 + central_moments[2,1,0]**2 \
             + central_moments[0,2,1]**2 + central_moments[2,0,1]**2 + 2*central_moments[3,0,0]*central_moments[1,2,0] \
             + 2*central_moments[3,0,0]*central_moments[1,0,2] + 2*central_moments[1,2,0]*central_moments[1,0,2] + 2*central_moments[0,0,3]*central_moments[2,0,1] \
             + 2*central_moments[0,0,3]*central_moments[0,2,1] + 2*central_moments[0,2,1]*central_moments[2,0,1] + 2*central_moments[0,3,0]*central_moments[0,1,2] \
             + 2*central_moments[0,3,0]*central_moments[2,1,0] + 2*central_moments[0,1,2]*central_moments[2,1,0] )

            I6[vid] = ( 1/(central_moments[0,0,0])**4 ) * \
             ( central_moments[2,0,0]*(central_moments[4,0,0] + central_moments[2,2,0] + central_moments[2,0,2]) \
             + central_moments[0,2,0]*(central_moments[2,2,0] + central_moments[0,4,0] + central_moments[0,2,2]) \
             + central_moments[0,0,2]*(central_moments[2,0,2] + central_moments[0,2,2] + central_moments[0,0,4]) \
             + 2*central_moments[1,1,0]*(central_moments[3,1,0] + central_moments[1,3,0] + central_moments[1,1,2]) \
             + 2*central_moments[1,0,1]*(central_moments[3,0,1] + central_moments[1,2,1] + central_moments[1,0,3]) \
             + 2*central_moments[0,1,1]*(central_moments[2,1,1] + central_moments[0,3,1] + central_moments[0,1,3]) )

        return I1, I2, I3, I4, I5, I6


def load_analysis( SpatialImageAnalysis, filename ):
    """
    Load a SpatialImageAnalysis from the file `filename`.
    """
    f = gzip.open( str(filename) , 'rb')
    SpatialImageAnalysis = pickle.load( f )
    f.close()
    print "File " + str(filename) + ".pklz succesfully loaded !!"


def outliers_exclusion( data, std_multiplier = 3, display_data_plot = False):
    """
    Return a list or a dict (same type as `data`) cleaned out of outliers.
    Outliers are detected according to a distance from standard deviation.
    """
    from numpy import std,mean
    import copy
    tmp = copy.deepcopy(data)
    if isinstance(data,list):
        borne = mean(tmp) + std_multiplier*std(tmp)
        N = len(tmp)
        n=0
        while n < N:
            if (tmp[n]>borne) or (tmp[n]<-borne):
                tmp.pop(n)
                N = len(tmp)
            else:
                n+=1
    if isinstance(data,dict):
        borne = mean(tmp.values()) + std_multiplier*std(tmp.values())
        for n in data:
            if (tmp[n]>borne) or (tmp[n]<-borne):
                tmp.pop(n)
    if display_data_plot:
        import matplotlib.pyplot as plt
        if isinstance(data,list):
            plt.plot( data )
            plt.plot( tmp )
        plt.show()
        if isinstance(data,dict):
            plt.plot( data.values() )
            plt.plot( tmp.values() )
        plt.show()
    return tmp


def vector_correlation(vect1,vect2):
    """
    Compute correlation between two vector, which is the the cosine of the angle between two vectors in Euclidean space of any number of dimensions.
    The dot product is directly related to the cosine of the angle between two vectors if they are normed !!!
    """
    # -- We make sure that we have normed vectors.
    from openalea.plantgl.math import norm, Vector3
    if (np.round(norm(Vector3(vect1))) != 1.):
        vect1 = vect1/norm(Vector3(vect1))
    if (np.round(norm(Vector3(vect2))) != 1.):
        vect2 = vect2/norm(Vector3(vect2))

    return np.round(np.dot(vect1,vect2),3)


def geometric_median(X, numIter = 50):
    """
    Compute the geometric medians of cells according to the coordinates of their voxels.
    The geometric medians coordinates will be expressed in the Spatial Image reference system (not in real world metrics).
    We use the Weiszfeld's algorithm (http://en.wikipedia.org/wiki/Geometric_median)

    :Parameters:
        - `X` voxels coordinate (3xN matrix)
        - `numIter` limit the length of the search for global optimum
    
    :Return:
        - np.array((x,y,z)): geometric median of the coordinates;
    """
    # Initialising 'median' to the centroid
    y =(( np.mean(X[0]),np.mean(X[1]),np.mean(X[2]) ))
    convergence=False #boolean testing the convergence toward a global optimum
    dist=[] #list recording the distance evolution

    # Minimizing the sum of the squares of the distances between each points in 'X' (cells walls voxels) and the median.
    i=0
    while ( (not convergence) and (i < numIter) ):
        num_x, num_y, num_z = 0.0, 0.0, 0.0
        denum = 0.0
        m = X.shape[1]
        d = 0
        for j in range(0,m):
            div = math.sqrt( (X[0,j]-y[0])**2 + (X[1,j]-y[1])**2 + (X[2,j]-y[2])**2 )
            num_x += X[0,j] / div
            num_y += X[1,j] / div
            num_z += X[2,j] / div
            denum += 1./div
            d += div**2 #distance (to the median) to miminize
        dist.append(d) #update of the distance evolution
        
        if denum == 0.:
            warnings.warn("Couldn't compute a geometric median, please check your data!")
            return [0,0,0]
        
        y = [num_x/denum, num_y/denum, num_z/denum] #update to the new value of the median
        if i > 3:
            convergence=(abs(dist[i]-dist[i-2])<0.1) #we test the convergence over three steps for stability
            #~ print abs(dist[i]-dist[i-2]), convergence
        i += 1
    if i == numIter:
        warnings.warn("The Weiszfeld's algoritm did not converged after"+str(numIter)+"iterations for cell #"+str(c)+"!!!!!!!!!")
    #When convergence or iterations limit is reached we assume that we found the median.

    return np.array(y)


def SpatialImageAnalysis(image, *args, **kwd):
    """
    Constructeur. Detect automatically if the image is 2D or 3D.
    """
    #~ print args, kwd
    assert len(image.shape) in [2,3]
    
    # -- Check if the image is 2D
    if len(image.shape) == 2 or image.shape[2] == 1:
        return SpatialImageAnalysis2D(image, *args, **kwd)
    # -- Else it's considered as a 3D image.
    else:
        return SpatialImageAnalysis3D(image, *args, **kwd)


def read_id_list( filename, sep='\n' ):
    """
    Read a *.txt file containing a list of ids separated by `sep`.
    """
    f = open(filename, 'r')
    r = f.read()
    
    k = r.split(sep)
    
    list_cell = []
    for c in k:
        if c != '':
            list_cell.append(int(c))
    
    return list_cell


    #~ def display_curvature_cross(self, shadow_layer=False):
        #~ """
        #~ Display curvature cross
        #~ """
        #~ from enthought.mayavi import mlab
#~ 
        #~ origin = self.principal_curvatures_origin
        #~ directions = self.principal_curvatures_directions
        #~ k1 = dict([tuple([a,self.principal_curvatures[a][0]]) for a in self.principal_curvatures])
        #~ k2 = dict([tuple([a,self.principal_curvatures[a][1]]) for a in self.principal_curvatures])
#~ 
        #~ oriX=np.array([origin[a][0] for a in origin.keys()])
        #~ oriY=np.array([origin[a][1] for a in origin.keys()])
        #~ oriZ=np.array([origin[a][2] for a in origin.keys()])
        #~ dir1X=np.array([k1[a]*directions[a][0][0] for a in directions.keys()])
        #~ dir1Y=np.array([k1[a]*directions[a][0][1] for a in directions.keys()])
        #~ dir1Z=np.array([k1[a]*directions[a][0][2] for a in directions.keys()])
        #~ dir2X=np.array([k2[a]*directions[a][1][0] for a in directions.keys()])
        #~ dir2Y=np.array([k2[a]*directions[a][1][1] for a in directions.keys()])
        #~ dir2Z=np.array([k2[a]*directions[a][1][2] for a in directions.keys()])
#~ 
        #~ fig = mlab.figure(1, fgcolor=(1, 1, 1), bgcolor=(0, 0, 0), size=(800, 800))
        #~ if shadow_layer:
            #~ im = self.first_voxel_layer()
            #~ im[im==1] = 0
            #~ x_all,y_all,z_all = np.where(im != 0)
            #~ pts = mlab.points3d( x_all, y_all, z_all, mode = 'point', color = tuple([1.,1.,1.], figure = fig))
#~ 
        #~ obj = mlab.quiver3d(oriX, oriY, oriZ, dir1X, dir1Y, dir1Z, mode = '2ddash', line_width=3, figure = fig )
        #~ obj2 = mlab.quiver3d(oriX, oriY, oriZ, dir2X, dir2Y, dir2Z, mode = '2ddash',line_width=3, figure = fig )
#~ 
        #~ obj.glyph.glyph_source.glyph_source.center = [0, 0, 0]
        #~ obj2.glyph.glyph_source.glyph_source.center = [0, 0, 0]


    #~ def mask_intersection(self, vid, geometric_mask):
        #~ """
        #~ Create the intersection between a geometric_mask and de first layer of voxel of the image.
        #~ Used for curvature computation.
        #~ """
        #~ x_max, y_max, z_max = self.first_voxel_layer().shape
        #~ x_size, y_size, z_size = geometric_mask.shape
        #~ if (x_size >= x_max) or (y_size >= y_max) or (z_size >= z_max):
            #~ if verbose: print 'the size of the geometrical object is too big !!!'
            #~ return None
#~ 
        #~ from openalea.image.all import geometric_median
        #~ x, y, z = np.where(self.first_voxel_layer() == vid)
        #~ median = geometric_median( np.array([list(x),list(y),list(z)]) )
        #~ 
        #~ integers=np.vectorize(integer)
        #~ median = integers(median)
        #~ 
        #~ x_bar, y_bar, z_bar = integers(np.round(np.array(geometric_mask.shape)/2.))
        #~ # -- We create the mask (with extended border so the geometrical mask can be applied even if it's center is close from the margins of the image)
        #~ mask = np.zeros( tuple([x_max+x_size, y_max+y_size, z_max+z_size]) )
        #~ # -- We create the extended version of the image
        #~ image = copy.copy(mask)
        #~ image[ x_bar:x_max+x_bar,y_bar:y_max+y_bar,z_bar:z_max+z_bar ] = self.first_voxel_layer()
        #~ # -- We now add the geometric_mask to the mask
        #~ mask[median[0]:median[0]+x_size,median[1]:median[1]+y_size,median[2]:median[2]+z_size] = geometric_mask
        #~ # -- We now applay the geometric_mask to the image
        #~ image = image * mask
        #~ image[image==1] = 0
        #~ 
        #~ return  image[ x_bar:x_max+x_bar,y_bar:y_max+y_bar,z_bar:z_max+z_bar ]


    #~ def __curvature_parameters2(func):
        #~ def wrapped_function(self, vids = None, sphere_size = 50, verbose = False):
            #~ """
            #~ """
            #~ # -- We start by taking out the border cells (we could keep them and to prevent the computation of the curvature for neighbours of margin cells)
            #~ if self.cells_in_image_margins() != [0, 1]:
                #~ self.remove_margins_cells(verbose = verbose)
#~ 
            #~ # -- If 'vids' is an integer... 
            #~ if isinstance(vids,int):
                #~ if (vids not in self.L1()): # - ...but not in the L1 list, there is nothing to do!
                    #~ print "Cell",vids,"is not in the L1. We won't compute it's curvature."
                    #~ return 0
                #~ else: # - ... and in the L1 list, we make it iterable.
                    #~ vids=[vids]
#~ 
            #~ # -- If 'vids' is a list, we make sure to keep only its 'vid' present in the L1 list!
            #~ if isinstance(vids,list):
                #~ tmp = copy.deepcopy(vids) # Ensure to scan all the elements of 'vids'
                #~ for vid in tmp:
                    #~ if vid not in self.L1():
                        #~ if verbose: print "Cell",vid,"is not in the L1. We won't compute it's curvature."
                        #~ vids.remove(vid)
                #~ if len(vids) == 0: # if there is no element left in the 'vids' list, there is nothing to do!
                    #~ print 'None of the cells you provided bellonged to the L1.'
                    #~ return 0
#~ 
            #~ # -- If 'vids' is `None`, we apply the function to all L1 cells:
            #~ if vids == None:
                #~ vids = self.L1()
#~ 
            #~ sphere = euclidean_sphere(sphere_size)
#~ 
            #~ if create_route_for_fitting:
                #~ create_route_for_fitting(vids) # Sort vids in a ways its you have a neighbors with estimated parameters for the quadratic plane.
#~ 
            #~ # -- Now we can compute the curvature by applying the function 'gaussian_curvature' OR 'mean_curvature'.
            #~ curvature={}
            #~ if verbose: print 'Computing curvature :'
            #~ for n,vid in enumerate(vids):
                #~ if verbose: print n,'/',len(vids)
                #~ if self.quadratic_parameters.has_key(vid): # if we already know the parameters of the quadratic plane, no need to search for the external wall.
                    #~ if self.principal_curvatures.has_key(vid):
                        #~ k1, k2 = self.principal_curvatures[vid]
                    #~ else:
                        #~ k1, k2 = principal_curvatures(self.quadratic_parameters[vid])
                        #~ self.principal_curvatures[vid] = [k1, k2]
                #~ else:
                    #~ masked_im = self.mask_intersection(vid,sphere)
                    #~ x, y, z = np.where( masked_im != 0 )
                    #~ params = quadratic_plane_fit(x,y,z)[0]
                    #~ self.quadratic_parameters[vid] = params
                    #~ k1, k2 = principal_curvatures(params)
                    #~ self.principal_curvatures[vid] = [k1, k2]
                #~ curvature[vid] = func( k1,k2 )
            #~ 
            #~ return curvature
        #~ return wrapped_function


    #~ @__curvature_parameters2
    #~ def gaussian_curvature2( k1, k2 ):
        #~ """
        #~ Gaussian curvature is the product of principal curvatures 'k1*k2'.
        #~ Here it comes from the first and second fundamental form of a quadratic plane fitted by nonlinear least square method.
        #~ """
        #~ return k1*k2


    #~ @__curvature_parameters2
    #~ def mean_curvature2( k1, k2 ):
        #~ """
        #~ Gaussian curvature is the product of principal curvatures ''1/2*(k1+k2)'.
        #~ Here it comes from the first and second fundamental form of a quadratic plane fitted by nonlinear least square method.
        #~ """
        #~ return 0.5*(k1+k2)


    #~ def neighborhood_surface_walls(self, vid, all_walls = None, verbose = False):
        #~ """
        #~ """
        #~ if all_walls == None:
            #~ all_walls = self.all_wall_voxels(1,verbose)
#~ 
        #~ walls = []
        #~ walls.append(all_walls[1,vid])
        #~ L1 = self.L1()
        #~ for k in self.neighbors(vid):
            #~ if k in L1:
                #~ walls.append( all_walls[1,k] )
#~ 
        #~ return walls


    #~ def brute_route_by_neighbors(self, id2list, starting_point = None, verbose = False):
        #~ """
        #~ Function returning a list of vids. It define a sequence of labels allowing to travel in a neighbors-like manner.
        #~ 
        #~ If return 0: the id2list do not define a connected region.
        #~ """
        #~ if verbose: print 'Creating a route by neighbors...'
        #~ remaining_labels = copy.deepcopy(id2list)
        #~ if 0 in remaining_labels: remaining_labels.remove(0)
        #~ if 1 in remaining_labels: remaining_labels.remove(1)
#~ 
        #~ if starting_point == None:
            #~ starting_point = remaining_labels[0]
#~ 
        #~ if starting_point in remaining_labels:
            #~ remaining_labels.remove(starting_point)
        #~ else:
            #~ print 'The starting point you provided is not in the L1!'
            #~ return 0
#~ 
        #~ max_iter = len(remaining_labels)
        #~ 
        #~ all_neighbors=self.neighbors()
        #~ 
        #~ route=[]
        #~ route.extend([starting_point])
        #~ nb_iter = 0
        #~ while len(remaining_labels) != 0 :
            #~ neighbors = all_neighbors[starting_point]
            #~ neighbors = list( set(remaining_labels)&set(neighbors) )
            #~ route.extend(neighbors)
            #~ remaining_labels = list( set(remaining_labels)-set(neighbors) )
            #~ for k in neighbors:
                #~ n = list( set(remaining_labels)&set(all_neighbors[k]) )
                #~ route.extend(n)
                #~ remaining_labels = list( set(remaining_labels)-set(n) )
            #~ 
            #~ back = 1
            #~ starting_point = route[len(route)-back]
            #~ while (len( set(remaining_labels)&set(all_neighbors[starting_point]) ) == 0) & (len(remaining_labels) != 0):
                #~ back +=1
                #~ starting_point = route[len(route)-back]
#~ 
            #~ nb_iter += 1
            #~ if nb_iter >= max_iter:
                #~ print 'There might be a problem: you maxed-up the number of iterations (',max_iter,').'
                #~ print 'remaining_labels',remaining_labels
                #~ print 'Computed route so far:', route
                #~ return 0
#~ 
        #~ return route


    #~ def __curvature_parameters3(func):
        #~ def wrapped_function(self, vids = None, radius = 50, verbose = False):
            #~ """
            #~ """
            #~ # -- We start by taking out the border cells (we could keep them and to prevent the computation of the curvature for neighbours of margin cells)
            #~ if self.cells_in_image_margins() != [0, 1]:
                #~ self.remove_margins_cells(verbose = verbose)
#~ 
            #~ # -- If 'vids' is an integer... 
            #~ if isinstance(vids,int):
                #~ if (vids not in self.L1()): # - ...but not in the L1 list, there is nothing to do!
                    #~ print "Cell",vids,"is not in the L1. We won't compute it's curvature."
                    #~ return 0
                #~ else: # - ... and in the L1 list, we make it iterable.
                    #~ vids=[vids]
#~ 
            #~ # -- If 'vids' is a list, we make sure to keep only its 'vid' present in the L1 list!
            #~ if isinstance(vids,list):
                #~ tmp = copy.deepcopy(vids) # Ensure to scan all the elements of 'vids'
                #~ for vid in tmp:
                    #~ if vid not in self.L1():
                        #~ if verbose: print "Cell",vid,"is not in the L1. We won't compute it's curvature."
                        #~ vids.remove(vid)
                #~ if len(vids) == 0: # if there is no element left in the 'vids' list, there is nothing to do!
                    #~ print 'None of the cells you provided bellonged to the L1.'
                    #~ return 0
#~ 
            #~ # -- If 'vids' is `None`, we apply the function to all L1 cells:
            #~ if vids == None:
                #~ vids = self.L1()
#~ 
            #~ # -- Now we can compute the curvature by applying the function 'gaussian_curvature' OR 'mean_curvature'.
            #~ curvature={}
            #~ if verbose: print 'Computing curvature :'
            #~ for n,vid in enumerate(vids):
                #~ if verbose: print n,'/',len(vids)
                #~ if self.quadratic_parameters.has_key(vid): # if we already know the parameters of the quadratic plane, no need to search for the external wall.
                    #~ if self.principal_curvatures.has_key(vid):
                        #~ k1, k2 = self.principal_curvatures[vid]
                    #~ else:
                        #~ k1, k2 = principal_curvatures(self.quadratic_parameters[vid])
                        #~ self.principal_curvatures[vid] = [k1, k2]
                #~ else:
                    #~ x, y, z = self.voxel_neighborhood(vid,radius)
                    #~ params = quadratic_plane_fit(x,y,z)[0]
                    #~ self.quadratic_parameters[vid] = params
                    #~ k1, k2 = principal_curvatures(params)
                    #~ self.principal_curvatures[vid] = [k1, k2]
                #~ curvature[vid] = func( k1,k2 )
            #~ 
            #~ return curvature
        #~ return wrapped_function


#~ @__curvature_parameters3
    #~ def gaussian_curvature3( k1, k2 ):
        #~ """
        #~ Gaussian curvature is the product of principal curvatures 'k1*k2'.
        #~ Here it comes from the first and second fundamental form of a quadratic plane fitted by nonlinear least square method.
        #~ """
        #~ return k1*k2


    #~ @__curvature_parameters3
    #~ def mean_curvature3( k1, k2 ):
        #~ """
        #~ Gaussian curvature is the product of principal curvatures ''1/2*(k1+k2)'.
        #~ Here it comes from the first and second fundamental form of a quadratic plane fitted by nonlinear least square method.
        #~ """


    #~ def voxel_neighborhood(self, vid, radius = 40., origin = 'Mean'):
        #~ """
        #~ Function returning the connected voxels to the one closest to the 'Mean' or 'Median' of the voxels cloud of cell 'vid'.
        #~ """
        #~ if self._first_voxel_layer == None:
            #~ self.first_voxel_layer(1, True, keep_background = False)
        #~ else:
            #~ if self._first_voxel_layer[0,0,0]==1:
                #~ self._first_voxel_layer[self._first_voxel_layer==1]=0
                #~ 
        #~ pts = [tuple([int(x[i]),int(y[i]),int(z[i])]) for i in xrange(len(x))]
#~ 
        #~ from openalea.plantgl.all import k_closest_points_from_ann, r_neighborhood
        #~ # adjacencies = k_closest_points_from_delaunay(pts,k=10)
        #~ adjacencies = k_closest_points_from_ann(pts,k=10)
#~ 
        #~ from openalea.image.all import geometric_median
        #~ x_vid, y_vid, z_vid = np.where(self.first_voxel_layer() == vid)
        #~ if origin == 'median':
            #~ median = geometric_median( np.array([list(x_vid),list(y_vid),list(z_vid)]) )
        #~ else:
            #~ median = np.mean( np.array([list(x_vid),list(y_vid),list(z_vid)]) )
#~ 
        #~ integers=np.vectorize(integer)
        #~ median = integers(median)
        #~ pts_vid = [tuple([int(x_vid[i]),int(y_vid[i]),int(z_vid[i])]) for i in xrange(len(x_vid))]
#~ 
        #~ min_dist = closest_from_A(median, pts_vid)
#~ 
        #~ neigborids = r_neighborhood(pts.index(min_dist), pts, adjacencies, radius)
#~ 
        #~ neigbor_pts=[]
        #~ for i in neigborids:
            #~ neigbor_pts.append(pts[i])
#~ 
        #~ neigbor_pts
#~ 
        #~ x_pts, y_pts, z_pts=[],[],[]
        #~ for i in neigborids:
            #~ x_pts.append(pts[i][0])
            #~ y_pts.append(pts[i][1])
            #~ z_pts.append(pts[i][2])
        #~ 
        #~ return x_pts, y_pts, z_pts


#~ def second_order_surface(params,data):
    #~ """
    #~ A second order analytic surface of the form z = a1.x^2 + a2.xy + a3.y^2 + a4.x + a5.y + a6
    #~ """
    #~ a1,a2,a3,a4,a5,a6=params
    #~ x,y=data
    #~ return (a1*x**2 + a2*x*y + a3*y**2 + a4*x + a5*y + a6)


#~ def quadratic_plane_fit( x, y, z, fit_init = [0,0,0,0,0,1] ):
    #~ """
    #~ Use non-linear least squares to fit a function, f, to data. The algorithm uses the Levenburg-Marquardt algorithm.
    #~ The function to be fitted will be called with two parameters:
        #~ - the first is a tuple containing all fit parameters, 
        #~ - the second is the first element of a data point. The return value must be a number.
    #~ """
    #~ import Scientific 
    #~ from Scientific.Functions.LeastSquares import leastSquaresFit
#~ 
    #~ if fit_init == None:
        #~ fit_init = [0,0,0,0,0,1]
#~ 
    #~ # --The first element specifies the independent variables of the model. 
    #~ # --The second element of each data point tuple is the number that the return value of the model function is supposed to match
    #~ wall=[tuple(( tuple((x[i],y[i])), z[i] )) for i in xrange(len(x))]
    #~ 
    #~ optimal_parameter_values, chi_squared=leastSquaresFit(second_order_surface, fit_init, wall, max_iterations=None)
    #~ 
    #~ return optimal_parameter_values, chi_squared


#~ def principal_curvatures(params, return_roots = False):
    #~ """
    #~ Compute principal curvature k1 and k2 from a second order analytic surface of the form z = a1.x^2 + a2.xy + a3.y^2 + a4.x + a5.y + a6.
    #~ """
    #~ # -- We first recover the parameters:
    #~ a1,a2,a3,a4,a5,a6=params
    #~ 
    #~ # -- Then we define the parameters E, F and G for the first fundamental form:
    #~ E=1+a4**2
    #~ F=a4*a5
    #~ G=1+a5**2
    #~ 
    #~ # -- Then we define the parameters e, f and g for the second fundamental form:    
    #~ e=(2*a1)/(math.sqrt(E*G-F**2))
    #~ f=(a2)/(math.sqrt(E*G-F**2))
    #~ g=(2*a3)/(math.sqrt(E*G-F**2))
    #~ 
    #~ # -- We now have to find the roots of the equation : (Fg - Gf) x**2 + (Eg - Ge) x + (Ef - Fe) = 0
    #~ a = (F*g - G*f)
    #~ b = (E*g - G*e)
    #~ c = (E*f - F*e)
    #~ discriminant = b**2 - 4*a*c
    #~ if discriminant > 0:
        #~ x_1 = ( -b-math.sqrt(discriminant) )/(2*a)
        #~ x_2 = ( -b+math.sqrt(discriminant) )/(2*a)
    #~ elif discriminant == 0:
        #~ x_1 = x_2 = (-b)/(2*a)
    #~ else:
        #~ import warnings
        #~ warnings.warn("No real solutions...")
        #~ return 0,0
        #~ 
    #~ if return_roots:
        #~ return (e+f*x_1)/(E+F*x_1), (e+f*x_2)/(E+F*x_2), x_1, x_2
    #~ else:
        #~ return (e+f*x_1)/(E+F*x_1), (e+f*x_2)/(E+F*x_2)


#~ def euclidean_sphere(size):
    #~ """
    #~ Generate a euclidean sphere for binary morphological operations
#~ 
    #~ :Parameters:
        #~ - `size` (int) - the shape of the euclidean sphere = 2*size + 1.
#~ 
    #~ :Returns:
        #~ - Euclidean sphere which may be used for binary morphological operations, with shape equal to 2*size + 1.
    #~ """
    #~ n = int(2*size + 1)
    #~ sphere = np.zeros((n,n,n),np.bool)
    #~ for x in range(n):
        #~ for y in range(n):
            #~ for z in range(n):
                #~ if (x-size)**2+(y-size)**2+(z-size)**2<=size**2:
                    #~ sphere[x,y,z]=True
    #~ return sphere


#~ def extract_L1(image):
    #~ """
    #~ Return the list of all cell labels in the layer 1.
#~ 
    #~ :Parameters:
        #~ - `image` (|SpatialImage|) - segmented image
#~ 
    #~ :Returns:
        #~ - `L1` (list)
    #~ """
    #~ return SpatialImageAnalysis(image).L1()
    #~ # L1 = []
    #~ # im = np.zeros_like(image)
    #~ # im[image!=1]=1
    #~ # ero = nd.binary_erosion(im)
    #~ # mask = im - ero
    #~ # res = np.where(mask==1,image,0)
    #~ # for cell in xrange(1,image.max()+1):
        #~ # if cell in res:
            #~ # L1.append(cell)
    #~ # return L1

