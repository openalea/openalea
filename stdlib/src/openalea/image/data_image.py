# -*- python -*-
#
#       basics : image package
#
#       Copyright 2006 - 2008 INRIA - CIRAD - INRA  
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

import numpy
from numpy import zeros
import Image

class DataImage (object) :
    """
    an array of pixel containing integrer values
    """
    def __init__ (self, width, height) :
        self._data=zeros( (width,height),"int" )

    def data (self) :
        """
        return the numpy array used to store data
        """
        return self._data
    
    def size (self) :
        return self._data.shape
    
    def pixel (self, x, y) :
        """
        return pixel value
        """
        return self._data[x,y]
    
    def __getitem__ (self, ind) :
        return self._data[ind]
    
    def set_pixel (self, x, y, val) :
        """
        set pixel value
        """
        self._data[x,y]=val
    
    def __setitem__ (self, ind, val) :
        self._data[ind]=val
    
    def extrema (self) :
        """
        return min and max pixel values
        """
        return numpy.min(self._data),numpy.max(self._data)

    def image (self, lookup_table) :
        w,h=self.size()
        im=Image.new("RGB",(w,h))
        pix=im.load()
        for i in xrange(w) :
            for j in xrange(h) :
                pix[i,j]=lookup_table(self[i,j])
        return im

def from_image (im, color_map) :
    """
    create a data image from a pil image
    color_map is function that map a color to an integer
    """
    w,h=im.size
    data_im=DataImage(w,h)
    pix=im.load()
    for i in xrange(w) :
        for j in xrange(h) :
            data_im[i,j]=color_map(pix[i,j])
    return data_im

if __name__ == "__main__" :
    from random import randint
    
    d=DataImage(100,100)
    w,h=d.size()
    max_val=10000
    for i in xrange(w) :
        for j in xrange(h) :
            d[i,j]=(i+w*j)%max_val
    
    def tab (val) :
        return (val*255/max_val,val*255/max_val,val*255/max_val)
    
    im=d.image(tab)
    im.save("toto.png")
