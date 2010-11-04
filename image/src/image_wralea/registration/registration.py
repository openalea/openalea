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

from openalea.image import cp2transfo, SpatialImage

def wra_points2transfo (image1,points1,image2,points2) :

    points1 = np.array(points1)
    points2 = np.array(points2)

    if not isinstance(image1,SpatialImage) :
	image1 = SpatialImage(image1)

    if not isinstance(image2,SpatialImage) :
	image2 = SpatialImage(image2)
    
    vrx = image1.resolution[0]
    vry = image1.resolution[1]
    vrz = image1.resolution[2]
    vfx = image2.resolution[0]
    vfy = image2.resolution[1]
    vfz = image2.resolution[2]

    # explain in the voxel world
    points1[:,0] *= vrx
    points1[:,1] *= vry
    points1[:,2] *= vrz
    points2[:,0] *= vfx
    points2[:,1] *= vfy
    points2[:,2] *= vfz

    T = cp2transfo(points1,points2)
    return T,
