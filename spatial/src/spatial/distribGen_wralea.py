# -*- python -*-
#
#       OpenAlea.Core.Library: OpenAlea Core Library module
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Da SILVA David <david.da_silva@cirad.fr>
#                       BOUDON Frederic <frederic.boudon@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#


from openalea.core import *

def register_packages(pkg_manager):
    
    metainfo={ 'version' : '0.0.1',
               'license' : 'CECILL-C',
               'authors' : 'F. Boudon and D. Da Silva',
               'institutes' : 'INRIA/CIRAD',
               'description' : 'Spatial distribution module.',
               'url' : 'http://www.scipy.org'
               }
    
    
    package = Package("spatial", metainfo)
    
    
###### begin nodes definitions #############

    nf = Factory( name="Spatial Distribution",
                  description="Generates spatials ditributions of different kind",
                  category="Spatial",
                  nodemodule="distribGen",
                  nodeclass="spatial_distrib",
                  inputs= ( dict( name = "n", interface=IInt, value = 100, showwidget=True ),
                            dict( name = "x-range", interface=ISequence, value = [0,1], showwidget= True ),
                            dict( name = "y-range", interface=ISequence, value = [0,1], showwidget=True ),
                            dict( name = "type", interface=IEnumStr(['Random', 'Regular', 'Neman Scott', 'Gibbs']), value = 'Random', showwidget=True ),
                            dict( name = "parameters", interface=IDict, value = {'cluster':5, 'cluster_radius':0.1}, showwidget=True ),
                          ),
                  outputs=( dict( name = "X positions", interface = ISequence ),
                            dict( name = "Y positions", interface = ISequence ),
                          ),
                  )

    package.add_factory( nf )


###### end nodes definitions ###############

    pkg_manager.add_package(package)
