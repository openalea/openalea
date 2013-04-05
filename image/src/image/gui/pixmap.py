# -*- python -*-
#
#       image: image manipulation GUI
#
#       Copyright 2006 - 2011 INRIA - CIRAD - INRA
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
#                       Eric Moscardi <eric.moscardi@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
################################################################################

"""
This module defines functions to transform images into QPixmaps
"""

__license__= "Cecill-C"
__revision__ = " $Id: __init__.py 2245 2010-02-08 17:11:34Z cokelaer $ "

from openalea.vpltk.qt import qt
#from qt.QtGui import QPixmap,QImage
from numpy import array,zeros,uint32,uint8

from openalea.image.spatial_image import SpatialImage
from openalea.image.gui.palette import palette_factory, from_argb_swap_columns_and_recast

QPixmap = qt.QtGui.QPixmap
QImage = qt.QtGui.QImage

def to_img (img, scalar_type=None, lut=None, forceNativeLut=None) :
    """Transform an image array into a QImage

    :Parameters:
     -`img` (NxMx3 or 4 array of int) - 2D matrix of RGB(A) image pixels
                       i will correspond to y and j to x with origin
                       in the top left corner

    :Returns Type: QImage
    """
    # -- personnal opinion (DB) : there shouldn't be ANY transposition
    # applied automatically in viewing code, except for transpositions
    # explicitly asked by the user view GUI or what. If the image is not
    # properly oriented it is up to the reading code to fix the orientation! --

    try:
        import Image, ImageQt
    except ImportError:
        return None
    #print isinstance(img, SpatialImage)
    if isinstance(img, SpatialImage):
        nb_dim = len(img.shape)
        if nb_dim == 3:
            img = img.transpose(1,0,2)
        elif nb_dim == 4:
            img = img.transpose(1,0,2,3)
        elif nb_dim == 2:
            print "hello world !!"
            img = img.transpose(1,0)
        else:
            raise Exception("Unknown image shape, cannot deduce pixel format")
    _img = Image.fromarray(img)
    pseudo_QImage = ImageQt.ImageQt(_img)
    return pseudo_QImage

    try:
        imgconvarray={
            1:QImage.Format_Indexed8,
            3:QImage.Format_RGB888,
            4:QImage.Format_ARGB32
            }
    except:
        imgconvarray={
            1:QImage.Format_Indexed8,
            4:QImage.Format_ARGB32
            }

    nb_dim = len(img.shape)
    if nb_dim == 3:
        vdim = img.shape[-1]
        img = img.transpose(1,0,2).copy("C")
    elif nb_dim == 4:
        vdim = img.shape[-1]
        img = img.transpose(1,0,2,3).copy("C")
    elif nb_dim == 2:
        vdim = 1
        img = img.transpose(1,0).copy("C")
    else:
        raise Exception("Unknown image shape, cannot deduce pixel format")

    if not img.flags['C_CONTIGUOUS']:
        img = img.copy("C")

    qimg = QImage(img.data,
                  img.shape[1],
                  img.shape[0],
                  imgconvarray[vdim])

    
    return qimg.copy()

def to_img_fast( img, scalar_type=None, lut=None, forceNativeLut=False):
    """Transform an image array into a QImage.

    The implementation tries to minimize data copies and casting by
    determining the exact flags for QImage and feeding it with the
    data pointer.

    :Returns Type: QImage
    """
    import sip

    l_sh = len(img.shape)
    if l_sh == 3:
        vdim = img.shape[2]
        img = img.transpose(1,0,2)
    elif l_sh == 4:
        vdim = img.shape[3]
        img = img.transpose(1,0,0,2)
    elif l_sh == 2:
        vdim = 1
        img = img.transpose(1,0)
    else:
        raise Exception("Unknown image shape, cannot deduce pixel format")


    if vdim == 1: # : We are working on scalar images, this includes argb32 encoded images
        if scalar_type == None:
            # -- make sure we always have a default lut to display indexed things --
            cmax = img.max()
            if lut is None:
                lut = palette_factory("grayscale", cmax)

            # -- if all values fit within a uint8, cast and operate on it.
            # Currently doesn't work on non-square images maybe  because all
            # data is not 32bits aligned.  --
            if forceNativeLut: #cmax <= 255:
                print "using native 8bit color map"
                if img.dtype != uint8 :
                    img = uint8(img)
                qim = QImage(sip.voidptr(img.ctypes.data), img.shape[0], img.shape[1], QImage.Format_Indexed8)
                qim.setColorTable(lut.tolist())
                return qim.copy()

            else:
                # -- QImages currently only allow indexing of 8bit images (up to value 255).
                # This disqualifies anything that has cmax > 255. However, these can be handled
                # on our side by converting them to RGBA and processing them as such --
                # print "casting from indexed to argb32"
                img = lut[img] # : this creates an rgba image (len(shape)==2)
                return to_img(img, scalar_type="argb32")

        elif scalar_type=="argb32":
            print "using native scalar argb32"
            qim = QImage(sip.voidptr(img.ctypes.data), img.shape[0], img.shape[1], QImage.Format_ARGB32).copy()
            return qim

    elif vdim in [3,4]  : # : We are working on vectorial things like RGB ...
        data = img.ctypes.data
        if vdim == 3:
            print "using native vectorial rgb888"
            fmt = QImage.Format_RGB888
        elif vdim == 4: # ... or RGBA
            print "using native vectorial argb32"
            fmt = QImage.Format_ARGB32
        else:
            raise Exception("Unhandled vectorial pixel type")
        qim = QImage(sip.voidptr(data), img.shape[0], img.shape[1], fmt)
        return qim.copy()

    else:
        raise Exception( "Arrays of shape length %s are not handled"%shape_len )


def to_pix( img, scalar_type=None, lut=None, forceNativeLut=False):
    """Transform an image array into a QPixmap

    :Parameters:
     -`img` (NxMx3 or 4 array of int) - 2D matrix of RGB(A) image pixels
                       i will correspond to x and j to y

    :Returns Type: QPixmap
    """
    return QPixmap.fromImage(to_img(img, scalar_type, lut, forceNativeLut) )

def to_tex (img) :
    """Transform an image array into an array usable for texture in opengl

    :Parameters:
     -`img` (NxMx3 or 4 array of int) - 2D matrix of RGB(A) image pixels
                       i will correspond to y and j to x with origin
                       in the top left corner

    :Returns Type: NxMx4 array of uint8
    """
    if img.shape[2] == 4 :
        return array(img,uint8)
    else :
        alpha = zeros(img.shape[:2],uint8) + 255
        ret = array([img[...,0],img[...,1],img[...,2],alpha],uint8)

        return ret.transpose( (1,2,0) )

