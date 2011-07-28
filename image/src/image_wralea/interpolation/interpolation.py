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

from scipy import ndimage
from openalea.image.interpolation.all import resampling

def wra_shift (img, shift, output, order, mode, cval, prefilter) :
    data = ndimage.shift(input=img, shift=shift, output=output, order=order, mode=mode, cval=cval, prefilter=prefilter)
    return data,

wra_shift.__doc__ = ndimage.shift.__doc__

def wra_rotate (img, angle, axes, reshape, output, order, mode, cval, prefilter) :
    data = ndimage.rotate(input=img, angle=angle, axes=axes, reshape=reshape, output=output, order=order, mode=mode, \
                          cval=cval, prefilter=prefilter)
    return data,

wra_rotate.__doc__ = ndimage.rotate.__doc__

def wra_zoom (img, zoom, output, order, mode, cval, prefilter) :
    data = ndimage.zoom(input=img, zoom=zoom, output=output, order=order, mode=mode, cval=cval, prefilter=prefilter)
    return data,

wra_zoom.__doc__ = ndimage.zoom.__doc__


def crop (img, xmin, ymin, xmax, ymax) :
    data = img[xmin:xmax,ymin:ymax,...]
    return data,

def resample (img, transformation, order=1, output_shape=None, output_voxels=None, mode='constant', cval=0.0, prefilter=True):
    data = resampling(img=img,transformation=transformation,order=order,output_shape=output_shape,output_voxels=output_voxels, \
                            mode=mode,cval=cval,prefilter=prefilter)
    return data,

resample.__doc__ = resampling.__doc__
