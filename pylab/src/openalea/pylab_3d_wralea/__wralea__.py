
# This file has been generated at Sat Mar  6 21:17:54 2010

from openalea.core import Factory


__name__ = 'openalea.pylab.mplot3d'

__editable__ = False
__description__ = 'pylab mplot3d.'
__license__ = 'CECILL-C'
__url__ = 'http://openalea.gforge.inria.fr/doc/openalea/pylab/doc/_build/html/contents.html'
__alias__ = []
__version__ = '0.8.0'
__authors__ = 'Thomas Cokelaer'
__institutes__ = 'INRIA/CIRAD'
__icon__ = 'icon.png'


__all__ = [
    'py_pylab_PyLabPlot3D',
]



py_pylab_PyLabPlot3D = Factory(name='PyLabPlot3D',
                description='pylab.fontproperties interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabPlot3D',
                inputs=None, outputs=None, widgetmodule=None, widgetclass=None,
                lazy=False
               )

