# -*- python -*-
#
#       OpenAlea.Core.Library: OpenAlea Core Library module
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Da SILVA David <david.da_silva@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#


__doc__="""
Wralea for Catalog.stats 
"""

__license__= "Cecill-C"
__revision__=" $Id$ "



from openalea.core import *

def register_packages(pkgmanager):
    """ Initialisation function
    Return a list of package to include in the package manager.
    This function is called by the package manager when it is updated
    """


    metainfo={ 'version' : '0.0.1',
               'license' : 'CECILL-C',
               'authors' : 'OpenAlea Consortium',
               'institutes' : 'INRIA/CIRAD',
               'description' : 'Catalog library.',
               'url' : 'http://openalea.gforge.inria.fr'
               }


    package = Package("Catalog.Stats", metainfo)

###### begin nodes definitions #############

    nf = Factory( name="LinearRegression",
                  description="compute the linear regression",
                  category="Stat",
                  nodemodule="stats",
                  nodeclass="LinearRegression",
                  inputs= ( dict( name = "X", interface=None, value=None ),
                            dict( name = "Y", interface=None, value=None ),
                            dict( name = "alpha", interface=IFloat, value=5. ),
                            dict( name = "origin", interface=IBool, value=False ),
                          ),
                  outputs=(dict(name="reg", interface = IDict),
                          ),
                  )

    package.add_factory( nf )

    nf = Factory( name="LRtoPlot",
                  description="generate plotable object from linear regression",
                  category="Stat",
                  nodemodule="stats",
                  nodeclass="LR2Plot",
                  inputs= ( dict( name='reg', interface=IDict ),
                            dict( name='pointLegend', interface=IStr, value='Data' ),
                            dict( name='pointMarker', interface=IStr, value='^' ),
                            dict( name='pointColor', interface=IStr, value='dodgerblue' ),
                            dict( name='regLineStyle', interface=IStr, value='-' ),
                          ),
                  outputs=( dict(name='plotObjList', interface=None),
                          ),
                  )

    package.add_factory( nf )


###### end nodes definitions ###############

    pkgmanager.add_package(package)


