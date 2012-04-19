# -*- python -*-
# -*- coding: latin-1 -*-
#
#       vplants.mars_alt.analysis.analysis
#
#       Copyright 2006 - 2011 INRIA - CIRAD - INRA
#
#       File author(s): Eric MOSCARDI <eric.moscardi@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
################################################################################

__license__ = "Cecill-C"
__revision__ = " $Id$ "

import numpy as np
import scipy.ndimage as nd
import math
import copy

from openalea.image.spatial_image import SpatialImage

def dilation(slices):
    return [ slice(max(0,s.start-1), s.stop+1) for s in slices]

def wall(mask_img,label_id):
    img = (mask_img == label_id)
    dil = nd.binary_dilation(img)
    contact = dil - img
    return mask_img[contact]

def contact_surface(mask_img,label_id):
    img = wall(mask_img,label_id)
    return set(np.unique(img))

def real_indices(slices, resolutions):
    return [ (s.start*r, s.stop*r) for s,r in zip(slices,resolutions)]


def hollow_out_cells(image):
    """
    Laplacian filter used to dectect and return an Spatial Image containing only cell walls.
    (The Laplacian of an image highlights regions of rapid intensity change.)
    :INPUT:
        .image: Spatial Image containing cells (segmented image)
    :OUTPUT:
        .m: Spatial Image containing hollowed out cells (cells walls from full segmented image)
    """
    print 'Hollowing out cells...'
    b=nd.laplace(image)
    m=image.copy()
    m[b==0]=0
    m[np.where(m==1)]=0
    print 'Done !!'
    return m


def cells_walls_coords(image, hollowed_out=False):
    """
    :INPUT:
        .image: Spatial Image containing cells (segmented image)
    :OUTPUT:
        .x,y,z: coordinates of the cells' boundaries (walls)
    """
    if not hollowed_out:
        image=hollow_out_cells(image)
    print 'Extracting cell walls coordinates...'
    x,y,z=np.where(image!=0)
    print 'Done !!'
    return list(x),list(y),list(z)


def cell_vertex_extraction(image, verbose=False):
    """
    Calculates cell's vertices positions according to the rule: a vertex is the point where you can find 4 differents cells (in 3D!!)
    For the surface, the outer 'cell' #1 is considered as a cell.

    :INPUTS:
        .image: Spatial Image containing cells (segmented image). Can be a full spatial image or an extracted surface.

    :OUTPUT:
        .barycentric_vtx:
            *keys = the 4 cells ids associated with the vertex position(values);
            *values = 3D coordinates of the vertex in the Spatial Image;
    """
    x, y, z = cells_walls_coords(image)
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


def cell2vertex_relations(cells2coords):
    """
    Creates cell2vtx, vtx2coords & vtx2cells dictionaries.
    
    :INPUT:
    - cells2coords: dict *keys=the 4 cells ids at the vertex position ; *values=3D coordinates of the vertex in the Spatial Image.
    
    :OUPTUTS:
    - cell2vtx: dict *keys=cell id ; *values= NEW ids of the vertex defining the cell
    - vtx2coords: dict *keys=vertex NEW id ; *values= 3D coordinates of the vertex in the Spatial Image
    - vtx2cells: dict *keys=vertex NEW id ; *values= ids of the 4 associated cells
    """
    vtx2cells = {} #associated cells to each vertex;
    cell2vtx = {} #associated vertex to each cells;
    vtx2coords = {}
    for n, i in enumerate(cells2coords.keys()):
        vtx2cells[n] = list(i)
        vtx2coords[n] = list(cells2coords[i])
        for j in list(i):
            #check if cell j is already in the dict
            if cell2vtx.has_key(j): 
                cell2vtx[j] = cell2vtx[j]+[n] #if true, keep the previous entry (vertex)and give the value of the associated vertex
            else:
                cell2vtx[j] = [n] #if false, create a new one and give the value of the associated vertex
    #~ del(cell2vtx[1]) #cell #1 doesn't really exist...
    return cell2vtx, vtx2coords, vtx2cells


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
        dist.append(d) #update of the distance évolution
        y = [num_x/denum, num_y/denum, num_z/denum] #update to the new value of the median
        if i > 3:
            convergence=(abs(dist[i]-dist[i-2])<0.1) #we test the convergence over three steps for stability
            #~ print abs(dist[i]-dist[i-2]), convergence
        i += 1
    if i == numIter:
        print "The Weiszfeld's algoritm did not converged after",numIter,"iterations for cell #",c,"!!!!!!!!!"
    #When convergence or iterations limit is reached we assume that we found the median.

    return np.array(y)


def OLS_wall(xyz):
    """
    Compute OLS (Ordinary Least Square) fitting of a plane in a 3D space.
    
    :Parameters:
        - `xyz` voxels coordinate (3xN or Nx3 matrix)
    """
    import numpy.linalg as ln
    if xyz.shape()[0] == 3: #if the matrix is 3xN, we convert it to a Nx3 matrix.
        xyz = xyz.transpose()
    
    ols_fit = ln.lstsq( xyz[:,0:2], xyz[:,2] )
        
    return ols_fit


def euclidean_sphere(size):
    """
    Generate a euclidean sphere for binary morphological operations

    :Parameters:
        - `size` (int) - the shape of the euclidean sphere = 2*size + 1.

    :Returns:
        - Euclidean sphere which may be used for binary morphological operations, with shape equal to 2*size + 1.
    """
    n = int(2*size + 1)
    sphere = np.zeros((n,n,n),np.bool)
    for x in range(n):
        for y in range(n):
            for z in range(n):
                if (x-size)**2+(y-size)**2+(z-size)**2<=size**2:
                    sphere[x,y,z]=True
    return sphere


class SpatialImageAnalysis(object):
    """
    This object can extract a number of geometric estimator from a SpatialImage,
    each cells volume, neighborhood structure and the shared surface area of two neighboring cells.
    """

    def __init__(self, image):
        """
        ..warning :: Label features in the images are an arithmetic progression of continous integers.
        """
        if not isinstance(image,SpatialImage):
            self.image = SpatialImage(image)
        else:
            self.image = image
        # variables for caching information
        self._labels = None # self.__labels()
        self._bbox = None
        self._kernels = None
        self._neighbors = None
        self._L1 = None # self.__L1() # Jonathan : 04.16.2012
        self._first_voxel_layer = None # Jonathan : 04.17.2012
        self.quadratic_parameters = {} # Jonathan : 04.18.2012
        self.principal_curvatures = {} # Jonathan : 04.18.2012


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
        if self._labels is None : self._labels = self.__labels()
        return self._labels

    def __labels(self):
        """ Compute the actual list of labels """
        return np.unique(self.image)


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
        return len(self._labels)


    def center_of_mass(self, labels=None, real=True):
        """
            Return the center of mass of the labels.
            Note that if input image is 2D, it is reshaped as a 3D image with last dimension as one.
            Thus center of mass always return a 3D vectors.

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

        center = nd.center_of_mass(self.image, self.image, index=labels)

        if real is True:
            center = np.multiply(center,self.image.resolution)
            return center.tolist()
        else:
            return center


    def volume(self,labels=None,real=True):
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

        volume = nd.sum(np.ones_like(self.image), self.image, index=labels)

        if real is True:
            if self.image.ndim == 2:
                volume = np.multiply(volume,(self.image.resolution[0]*self.image.resolution[1]))
            elif self.image.ndim == 3:
                volume = np.multiply(volume,(self.image.resolution[0]*self.image.resolution[1]*self.image.resolution[2]))
            return volume.tolist()
        else:
            return volume


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

    def neighbors(self,labels=None):
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
        return self._kernels


    def get_voxel_face_surface(self):
        a = self.image.resolution
        return np.array([a[1] * a[2],a[2] * a[0],a[0] * a[1] ])


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
            print "You got it wrong dude,",label_1 ,"and", label_2,"are not neighbors!!"

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


    def all_wall_voxels(self, label_1, verbose=False):
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
        for a in xrange(6):
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


    def __L1(self, background = 1):
        return self.neighbors(background)

    def L1(self, background = 1):
        if self._L1 is None : self._L1 = self.__L1(background)
        if 0 in self._L1: self._L1.remove(0)
        return self._L1


    def __first_voxel_layer(self, background = 1, remove_margins_cells = True, keep_background = True):
        """
        Extract the first layer of voxels at the surface of the biological object.
        """
        if remove_margins_cells:
            self.remove_margins_cells()
        
        mask_img_1 = (self.image == 1)
        struct = nd.generate_binary_structure(3, 1)
        dil_1 = nd.binary_dilation(mask_img_1, structure=struct)
        
        layer = dil_1 - mask_img_1
        
        if keep_background:
            return self.image * layer + mask_img_1
        else:
            return self.image * layer

    def first_voxel_layer(self, background = 1, remove_margins_cells = True, keep_background = False):
        if self._first_voxel_layer is None :
            self._first_voxel_layer = self.__first_voxel_layer(background, remove_margins_cells, keep_background)
        return self._first_voxel_layer


    def border_cells(self):
        borders = set()
        for l in [np.unique(self.image[0,:,:]),np.unique(self.image[-1,:,:]),np.unique(self.image[:,0,:]),np.unique(self.image[:,-1,:])]:
            borders.update(l)
        if self.image.shape[2] != 1 :
            borders.update(np.unique(self.image[:,:,0]))
            borders.update(np.unique(self.image[:,:,-1]))
        return list(borders)


    def inertia_axis(self, labels = None, center_of_mass = None, real = True):
        unique_label = False
        if labels is None : labels = self.labels()
        elif not isinstance(labels,list) :
            labels = [labels]
            unique_label = True

        is2d = (self.image.shape[2] <= 1)
        # results
        inertia_eig_vec = []
        inertia_eig_val = []

        # if center of mass is not specified
        if center_of_mass is None:
            center_of_mass = self.center_of_mass(labels)
        for i,label in enumerate(labels):
            slices = self.boundingbox(label)
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

            if is2d : coord = np.array([x,y])
            else:
                z = z - center[2]
                coord = np.array([x,y,z])

            # compute P.P^T
            cov = np.dot(coord,coord.T)


            # Find the eigen values and vectors.
            eig_val, eig_vec = np.linalg.eig(cov)

            inertia_eig_vec.append(eig_vec)

            if real:
                if self.image.shape[2] > 1:
                    for i in xrange(3):
                        eig_val[i] *= np.linalg.norm(np.multiply(eig_vec[i],self.image.resolution))
                else:
                    for i in xrange(2):
                        eig_val[i] *= np.linalg.norm(np.multiply(eig_vec[i],self.image.resolution[:2]))

            inertia_eig_val.append(eig_val)

        if unique_label :
            return inertia_eig_vec[0], inertia_eig_val[0]
        else:
            return inertia_eig_vec, inertia_eig_val


    def remove_margins_cells(self, save = "", display = False, verbose = False):
        """
        !!!!WARNING!!!!
        This function modify the SpatialImage on self.image
        !!!!WARNING!!!!
        Function removing the cell's at the magins, because most probably cut during stack aquisition.
        
        :INPUTS:
            .save: text (if present) indicating under which name to save the Spatial Image containing the cells of the first layer;
            .display: boolean indicating if we should display the previously computed image;
        
        :OUPUT:
            Spatial Image without the cell's at the magins.
        """
        
        if verbose: print "Removing the cell's at the magins..."
        
        border_cells = self.border_cells()
        border_cells.remove(1)
        len_border_cells = len(border_cells)
        for n,c in enumerate(border_cells):
            if verbose and n%20 == 0: print n,'/',len_border_cells
            xyz = np.where( (self.image[self.boundingbox(c)]) == c )
            self.image[tuple((xyz[0]+self.boundingbox(c)[0].start,xyz[1]+self.boundingbox(c)[1].start,xyz[2]+self.boundingbox(c)[2].start))]=0

        if save != "":
            imsave(self.image,save)

        if display:
            from vplants.tissue_analysis.growth_analysis import visu_spatial_image
            visu_spatial_image(self.image)
        
        if verbose: print 'Done !!'
        
        self.__init__(self.image)


    def mask_intersection(self, vid, geometric_mask):
        """
        Create the intersection between a geometric_mask and de first layer of voxel of the image.
        Used for curvature computation.
        """
        x_max, y_max, z_max = self.first_voxel_layer().shape
        x_size, y_size, z_size = geometric_mask.shape
        if (x_size >= x_max) or (y_size >= y_max) or (z_size >= z_max):
            if verbose: print 'the size of the geometrical object is too big !!!'
            return None

        from openalea.image.all import geometric_median
        x, y, z = np.where(self.first_voxel_layer() == vid)
        median = geometric_median( np.array([list(x),list(y),list(z)]) )
        
        def integer(x):
            return int(x)

        integers=np.vectorize(integer)
        median = integers(median)
        
        x_bar, y_bar, z_bar = integers(np.round(np.array(geometric_mask.shape)/2.))
        # -- We create the mask (with extended border so the geometrical mask can be applied even if it's center is close from the margins of the image)
        mask = np.zeros( tuple([x_max+x_size, y_max+y_size, z_max+z_size]) )
        # -- We create the extended version of the image
        image = copy.copy(mask)
        image[ x_bar:x_max+x_bar,y_bar:y_max+y_bar,z_bar:z_max+z_bar ] = self.first_voxel_layer()
        # -- We now add the geometric_mask to the mask
        mask[median[0]:median[0]+x_size,median[1]:median[1]+y_size,median[2]:median[2]+z_size] = geometric_mask
        # -- We now applay the geometric_mask to the image
        image = image * mask
        image[image==1] = 0
        
        return  image[ x_bar:x_max+x_bar,y_bar:y_max+y_bar,z_bar:z_max+z_bar ]


    def __curvature_parameters2(func):
        def wrapped_function(self, vids = None, sphere_size = 50, verbose = False):
            """
            """
            # -- We start by taking out the border cells (we could keep them and to prevent the computation of the curvature for neighbours of margin cells)
            if self.border_cells() != [0, 1]:
                self.remove_margins_cells(verbose = verbose)

            # -- If 'vids' is an integer... 
            if isinstance(vids,int):
                if (vids not in self.L1()): # - ...but not in the L1 list, there is nothing to do!
                    print "Cell",vids,"is not in the L1. We won't compute it's curvature."
                    return 0
                else: # - ... and in the L1 list, we make it iterable.
                    vids=[vids]

            # -- If 'vids' is a list, we make sure to keep only its 'vid' present in the L1 list!
            if isinstance(vids,list):
                tmp = copy.deepcopy(vids) # Ensure to scan all the elements of 'vids'
                for vid in tmp:
                    if vid not in self.L1():
                        if verbose: print "Cell",vid,"is not in the L1. We won't compute it's curvature."
                        vids.remove(vid)
                if len(vids) == 0: # if there is no element left in the 'vids' list, there is nothing to do!
                    print 'None of the cells you provided bellonged to the L1.'
                    return 0

            # -- If 'vids' is `None`, we apply the function to all L1 cells:
            if vids == None:
                vids = self.L1()

            sphere = euclidean_sphere(sphere_size)

            #~ if create_route_for_fitting:
                #~ create_route_for_fitting(vids) # Sort vids in a ways its you have a neighbors with estimated parameters for the quadratic plane.

            # -- Now we can compute the curvature by applying the function 'gaussian_curvature' OR 'mean_curvature'.
            curvature={}
            if verbose: print 'Computing curvature :'
            for n,vid in enumerate(vids):
                if verbose: print n,'/',len(vids)
                if self.quadratic_parameters.has_key(vid): # if we already know the parameters of the quadratic plane, no need to search for the external wall.
                    if self.principal_curvatures.has_key(vid):
                        k1, k2 = self.principal_curvatures[vid]
                    else:
                        k1, k2 = principal_curvatures(self.quadratic_parameters[vid])
                        self.principal_curvatures[vid] = [k1, k2]
                else:
                    masked_im = self.mask_intersection(vid,sphere)
                    x, y, z = np.where( masked_im != 0 )
                    params = quadratic_plane_fit(x,y,z)[0]
                    self.quadratic_parameters[vid] = params
                    k1, k2 = principal_curvatures(params)
                    self.principal_curvatures[vid] = [k1, k2]
                curvature[vid] = func( k1,k2 )
            
            return curvature
        return wrapped_function


    @__curvature_parameters2
    def gaussian_curvature2( k1, k2 ):
        """
        Gaussian curvature is the product of principal curvatures 'k1*k2'.
        Here it comes from the first and second fundamental form of a quadratic plane fitted by nonlinear least square method.
        """
        return k1*k2

    @__curvature_parameters2
    def mean_curvature2( k1, k2 ):
        """
        Gaussian curvature is the product of principal curvatures ''1/2*(k1+k2)'.
        Here it comes from the first and second fundamental form of a quadratic plane fitted by nonlinear least square method.
        """
        return 0.5*(k1+k2)


    #~ def __curvature_parameters(func):
        #~ def wrapped_function(self, vids = None, init_fitting_from_neighbors = False, verbose = False):
            #~ """
            #~ """
            #~ # -- We start by taking out the border cells (we could keep them and to prevent the computation of the curvature for neighbours of margin cells)
            #~ if self.border_cells() != [0, 1]:
                #~ self.remove_margins_cells(verbose = verbose)
#~ 
            #~ # -- If 'vids' is an integer but not in the L1 list, there is nothing to do!
            #~ if isinstance(vids,int) and (vids not in self.L1()):
                #~ if verbose: print "Cell",vids,"is not in the L1. We won't compute it's curvature."
                #~ return 0
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
            #~ # - For a single vertex id, compute a single result
            #~ if isinstance(vids,int): 
                #~ if self.quadratic_parameters.has_key(vids): # if we already know the parameters of the quadratic plane, no need to search for the external wall.
                    #~ curvature[vids] = func( self, vids, None )
                #~ else:
                    #~ curvature[vids] = func( self, vids, self.neighborhood_surface_walls(vids) )
                #~ return curvature
#~ 
            #~ # - For a list of ids, we compute the dictionary of resulting values.
            #~ if isinstance(vids,list):
                #~ try :
                    #~ sum([self.quadratic_parameters.has_key(vid) for vid in vids]) != 0
                #~ except:    
                    #~ all_walls = self.all_wall_voxels(1,verbose)
                    #~ if init_fitting_from_neighbors :
                        #~ route = self.brute_route_by_neighbors(vids)
                        #~ if route != 0: # if route == 0 : not a connected region, therfore we can't use the information from the neighbors for the fitting.
                            #~ medians={}
                            #~ for n,vid in enumerate(route):
                                #~ if verbose and n%2 == 0: print n,'/',len(vids)
                                #~ medians[vid] = geometric_median(all_walls[((1,vid))])
                                #~ xA, yA, zA = medians[vid]
                                #~ min_dist = 0
                                #~ dist_1 = float('inf')
                                #~ common_list = list( set(medians.keys())&set(self.neighbors(vid)) )
                                #~ if n != 0:
                                    #~ for k in common_list:
                                        #~ xB, yB, zB = medians[k]
                                        #~ dist_2 = math.sqrt((xA-xB)**2+(yA-yB)**2+(zA-zB)**2)
                                        #~ if dist_2 < dist_1:
                                            #~ min_dist = k
                                    #~ curvature[vid] = func( self, vid, self.neighborhood_surface_walls(vid, all_walls), self.quadratic_parameters[min_dist] if min_dist != 0 else None )
                                #~ else:
                                    #~ curvature[vid] = func( self, vid, self.neighborhood_surface_walls(vid, all_walls), None )
                    #~ else:
                        #~ for n,vid in enumerate(vids):
                            #~ if verbose and n%2 == 0: print n,'/',len(vids)
                            #~ curvature[vid] = func( self, vid, self.neighborhood_surface_walls(vid, all_walls), None )
                #~ else:
                    #~ for n,vid in enumerate(vids):
                        #~ if verbose and n%20 == 0: print n,'/',len(vids)
                        #~ if self.quadratic_parameters.has_key(vid): # if we already know the parameters of the quadratic plane, no need to search for the external wall.
                            #~ curvature[vid] = func( self, vid, None )
                        #~ else:
                            #~ curvature[vid] = func( self, vid, self.neighborhood_surface_walls(vid, all_walls), None )
                    #~ 
                #~ return curvature        
        #~ return wrapped_function
#~ 
#~ 
    #~ @__curvature_parameters
    #~ def gaussian_curvature( self, vid, walls, fit_init = None ):
        #~ """
        #~ Gaussian curvature as the product of principal curvatures 'k1*k2' from quadratic plane fitted by nonlinear least square method.
        #~ """
#~ 
        #~ if (walls == None): # Special case from '__curvature_parameters' where "self.quadratic_parameters.has_key(vid)".
            #~ if self.principal_curvatures.has_key(vid):
                #~ k1, k2 = self.principal_curvatures[vid]
                #~ return k1*k2
            #~ else:
                #~ k1, k2 = principal_curvatures( params )
                #~ self.principal_curvatures[vid] = [k1,k2]
                #~ return k1*k2
        #~ else:
            #~ params = quadratic_plane_fit( walls, fit_init )[0]
            #~ self.quadratic_parameters[vid] = params
            #~ k1, k2 = principal_curvatures( params )
            #~ self.principal_curvatures[vid] = [k1,k2]
            #~ return k1*k2
#~ 
#~ 
    #~ @__curvature_parameters
    #~ def mean_curvature( self, vid, walls, fit_init = None ):
        #~ """
        #~ Mean curvature as the half sum of principal curvatures '1/2*(k1+k2)' from quadratic plane fitted by nonlinear least square method.
        #~ """
        #~ if (walls == None): # -- Special case from '__curvature_parameters' where "self.quadratic_parameters.has_key(vid)".
            #~ if self.principal_curvatures.has_key(vid):
                #~ k1, k2 = self.principal_curvatures[vid]
                #~ return 0.5*(k1+k2)
            #~ else:
                #~ k1, k2 = principal_curvatures( params )
                #~ self.principal_curvatures[vid] = [k1,k2]
                #~ return 0.5*(k1+k2)
        #~ else:
            #~ params = quadratic_plane_fit( walls, fit_init )[0]
            #~ self.quadratic_parameters[vid] = params
            #~ k1, k2 = principal_curvatures( params )
            #~ self.principal_curvatures[vid] = [k1,k2]
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
#~ 
#~ 
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
    

def second_order_surface(params,data):
    """
    A second order analytic surface of the form z = a1.x^2 + a2.xy + a3.y^2 + a4.x + a5.y + a6
    """
    a1,a2,a3,a4,a5,a6=params
    x,y=data
    return (a1*x**2 + a2*x*y + a3*y**2 + a4*x + a5*y + a6)


def quadratic_plane_fit( x, y, z, fit_init = [0,0,0,0,0,1] ):
    """
    Use non-linear least squares to fit a function, f, to data. The algorithm uses the Levenburg-Marquardt algorithm.
    The function to be fitted will be called with two parameters:
        - the first is a tuple containing all fit parameters, 
        - the second is the first element of a data point. The return value must be a number.
    """
    import Scientific 
    from Scientific.Functions.LeastSquares import leastSquaresFit

    if fit_init == None:
        fit_init = [0,0,0,0,0,1]

    # --The first element specifies the independent variables of the model. 
    # --The second element of each data point tuple is the number that the return value of the model function is supposed to match
    wall=[tuple(( tuple((x[i],y[i])), z[i] )) for i in xrange(len(x))]
    
    optimal_parameter_values, chi_squared=leastSquaresFit(second_order_surface, fit_init, wall, max_iterations=None)
    
    return optimal_parameter_values, chi_squared


def quadratic_plane_fit2( walls ):
    """
    Use non-linear least squares to fit a function, f, to data.
    Assumes ydata = f(xdata, *params) + eps
    The algorithm uses the Levenburg-Marquardt algorithm through leastsq.
    """
    import scipy 
    from scipy.optimize import curve_fit
    
    x,y,z=[],[],[]
    for i in xrange(len(walls)):
        x.extend(list(walls[i][0]))
        y.extend(list(walls[i][1]))
        z.extend(list(walls[i][2]))
    
    optimal_parameter_values, covariance=curve_fit(second_order_surface,[x,y],z)
    
    return optimal_parameter_values, covariance


def principal_curvatures(params):
    """
    Compute principal curvature k1 and k2 from a second order analytic surface of the form z = a1.x^2 + a2.xy + a3.y^2 + a4.x + a5.y + a6.
    """
    # -- We first recover the parameters:
    a1,a2,a3,a4,a5,a6=params
    
    # -- Then we define the parameters E, F and G for the first fundamental form:
    E=1+a4**2
    F=a4*a5
    G=1+a5**2
    
    # -- Then we define the parameters e, f and g for the second fundamental form:    
    e=(2*a1)/float(math.sqrt(E*G-F**2))
    f=(a2)/float(math.sqrt(E*G-F**2))
    g=(2*a3)/float(math.sqrt(E*G-F**2))
    
    # -- We now have to find the roots of the equation : (Fg - Gf) x**2 + (Eg - Ge) x + (Ef - Fe) = 0
    a = (F*g - G*f)
    b = (E*g - G*e)
    c = (E*f - F*e)
    discriminant = b**2 - 4*a*c
    if discriminant > 0:
        x_1 = ( -b-math.sqrt(discriminant) )/float(2*a)
        x_2 = ( -b+math.sqrt(discriminant) )/float(2*a)
    elif discriminant == 0:
        x_1 = x_2 = (-b)/float(2*a)
    else:
        import warnings
        warnings.warn("No real solutions...")
        return 0,0
        
    return (e+f*x_1)/float(E+F*x_1),(e+f*x_2)/float(E+F*x_2)


def extract_L1(image):
    """
    Return the list of all cell labels in the layer 1.

    :Parameters:
        - `image` (|SpatialImage|) - segmented image

    :Returns:
        - `L1` (list)
    """
    return SpatialImageAnalysis(image).L1()
    # L1 = []
    # im = np.zeros_like(image)
    # im[image!=1]=1
    # ero = nd.binary_erosion(im)
    # mask = im - ero
    # res = np.where(mask==1,image,0)
    # for cell in xrange(1,image.max()+1):
        # if cell in res:
            # L1.append(cell)
    # return L1
