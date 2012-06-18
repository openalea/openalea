
# This file has been generated at Sat Mar  6 21:17:54 2010

from openalea.core import Factory
from openalea.deploy import get_metainfo

version = get_metainfo('openalea.pylab', 'version')
authors = get_metainfo('openalea.pylab', 'author')


__name__ = 'openalea.pylab.mplot3d'

__editable__ = False
__description__ = '3D visualisation nodes related to pylab.mplot3d.'
__license__ = 'CECILL-C'
__url__ = 'http://openalea.gforge.inria.fr/doc/openalea/pylab/doc/_build/html/contents.html'
__alias__ = []
__version__ = version
__authors__ = authors
__institutes__ = 'INRIA/CIRAD'
__icon__ = 'icon.png'


__all__ = [
    'py_pylab_PyLabPlot3D',
    'py_pylab_PyLabContour3D',
    'py_pylab_PyLabContourf3D',

]



py_pylab_PyLabPlot3D = Factory(name='PyLabPlot3D',
                description='pylab.fontproperties interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabPlot3D',
                inputs=None, outputs=None, widgetmodule=None, widgetclass=None,
                lazy=False
               )

py_pylab_PyLabContour3D = Factory(name='PyLabContour3D',
                description='pylab.fontproperties interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabContour3D',
                inputs=None, outputs=None, widgetmodule=None, widgetclass=None,
                lazy=False
               )


py_pylab_PyLabContourf3D = Factory(name='PyLabContourf3D',
                description='pylab.fontproperties interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabContourf3D',
                inputs=None, outputs=None, widgetmodule=None, widgetclass=None,
                lazy=False
               )

