# -*- python -*-
#
#       OpenAlea.Image
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA  
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################
"""Node declaration for image
"""

__license__ = "Cecill-C"
__revision__ = " $Id: __wralea__.py 2585 2010-07-02 15:28:03Z chopard $ "

from openalea.core import *
from openalea.image_wralea import IImage

__name__ = "openalea.image.serial"

__all__ = []

load = Factory(name = "load",
                description = "load image",
                category = "datatype,image",
                nodemodule = "serial",
                nodeclass = "load",
                inputs = (dict(name = "name", interface = IFileStr),),
                outputs = (dict(name = "img", interface = IImage),),
                )

__all__.append("load")


