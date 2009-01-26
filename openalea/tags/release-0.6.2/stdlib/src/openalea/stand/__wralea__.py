# -*- python -*-
#
#       OpenAlea.Core.Library: OpenAlea Core Library module
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA  
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

__name__ = 'vplants.stand'
__alias__ = ['stand']

__version__ = '0.0.1'
__license__ = 'CECILL-C'
__authors__ = 'F. Boudon and D. Da Silva'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'Spatial distribution module.'
__url__ = 'http://www.scipy.org'
               
    
__all__ = ['stand_pos', 'stand_dresser']    

stand_pos = Factory( name="Stand Positioner",
                     description="Add spatial position to each object from list",
                     category="scene",
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


stand_dresser = Factory( name="Stand Dresser",
                         description="Add geometry to each object from list",
                         category="scene",
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



