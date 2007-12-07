
# This file has been generated at $TIME

from openalea.core import *

def register_packages(pkgmanager):
    
    metainfo = {'description': '', 'license': '', 'url': '', 'version': '', 'authors': '', 'institutes': ''} 
    pkg = UserPackage("Demo.Caribu", metainfo)

    

    nf = CompositeNodeFactory(name='demo', 
                              description='', 
                              category='Stat',
                              doc='',
                              inputs=[],
                              outputs=[],
                              elt_factory={2: ('Caribu', 'Periodise'), 3: ('Caribu', 'S2v'), 4: ('Caribu', 'Canestra'), 5: ('Caribu', 'MCSail'), 6: ('Caribu', 'CaribuOptions'), 7: ('Catalog.Data', 'filename'), 8: ('Catalog.Data', 'filename'), 9: ('Catalog.Data', 'filename'), 10: ('System', 'annotation'), 11: ('System', 'annotation'), 12: ('Caribu.Visualisation', 'Plot Can File'), 13: ('System', 'annotation'), 14: ('Demo.Caribu', 'ViewMapOnCan'), 15: ('System', 'annotation'), 16: ('System', 'annotation')},
                              elt_connections={9723808: (9, 0, 4, 4), 9723712: (6, 0, 2, 1), 9723580: (6, 2, 3, 3), 9723748: (8, 0, 4, 3), 9723628: (2, 0, 3, 0), 9723676: (2, 0, 4, 0), 9723784: (6, 6, 4, 13), 9723724: (2, 0, 12, 0), 9723592: (6, 0, 4, 1), 9723820: (4, 1, 14, 0), 9723640: (7, 0, 2, 0), 9723760: (6, 4, 4, 7), 9723688: (9, 0, 3, 4), 9723796: (3, 0, 5, 0), 9723604: (6, 1, 3, 2), 9723652: (5, 0, 4, 2), 9723736: (6, 0, 3, 1), 9723700: (6, 5, 4, 8), 9723772: (6, 3, 4, 5), 9723616: (4, 2, 14, 1), 9723664: (8, 0, 5, 1)},
                              elt_data={2: {'lazy': True, 'hide': False, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Periodise', 'posx': 27.5, 'posy': 147.5, 'minimal': False}, 3: {'lazy': True, 'hide': False, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'S2v', 'posx': 127.5, 'posy': 222.5, 'minimal': False}, 4: {'lazy': True, 'hide': False, 'port_hide_changed': set([6, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]), 'priority': 0, 'caption': '                                                     Canestra', 'posx': 400.0, 'posy': 458.75, 'minimal': False}, 5: {'lazy': True, 'hide': False, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'MCSail', 'posx': 291.25, 'posy': 278.75, 'minimal': False}, 6: {'lazy': True, 'hide': False, 'port_hide_changed': set([]), 'priority': 0, 'caption': ' CaribuOptions ', 'posx': 402.91666666666674, 'posy': 148.88888888888886, 'minimal': False}, 7: {'lazy': True, 'hide': False, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'CanFile', 'posx': 20.0, 'posy': 61.25, 'minimal': False}, 8: {'lazy': True, 'hide': False, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'LightFile', 'posx': 295.0, 'posy': 61.25, 'minimal': False}, 9: {'lazy': True, 'hide': False, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'OpticalFile', 'posx': 178.75, 'posy': 63.75, 'minimal': False}, 10: {'txt': 'Packages : Caribu, PlantGL', 'posx': 731.74931129476545, 'posy': 125.21913348359627}, 11: {'txt': 'Authors : C. Fournier, C. Pradal', 'posx': 730.97817013106271, 'posy': 94.782536104850152}, 12: {'lazy': True, 'hide': False, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Plot Can File', 'posx': -78.75, 'posy': 220.0, 'minimal': False}, 13: {'txt': 'Caribu Demonstration', 'posx': 731.25, 'posy': 65.0}, 14: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'ViewMapOnCan', 'posx': 490.0, 'posy': 552.5, 'minimal': False}, 15: {'txt': 'Team : INRA, Virtual Plants', 'posx': 730.44494532097826, 'posy': 156.52391685449527}, 16: {'txt': 'Credits : M. Chelle', 'posx': 733.05367726855297, 'posy': 185.21996827781942}, '__out__': {'lazy': True, 'hide': False, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Out', 'posx': 20.0, 'posy': 250.0, 'minimal': False}, '__in__': {'lazy': True, 'hide': False, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'In', 'posx': 20.0, 'posy': 5.0, 'minimal': False}},
                              elt_value={2: [], 3: [], 4: [(6, 'None'), (9, 'None'), (10, 'False'), (11, 'True'), (12, 'True'), (14, 'None'), (15, 'None'), (16, 'None'), (17, 'None'), (18, 'None'), (19, 'None'), (20, 'False'), (21, 'None'), (22, 'False'), (23, 'False')], 5: [], 6: [(0, 'True'), (1, "'D:/pradal/devlp/alea/openalea/trunk/demo/caribu/data/maize.8'"), (2, 'True'), (3, '2'), (4, 'True'), (5, 'None'), (6, 'None'), (7, 'None'), (8, 'False'), (9, 'False'), (10, "'Caribu.log'"), (11, 'False')], 7: [(0, "'D:/pradal/devlp/alea/openalea/trunk/demo/caribu/data/f331s1_100plantes.can'"), (1, "''")], 8: [(0, "'D:/pradal/devlp/alea/openalea/trunk/demo/caribu/data/zenith.light'"), (1, "''")], 9: [(0, "'D:/pradal/devlp/alea/openalea/trunk/demo/caribu/data/par.opt'"), (1, "''")], 10: [], 11: [], 12: [(1, 'None')], 13: [], 14: [], 15: [], 16: [], '__out__': [], '__in__': []},
                              lazy=True,
                              )

    pkg.add_factory(nf)


    nf = CompositeNodeFactory(name='ViewMapOnCan', 
                              description='', 
                              category='Visualisation.Color',
                              doc='',
                              inputs=[{'interface': None, 'name': 'IN1', 'value': None}, {'interface': None, 'name': 'IN2', 'value': None}],
                              outputs=[],
                              elt_factory={2: ('Catalog.Math', 'min'), 3: ('Caribu.Visualisation', 'Read Vec File'), 4: ('Catalog.Math', 'max'), 5: ('Catalog.Color', 'ColorMap'), 6: ('Catalog.Functional', 'map'), 7: ('Caribu.Visualisation', 'Plot Can File')},
                              elt_connections={9853536: (2, 0, 5, 1), 9853572: (5, 0, 6, 0), 9853512: (3, 0, 4, 0), 9853548: (6, 0, 7, 1), 9853488: ('__in__', 0, 7, 0), 9853524: (4, 0, 5, 2), 9853560: (3, 0, 2, 0), 9853476: ('__in__', 1, 3, 0), 9853500: (3, 0, 6, 1)},
                              elt_data={2: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'min', 'posx': 347.5, 'posy': 128.75, 'minimal': False}, 3: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Read Vec File', 'posx': 351.25, 'posy': 31.25, 'minimal': False}, 4: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'max', 'posx': 435.0, 'posy': 128.75, 'minimal': False}, 5: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'ColorMap', 'posx': 360.0, 'posy': 225.0, 'minimal': False}, 6: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'map', 'posx': 501.25, 'posy': 272.5, 'minimal': False}, 7: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Plot Can File', 'posx': 397.5, 'posy': 333.75, 'minimal': False}, '__out__': {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Out', 'posx': 20.0, 'posy': 250.0, 'minimal': False}, '__in__': {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'In', 'posx': 205.0, 'posy': 27.5, 'minimal': False}},
                              elt_value={2: [], 3: [], 4: [], 5: [(0, 'None'), (3, '250.0'), (4, '20.0')], 6: [], 7: [], '__out__': [], '__in__': []},
                              lazy=True,
                              )

    pkg.add_factory(nf)


    pkgmanager.add_package(pkg)


