
from openalea.core import *


__name__ = 'openalea.data file'
__alias__ = []

__version__ = '0.0.1'
__license__ = "Cecill-C"
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = ''
__url__ = 'http://openalea.gforge.inria.fr'


__all__ = ['datafile_GetDataBrowser']



datafile_GetDataBrowser = Factory(name='get_data',
                authors='OpenAlea Consortium',
                description='This node permits to find a shared data file located in a given Python package. \
The data file is searched among the data nodes of the PackageManager.',
                category='data i/o',
                nodemodule='datafile',
                nodeclass='GetData',
                inputs=[{'interface': IStr, 'name': 'package', 'value': None, 'desc': ''}, 
                        {'interface': IStr, 'name': 'glob', 'value': '*'}, 
                        {'interface': IStr, 'name': 'filename', 'value': None}],
                outputs=[{'interface': IStr, 'name': 'filepath'}],
                widgetmodule='datafile_widget',
                widgetclass='GetDataBrowser',
               )

