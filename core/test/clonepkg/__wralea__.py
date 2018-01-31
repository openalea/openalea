
# This file has been generated at Wed Jan 31 21:28:23 2018

from openalea.core import *


__name__ = 'ClonePkg'

__editable__ = True
__description__ = 'Base library.'
__license__ = 'CECILL-C'
__url__ = 'http://openalea.gforge.inria.fr'
__version__ = '0.0.1'
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__icon__ = ''


__all__ = ['TestFact_TestFact']



TestFact_TestFact = Factory(name='TestFact',
                authors='OpenAlea Consortium (wralea authors)',
                description='this is a test',
                category='category test',
                nodemodule='TestFact',
                nodeclass='TestFact',
                inputs=[{'interface': None, 'name': 't0', 'value': 0}, {'interface': None, 'name': 't1', 'value': 1}, {'interface': None, 'name': 't2', 'value': 2}],
                outputs=[{'interface': None, 'name': 't0', 'value': 0}, {'interface': None, 'name': 't1', 'value': 1}],
                widgetmodule=None,
                widgetclass=None,
               )




