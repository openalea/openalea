
# This file has been generated at $TIME

from openalea.core import *

def register_packages(pkgmanager):
    
    metainfo = {'version': '0.1', 'description': 'stand generation from forestry data', 'license': 'CECILL-C', 'authors': 'Da SILVA', 'url': '', 'institutes': 'INRIA CIRAD INRA'} 
    pkg = UserPackage("Demo.Stand.Forestry", metainfo)

    nf = CompositeNodeFactory(name='demo_data2scene', 
                              description='scene generation from data', 
                              category='Modelling',
                              doc='',
                              inputs=[],
                              outputs=[],
                              elt_factory={2: ('PlantGL.Dresser', 'PGL Dresser'), 3: ('Catalog.Python', 'fread'), 4: ('Catalog.Csv', 'csv2objs'), 5: ('stand', 'Stand Positioner'), 6: ('spatial', 'Spatial Distribution'), 7: ('stand', 'Stand Dresser'), 8: ('PlantGL Objects', 'Scene'), 9: ('PlantGL Visualization', 'plot3D'), 10: ('PlotTools', 'VS Plot'), 11: ('PlotTools', 'Iterables to Sequence')},
                              elt_connections={135572928: (3, 0, 4, 0), 135572964: (6, 1, 11, 1), 135573000: (6, 0, 5, 1), 135572988: (6, 0, 11, 0), 135572940: (4, 0, 5, 0), 135572976: (6, 1, 5, 2), 135572904: (11, 0, 10, 0), 135573012: (8, 0, 9, 0), 135572952: (2, 0, 7, 1), 135572916: (5, 0, 7, 0), 135572892: (7, 0, 8, 0)},
                              elt_data={2: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'PGL Dresser', 'posx': 155.86388103175881, 'posy': 548.70447914241618, 'minimal': False}, 3: {'lazy': False, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'fread', 'posx': -157.46641412146533, 'posy': 131.29273610396567, 'minimal': False}, 4: {'lazy': False, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'csv2objs', 'posx': -148.19537113928365, 'posy': 267.26092873591995, 'minimal': False}, 5: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Stand Positioner', 'posx': -71.570149453358624, 'posy': 427.83044895452161, 'minimal': False}, 6: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Spatial Distribution', 'posx': 10.503254485342524, 'posy': 147.79642954923102, 'minimal': False}, 7: {'lazy': False, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Stand Dresser', 'posx': -85.884179344030358, 'posy': 655.26447943963899, 'minimal': False}, 8: {'lazy': False, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Scene', 'posx': -61.653429215412615, 'posy': 766.06407940085626, 'minimal': False}, 9: {'lazy': False, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'plot3D', 'posx': -11.653429215412615, 'posy': 929.1133032725254, 'minimal': False}, 10: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'VS Plot', 'posx': 349.42590672291624, 'posy': 473.37077644400705, 'minimal': False}, 11: {'lazy': False, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Iterables to Sequence', 'posx': 236.59553538300366, 'posy': 353.35696842916121, 'minimal': False}, '__out__': {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Out', 'posx': 20.0, 'posy': 250.0, 'minimal': False}, '__in__': {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'In', 'posx': 20.0, 'posy': 5.0, 'minimal': False}},
                              elt_value={2: [(0, "'ChupaChups'")], 3: [(0, "'/home/ddasilva/dev/fractalysis/PlantDB/stands/placette3_openalea.csv'")], 4: [(1, "','"), (2, "'\\n'")], 5: [(3, "'Position mapping (PM)'"), (4, '{}')], 6: [(0, '91'), (1, '[-1675, 1977]'), (2, '[-2094, 1617]'), (3, "'Random'"), (4, "{'cluster': 10, 'cluster_radius': 500}")], 7: [(2, "{'radiusHoup': 'r_houp2'}")], 8: [], 9: [], 10: [(1, "'PointLine'"), (2, "'MyPlot'"), (3, "'x-axis-label'"), (4, "'y-axis-label'"), (5, '0')], 11: [], '__out__': [], '__in__': []},
                              lazy=True,
                              )

    pkg.add_factory(nf)
   

    pkgmanager.add_package(pkg)


