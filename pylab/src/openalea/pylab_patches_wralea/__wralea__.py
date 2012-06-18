
# This file has been generated at Sat Mar  6 21:17:54 2010

from openalea.core import Factory
from openalea.deploy import get_metainfo


version = get_metainfo('openalea.pylab', 'version')
authors = get_metainfo('openalea.pylab', 'author')


__name__ = 'openalea.pylab.patches'

__editable__ = False
__description__ = 'patches (ellipse, rectangle) from pylab.patches'
__license__ = 'CECILL-C'
__url__ = 'http://openalea.gforge.inria.fr/doc/openalea/pylab/doc/_build/html/contents.html'
__alias__ = []
__version__ = version
__authors__ = authors
__institutes__ = 'INRIA/CIRAD'
__icon__ = 'icon.png'


__all__ = [
'py_pylab_PyLabPatchDictionary',
'py_pylab_PyLabCircle',
'py_pylab_PyLabEllipse',
'py_pylab_PyLabRectangle',
'py_pylab_PyLabPolygon',
'py_pylab_PyLabWedge',
]



py_pylab_PyLabPatchDictionary = Factory(name='PyLabPatchDictionary',
                description='pylab.fontproperties interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabPatchDictionary',
                inputs=None, outputs=None, widgetmodule=None, widgetclass=None, lazy=False
               )

py_pylab_PyLabCircle = Factory(name='PyLabCircle',
                description='pylab.fontproperties interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabCircle',
                inputs=None, outputs=None, widgetmodule=None, widgetclass=None, lazy=False
                )


py_pylab_PyLabEllipse = Factory(name='PyLabEllipse',
                description='pylab.fontproperties interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabEllipse',
                inputs=None, outputs=None, widgetmodule=None, widgetclass=None, lazy=False
                )

py_pylab_PyLabRectangle = Factory(name='PyLabRectangle',
                description='pylab.fontproperties interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabRectangle',
                inputs=None, outputs=None, widgetmodule=None, widgetclass=None, lazy=False
                )

py_pylab_PyLabPolygon = Factory(name='PyLabPolygon',
                description='pylab.fontproperties interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabPolygon',
                inputs=None, outputs=None, widgetmodule=None, widgetclass=None, lazy=False
                )

py_pylab_PyLabWedge = Factory(name='PyLabWedge',
                description='pylab.fontproperties interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabWedge',
                inputs=None, outputs=None, widgetmodule=None, widgetclass=None, lazy=False
                )
