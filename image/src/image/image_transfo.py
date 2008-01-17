# -*- python -*-
# -*- coding: latin-1 -*-
#
#       basics : image package
#
#       Copyright or © or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Da SILVA David <david.da_silva@cirad.fr>
#			Jerome Chopard <jerome.chopard@sophia.inria.fr>
#			Fernandez Romain <romain.fernandez@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

__doc__="""
This module provide basics function to handle 2D images
"""

__license__= "Cecill-C"
__revision__=" $Id: graph.py 116 2007-02-07 17:44:59Z tyvokka $ "

import Image
import numpy
from Image import Image as Im

def blend (image1, image2, alpha) :
    return Image.blend(image1,image2,alpha)

blend.__doc__=Image.blend.__doc__

def composite (image1, image2, mask) :
    return Image.composite(image1,image2,mask)

composite.__doc__=Image.composite.__doc__

def merge (mode, bands) :
    return Image.merge(mode,bands)

merge.__doc__=Image.merge.__doc__

def merge_rgb (R=None, G=None, B=None, A=None) :
    valid_im_list=[channel for channel in (R,G,B,A) if channel is not None]
    if len(valid_im_list)==0 :
        raise UserWarning("at least one band must be a valid image")
    w,h=valid_im_list[0].size
    if R is None :
        R=Image.new("L",(w,h))
    if G is None :
        G=Image.new("L",(w,h))
    if B is None :
        B=Image.new("L",(w,h))
    if A is None :
        im=Image.merge("RGB",(R,G,B))
        im.putalpha(255)
    else :
        im=Image.merge("RGBA",(R,G,B,A))
    return im

merge_rgb.__doc__=Image.merge.__doc__

def paste (image_target, image_source, x, y) :
    """
    paste image_source into image_target at position x,y
    """
    return image_target.paste(image_source,(x,y))

paste.__doc__=Im.paste.__doc__

def fill (image, color, xmin, xmax, ymin, ymax) :
    """
    fill a rectangle region with the given color
    """
    im=image.copy()
    im.paste(color,(xmin,ymin,xmax,ymax))
    return im

def put_alpha (image, band) :
    return image.putalpha(band)

put_alpha.__doc__=Im.putalpha.__doc__

def split(image) :
    return image.split()

split.__doc__=Im.split.__doc__


def __threshold(x, low, high):
    if x < low :
      return 255
    elif x > high :
      return 0
    else :
      return x

def seuillage(image, low, high) :
    width,height = image.size
    imdata = image.getdata()
    tab = numpy.array(imdata)
    thd_img = map( lambda x : __threshold(x, low, high), tab )
    img = Image.new('L', image.size, 0)
    img.putdata(thd_img)
    #matrix = numpy.reshape(th,(width,heigh))
    return img,

