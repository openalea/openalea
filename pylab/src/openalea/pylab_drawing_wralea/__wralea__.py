
# This file has been generated at Sat Mar  6 21:17:54 2010

from openalea.core import Factory
from openalea.deploy import get_metainfo

version = get_metainfo('openalea.pylab', 'version')
authors = get_metainfo('openalea.pylab', 'author')

__name__ = 'openalea.pylab.Drawing'

__editable__ = False
__description__ = 'nodes that add features in an axe (no input data required)'
__license__ = 'CECILL-C'
__url__ = 'http://openalea.gforge.inria.fr/doc/openalea/pylab/doc/_build/html/contents.html'
__alias__ = []
__version__ = version
__authors__ = authors
__institutes__ = 'INRIA/CIRAD'
__icon__ = 'icon.png'


__all__ = [
'py_pylab_PyLabAnnotate',
'py_pylab_PyLabYAArowDict',
'py_pylab_PyLabFancyArrowDict',
'py_pylab_PyLabAxhline',
'py_pylab_PyLabAxvline',
'py_pylab_PyLabAxhspan',
'py_pylab_PyLabAxvspan',
'py_pylab_PyLabBBox',
]




py_pylab_PyLabAnnotate = Factory(name='PyLabAnnotate',
                description='pylab.fontproperties interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabAnnotate',
                inputs=None,
                outputs=None,
                widgetmodule=None,
                widgetclass=None,
                lazy=False
               )

py_pylab_PyLabBBox = Factory(name='PyLabBBox',
                description='pylab.fontproperties interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabBBox',
                inputs=None,
                outputs=None,
                widgetmodule=None,
                widgetclass=None,
                lazy=False
               )



py_pylab_PyLabYAArowDict = Factory(name='PyLabYAArowDict',
                description='pylab.fontproperties interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabYAArowDict',
                inputs=None,
                outputs=None,
                widgetmodule=None,
                widgetclass=None,
                lazy=False
               )


py_pylab_PyLabFancyArrowDict = Factory(name='PyLabFancyArrowDict',
                description='pylab.fontproperties interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabFancyArrowDict',
                inputs=None,
                outputs=None,
                widgetmodule=None,
                widgetclass=None,
                lazy=False
               )

py_pylab_PyLabAxhline = Factory(name='PyLabAxhline',
                description='pylab.fontproperties interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabAxhline',
                inputs=None,
                outputs=None,
                widgetmodule=None,
                widgetclass=None,
                lazy=False
               )

py_pylab_PyLabAxvline = Factory(name='PyLabAxvline',
                description='pylab.fontproperties interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabAxvline',
                inputs=None, outputs=None, widgetmodule=None, widgetclass=None, lazy=False
               )


py_pylab_PyLabAxhspan = Factory(name='PyLabAxhspan',
                description='pylab.fontproperties interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabAxhspan',
                inputs=None, outputs=None, widgetmodule=None, widgetclass=None, lazy=False
               )

py_pylab_PyLabAxvspan = Factory(name='PyLabAxvspan',
                description='pylab.fontproperties interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabAxvspan',
                inputs=None, outputs=None, widgetmodule=None, widgetclass=None, lazy=False
                )


