
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
                              elt_factory={2: ('PlantGL.Dresser', 'PGL Dresser'), 3: ('Catalog.Python', 'fread'), 4: ('Catalog.Csv', 'csv2objs'), 5: ('stand', 'Stand Positioner'), 6: ('spatial', 'Spatial Distribution'), 7: ('Catalog.Functional', 'map'), 8: ('PlantGL Objects', 'Scene'), 9: ('PlantGL Visualization', 'plot3D'), 10: ('PlotTools', 'VS Plot'), 11: ('PlotTools', 'Iterables to Sequence'), 12: ('Catalog.Python', 'len'), 13: ('Catalog.Python', 'flatten'), 14: ('System', 'annotation'), 15: ('System', 'annotation'), 16: ('System', 'annotation'), 17: ('System', 'annotation'), 18: ('System', 'annotation'), 19: ('System', 'annotation')},
                              elt_connections={142135104: (8, 0, 9, 0), 142135056: (4, 0, 12, 0), 142135140: (11, 0, 10, 0), 142135020: (2, 0, 7, 0), 142135176: (6, 1, 11, 1), 142135068: (5, 0, 7, 1), 142135116: (4, 0, 5, 0), 142135032: (6, 0, 11, 0), 142135152: (3, 0, 4, 0), 142135080: (12, 0, 6, 0), 142135188: (13, 0, 8, 0), 142135128: (6, 0, 5, 1), 142135092: (7, 0, 13, 0), 142135164: (6, 1, 5, 2)},
                              elt_data={2: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'PGL Dresser', 'posx': 82.895776400826648, 'posy': 548.42440401200258, 'minimal': False}, 3: {'lazy': False, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'fread', 'posx': 89.515184995894515, 'posy': 74.877084352912632, 'minimal': False}, 4: {'lazy': False, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'csv2objs', 'posx': 106.73865934583375, 'posy': 142.28376433722542, 'minimal': False}, 5: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Stand Positioner', 'posx': 87.633671886223624, 'posy': 424.33146387013517, 'minimal': False}, 6: {'lazy': True, 'hide': True, 'port_hide_changed': set([1, 2, 4]), 'priority': 0, 'caption': 'Spatial Distribution', 'posx': 209.94540429536852, 'posy': 312.24872851539288, 'minimal': False}, 7: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'map', 'posx': 196.91792423689574, 'posy': 606.16675477111107, 'minimal': False}, 8: {'lazy': False, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Scene', 'posx': 196.00584818229177, 'posy': 735.50046985258882, 'minimal': False}, 9: {'lazy': False, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'plot3D', 'posx': 193.66150323528066, 'posy': 794.22542929925032, 'minimal': False}, 10: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'VS Plot', 'posx': 465.57417250694294, 'posy': 485.14956913739837, 'minimal': False}, 11: {'lazy': False, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Iterables to Sequence', 'posx': 402.74380116703031, 'posy': 420.69131667810808, 'minimal': False}, 12: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'len', 'posx': 189.9441796412533, 'posy': 253.67641861801565, 'minimal': False}, 13: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'flatten', 'posx': 188.47394183026799, 'posy': 667.60449514807488, 'minimal': False}, 14: {'txt': 'Read stand description', 'posx': 188.8888888888888, 'posy': 79.166666666666643}, 15: {'txt': 'Choose a distribution', 'posx': 401.3888888888888, 'posy': 316.66666666666663}, 16: {'txt': '2D View', 'posx': 649.99999999999977, 'posy': 493.05555555555549}, 17: {'txt': 'Apply a shape', 'posx': 18.0555555555555, 'posy': 505.55555555555537}, 18: {'txt': 'PlantGL Scene builder', 'posx': 280.55555555555549, 'posy': 744.44444444444423}, 19: {'txt': 'New tree position', 'posx': 209.72222222222214, 'posy': 469.44444444444434}, '__out__': {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Out', 'posx': 20.0, 'posy': 250.0, 'minimal': False}, '__in__': {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'In', 'posx': 20.0, 'posy': 5.0, 'minimal': False}},
                              elt_value={2: [(0, 'None'), (1, "'AsymetricSwung'"), (2, '{}')], 3: [(0, "'/home/sdufour/Bureau/placette3_openalea.csv'")], 4: [(1, "','"), (2, "'\\n'")], 5: [(3, "'Position mapping (PM)'"), (4, '{}')], 6: [(1, '[-1675, 1977]'), (2, '[-2094, 1617]'), (3, "'Random'"), (4, "{'cluster': 10, 'cluster_radius': 500}")], 7: [], 8: [], 9: [], 10: [(1, "'PointLine'"), (2, "'MyPlot'"), (3, "'x-axis-label'"), (4, "'y-axis-label'"), (5, '0')], 11: [], 12: [], 13: [], 14: [], 15: [], 16: [], 17: [], 18: [], 19: [], '__out__': [], '__in__': []},
                              lazy=True,
                              )

    pkg.add_factory(nf)


    pkgmanager.add_package(pkg)


