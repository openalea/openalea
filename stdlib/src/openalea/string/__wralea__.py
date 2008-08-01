# -*- python -*-
#
#       OpenAlea.Catalog
#
#       Copyright 2006 - 2007 INRIA - CIRAD - INRA  
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################

__doc__ = """ catalog.string """
__revision__ = " $Id$ "


from openalea.core import *


__name__ = "openalea.string"
__alias__ = ["catalog.string"]

__version__ = '0.0.1'
__license__ = 'CECILL-C'
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'String library'
__url__ = 'http://openalea.gforge.inria.fr'


__all__ = ['split', 'join', 'strip']

split = Factory( name="split", 
              description="split a string", 
              category="String", 
              nodemodule="strings",
              nodeclass="str_split",
              
              inputs=(dict(name="String", interface=IStr, value=''),
                      dict(name="Split Char", interface=IStr, value='\n'),
                      ),
              outputs=(dict(name="List", interface=ISequence),),
              )

strip = Factory( name="strip", 
              description="Return a copy of the string s with leading and trailing whitespace removed.", 
              category="String", 
              nodemodule="strings",
              nodeclass="str_strip",
              
              inputs=(dict(name="string", interface=IStr, value=''),
                      dict(name="chars", interface=IStr, value=' '),
                      ),
              outputs=(dict(name="ostring", interface=IStr),),
              )
   
join = Factory( name="join", 
                description="Join a list of string", 
                category="String", 
                nodemodule="strings",
                nodeclass="str_join",
                
                inputs=(dict(name="String List", interface=ISequence, value=[]),
                        dict(name="Join Char", interface=IStr, value='\n'),
                        ),
                outputs=(dict(name="List", interface=IStr),),
                )


