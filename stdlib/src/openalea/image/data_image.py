# -*- python -*-
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


class DataImage (object) :
    """
    an array of pixel containing integrer values
    """
    def __init__ (self, width, height) :
        """todo"""
        self._data = zeros( (width,height),"int" )

    def data(self):
        """
        return the numpy array used to store data
        """
        return self._data
    
    def size(self):
        """todo"""
        return self._data.shape
    
    def pixel(self, x, y):
        """
        return pixel value
        """
        return self._data[x, y]
    
    def __getitem__(self, ind):
        """todo"""
        return self._data[ind]
    
    def set_pixel(self, x, y, val):
        """
        set pixel value
        """
        self._data[x, y] = val
    
    def __setitem__(self, ind, val):
        """todo"""
        self._data[ind] = val
    
    def extrema(self):
        """
        return min and max pixel values
        """
        return numpy.min(self._data), numpy.max(self._data)

    def image(self, lookup_table):
        """ todo """
        w, h = self.size()
        im = Image.new("RGB", (w, h))
        pix = im.load()
        for i in xrange(w):
            for j in xrange(h):
                pix[i, j] = lookup_table(self[i, j])
        return im


def from_image (im, color_map) :
    """
    create a data image from a PIL image
    color_map is function that map a color to an integer
    """
    width, height = im.size
    data_im = DataImage(width, height)
    pix = im.load()
    for i in xrange(width) :
        for j in xrange(height) :
            data_im[i, j] = color_map(pix[i, j])
    return data_im


if __name__ == "__main__" :
    from random import randint
    
    data = DataImage(100, 100)
    width, height = data.size()
    max_val = 10000
    for i in xrange(width) :
        for j in xrange(height) :
            data[i, j] = (i + width * j) % max_val
    
    def tab(val):
        """todo"""
        return (val*255/max_val, val*255/max_val, val*255/max_val)
    
    im = data.image(tab)
    im.save("toto.png")
