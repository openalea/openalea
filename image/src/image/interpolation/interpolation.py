# -*- python -*-
#
#       image: geometric transform filters
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Eric Moscardi <eric.moscardi@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
"""
This module import functions for Geometric Transformation Filters
"""

__license__= "Cecill-C"
__revision__ = " $Id:  $ "

import numpy as np
from scipy.ndimage import geometric_transform, affine_transform
from ..spatial_image import SpatialImage


__all__ = ["resampling"]

def _apply_field(output_coords,tx,ty,tz):
    return (output_coords[0] + tx[output_coords], output_coords[1] + ty[output_coords], output_coords[2] + tz[output_coords])


def resampling(img, transformation, order=1, output_shape=None, output_voxels=None, mode='constant', cval=0.0, prefilter=True):
    """
    It resamples a 2-D or 3-D image using a 4*4 transformation matrix or a deformation field .

    The value of a point in the result image is determined by spline interpolation of the requested order.

    :Parameters: 
    - `img`

    - `transformation` (array) - Matrix 4x4 or deformation field 
                    
    - `order` (int) - optional
    order corresponds to the degree of a polynomial used to the spline interpolation
    By default, order = 1 (linear interpolation)

    - `output_shape` (tuple) - optional
    The output shape can optionally be given.
    By default, it is equal to the input shape

    - `output_type` (tuple) - optional
    The output data type can optionally be given.
    By default, it is equal to the input data type

    - `output_voxels` (tuple) - optional
    The output voxels size can optionally be given.
    By default, it is equal to the input voxels size

    - `mode` (string) - optional
    Points outside the boundaries of the input are filled 
    according to the given mode ("constant", "nearest", "reflect" or "wrap")                
    By default, the given mode is "constant"

    - `prefilter` (boolean) - optional
    The parameter prefilter determines if the input is pre-filtered before interpolation 
    (necessary for spline interpolation of order > 1)
    If False it is assumed that the input is already filtered

    :Returns Type: image resampled by the transformation
    """

    if transformation.shape != (4,4):
        print('using of a field deformation')
        _tx = transformation[:,:,:,0]
        _ty = transformation[:,:,:,1]
        _tz = transformation[:,:,:,2]

        _data = geometric_transform(img, _apply_field, extra_arguments = (_tx, _ty, _tz), order=order)
        _data = SpatialImage(_data,img.resolution)

        transformation = np.identity(4)

    else:
        if not isinstance(img,SpatialImage) :
	    _data = SpatialImage(img)
        else:
            _data = img

    #extraction of the Rotation and Translation matrix (R,t) 
    _R = transformation[0:3,0:3]
    _t = transformation[0:3,3]
        
    #extraction of voxel size of image
    vx,vy,vz = _data.resolution

    #creating of output
    if output_voxels is None:
        output_voxels = vx,vy,vz
    vox,voy,voz = output_voxels

    #scaling matrix  
    _output_scaling = np.diag([vox,voy,voz])
    _input_scaling = np.diag([1. / vx, 1. / vy, 1. / vz])

    #change of basis
    R = np.dot(_input_scaling, np.dot(_R, _output_scaling) )
    t = np.dot(_input_scaling, _t)

    _output = affine_transform(_data, R, offset = list(t), order=order, output_shape=output_shape, mode=mode, cval=cval, prefilter=prefilter)

    output = SpatialImage(_output, output_voxels)
    return output

