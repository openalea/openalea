
# This file has been generated at Sun May 20 19:47:26 2012

from openalea.core import *


__name__ = 'openalea.misc'

__editable__ = True
__description__ = 'shortcut to the script make_develop'
__license__ = 'CECILL-C'
__url__ = 'http://openalea.gforge.inria.fr'
__alias__ = []
__version__ = '0.0.1'
__authors__ = 'moscardi, cokelaer'
__institutes__ = 'INRIA/CIRAD'
__icon__ = ''


__all__ = ['openalea_packages_openalea_packages', 'multisetup_multisetup', 'alinea_packages_alinea_packages', 'commands_commands', 'vplants_packages_vplants_packages', 'list_packages_list_packages', 'list_selector_Select', 'shared_data_SharedDataBrowser']



openalea_packages_openalea_packages = Factory(name='openalea_packages',
                authors='moscardi, cokelaer (wralea authors)',
                description='List of packages to release from openalea project',
                category='data i/o',
                nodemodule='openalea_packages',
                nodeclass='openalea_packages',
                inputs=[{'interface': None, 'hide': True, 'name': 'in1', 'value': None, 'desc': ''}],
                outputs=[{'interface': ISequence, 'name': 'openalea_packages', 'desc': 'List of packages to release from openalea project'}],
                widgetmodule=None,
                widgetclass=None,
               )




multisetup_multisetup = Factory(name='multisetup',
                authors='moscardi, cokelaer (wralea authors)',
                description='Multi Setup allows to build and install all the packages',
                category='data i/o',
                nodemodule='multisetup',
                nodeclass='multisetup',
                inputs=[{'interface': IDirStr, 'name': 'directory', 'value': '', 'desc': 'Project directory'}, {'interface': ISequence, 'name': 'command', 'value': ['install', 'bdist_egg -d .dist'], 'desc': 'Python list of user commands'}, {'interface': ISequence, 'name': 'packages', 'value': [], 'desc': 'list of packages to process'}, {'interface': IBool, 'name': 'verbose', 'value': False, 'desc': 'run verbosely'}],
                outputs=[{'interface': IBool, 'name': 'status', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




alinea_packages_alinea_packages = Factory(name='alinea_packages',
                authors='moscardi, cokelaer (wralea authors)',
                description='List of packages to release from alinea project',
                category='data i/o',
                nodemodule='alinea_packages',
                nodeclass='alinea_packages',
                inputs=[{'interface': None, 'hide': True, 'name': 'in1', 'value': None, 'desc': ''}],
                outputs=[{'interface': ISequence, 'name': 'alinea_packages', 'desc': 'List of packages to release from alinea project'}],
                widgetmodule=None,
                widgetclass=None,
               )




commands_commands = Factory(name='commands',
                authors='moscardi, cokelaer (wralea authors)',
                description='List of commands for setup.py',
                category='data i/o',
                nodemodule='commands',
                nodeclass='commands',
                inputs=[{'interface': None, 'hide': True, 'name': 'in1', 'value': None, 'desc': ''}],
                outputs=[{'interface': ISequence, 'name': 'commands', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




vplants_packages_vplants_packages = Factory(name='vplants_packages',
                authors='moscardi, cokelaer (wralea authors)',
                description='List of packages to release from vplants project',
                category='data i/o',
                nodemodule='vplants_packages',
                nodeclass='vplants_packages',
                inputs=[{'interface': None, 'hide': True, 'name': 'in1', 'value': None, 'desc': ''}],
                outputs=[{'interface': ISequence, 'name': 'vplants_packages', 'desc': 'List of packages to release from openalea project'}],
                widgetmodule=None,
                widgetclass=None,
               )




list_packages_list_packages = Factory(name='list_packages',
                authors='moscardi, cokelaer (wralea authors)',
                description='List of packages from a directory',
                category='data i/o',
                nodemodule='list_packages',
                nodeclass='list_packages',
                inputs=[{'interface': IDirStr, 'name': 'project', 'value': None, 'desc': 'project directory'}, {'interface': ISequence, 'name': 'exclude_list', 'value': [], 'desc': 'list of packages to exclude'}],
                outputs=[{'interface': None, 'name': 'packages', 'desc': 'List of packages'}],
                widgetmodule=None,
                widgetclass=None,
               )




list_selector_Select = Factory(name='list_selector',
                authors='moscardi, cokelaer (wralea authors)',
                description='This Widget allows to select some elements in a list',
                category='data i/o',
                nodemodule='list_selector',
                nodeclass='Select',
                inputs=[{'interface': ISequence, 'name': 'in_list', 'value': [], 'desc': ''}],
                outputs=[{'interface': ISequence, 'name': 'out_list', 'desc': ''}],
                widgetmodule='list_selector_widget',
                widgetclass='ListSelector',
               )




shared_data_SharedDataBrowser = Factory(name='SharedDataBrowser',
                authors='Thomas Cokelaer',
                description='This widget permits to select a shared data file located in a given Python package.',
                category='data i/o',
                nodemodule='shared_data',
                nodeclass='SharedDataBrowser',
                inputs=[{'interface': IStr, 'name': 'package', 'value': None, 'desc': ''}, {'interface': IStr, 'name': 'glob', 'value': '*'}, {'interface': IStr, 'name': 'filename', 'value': None}],
                outputs=[{'interface': IStr, 'name': 'filepath'}],
                widgetmodule='shared_data_widget',
                widgetclass='SharedDataBrowser',
               )




