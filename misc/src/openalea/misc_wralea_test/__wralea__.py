
# This file has been generated at Fri Feb 28 16:23:05 2014

from openalea.core import *


__name__ = 'openalea.misc.test'

__editable__ = True
__description__ = 'tests on misc package nodes'
__license__ = 'CECILL-C'
__url__ = 'http://openalea.gforge.inria.fr'
__alias__ = []
__version__ = '0.0.1'
__authors__ = 'Thomas Cokelaer'
__institutes__ = 'INRIA/CIRAD'
__icon__ = ''


__all__ = ['_113660496']



_113660496 = CompositeNodeFactory(name='shared_data_browser',
                             description='',
                             category='Unclassified',
                             doc='',
                             inputs=[],
                             outputs=[],
                             elt_factory={  2: ('openalea.misc', 'SharedDataBrowser'),
   3: ('openalea.data structure.string', 'string'),
   4: ('openalea.data structure.string', 'string')},
                             elt_connections={  33864952: (3, 0, 2, 0), 33864976: (4, 0, 2, 2)},
                             elt_data={  2: {  'block': False,
         'caption': 'SharedDataBrowser',
         'delay': 0,
         'hide': True,
         'id': 2,
         'lazy': True,
         'port_hide_changed': set(),
         'posx': -11.081232477455686,
         'posy': 19.16129782560044,
         'priority': 0,
         'use_user_color': False,
         'user_application': None,
         'user_color': None},
   3: {  'block': False,
         'caption': 'alinea.echap',
         'delay': 0,
         'hide': True,
         'id': 3,
         'lazy': True,
         'port_hide_changed': set(),
         'posx': -33.93627446220801,
         'posy': -38.091736641253895,
         'priority': 0,
         'use_user_color': False,
         'user_application': None,
         'user_color': None},
   4: {  'block': False,
         'caption': 'Mercia_axeT.csv',
         'delay': 0,
         'hide': True,
         'id': 4,
         'lazy': True,
         'port_hide_changed': set(),
         'posx': 76.48739486473406,
         'posy': -37.32609703913363,
         'priority': 0,
         'use_user_color': False,
         'user_application': None,
         'user_color': None},
   '__in__': {  'block': False,
                'caption': 'In',
                'delay': 0,
                'hide': True,
                'id': 0,
                'lazy': True,
                'port_hide_changed': set(),
                'posx': 0,
                'posy': 0,
                'priority': 0,
                'use_user_color': True,
                'user_application': None,
                'user_color': None},
   '__out__': {  'block': False,
                 'caption': 'Out',
                 'delay': 0,
                 'hide': True,
                 'id': 1,
                 'lazy': True,
                 'port_hide_changed': set(),
                 'posx': 0,
                 'posy': 0,
                 'priority': 0,
                 'use_user_color': True,
                 'user_application': None,
                 'user_color': None}},
                             elt_value={  2: [(1, 'None')],
   3: [(0, "'alinea.echap'")],
   4: [(0, "'Mercia_axeT.csv'")],
   '__in__': [],
   '__out__': []},
                             elt_ad_hoc={  2: {'position': [-11.081232477455686, 19.16129782560044], 'userColor': None, 'useUserColor': False},
   3: {'position': [-33.93627446220801, -38.091736641253895], 'userColor': None, 'useUserColor': False},
   4: {'useUserColor': False, 'position': [76.48739486473406, -37.32609703913363], 'userColor': None},
   '__in__': {'position': [0, 0], 'userColor': None, 'useUserColor': True},
   '__out__': {'position': [0, 0], 'userColor': None, 'useUserColor': True}},
                             lazy=True,
                             eval_algo='LambdaEvaluation',
                             )




