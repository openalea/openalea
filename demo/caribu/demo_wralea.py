# -*- python -*-

from openalea.core import *


def register_packages(pkgmanager):

    metainfo = dict(version='0.1.0',
                    license='CECILL',
                    authors='C. Pradal, C. Fournier',
                    institutes='INRA/CIRAD',
                    description='Tools to explore and display Canestra files.',
                    url='http://openalea.gforge.inria.fr'
                    )


    package = Package("Demo.Caribu.Visualisation", metainfo)
    
    nf = CompositeNodeFactory(name='plot_can_file_with_colors', 
                              description='', 
                              category='Visualisation.Caribu',
                              doc='',
                              inputs=[],
                              outputs=[],
                              elt_factory={2: ('Catalog.Maths', 'min'), 
                              3: ('Caribu.Visualisation', 'Read Vec File'), 
                              4: ('Catalog.Maths', 'max'), 
                              5: ('Catalog.Color', 'ColorMap'), 
                              6: ('Catalog.Functional', 'map'), 
                              7: ('Caribu.Visualisation', 'Plot Can File')},

                              elt_connections={ 9720068: (5, 0, 6, 0), 
                                                9720104: (3, 0, 2, 0), 
                                                9720044: (6, 0, 7, 1), 
                                                9720080: (2, 0, 5, 1), 
                                                9720116: (4, 0, 5, 2), 
                                                9720056: (3, 0, 4, 0), 
                                                9720092: (3, 0, 6, 1)},
                              elt_data={ 2: {'lazy': True, 
                                             'hide': True, 
                                             'port_hide_changed': set([]), 
                                             'priority': 0, 
                                             'caption': 'min', 
                                             'posx': 347.5, 
                                             'posy': 128.75, 
                                             'minimal': False}, 
                                         3: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Read Vec File', 'posx': 351.25, 'posy': 31.25, 'minimal': False}, 
                                         4: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'max', 'posx': 435.0, 'posy': 128.75, 'minimal': False}, 
                                         5: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'ColorMap', 'posx': 360.0, 'posy': 225.0, 'minimal': False}, 
                                         6: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'map', 'posx': 501.25, 'posy': 272.5, 'minimal': False}, 
                                         7: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Plot Can File', 'posx': 397.5, 'posy': 333.75, 'minimal': False}, 
                                         '__out__': {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Out', 'posx': 20.0, 'posy': 250.0, 'minimal': False}, 
                                         '__in__': {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'In', 'posx': 20.0, 'posy': 5.0, 'minimal': False}},
                              elt_value={2: [], 3: [(0, "'D:/pradal/devlp/alea/tutorial01/caribu/Eabs.vec'")], 4: [], 5: [(0, 'None'), (3, '250.0'), (4, '20.0')], 6: [], 7: [(0, "'D:/pradal/devlp/alea/tutorial01/caribu/scene.can'")], '__out__': [], '__in__': []},
                              lazy=True,
                              )

    pkg.add_factory(nf)


    pkgmanager.add_package(pkg)


