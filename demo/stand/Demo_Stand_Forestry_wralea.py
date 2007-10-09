
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
                              elt_factory={2: ('PlantGL.Dresser', 'PGL Dresser'), 3: ('Catalog.Python', 'fread'), 4: ('Catalog.Csv', 'csv2objs'), 5: ('stand', 'Stand Positioner'), 6: ('spatial', 'Spatial Distribution'), 7: ('stand', 'Stand Dresser'), 8: ('PlantGL Objects', 'Scene'), 9: ('PlantGL Visualization', 'plot3D'), 10: ('PlotTools', 'VS Plot'), 11: ('PlotTools', 'Iterables to Sequence'), 12: ('Catalog.Python', 'len'), 13: ('System', 'annotation'), 14: ('System', 'annotation'), 15: ('System', 'annotation'), 16: ('System', 'annotation'), 17: ('System', 'annotation')},
                              elt_connections={146591552: (8, 0, 9, 0), 146591504: (12, 0, 6, 0), 146591588: (4, 0, 5, 0), 146591624: (6, 1, 11, 1), 146591516: (6, 0, 11, 0), 146591564: (11, 0, 10, 0), 146591600: (7, 0, 8, 0), 146591528: (5, 0, 7, 0), 146591636: (3, 0, 4, 0), 146591492: (4, 0, 12, 0), 146591576: (6, 1, 5, 2), 146591540: (2, 0, 7, 1), 146591612: (6, 0, 5, 1)},
                              elt_data={2: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'PGL Dresser', 'posx': 157.32434729955514, 'posy': 548.70447914241618, 'minimal': False}, 3: {'lazy': False, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'fread', 'posx': -157.46641412146533, 'posy': 131.29273610396567, 'minimal': False}, 4: {'lazy': False, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'csv2objs', 'posx': -142.35350606809837, 'posy': 220.52600816643775, 'minimal': False}, 5: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Stand Positioner', 'posx': -71.570149453358624, 'posy': 427.83044895452161, 'minimal': False}, 6: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Spatial Distribution', 'posx': 56.795910414301289, 'posy': 228.80638195475657, 'minimal': False}, 7: {'lazy': False, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Stand Dresser', 'posx': -85.884179344030358, 'posy': 655.26447943963899, 'minimal': False}, 8: {'lazy': False, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Scene', 'posx': -61.653429215412615, 'posy': 766.06407940085626, 'minimal': False}, 9: {'lazy': False, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'plot3D', 'posx': -71.694820224816851, 'posy': 862.58095107291535, 'minimal': False}, 10: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'VS Plot', 'posx': 305.61191868902671, 'posy': 432.80226900522047, 'minimal': False}, 11: {'lazy': False, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Iterables to Sequence', 'posx': 236.59553538300366, 'posy': 353.35696842916121, 'minimal': False}, 12: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'len', 'posx': 60.690487128424806, 'posy': 158.21717901126786, 'minimal': False}, 13: {'txt': 'PlantGL viewer', 'posx': 50.304949224095445, 'posy': 874.65702038023983}, 14: {'txt': 'Shape', 'posx': 292.09325355926376, 'posy': 563.09088325035862}, 15: {'txt': '2D Plot', 'posx': 486.82208926543967, 'posy': 441.38536093399853}, 16: {'txt': 'Stand description file', 'posx': -137.93292529187457, 'posy': 74.646053687367399}, 17: {'txt': 'Tree Distribution', 'posx': 248.27926552537423, 'posy': 228.8063819547566}, '__out__': {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Out', 'posx': 20.0, 'posy': 250.0, 'minimal': False}, '__in__': {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'In', 'posx': 20.0, 'posy': 5.0, 'minimal': False}},
                              elt_value={2: [(0, "'AsymetricSwung'")], 3: [(0, "'/home/sdufour/Bureau/placette2_openalea.csv'")], 4: [(1, "','"), (2, "'\\n'")], 5: [(3, "'Position mapping (PM)'"), (4, '{}')], 6: [(1, '[-1675, 1977]'), (2, '[-2094, 1617]'), (3, "'Random'"), (4, "{'cluster': 10, 'cluster_radius': 500}")], 7: [(2, "{'radiusHoup': 'r_houp2'}")], 8: [], 9: [], 10: [(1, "'PointLine'"), (2, "'MyPlot'"), (3, "'x-axis-label'"), (4, "'y-axis-label'"), (5, '0')], 11: [], 12: [], 13: [], 14: [], 15: [], 16: [], 17: [], '__out__': [], '__in__': []},
                              lazy=True,
                              )

    pkg.add_factory(nf)


    pkgmanager.add_package(pkg)


