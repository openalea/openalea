
# This file has been generated at Mon Oct 19 10:50:53 2009

from openalea.core import *


__name__ = 'openalea.misc'

__description__ = 'shortcut to the script make_develop'
__license__ = 'CECILL-C'
__url__ = 'http://openalea.gforge.inria.fr'
__alias__ = ['multisetup']
__version__ = '0.0.1'
__authors__ = 'moscardi'
__institutes__ = 'INRIA/CIRAD'


__all__ = []


list_packages = Factory(name='list_packages',
                description='List of packages from a directory',
                category='data i/o',
                nodemodule='list_packages',
                nodeclass='list_packages',
                inputs=[{'interface': IDirStr, 'name': 'project', 'value': None, 'desc': 'project directory'}, 
                        {'interface': ISequence, 'name': 'exclude_list', 'value': [], 'desc': 'list of packages to exclude'}],
                outputs=[{'interface': None, 'name': 'packages', 'desc': 'List of packages'}],
                widgetmodule=None,
                widgetclass=None,
               )

__all__.append("list_packages")


multisetup = Factory(name='multisetup',
                description='Multi Setup allows to build and install all the packages',
                category='data i/o',
                nodemodule='multisetup',
                nodeclass='multisetup',
                inputs=[{'interface': IDirStr, 'name': 'directory', 'value': '', 'desc': 'Project directory'}, 
                        {'interface': ISequence, 'name': 'command', 'value': ['install', 'bdist_egg -d ../dist'], 'desc': 'Python list of user commands'}, 
                        {'interface': ISequence, 'name': 'packages', 'value': [], 'desc': 'list of packages to process'}, 
                        {'interface': IBool, 'name': 'verbose', 'value': False, 'desc': 'run verbosely'}],
                outputs=[{'interface': IBool, 'name': 'status', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )

__all__.append("multisetup")


list_selector = Factory(name='list_selector',
                description='This Widget allows to select some elements in a list',
                category='data i/o',
                nodemodule='list_selector',
                nodeclass='Select',
                inputs=[{'interface': ISequence, 'name': 'in_list', 'value': [], 'desc': ''}],
                outputs=[{'interface': ISequence, 'name': 'out_list', 'desc': ''}],
                widgetmodule='list_selector_widget',
                widgetclass='ListSelector',
               )

__all__.append("list_selector")


openalea_packages = Factory(name='openalea_packages',
                description='List of packages to release from openalea project',
                category='data i/o',
                nodemodule='openalea_packages',
                nodeclass='openalea_packages',
                inputs=[{'interface': None, 'name': 'in1', 'value': None, 'desc': '', 'hide': True}],
                outputs=[{'interface': ISequence, 'name': 'openalea_packages', 'desc': 'List of packages to release from openalea project'}],
                widgetmodule=None,
                widgetclass=None,
               )

__all__.append("openalea_packages")


vplants_packages = Factory(name='vplants_packages',
                description='List of packages to release from vplants project',
                category='data i/o',
                nodemodule='vplants_packages',
                nodeclass='vplants_packages',
                inputs=[{'interface': None, 'name': 'in1', 'value': None, 'desc': '', 'hide': True}],
                outputs=[{'interface': ISequence, 'name': 'vplants_packages', 'desc': 'List of packages to release from openalea project'}],
                widgetmodule=None,
                widgetclass=None,
               )

__all__.append("vplants_packages")


alinea_packages = Factory(name='alinea_packages',
                description='List of packages to release from alinea project',
                category='data i/o',
                nodemodule='alinea_packages',
                nodeclass='alinea_packages',
                inputs=[{'interface': None, 'name': 'in1', 'value': None, 'desc': '', 'hide': True}],
                outputs=[{'interface': ISequence, 'name': 'alinea_packages', 'desc': 'List of packages to release from alinea project'}],
                widgetmodule=None,
                widgetclass=None,
               )

__all__.append("alinea_packages")











