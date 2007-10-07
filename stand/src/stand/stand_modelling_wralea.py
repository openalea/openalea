# -*- python -*-
#
#       OpenAlea.Core.Library: OpenAlea Core Library module
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): BOUDON Frederic <frederic.boudon@cirad.fr>
#                       Da SILVA David <david.da_silva@cirad.fr>
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
    
    
    package = Package("stand", metainfo)
    
    
###### begin nodes definitions #############

    nf = Factory( name="Stand Positioner",
                  description="Add spatial position to each object from list",
                  category="Stand",
                  nodemodule="stand_modelling",
                  nodeclass="stand_positioner",
                  inputs= ( dict( name = "Object List", interface=ISequence, showwidget = False),
                            dict( name = "X distribution", interface=ISequence, showwidget = False ),
                            dict( name = "Y distribution", interface=ISequence, showwidget = False ),
                            dict( name = "type", interface=IEnumStr(['Position mapping (PM)', 'Best PM', 'Best PM with radius deformation', 'Gibbs']), value = 'Position mapping (PM)', showwidget=True ),
                            dict( name = "parameters", interface=IDict, showwidget=True ),
                          ),
                  outputs=(dict(name="modified object list", interface = ISequence),
                          ),
                  )

    package.add_factory( nf )

    nf = Factory( name="Stand Dresser",
                  description="Add geometry to each object from list",
                  category="Stand",
                  nodemodule="stand_modelling",
                  nodeclass="stand_dresser",
                  lazy = False,
                  inputs= ( dict( name = "Object List", interface=ISequence, showwidget = False),
                            dict( name = "dresser" ),
                            dict( name = "parameters", interface=IDict, showwidget=True ),
                          ),
                  outputs=(dict(name="modified object list", interface = ISequence),
                          ),
                  )

    package.add_factory( nf )


###### end nodes definitions ###############

    pkg_manager.add_package(package)
