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

from data_image import DataImage

def operation_not (data_im) :
    w, h = data_im.size()
    not_im = DataImage(w, h)
    for i in xrange(w) :
        for j in xrange(h) :
            not_im[i, j] = 1 - data_im[i, j]
    return not_im

__all__ = ["operation_not"]
