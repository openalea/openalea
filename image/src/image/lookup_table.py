# -*- coding: latin-1 -*-
#
#       basics : image package
#
#       Copyright or © or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Da SILVA David <david.da_silva@cirad.fr>
#						Jerome Chopard <jerome.chopard@sophia.inria.fr>
#						Fernandez Romain <romain.fernandez@sophia.inria.fr>
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

from numpy import zeros

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
        self._table=zeros( (max_index+1,3),"int" )

    def __call__ (self, index) :
        return tuple(self._table[index,])

class LookupFunc (ILookupTable) :
    """
    implementation of ILookupTable using an array
    """
    def __init__ (self, max_index) :
        self._imax=float(max_index)

    def __call__ (self, index) :
        return (int(index/self._imax*255),int(index/self._imax*255),int(index/self._imax*255))
