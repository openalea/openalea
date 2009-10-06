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

from numpy import zeros,ones, array
from openalea.image.transformations.image_transfo import hsl2rgb,merge_rgbData

class ILookupTable (object) :
    """
    base class for all lookup table
    defining RGB palette for gray tone data images
    """
    def __call__ (self, index) :
        """
        return an RGB tuple associated to a level index
        """
        raise NotImplementedError

class LookupTable (ILookupTable) :
    """
    implementation of ILookupTable using an array
    """
    def __init__ (self, max_index) :
        self._table = zeros( (max_index+1, 3), "int" )

    def max_index(self) :
        return self._table.shape[0]-1

    def table(self) :
        return self._table


    def __call__ (self, index) :
        return tuple(self._table[index, ])

class LookupTableRainbow (LookupTable) :
    """
    implementation of a rainbow LookupTable using an array
    """
    def __init__ (self, max_index) :
        LookupTable.__init__(self, max_index)
        #note that the upper bound is excluded
        H = ([0.7-i*0.7/float(max_index) for i in xrange(0, max_index+1)])
        
        S = ones( (max_index+1, ), "float" )
        L = ones( (max_index+1, ), "float" )/2.0
        R, G, B = hsl2rgb(H, S, L)
        t = array([R, G, B])
        self._table = t.transpose()


def create_rainbow_LUT(max_index):
    lut = LookupTableRainbow(max_index)
    return lut

def rainbow_lut2image(lut) :
    t = array(lut.table())
    print "shape",t.shape
    #a=t.shape
    t = t.transpose()
    return ( merge_rgbData (t[0,], t[1,], t[2,], lut.max_index()+1, 1) )

class LookupFunc (ILookupTable) :
    """
    implementation of ILookupTable using an array
    """
    def __init__ (self, max_index):
        self._imax = float(max_index)

    def __call__ (self, index):
        return (int(index/self._imax*255), int(index/self._imax*255), \
                int(index/self._imax*255))
