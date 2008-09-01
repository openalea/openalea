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

__doc__ = """ catalog.pickle """
__revision__ = " $Id$ "


from openalea.core import *

__name__ = "openalea.pickle"
__alias__ = ["catalog.pickle"]

__version__ = '0.0.1'
__license__ = 'CECILL-C'
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'Python Node library'
__url__ = 'http://openalea.gforge.inria.fr'


__all__ = ['load', 'dump']

load = Factory(name = "pickle load", 
               description = "load pickled data", 
               category = "Python", 
               nodemodule ="pickling",
               nodeclass = "py_load",
               inputs = (dict(name="file_path", interface=IFileStr),
                          ),
               outputs = (dict(name="data", interface=None,),
                          ),
               lazy=False,
               )


dump = Factory(name = "pickle dump", 
               description = "pickled data writer", 
               category = "Python", 
               nodemodule ="pickling",
               nodeclass = "py_dump",
               inputs = (dict(name="data", interface=None,),
                         dict(name="file_path", interface=IFileStr),
                         dict(name="append", interface=IBool, value=False,),
                         ),
               outputs = (),
               lazy=False,
               )

