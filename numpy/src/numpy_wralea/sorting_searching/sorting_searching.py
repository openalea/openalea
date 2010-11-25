# -*- python -*-
# -*- coding: latin-1 -*-
#
#       sorting_searching : numpy package
#
#       Copyright 2006 - 2010 INRIA - CIRAD - INRA  
#
#       File author(s): Eric MOSCARDI <eric.moscardi@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
################################################################################

__license__ = "Cecill-C"
__revision__ = " $Id: $ "

import numpy as np

def wra_where(condition, x=None, y=None):
    if x is None or y is None :
        return (np.where(condition))
    else :
        return (np.where(condition,x,y))
