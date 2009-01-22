# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA  
#
#       File author(s): Da SILVA David <david.da_silva@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#


from openalea.core import *
from PyQt4 import QtGui
import Image
import os

def image_size(width, height):
  return (int(width), int(height)),

class Pix(Node):
    """
Text Variable
Input 0 : The stored image
Ouput 0 : Transmit the stored image
    """

    def __call__(self, inputs):
        """ inputs is the list of input values """
        return ( str(inputs[0]), )


def loadimage(filename):
    """
Load an image from a file:
Input 0 : File name
Output 0 : Image object
    """
    img_pil = Image.open(filename)
    return img_pil,

def rotate(img, angle, clockwise=False):
  if clockwise:
    angle = -angle
  return img.rotate(angle)

def perspectiveTransform(img):
        # this is just an example to demonstrate that one can do
        # perspective transformations with PIL (something not
        # supported with Qt, it "only" can do affine transformations).
        size = img.size
        return img.transform(size,Image.PERSPECTIVE,[2,0,0,0,2,0,0.002,0.002,1],Image.BILINEAR)
        



