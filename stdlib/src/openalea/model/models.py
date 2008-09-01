# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006 - 2008 INRIA - CIRAD - INRA  
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################


__doc__=""" Model nodes """
__license__= "Cecill-C"
__revision__=" $Id$ "


from openalea.core import global_module


def linearmodel(x=0., a=0., b=0.):
    """ return a*x + b  """
    
    return a*x + b


