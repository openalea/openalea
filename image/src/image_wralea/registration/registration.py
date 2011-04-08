# -*- python -*-
#
#       image: image registration
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
This module import functions to registration images
"""

__license__= "Cecill-C"
__revision__ = " $Id:  $ "

import numpy as np
from openalea.core import Node
from openalea.core import Factory, IFileStr, IInt, IBool, IFloat, \
    ISequence, IEnumStr, IStr, IDirStr, ITuple, IDict
from openalea.image import pts2transfo, angles2transfo



def wra_points2transfo (points1,points2) :
    transformation = pts2transfo(points1,points2)
    return transformation

def wra_angles2transfo (image1, image2, angleX, angleY, angleZ) :
    return angles2transfo(image1, image2, angleX, angleY, angleZ)
