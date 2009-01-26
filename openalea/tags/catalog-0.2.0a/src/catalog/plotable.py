# -*- python -*-
#
#       OpenAlea Library: OpenAlea Library module
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): David Da SILVA <david.da_silva@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

__doc__="""
Definition of plotable object
"""

__license__= "Cecill-C"
__revision__=" $Id$ "

"""
:Abstract: Contain definition of plotable object
"""

class plotObject:

    def __init__( self, x, y, legend, linestyle, marker, color, ):
        self.x = x
        self.y = y
        self.legend = str(legend)
        self.linestyle = str(linestyle)
        self.marker = str(marker)
        self.color = str(color)

    def __call__(self, inputs = ()):
        pass
