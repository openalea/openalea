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


class SpatialImageAnalysis(object):
    """
    This object can extract a number of geometric estimator from a SpatialImage,
    each cells volume, neighborhood structure and the shared surface area of two neighboring cells.
    """

    def __init__(self,image):
        """
        ..warning :: Label features in the images are an arithmetic progression of continous integers.
        """
        if not isinstance(image,SpatialImage):
            self.image = SpatialImage(image)
        else:
            self.image = image

    def _region(self, label):
        """
        """
        _coords = ndimage.find_objects(self.image==label)[0]

        if self.image.ndim == 2 :
            _x,_y = _coords
            _xmax,_ymax = self.image.shape

            _neighbors = list()
            for i in xrange(_x.start,_x.stop):
                for j in xrange(_y.start,_y.stop):
                    if self.image[slice(i,i+1),slice(j,j+1)] == label:
                        _neighbors += list(np.unique(self.image[slice(i-1,i),slice(j,j+1)]))
                        _neighbors += list(np.unique(self.image[slice(i+1,i+2),slice(j,j+1)]))
                        _neighbors += list(np.unique(self.image[slice(i,i+1),slice(j-1,j)]))
                        _neighbors += list(np.unique(self.image[slice(i,i+1),slice(j+1,j+2)]))

            return _neighbors

        elif self.image.ndim == 3 :
            _x,_y,_z = _coords
            _xmax,_ymax,_zmax = self.image.shape

            _neighbors = list()
            for i in xrange(_x.start,_x.stop):
                for j in xrange(_y.start,_y.stop):
                    for k in xrange(_z.start,_z.stop):

                        if self.image[slice(i,i+1),slice(j,j+1),slice(k,k+1)] == label:
                            _neighbors += list(np.unique(self.image[slice(i-1,i),slice(j,j+1),slice(k,k+1)]))
                            _neighbors += list(np.unique(self.image[slice(i+1,i+2),slice(j,j+1),slice(k,k+1)]))
                            _neighbors += list(np.unique(self.image[slice(i,i+1),slice(j-1,j),slice(k,k+1)]))
                            _neighbors += list(np.unique(self.image[slice(i,i+1),slice(j+1,j+2),slice(k,k+1)]))
                            _neighbors += list(np.unique(self.image[slice(i,i+1),slice(j,j+1),slice(k-1,k)]))
                            _neighbors += list(np.unique(self.image[slice(i,i+1),slice(j,j+1),slice(k+1,k+2)]))

            return _neighbors


    def _neighbors(self,label):
        """
        """
        if label != 1:
            _labels = self._region(label)
            _neighbors = list(set(_labels))
            neighbors = [x for x in _neighbors if x!=label]
            return len(neighbors), neighbors
        else:
            print 'Label 1 is the background, not a valid cell.'


    def nlabels(self):
        """
        Return the number of labels.

        :Examples:

        >>> import numpy as np
        >>> a = np.array([[1, 2, 7, 7, 1, 1],
                          [1, 6, 5, 7, 3, 3],
                          [2, 2, 1, 7, 3, 3],
                          [1, 1, 1, 4, 1, 1]])

        >>> from openalea.image.algo.analysis import ImageAnalysis
        >>> analysis = ImageAnalysis(a)

        >>> analysis.nlabels()
        7
        """
        return self.image.max()


    def center_of_mass(self,labels=None, real=True):
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

        >>> from openalea.image.algo.analysis import ImageAnalysis
        >>> analysis = ImageAnalysis(a)

        >>> analysis.center_of_mass(7)
        [0.75, 2.75]

        >>> analysis.center_of_mass([7,2])
        [[0.75, 2.75], [1.3333333333333333, 0.66666666666666663]]

        >>> analysis.center_of_mass()
        [[1.8, 2.2999999999999998],
         [1.3333333333333333, 0.66666666666666663],
         [1.5, 4.5],
         [3.0, 3.0],
         [1.0, 2.0],
         [1.0, 1.0],
         [0.75, 2.75]]
        """
        if labels is None:
            center = ndimage.center_of_mass(self.image.astype(np.float), self.image.astype(np.float), index=xrange(1,self.image.max()+1))
        else:
            center = ndimage.center_of_mass(self.image.astype(np.float), self.image.astype(np.float), index=labels)

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

        >>> from openalea.image.algo.analysis import ImageAnalysis
        >>> analysis = ImageAnalysis(a)

        >>> analysis.volume(7)
        4.0

        >>> analysis.volume([7,2])
        [4.0, 3.0]

        >>> analysis.volume()
        [10.0, 3.0, 4.0, 1.0, 1.0, 1.0, 4.0]
        """
        if labels is None:
            volume = ndimage.sum(np.ones_like(self.image), self.image, xrange(1,self.image.max()+1))
        else:
            volume = ndimage.sum(np.ones_like(self.image), self.image, index=labels)

        if real is True:
            if self.image.ndim == 2:
                volume = np.multiply(volume,(self.image.resolution[0]*self.image.resolution[1]))
            elif self.image.ndim == 3:
                volume = np.multiply(volume,(self.image.resolution[0]*self.image.resolution[1]*self.image.resolution[2]))
            return volume.tolist()
        else:
            return volume


    def neighbors(self,labels=None):
        """
        Return the list of neighbors of a label.

        :Examples:

        >>> import numpy as np
        >>> a = np.array([[1, 2, 7, 7, 1, 1],
                          [1, 6, 5, 7, 3, 3],
                          [2, 2, 1, 7, 3, 3],
                          [1, 1, 1, 4, 1, 1]])

        >>> from openalea.image.algo.analysis import ImageAnalysis
        >>> analysis = ImageAnalysis(a)

        >>> analysis.neighbors(7)
        [(5, [1, 2, 3, 4, 5])]

        >>> analysis.neighbors([7,2])
        [(5, [1, 2, 3, 4, 5]), (3, [1, 6, 7])]

        >>> analysis.neighbors()
        [None,
         (3, [1, 6, 7]),
         (2, [1, 7]),
         (2, [1, 7]),
         (3, [1, 6, 7]),
         (3, [1, 2, 5]),
         (5, [1, 2, 3, 4, 5])]
        """
        if labels is None:
            labels = xrange(1,self.image.max()+1)
        elif not isinstance (labels, list):
            labels = [labels]
        neighbors = map(self._neighbors,labels)
        return neighbors

    def all_neighbors(self):
        slice_label = ndimage.find_objects(img)[1:]
        for label, slices in enumerate(slice_label):
            # label_id = label +2 because the label_id begin at 2
            # and the enumerate begin at 0.
            label_id = label+2

            # sometimes, the label doesn't exist ans slices is None
            if slices is None:
               continue

            ex_slices = dilation(slices)
            mask_img = img[ex_slices]
            #neigh = compute_neigh(label_id, slices, img)
            neigh = list(contact_surface(mask_img,label_id))

            edges[label_id]=neigh



    def surface_area(self,label1,label2,real=True):
        """
        Return the surface of contact between two labels.

        :Examples:

        >>> import numpy as np
        >>> a = np.array([[1, 2, 7, 7, 1, 1],
                          [1, 6, 5, 1, 3, 3],
                          [2, 2, 1, 1, 3, 3],
                          [1, 1, 1, 4, 1, 1]])

        >>> from openalea.image.algo.analysis import ImageAnalysis
        >>> analysis = ImageAnalysis(a)

        >>> analysis.surface_area(7,2)
        1
        """
        _labels = self._region(label1)
        surface = [x for x in _labels if x==label2]
        if real is True:
            surface = len(surface) * reduce(lambda x,y:x*y,self.image.resolution)
        else:
            surface = len(surface)
        return surface


def extract_L1(image):
    """
    Return the list of all cell labels in the layer 1.

    :Parameters:
        - `image` (|SpatialImage|) - segmented image

    :Returns:
        - `L1` (list)
    """
    L1 = []
    im = np.zeros_like(image)
    im[image!=1]=1
    ero = ndimage.binary_erosion(im)
    mask = im - ero
    res = np.where(mask==1,image,0)
    for cell in xrange(1,image.max()+1):
        if cell in res:
            L1.append(cell)
    return L1
