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


    nf = Factory( name="Domain",
                  description="Generates domain tuple",
                  category="Spatial",
                  nodemodule="distribGen",
                  nodeclass="domain",
                  inputs= ( dict( name = "X min", interface=IInt, value = 0, showwidget=True ),
                            dict( name = "X max", interface=IInt, value = 1, showwidget=True ),
                            dict( name = "Y min", interface=IInt, value = 0, showwidget=True ),
                            dict( name = "Y max", interface=IInt, value = 1, showwidget=True ),
                            dict( name = "Scale factor", interface=IFloat(min=1, step=10), value = 1, showwidget=True ),
                          ),
                  outputs=( dict( name = "domain2D", ),
                          ),
                  )

    package.add_factory( nf )

    nf = Factory( name= "Basic Distribution", 
                  description= "Basic spatial distributions", 
                  category = "Spatial", 
                  nodemodule = "distribGen",
                  nodeclass = "basic_distrib",
                  )

    package.add_factory( nf )

    nf = Factory( name= "Aggregative Distribution", 
                  description= "clustered distributions", 
                  category = "Spatial", 
                  nodemodule = "distribGen",
                  nodeclass = "aggregative_distrib",
                  )

    package.add_factory( nf )

    nf = Factory( name="Random 2D",
                  description="Generates random spatial distribution in a 2D domain",
                  category="Spatial",
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

    package.add_factory( nf )


    nf = CompositeNodeFactory(name='Spatial Distribution', 
                              description='', 
                              category='Spatial',
                              doc='',
                              inputs=[{'interface': IInt, 'name': 'Size', 'value': 10}],
                              outputs=[{'interface': ISequence, 'name': 'X'}, 
                                       {'interface': ISequence, 'name': 'Y'}],
                              elt_factory={2: ('spatial', 'Basic Distribution'), 
                                           3: ('spatial', 'Random 2D'), 
                                           4: ('spatial', 'Domain')},

                              elt_connections={147103624: (2, 0, 3, 1), 147103612: (4, 0, 3, 2), 147103588: (3, 1, '__out__', 1), 147103636: ('__in__', 0, 3, 0), 147103600: (3, 0, '__out__', 0)},
                              elt_data={3: 
{'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Random 2D', 'posx': 140.0, 'posy': 228.75, 'minimal': False}, 2: {'lazy': True, 'hide': False, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Basic Distribution', 'posx': 140.0, 'posy': 122.5, 'minimal': False}, '__in__': {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'In', 'posx': 20.0, 'posy': 5.0, 'minimal': False}, 4: {'lazy': True, 'hide': False, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Domain', 'posx': 308.75, 'posy': 131.25, 'minimal': False}, '__out__': {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Out', 'posx': 152.5, 'posy': 306.25, 'minimal': False}},
                              elt_value={3: [], 2: [(0, "'Random'")], '__in__': [], 4: [(0, '0'), (1, '1'), (2, '0'), (3, '1')], '__out__': []},
                              lazy=True,
                              )

    package.add_factory(nf)




###### end nodes definitions ###############

    pkg_manager.add_package(package)
