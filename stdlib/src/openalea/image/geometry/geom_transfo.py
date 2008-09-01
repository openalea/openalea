# -*- python -*-
# -*- coding: latin-1 -*-
#
#       basics : image package
#
#       Copyright 2006 - 2008 INRIA - CIRAD - INRA  
#
#       File author(s): Da SILVA David <david.da_silva@cirad.fr>
#                       Jerome Chopard <jerome.chopard@sophia.inria.fr>
#                       Fernandez Romain <romain.fernandez@sophia.inria.fr>
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
from Image import Image as Im
from openalea.image.interface import IPix
from openalea.core import *

def crop (image, xmin, xmax, ymin, ymax) :
    im=image.crop( (xmin,ymin,xmax,ymax) )
    im.load()
    return im

crop.__doc__=Im.crop.__doc__

#def resize (image, width, height, filter_mode=Image.NEAREST) :
#    return image.resize( (width,height), filter_mode )
#
#resize.__doc__=Im.resize.__doc__

#def rotate (image, angle, filter_mode=Image.NEAREST, expand=0) :
#    return image.rotate(angle,filter_mode,expand)
#
#rotate.__doc__=Im.rotate.__doc__

def transform (image, args) :
    raise NotImplementedError

transform.__doc__=Im.transform.__doc__

def mirror (image, horizontal=True) :
    """
    flip the image horizontally or vertically
    """
    if horizontal :
        return image.transpose(Image.FLIP_LEFT_RIGHT)
    else :
        return image.transpose(Image.FLIP_TOP_BOTTOM)

class resize( Node ): 
    mode_func= { "Nearest" : Image.NEAREST,
                  "Bilinear" : Image.BILINEAR,
                  "Bicubic" : Image.BICUBIC,
                  "Antialias" : Image.ANTIALIAS,
              } 
    
    def __init__(self):
    
        Node.__init__(self)

        funs= self.mode_func.keys()
        funs.sort()
        self.add_input( name = "Image", interface = IPix,) 
        self.add_input( name = "Width", label='totot',interface = IInt(min=0), value=314) 
        self.add_input( name = "Height", interface = IInt(min=0), value=159) 
        self.add_input( name = "Mode", interface = IEnumStr(funs), value = funs[-1]) 
        self.add_output( name = "Image", interface = IPix)
        self.__doc__=Im.resize.__doc__

    def __call__(self, inputs):
        im = self.get_input("Image")
        w = self.get_input("Width")
        h = self.get_input("Height")
        fm = self.mode_func[self.get_input("Mode")]
        return im.resize( (w,h), fm )

class rotate( Node ): 
    mode_func= { "Nearest" : Image.NEAREST,
                  "Bilinear" : Image.BILINEAR,
                  "Bicubic" : Image.BICUBIC,
                  "Antialias" : Image.ANTIALIAS,
              } 
    
    def __init__(self):
    
        Node.__init__(self)

        funs= self.mode_func.keys()
        funs.sort()
        self.add_input( name = "Image", interface = IPix,) 
        self.add_input( name = "Angle", interface = IFloat(min=0., max=359.),) 
        self.add_input( name = "Mode", interface = IEnumStr(funs), value = funs[-1]) 
        self.add_input( name = "Expand", interface = IBool, value=True) 

        self.add_output( name = "Image", interface = IPix)
        self.__doc__=Im.rotate.__doc__

    def __call__(self, inputs):
        im = self.get_input("Image")
        angle = self.get_input("Angle")
        fm = self.mode_func[self.get_input("Mode")]
        expand = self.get_input("Expand")
        return im.rotate( angle, fm, expand )


