# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA  
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

__name__ = "openalea.spatial"
__alias__ = ["spatial"]

__version__ = '0.0.1'
__license__ = 'CECILL-C'
__authors__ = 'F. Boudon and D. Da Silva'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'Spatial distribution module.',
__url__ = 'http://www.scipy.org'
    
__all__ = ["domain", 'basic_dist', 'aggr_dist', 'rand2d', 'spatial_dist']    
    
###### begin nodes definitions #############


domain = Factory( name="Domain",
                  description="Generates domain tuple",
                  category="Spatial,scene",
                  nodemodule="distribGen",
                  nodeclass="domain",
                  inputs= ( dict( name = "X min", interface=IInt, value = 0, showwidget=True ),
                            dict( name = "X max", interface=IInt, value = 1, showwidget=True ),
                            dict( name = "Y min", interface=IInt, value = 0, showwidget=True ),
                            dict( name = "Y max", interface=IInt, value = 1, showwidget=True ),
                            dict( name = "Scale factor", interface=IFloat(min=1, step=10), 
                                  value = 1, showwidget=True ),
                            ),
                  outputs=( dict( name = "domain2D", ),
                            ),
                  )


basic_dist = Factory( name= "Basic Distribution", 
                      description= "Basic spatial distributions", 
                      category = "Spatial,scene", 
                      nodemodule = "distribGen",
                      nodeclass = "basic_distrib",
                      )


aggr_dist = Factory( name= "Aggregative Distribution", 
                     description= "clustered distributions", 
                     category = "Spatial,scene", 
                     nodemodule = "distribGen",
                     nodeclass = "aggregative_distrib",
                     )


rand2d = Factory( name="Random 2D",
                  description="Generates random spatial distribution in a 2D domain",
                  category="Spatial,scene",
                  nodemodule="distribGen",
                  nodeclass="random2D",
                  inputs= ( dict( name = "n", interface=IInt(min=0), value = 10, showwidget=True ),
                            dict( name = "distribution", interface=IFunction, ),
                            dict( name = "domain2D", interface=None,),
                          ),
                  outputs=( dict( name = "x", interface = ISequence),
                            dict( name = "y", interface = ISequence)
                          ),
                  )




spatial_dist = CompositeNodeFactory(name='Spatial Distribution', 
                              description='', 
                              category='scene,composite,Spatial',
                              doc='',
                              inputs=[  {'interface': IInt, 'name': 'Size', 'value': 10},
                                        {'interface': IInt, 'name': 'Min_x', 'value': 0},
                                        {'interface': IInt, 'name': 'Max_x', 'value': 100},
                                        {'interface': IInt, 'name': 'Min_y', 'value': 0},
                                        {'interface': IInt, 'name': 'Max_y', 'value': 100}],
                                    outputs=[{'interface': ISequence, 'name': 'X'}, 
                                             {'interface': ISequence, 'name': 'Y'}],
                                    elt_factory={  2: ('spatial', 'Basic Distribution'),
                                                   3: ('spatial', 'Random 2D'),
                                                   4: ('spatial', 'Domain')},
                                    elt_connections={  140066612: ('__in__', 4, 4, 3),
                                                       140066624: ('__in__', 3, 4, 2),
                                                       140066636: ('__in__', 2, 4, 1),
                                                       140066648: ('__in__', 1, 4, 0),
                                                       140066660: (3, 0, '__out__', 0),
                                                       140066672: (4, 0, 3, 2),
                                                       140066684: ('__in__', 0, 3, 0),
                                                       140066696: (3, 1, '__out__', 1),
                                                       140066708: (2, 0, 3, 1)},
                                    elt_data={  2: {  'caption': 'Basic Distribution',
                                                      'hide': False,
                                                      'lazy': True,
                                                      'minimal': False,
                                                      'port_hide_changed': set([]),
                                                      'posx': 140.0,
                                                      'posy': 122.5,
                                                      'priority': 0},
                                                3: {  'caption': 'Random 2D',
                                                      'hide': True,
                                                      'lazy': True,
                                                      'minimal': False,
                                                      'port_hide_changed': set([]),
                                                      'posx': 140.0,
                                                      'posy': 228.75,
                                                      'priority': 0},
                                                4: {  'caption': 'Domain',
                                                      'hide': False,
                                                      'lazy': True,
                                                      'minimal': False,
                                                      'port_hide_changed': set([]),
                                                      'posx': 308.75,
                                                      'posy': 131.25,
                                                      'priority': 0},
                                                '__in__': {  'caption': 'In',
                                                             'hide': True,
                                                             'lazy': True,
                                                             'minimal': False,
                                                             'port_hide_changed': set([]),
                                                             'posx': 20.0,
                                                             'posy': 5.0,
                                                             'priority': 0},
                                                '__out__': {  'caption': 'Out',
                                                              'hide': True,
                                                              'lazy': True,
                                                              'minimal': False,
                                                              'port_hide_changed': set([]),
                                                              'posx': 152.5,
                                                              'posy': 306.25,
                                                              'priority': 0}},
                                    elt_value={  2: [(0, "'Random'")],
                                                 3: [],
                                                 4: [(4, '1')],
                                                 '__in__': [],
                                                 '__out__': [(0, '[]'), (1, '[]')]},
                                    lazy=True,
                                    )

