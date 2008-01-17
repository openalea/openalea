# -*- python -*-
# -*- coding: latin-1 -*-
#
#       SVGWralea : image package
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

from openalea.core import *
from openalea.core.interface import *

def register_packages(pkg_manager):
    
    metainfo={ 'version' : '0.0.1',
               'license' : 'CECILL-C',
               'authors' : 'J. Chopard',
               'institutes' : 'INRIA/CIRAD',
               'description' : 'PIL wrapping and svg module.',
               'url' : 'http://www.svg.org'
               }
    
    
    package = Package("image.svg", metainfo)

    pkg_manager.add_package(package)
