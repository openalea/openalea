# -*- python -*-
#
#       OpenAlea.Core.Library: OpenAlea Core Library module
#
#       Copyright 2006 INRIA - CIRAD - INRA  
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
import os

def image_size(width, height):
  return (int(width), int(height)),


def PIL2Qt(pil_img):
  file = os.path.join(os.path.abspath(os.curdir), 'imgTmp.jpg')
  pil_img.save(file, "JPEG")
  qpix = QtGui.QPixmap(file)
  os.remove(file)
  return qpix,


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
  
    return QtGui.QPixmap(filename),




