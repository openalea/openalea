
# This file has been generated at Tue Mar  9 09:07:19 2010

from openalea.core import *


__name__ = 'openalea.multiprocessing'

__editable__ = True
__description__ = 'Functional Node library.'
__license__ = 'CECILL-C'
__url__ = 'http://openalea.gforge.inria.fr'
__alias__ = []
__version__ = '0.1.0'
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__icon__ = ''


__all__ = ['parallel_map_parallel_map', 'parallel_pymap']



parallel_map_parallel_map = Factory(name='parallel map',
                description='',
                category='Unclassified',
                nodemodule='parallel_map',
                nodeclass='parallel_map',
                inputs=[{'interface': IFunction, 'name': 'function', 'value': None, 'desc': ''}, {'interface': ISequence, 'name': 'seq', 'value': None, 'desc': ''}],
                outputs=[{'interface': None, 'name': 'result', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




parallel_pymap = Factory(name='pmap',
                description='Apply a function on a sequence',
                category='Functional',
                nodemodule='parallel',
                nodeclass='pymap',
                inputs=({'interface': IFunction, 'name': 'func'}, {'interface': ISequence, 'name': 'seq'}, {'interface': IInt(min=1, max=16777216, step=1), 'name': 'N'}),
                outputs=None,
                widgetmodule=None,
                widgetclass=None,
               )




