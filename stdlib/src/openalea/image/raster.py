# -*- coding: latin-1 -*-
#
#       basics : image package
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA  
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
"""This module provide basics function to handle 2D images"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

import numpy
from numpy import zeros
import Image

class Raster (object) :
    """
    a list of 2D points
    """
    def __init__ (self, nb_points) :
        self._coords=zeros( (nb_points, 2),"int" )

    def nb_points (self)  :
        """
        number of points in the raster
        """
        return self._coords.shape[0]
    
    def __len__ (self) :
        return self.nb_points()
    
    def point (self, ind) :
        """
        return point coordinates
        """
        return self._coords[ind,]
    
    def points (self) :
        for i in xrange(len(self)) :
            yield self.point(i)
    
    def xlist (self) :
        """
        return list of x coordinates
        """
        return self._coords.transpose()[0, ]

    def ylist (self) :
        """
        return list of y coordinates
        """
        return self._coords.transpose()[1, ]

    def bounding_box (self) :
        coords = self._coords.transpose()
        return numpy.min(coords[0, ]), numpy.max(coords[0, ]), \
            numpy.min(coords[1, ]), numpy.max(coords[1, ])
    
    def set_point (self, pt_ind, x, y) :
        self._coords[pt_ind, ] = [x, y]
    
    def mask (self, mask=None) :
        if mask is None :
            xmin, xmax, ymin, ymax = self.bounding_box()
            mask = Image.new("L", (xmax-xmin+1, ymax-ymin+1), 0)
        else :
            xmin, ymin = 0, 0
        pix = mask.load()
        for x, y in self.points() :
            pix[x-xmin, y-ymin] = 1
        return (xmin, ymin), mask

def create_raster (points) :
    r = Raster(len(points))
    for ind, (x, y) in enumerate(points) :
        r.set_point(ind, x, y)
    return r

if __name__=="__main__" :
    from random import randint
    pts = [ (randint(0, 100), randint(50, 100)) for i in xrange(1000)]
    r = create_raster(pts)
    (xmin,ymin), m = r.mask()
    m.save("mask.png")
