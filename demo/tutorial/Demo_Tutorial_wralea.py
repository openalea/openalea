
# This file has been generated at $TIME

from openalea.core import *

def register_packages(pkgmanager):
    
    metainfo = {'description': 'Tutorials', 'license': '', 'url': '', 'version': '0', 'authors': '', 'institutes': ''} 
    pkg = UserPackage("Demo.Tutorial", metainfo)

    

    nf = CompositeNodeFactory(name='Spatial2D', 
                              description='2D random spatial distribution', 
                              category='Spatial',
                              doc='',
                              inputs=[],
                              outputs=[],
                              elt_factory={2: ('spatial', 'Aggregative Distribution'), 3: ('spatial', 'Basic Distribution'), 4: ('spatial', 'Random 2D'), 5: ('spatial', 'Domain'), 6: ('PlotTools', 'Iterables to Sequence'), 7: ('PlotTools', 'VS Plot')},
                              elt_connections={135573000: (2, 0, 4, 1), 135572988: (4, 0, 6, 0), 135572964: (6, 0, 7, 0), 135573012: (5, 0, 4, 2), 135572976: (4, 1, 6, 1)},
                              elt_data={2: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'NemanScott', 'posx': 763.75, 'posy': 156.25, 'minimal': False}, 3: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Regular', 'posx': 653.75, 'posy': 226.25, 'minimal': False}, 4: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Random 2D', 'posx': 706.25, 'posy': 405.0, 'minimal': False}, 5: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Domain', 'posx': 925.0, 'posy': 333.75, 'minimal': False}, 6: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Iterables to Sequence', 'posx': 655.0, 'posy': 526.25, 'minimal': False}, 7: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'VS Plot', 'posx': 758.75, 'posy': 740.0, 'minimal': False}, '__out__': {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Out', 'posx': 20.0, 'posy': 250.0, 'minimal': False}, '__in__': {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'In', 'posx': 20.0, 'posy': 5.0, 'minimal': False}},
                              elt_value={2: [(0, "'NemanScott'"), (1, '2'), (2, '0.050000000000000003')], 3: [(0, "'Regular'")], 4: [(0, '100')], 5: [(0, '0'), (1, '1'), (2, '0'), (3, '1')], 6: [], 7: [(1, "'PointLine'"), (2, "'MyPlot'"), (3, "'x-axis-label'"), (4, "'y-axis-label'"), (5, '0')], '__out__': [], '__in__': []},
                              lazy=True,
                              )

    pkg.add_factory(nf)


    nf = CompositeNodeFactory(name='simple expression', 
                              description='simple expression', 
                              category='Tutorial',
                              doc='',
                              inputs=[],
                              outputs=[],
                              elt_factory={2: ('Catalog.Math', '+'), 3: ('Catalog.Python', 'print'), 4: ('Catalog.Data', 'float'), 5: ('Catalog.Data', 'float'), 6: ('Catalog.Math', 'random'), 7: ('Catalog.Math', '*'), 8: ('System', 'annotation')},
                              elt_connections={147627912: (6, 0, 7, 0), 147627876: (2, 0, 3, 0), 147627924: (5, 0, 7, 1), 147627900: (7, 0, 2, 1), 147627888: (4, 0, 2, 0)},
                              elt_data={2: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': '+', 'posx': 218.75, 'posy': 172.5, 'minimal': False}, 3: {'lazy': False, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'print', 'posx': 247.5, 'posy': 258.75, 'minimal': False}, 4: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': '5.0', 'posx': 137.5, 'posy': 71.25, 'minimal': False}, 5: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': '20.0', 'posx': 361.25, 'posy': 32.5, 'minimal': False}, 6: {'lazy': False, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'random', 'posx': 241.25, 'posy': 35.0, 'minimal': False}, 7: {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': '*', 'posx': 286.25, 'posy': 103.75, 'minimal': False}, 8: {'txt': 'Simple expression', 'posx': 391.25, 'posy': 135.0}, '__out__': {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Out', 'posx': 20.0, 'posy': 250.0, 'minimal': False}, '__in__': {'lazy': True, 'hide': True, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'In', 'posx': 20.0, 'posy': 5.0, 'minimal': False}},
                              elt_value={2: [], 3: [], 4: [(0, '5.0')], 5: [(0, '20.0')], 6: [], 7: [], 8: [], '__out__': [], '__in__': []},
                              lazy=True,
                              )

    pkg.add_factory(nf)


    pkgmanager.add_package(pkg)


