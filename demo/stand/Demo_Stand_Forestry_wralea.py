
# This file has been generated at $TIME

from openalea.core import *

def register_packages(pkgmanager):
    
    metainfo = {'description': 'stand generation from forestry data', 'license': 'CECILL-C', 'url': '', 'version': '0.1', 'authors': 'Da SILVA', 'institutes': 'INRIA CIRAD INRA'} 
    pkg = UserPackage("Demo.Stand.Forestry", metainfo)

    

    nf = CompositeNodeFactory(name='demo_data2scene', 
                              description='scene generation from data', 
                              category='Modelling',
                              doc='',
                              inputs=[],
                              outputs=[],
                              elt_factory={2: ('PlantGL.Dresser', 'PGL Dresser'), 3: ('Catalog.Python', 'fread'), 4: ('Catalog.Csv', 'csv2objs'), 5: ('stand', 'Stand Positioner'), 6: ('spatial', 'Spatial Distribution'), 7: ('Catalog.Functional', 'map'), 8: ('PlantGL Objects', 'Scene'), 9: ('PlantGL Visualization', 'plot3D'), 10: ('PlotTools', 'VS Plot'), 11: ('PlotTools', 'Iterables to Sequence'), 12: ('Catalog.Python', 'len'), 13: ('Catalog.Python', 'flatten'), 14: ('Catalog.Csv', 'obj2cvs'), 15: ('Catalog.Python', 'len')},
                              elt_connections={10755936: (12, 0, 6, 0), 10755840: (3, 0, 4, 0), 10755876: (2, 0, 7, 0), 10755780: (5, 0, 14, 0), 10755912: (6, 1, 5, 2), 10755852: (4, 0, 5, 0), 10755768: (4, 1, 15, 0), 10755948: (4, 0, 12, 0), 10755792: (6, 0, 5, 1), 10755888: (6, 1, 11, 1), 10755816: (7, 0, 13, 0), 10755924: (6, 0, 11, 0), 10755804: (11, 0, 10, 0), 10755864: (13, 0, 8, 0), 10755828: (8, 0, 9, 0), 10755900: (5, 0, 7, 1)},
                              elt_data={2: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'PGL Dresser', 'posx': 81.506887511937762, 'posy': 578.97995956755813, 'minimal': False}, 3: {'lazy': False, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'fread', 'posx': 1.7374072181167435, 'posy': 127.7937510195793, 'minimal': False}, 4: {'lazy': False, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'csv2objs', 'posx': 106.73865934583375, 'posy': 142.28376433722542, 'minimal': False}, 5: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Stand Positioner', 'posx': 87.633671886223624, 'posy': 424.33146387013517, 'minimal': False}, 6: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Spatial Distribution', 'posx': 209.94540429536852, 'posy': 312.24872851539288, 'minimal': False}, 7: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'map', 'posx': 187.19570201467354, 'posy': 670.05564365999999, 'minimal': False}, 8: {'lazy': False, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Scene', 'posx': 168.64473707118066, 'posy': 833.83380318592208, 'minimal': False}, 9: {'lazy': False, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'plot3D', 'posx': 147.55039212416955, 'posy': 925.61431818813912, 'minimal': False}, 10: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'VS Plot', 'posx': 508.62972806249843, 'posy': 469.8717913596206, 'minimal': False}, 11: {'lazy': False, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Iterables to Sequence', 'posx': 395.79935672258591, 'posy': 349.85798334477477, 'minimal': False}, 12: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'len', 'posx': 189.9441796412533, 'posy': 253.67641861801565, 'minimal': False}, 13: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'flatten', 'posx': 172.50171960804576, 'posy': 741.91005070363042, 'minimal': False}, 14: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'obj2cvs', 'posx': 305.0, 'posy': 572.5, 'minimal': False}, 15: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'len', 'posx': 243.6941796412533, 'posy': 197.42641861801565, 'minimal': False}, '__out__': {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Out', 'posx': 20.0, 'posy': 250.0, 'minimal': False}, '__in__': {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'In', 'posx': 20.0, 'posy': 5.0, 'minimal': False}},
                              elt_value={2: [(0, 'None'), (1, "'AsymetricSwung'"), (2, '{}')], 3: [(0, "'D:/Fred/Mes Documents/Develop/openalea/demo/stand/placette3_openalea.csv'")], 4: [(1, "','"), (2, "'\\n'")], 5: [(3, "'Position mapping (PM)'"), (4, '{}')], 6: [(1, '[-1675, 1977]'), (2, '[-2094, 1617]'), (3, "'Random'"), (4, "{'cluster': 10, 'cluster_radius': 500}")], 7: [], 8: [], 9: [], 10: [(1, "'PointLine'"), (2, "'MyPlot'"), (3, "'x-axis-label'"), (4, "'y-axis-label'"), (5, '0')], 11: [], 12: [], 13: [], 14: [(1, "','"), (2, "'\\n'")], 15: [], '__out__': [], '__in__': []},
                              lazy=True,
                              )

    pkg.add_factory(nf)


    pkgmanager.add_package(pkg)


