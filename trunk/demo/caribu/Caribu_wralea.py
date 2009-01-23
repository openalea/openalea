
# This file has been generated at $TIME

from openalea.core import *

def register_packages(pkgmanager):
    
    metainfo = {'description': '', 'license': '', 'url': '', 'version': '', 'authors': 'M. Chelle,C. Fournier', 'institutes': 'INRA'} 
    pkg = Package("Caribu", metainfo)

    

    nf = CompositeNodeFactory(name='Caribu', 
                              description='Compute light distribution on 3D Scene with nested radiosity', 
                              category='Models',
                              doc='',
                              inputs=[],
                              outputs=[],
                              elt_factory={2: ('Caribu', 'Periodise'), 3: ('Caribu', 'S2v'), 4: ('Caribu', 'Canestra'), 5: ('Caribu', 'MCSail'), 6: ('Caribu', 'CaribuOptions'), 7: ('Catalog.Data', 'filename'), 8: ('Catalog.Data', 'filename'), 9: ('Catalog.Data', 'filename')},
                              elt_connections={9853472: (6, 2, 3, 3), 9853424: (2, 0, 3, 0), 9853388: (6, 1, 3, 2), 9853508: (8, 0, 4, 3), 9853352: (6, 5, 4, 8), 9853448: (6, 3, 4, 5), 9853436: (6, 0, 2, 1), 9853364: (6, 0, 4, 1), 9853484: (6, 4, 4, 7), 9853520: (2, 0, 4, 0), 9853400: (6, 6, 4, 13), 9853328: (6, 0, 3, 1), 9853460: (8, 0, 5, 1), 9853496: (7, 0, 2, 0), 9853412: (5, 0, 4, 2), 9853340: (9, 0, 4, 4), 9853376: (9, 0, 3, 4), 9853532: (3, 0, 5, 0)},
                              elt_data={2: {'lazy': True, 'hide': False, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Periodise', 'posx': 27.5, 'posy': 147.5, 'minimal': False}, 3: {'lazy': True, 'hide': False, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'S2v', 'posx': 127.5, 'posy': 222.5, 'minimal': False}, 4: {'lazy': True, 'hide': False, 'port_hide_changed': set([6, 9, 10, 11, 12, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23]), 'priority': 0, 'caption': '                                                     Canestra', 'posx': 400.0, 'posy': 458.75, 'minimal': False}, 5: {'lazy': True, 'hide': False, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'MCSail', 'posx': 291.25, 'posy': 278.75, 'minimal': False}, 6: {'lazy': True, 'hide': False, 'port_hide_changed': set([]), 'priority': 0, 'caption': ' CaribuOptions ', 'posx': 420.0, 'posy': 37.5, 'minimal': False}, 7: {'lazy': True, 'hide': False, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'CanFile', 'posx': 26.25, 'posy': 36.25, 'minimal': False}, 8: {'lazy': True, 'hide': False, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'LightFile', 'posx': 290.0, 'posy': 38.75, 'minimal': False}, 9: {'lazy': True, 'hide': False, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'OpticalFile', 'posx': 163.75, 'posy': 36.25, 'minimal': False}, '__out__': {'lazy': True, 'hide': False, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'Out', 'posx': 20.0, 'posy': 250.0, 'minimal': False}, '__in__': {'lazy': True, 'hide': False, 'port_hide_changed': set([]), 'priority': 0, 'caption': 'In', 'posx': 20.0, 'posy': 5.0, 'minimal': False}},
                              elt_value={2: [], 3: [], 4: [(6, 'None'), (9, 'None'), (10, 'False'), (11, 'True'), (12, 'True'), (14, 'None'), (15, 'None'), (16, 'None'), (17, 'None'), (18, 'None'), (19, 'None'), (20, 'False'), (21, 'None'), (22, 'False'), (23, 'False')], 5: [], 6: [(0, 'False'), (1, 'None'), (2, 'False'), (3, '2'), (4, 'True'), (5, 'None'), (6, 'None'), (7, 'None'), (8, 'False'), (9, 'False'), (10, "'Caribu.log'"), (11, 'False')], 7: [(0, "'D:/Christian/Softs/WinCaribu_4.4/Tout.can'")], 8: [(0, "'D:/Christian/Softs/2006_pycaribu/trunk/test/par_Plop_sources.light'")], 9: [(0, "'D:/Christian/Softs/WinCaribu_4.4/par.opt'")], '__out__': [], '__in__': []},
                              lazy=True,
                              )

    pkg.add_factory(nf)


    nf = Factory(name='Canestra', 
                 description='Nested radiosity illumination of a 3D Scene ', 
                 category='Stat', 
                 nodemodule='Canestra',
                 nodeclass='Canestra',
                 inputs=[{'interface': IFileStr('*.can'), 'name': 'CanFile', 'value': None}, {'interface': IFileStr('*.8'), 'name': 'PatternFile', 'value': None}, {'interface': IFileStr('*.env'), 'name': 'SailFile', 'value': None}, {'interface': IFileStr('*.light') , 'name': 'LightSourceFile', 'value': None}, {'interface': IFileStr('*.opt'), 'name': 'OpticalFile', 'value': None}, {'interface': IInt, 'name': 'Max Nb of soil triangle to add', 'value': None}, {'interface': IFileStr('*.can'), 'name': 'SensorFile', 'value': None}, {'interface': IFileStr, 'name': 'FFoutFile', 'value': None}, {'interface': IFileStr, 'name': 'FFInFile', 'value': None}, {'interface': IDirStr, 'name': 'FFInDir', 'value': None}, {'interface': IBool, 'name': 'printFF', 'value': False}, {'interface': IBool, 'name': 'genCan', 'value': True}, {'interface': IBool, 'name': 'genEtri', 'value': True}, {'interface': IFloat, 'name': 'Sphere radius', 'value': None}, {'interface': IFloat, 'name': 'Sphere diameter', 'value': None}, {'interface': IInt, 'name': 'disc resolution', 'value': None}, {'interface': IInt, 'name': 'nbSim', 'value': None}, {'interface': IInt, 'name': 'CG nbiter', 'value': None}, {'interface': IFloat, 'name': 'CG threshold', 'value': None}, {'interface': IInt, 'name': 'LightScreen resolution', 'value': None}, {'interface': IBool, 'name': 'test Inner Triangle', 'value': False}, {'interface': IInt, 'name': 'verbose level', 'value': None}, {'interface': IBool, 'name': 'estimate memory', 'value': False}, {'interface': IBool, 'name': 'print help', 'value': False}],
                 outputs=[{'interface': IDirStr, 'name': 'OutDir'}, {'interface': IFileStr('*.can'), 'name': 'CanFile', 'value': None},{'interface': IFileStr('*.vec'), 'name': 'Eabs File', 'value': None},{'interface': IStr, 'name': 'Log'}],
                 widgetmodule=None,
                 widgetclass=None,
                 )

    pkg.add_factory( nf )



    nf = Factory(name='Periodise', 
                 description='Retail a scene along a pattern for use as a periodic motif', 
                 category='Stat', 
                 nodemodule='Periodise',
                 nodeclass='Periodise',
                 inputs=[{'interface': IFileStr('*.can'), 'name': 'CanFile'}, {'interface': IFileStr('*.8'), 'name': 'PatternFile', 'value': 'NoPattern'}],
                 outputs=[{'interface': IFileStr, 'name': 'OutFile'}, {'interface': IStr, 'name': 'Log'}],
                 widgetmodule=None,
                 widgetclass=None,
                 )

    pkg.add_factory( nf )



    nf = Factory(name='S2v', 
                 description='Produce volumetric statistics from CanFile.', 
                 category='Stat', 
                 nodemodule='S2v',
                 nodeclass='S2v',
                 inputs=[{'interface':IFileStr('*.can'), 'name': 'CanFile'}, {'interface':IFileStr('*.8'), 'name': 'PatternFile', 'value': None}, {'interface': IInt, 'name': 'nz', 'value': None}, {'interface': IFloat, 'name': 'Dz', 'value': None}, {'interface':IFileStr('*.opt'), 'name': 'OpticalFile', 'value': None}],
                 outputs=[{'interface': IDirStr, 'name': 'OutDir'}, {'interface': IStr, 'name': 'Log'}],
                 widgetmodule=None,
                 widgetclass=None,
                 )

    pkg.add_factory( nf )



    nf = Factory(name='CaribuOptions', 
                 description='Nested radiosity illumination of a 3D Scene ', 
                 category='Stat', 
                 nodemodule='CaribuOptions',
                 nodeclass='CaribuOptions',
                 inputs=[{'interface': IBool, 'name': 'simulate infinite canopy', 'value': False}, {'interface':IFileStr('*.8'), 'name': 'PatternFile', 'value': None}, {'interface': IBool, 'name': 'add a Soil', 'value': False}, {'interface': IInt, 'name': 'max nb of triangle for soil', 'value': 2}, {'interface': IBool, 'name': 'No multiple scattering', 'value': True}, {'interface': IInt, 'name': 'nb of layers', 'value': None}, {'interface': IFloat, 'name': 'max heigth of layers', 'value': None}, {'interface': IFloat, 'name': 'Sphere radius', 'value': None}, {'interface': IBool, 'name': 're-use FormFactor', 'value': False}, {'interface': IBool, 'name': 'save logfile', 'value': False}, {'interface':IFileStr('Caribu.log'), 'name': 'logFile', 'value': 'Caribu.log'}, {'interface': IBool, 'name': 'CleanUp', 'value': False}],
                 outputs=[{'interface': IFileStr, 'name': 'PatternFile', 'value': None}, {'interface': IInt, 'name': 'nb of layers', 'value': None}, {'interface': IFloat, 'name': 'max heigth of layers', 'value': None}, {'interface': IInt, 'name': 'max nb of triangle for soil', 'value': 2}, {'interface': IFileStr, 'name': 'FFOutFile', 'value': None}, {'interface': IFileStr, 'name': 'FFInFile', 'value': None}, {'interface': IFloat, 'name': 'Sphere radius', 'value': None}],
                 widgetmodule=None,
                 widgetclass=None,
                 )

    pkg.add_factory( nf )



    nf = Factory(name='MCSail', 
                 description='Compute mean fluxes on layered canopy', 
                 category='Stat', 
                 nodemodule='MCSail',
                 nodeclass='MCSail',
                 inputs=[{'interface': IDirStr, 'name': 'S2vDir'}, {'interface':IFileStr('*.light'), 'name': 'LightSourceFile', 'value': None}],
                 outputs=[{'interface': IFileStr, 'name': 'OutFile'}, {'interface': IStr, 'name': 'Log'}],
                 widgetmodule=None,
                 widgetclass=None,
                 )

    pkg.add_factory( nf )



    pkgmanager.add_package(pkg)


