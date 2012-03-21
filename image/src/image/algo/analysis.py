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
from scipy import ndimage

from openalea.image.spatial_image import SpatialImage

def dilation(slices):
    return [ slice(max(0,s.start-1), s.stop+1) for s in slices]

def wall(mask_img,label_id):
    img = (mask_img == label_id)
    dil = ndimage.binary_dilation(img)
    contact = dil - img
    return mask_img[contact]
    
def contact_surface(mask_img,label_id):
    img = wall(mask_img,label_id)
    return set(np.unique(img))

def real_indices(slices, resolutions):
    return [ (s.start*r, s.stop*r) for s,r in zip(slices,resolutions)]
    
def hollow_out_cells(mat):
    """
    Laplacian filter used to dectect and return an Spatial Image containing only cell walls.
    (The Laplacian of an image highlights regions of rapid intensity change.)
    :INPUT:
        .mat: Spatial Image containing cells (segmented image)
    :OUTPUT:
        .mat: Spatial Image containing hollowed out cells (cells walls from full segmented image)
    """
    print 'Hollowing out cells...'
    b=nd.laplace(mat)
    mat[b==0]=0
    mat[np.where(mat==1)]=0
    print 'Done !!'
    return mat
    
def cells_walls_detection(mat, hollowed_out=False):
    """
    :INPUT:
        .mat: Spatial Image containing cells (segmented image)
    :OUTPUT:
        .x,y,z: coordinates of the cells' boundaries (walls)
    """
    if not hollowed_out:
        mat=hollow_out_cells(mat)
    print 'Extracting cell walls coordinates...'
    x,y,z=np.where(mat!=0)
    print 'Done !!'
    return list(x),list(y),list(z)

def extraction_vertex(mat,display=False,display_edges=False,remove_borders=False):
    """
    Calculates cell's vertices positions according to the rule: a vertex is the point where you can find 4 differents cells (in 3D!!)
    For the surface, the outer 'cell' #1 is considered as a cell.
    
    :INPUTS:
        .mat: Spatial Image containing cells (segmented image). Can be a full spatial image or an extracted surface.
        .display: boolean defining if the function should open an mlab window to represent the cells and the vertex (red cubes)
        .remove_borders: boolean defining if the function sould try to remove cells at the border of the stack before representation.
    
    :OUTPUT:
        .Bary_vrtx: 
            *keys = the 4 cells ids associated with the vertex position(values);
            *values = 3D coordinates of the vertex in the Spatial Image;
    """
    x,y,z=cells_walls_detection(mat)
    ## Compute vertices positions by findind the voxel belonging to each vertex.
    print 'Compute cell vertex positions...'
    Vvox_c={}
    Evox_c={}
    dim=len(x)
    for n in xrange(dim):
        if n%20000==0:
            print n,'/',dim
        i,j,k=x[n],y[n],z[n]
        sub=mat[(i-1):(i+2),(j-1):(j+2),(k-1):(k+2)] # we generate a sub-matrix...
        sub=tuple(np.unique(sub)) 
        # -- Now we detect voxels defining cells' vertices.
        if (len(sub)==4): # ...in which we search for 4 different labels
            if Vvox_c.has_key(sub):
                Vvox_c[sub]=np.vstack((Vvox_c[sub],np.array((i,j,k)).T)) # we group voxels defining the same vertex by the IDs of the 4 cells.
            else:
                Vvox_c[sub]=np.ndarray((0,3))
        # -- If asked, we detect voxels defining cells' edges (an edge is where you can find4 differents cells -in 3D!!-).
        if display_edges:
            if (len(sub)==3):# ...in which we search for 3 different labels
                if Evox_c.has_key(sub):
                    Evox_c[sub]=np.vstack((Evox_c[sub],np.array((i,j,k)).T))
                else:
                    Evox_c[sub]=np.ndarray((0,3))
    ## Compute the barycenter of the voxels associated to each vertex (correspondig to the 3 cells detected previously).
    Bary_vrtx={}
    for i in Vvox_c.keys():
        Bary_vrtx[i]=np.mean(Vvox_c[i],0)
    print 'Done !!'

    if display:
        Vvox_x,Vvox_y,Vvox_z=[],[],[]
        Bary_vrtx_x,Bary_vrtx_y,Bary_vrtx_z=[],[],[]
        for i in Vvox_c.keys():
            if len(Vvox_c[i]) != 0:
                Vvox_x+=list(Vvox_c[i][:,0])
                Vvox_y+=list(Vvox_c[i][:,1])
                Vvox_z+=list(Vvox_c[i][:,2])
                Bary_vrtx_x.append(np.mean(Vvox_c[i][:,0]))
                Bary_vrtx_y.append(np.mean(Vvox_c[i][:,1]))
                Bary_vrtx_z.append(np.mean(Vvox_c[i][:,2]))
        print 'Generating mlab representation of the surface. Red cube indicate the location of the vertices.'
        around=np.vectorize(np.around)
        intv=np.vectorize(int)
        s=mat[intv(around(Bary_vrtx_x)),intv(around(Bary_vrtx_y)),intv(around(Bary_vrtx_z))]
        mlab.figure(size=(800, 800))
        mlab.points3d(Bary_vrtx_x,Bary_vrtx_y,Bary_vrtx_z,s,mode="cube",scale_mode='none',scale_factor=2,color=(1,0,0),opacity=0.6)
        if display_edges:
            mlab.points3d(Evox_c[0],Evox_c[1],Evox_c[2],s,mode="cube",scale_mode='none',scale_factor=1,color=(0,0,0),opacity=0.3)
        x,y,z=cells_walls_detection(mat)        
        mlab.points3d(x,y,z,mat[x,y,z],mode="point",scale_mode='none',scale_factor=0.3,colormap='prism')
        mlab.show()

    return Bary_vrtx


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
        self._labels = self.__labels()
        self._bbox = None
        self._kernels = None
        self._neighbors = None
    
    
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
        # center = ndimage.center_of_mass(img_as_float, img_as_float, index=labels)

        center = ndimage.center_of_mass(self.image, self.image, index=labels)
        
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
        
        volume = ndimage.sum(np.ones_like(self.image), self.image, index=labels)

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
            self._bbox = ndimage.find_objects(self.image)
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
        { 7:[1, 2, 3, 4, 5]}

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
            return dict([(labels,self._neighbors_with_mask(labels))])
        else:
            return self._neighbors_from_list_with_mask(labels)

    def _neighbors_with_mask(self,labels):
        if not self._neighbors is None:
            return { labels:self._neighbors[labels] }
        
        slices = self.boundingbox(labels)
        
        ex_slices = dilation(slices)
        mask_img = self.image[ex_slices]
        return list(contact_surface(mask_img,labels))

        
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
            dil = ndimage.binary_dilation(mask_img, structure=xyz_kernels[a])
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

        >>> analysis.all_wall_surfaces({ 1 : [2, 3], 2 : [6] })
       {(1, 2): 5.0, (1, 3): 4.0, (2, 6): 2.0 }
        
        >>> analysis.all_wall_surfaces()
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
    
    def L1(self, background = 1):
        return self.neighbors(background)
        
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
    # ero = ndimage.binary_erosion(im)
    # mask = im - ero
    # res = np.where(mask==1,image,0)
    # for cell in xrange(1,image.max()+1):
        # if cell in res:
            # L1.append(cell)
    # return L1
