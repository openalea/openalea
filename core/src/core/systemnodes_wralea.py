# -*- python -*-
#
#       OpenAlea.Core.Library: OpenAlea Core Library module
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Christophe Pradal <christophe.prada@cirad.fr>
#                       Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#


__doc__="""
Wralea for System nodes
"""

__license__= "Cecill-C"
__revision__=" $Id: python_wralea.py 603 2007-06-21 14:41:17Z dufourko $ "


from openalea.core import *


def register_packages(pkgmanager):
    """ Initialisation function
    Return a list of package to include in the package manager.
    This function is called by the package manager when it is updated
    """

    # Base Library

    metainfo = dict(version='0.0.1',
                    license='CECILL-C',
                    authors='OpenAlea Consortium',
                    institutes='INRIA/CIRAD',
                    description='System Node library.',
                    url='http://openalea.gforge.inria.fr'
                    )


    package = Package("System", metainfo)


    # Factories
    nf = Factory(name="annotation", 
                 description="Annotation", 
                 category="System", 
                 nodemodule="systemnodes",
                 nodeclass="AnnotationNode",
                 )

    package.add_factory(nf)

    
    pkgmanager.add_package(package)

