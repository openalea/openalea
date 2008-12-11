
# This file has been generated at $TIME

from openalea.core import *

def register_packages(pkgmanager):
    
    metainfo = {} 
    pkg = UserPackage("Demo.PhyllotaxisModel", metainfo)

    

    nf = CompositeNodeFactory(name=' Snow&Snow model (decomposed)', 
                              description='', 
                              category='Demo',
                              doc='',
                              inputs=[],
                              outputs=[],
                              elt_factory={2: ('PhyllotaxisModel', 'Snow&Snow phyllotaxis model'), 3: ('PhyllotaxisModel', 'Prim time differences'), 4: ('PhyllotaxisModel', 'Prim absolute angles'), 5: ('System', 'annotation'), 6: ('PhyllotaxisModel', 'Prim time creation'), 7: ('PlotTools', 'VS Plot'), 8: ('PlotTools', 'PointLine Style'), 9: ('PlotTools', 'VS Plot'), 10: ('System', 'rendez vous'), 11: ('PhyllotaxisModel', 'Prim divergence angles'), 12: ('Catalog.Python', 'getitem'), 13: ('Catalog.Data', 'string'), 14: ('Catalog.Data', 'int'), 15: ('Catalog.Math', '+'), 16: ('Catalog.Python', 'range'), 17: ('System', 'iter'), 18: ('Catalog.Python', 'ifelse'), 19: ('Catalog.Data', 'int'), 20: ('Catalog.Data', 'int'), 21: ('System', 'annotation'), 22: ('System', 'annotation'), 23: ('System', 'annotation'), 24: ('System', 'annotation'), 25: ('System', 'annotation'), 26: ('System', 'annotation'), 27: ('System', 'annotation'), 28: ('System', 'annotation'), 29: ('System', 'annotation'), 30: ('System', 'annotation'), 31: ('System', 'annotation'), 32: ('System', 'annotation'), 33: ('System', 'annotation'), 34: ('System', 'annotation')},
                              elt_connections={9789568: (7, 0, 10, 0), 9789700: (9, 0, 10, 1), 9789580: (12, 0, 18, 1), 9789712: (11, 0, 7, 0), 9789592: (4, 0, 7, 0), 9789724: (2, 0, 3, 0), 9789472: (12, 0, 18, 0), 9789604: (13, 0, 12, 1), 9789736: (2, 0, 12, 0), 9789484: (14, 0, 15, 1), 9789616: (3, 0, 8, 0), 9789748: (18, 0, 16, 0), 9789496: (8, 0, 7, 0), 9789628: (18, 0, 15, 0), 9789508: (2, 0, 4, 0), 9789640: (17, 0, 2, 1), 9789520: (19, 0, 18, 2), 9789652: (20, 0, 16, 2), 9789532: (6, 0, 7, 0), 9789664: (16, 0, 17, 0), 9789544: (15, 0, 16, 1), 9789676: (2, 0, 6, 0), 9789556: (2, 0, 11, 0), 9789688: (11, 0, 9, 0)},
                              elt_value={2: [(0, '1.1000000000000001'), (2, '20'), (3, 'True'), (4, 'True'), (5, 'True')], 3: [], 4: [], 5: [], 6: [], 7: [(1, "'PointLine'"), (2, "'Phyllotaxis summary'"), (3, "'Primordia'"), (4, "'Time/Angle'"), (5, '0')], 8: [(1, "'Default'"), (2, "'Default'"), (3, "'Default'"), (4, "'b'")], 9: [(1, "'Hist'"), (2, "'Divergence angle Hisogram'"), (3, "'Primordium'"), (4, "'Angle'"), (5, '1')], 10: [], 11: [], 12: [], 13: [(0, "'current_prim'")], 14: [(0, '20')], 15: [], 16: [], 17: [], 18: [], 19: [(0, '0')], 20: [(0, '1')], 21: [], 22: [], 23: [], 24: [], 25: [], 26: [], 27: [], 28: [], 29: [], 30: [], 31: [], 32: [], 33: [], 34: [], '__out__': [], '__in__': []},
                              lazy=True,
                              )

    pkg.add_factory(nf)


    pkgmanager.add_package(pkg)


