
# This file has been generated at Sat Mar  6 21:17:54 2010

from openalea.core import Factory
from openalea.deploy import get_metainfo

version = get_metainfo('openalea.pylab', 'version')
authors = get_metainfo('openalea.pylab', 'author')


__name__ = 'openalea.pylab.Axes decorators'

__editable__ = False
__description__ = 'Utilities to manipulate axes or add components on them.'
__license__ = 'CECILL-C'
__url__ = 'http://openalea.gforge.inria.fr/doc/openalea/pylab/doc/_build/html/contents.html'
__alias__ = []
__version__ = version
__authors__ = authors
__institutes__ = 'INRIA/CIRAD'
__icon__ = 'icon.png'


__all__ = [
'py_pylab_PyLabFigure',
'py_pylab_PyLabXLabel',
'py_pylab_PyLabYLabel',
'py_pylab_PyLabXLim',
'py_pylab_PyLabYLim',
'py_pylab_PyLabLegend',
'py_pylab_PyLabAxes',
'py_pylab_PyLabGrid',
'py_pylab_PyLabFontProperties',
'py_pylab_PyLabTextProperties',
'py_pylab_PyLabAxis',
'py_pylab_PyLabTitle',
'py_pylab_PyLabCLF',
'py_pylab_PyLabTickParams',
'py_pylab_PyLabXTicks',
'py_pylab_PyLabYTicks',
'py_pylab_PyLabSaveFig',
'py_pylab_PyLabAxesDecorator',
'py_pylab_PyLabShow',
'py_pylab_PyLabTextOptions',
'py_pylab_PyLabColorMap',
'py_pylab_PyLabBox',
]


py_pylab_PyLabShow = Factory(name='PyLabShow',
                description='calls pylab.show()',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabShow',
                inputs=None, outputs=None, widgetmodule=None, widgetclass=None, lazy=False
                )

py_pylab_PyLabTickParams = Factory(name='PyLabTickParams',
                description='pylab.fontproperties interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabTickParams',
                inputs=None, outputs=None, widgetmodule=None, widgetclass=None, lazy=False
                )

py_pylab_PyLabBox = Factory(name='PyLabBox',
                description='pylab.fontproperties interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabBox',
                inputs=None, outputs=None, widgetmodule=None, widgetclass=None, lazy=False
                )

py_pylab_PyLabFigure = Factory(name='PyLabFigure',
                description='pylab.figure interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabFigure',
                inputs=None,
                outputs=None,
                widgetmodule=None,
                widgetclass=None,
                lazy=False
               )

py_pylab_PyLabXLabel = Factory(name='PyLabXLabel',
                description='pylab.xlabel interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabXLabel',
                inputs=None,
                outputs=None,
                widgetmodule=None,
                widgetclass=None,
                lazy=False
               )

py_pylab_PyLabYLabel = Factory(name='PyLabYLabel',
                description='pylab.ylabel interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabYLabel',
                inputs=None,
                outputs=None,
                widgetmodule=None,
                widgetclass=None,
                lazy=False
               )

py_pylab_PyLabLegend = Factory(name='PyLabLegend',
                description='pylab.legend interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabLegend',
                inputs=None,
                outputs=None,
                widgetmodule=None,
                widgetclass=None,
                lazy=False
               )




py_pylab_PyLabTextOptions = Factory(name='PyLabTextOptions',
                description='pylab.text interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabTextOptions',
                inputs=None,
                outputs=None,
                widgetmodule=None,
                widgetclass=None,
                lazy=False
               )


py_pylab_PyLabAxes = Factory(name='PyLabAxes',
                description='pylab.axes interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabAxes',
                inputs=None,
                outputs=None,
                widgetmodule=None,
                widgetclass=None,
                lazy=False
               )

py_pylab_PyLabAxis = Factory(name='PyLabAxis',
                description='pylab.axes interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabAxis',
                inputs=None,
                outputs=None,
                widgetmodule=None,
                widgetclass=None,
                lazy=False
               )


py_pylab_PyLabTitle = Factory(name='PyLabTitle',
                description='pylab.title interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabTitle',
                inputs=None,
                outputs=None,
                widgetmodule=None,
                widgetclass=None,
                lazy=False
               )

py_pylab_PyLabCLF = Factory(name='PyLabClearFigure',
                description='pylab.title interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabClearFigure',
                inputs=None,
                outputs=None,
                widgetmodule=None,
                widgetclass=None,
                lazy=False
               )


py_pylab_PyLabTextProperties = Factory(name='PyLabTextProperties',
                description='pylab.fontproperties interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabTextProperties',
                inputs=None,
                outputs=None,
                widgetmodule=None,
                widgetclass=None,
                lazy=False
               )


py_pylab_PyLabFontProperties = Factory(name='PyLabFontProperties',
                description='pylab.fontproperties interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabFontProperties',
                inputs=None,
                outputs=None,
                widgetmodule=None,
                widgetclass=None,
                lazy=False
               )




py_pylab_PyLabSaveFig = Factory(name='PyLabSaveFig',
                description='pylab.fontproperties interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabSaveFig',
                inputs=None,
                outputs=None,
                widgetmodule=None,
                widgetclass=None,
                lazy=False
               )


py_pylab_PyLabColorMap = Factory(name='PyLabColorMap',
                description='pylab.fontproperties interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabColorMap',
                inputs=None,
                outputs=None,
                widgetmodule=None,
                widgetclass=None,
                lazy=False
               )



py_pylab_PyLabXLim = Factory(name='PyLabXLim',
                description='pylab.fontproperties interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabXLim',
                inputs=None, outputs=None, widgetmodule=None, widgetclass=None, lazy=False
                )

py_pylab_PyLabYLim = Factory(name='PyLabYLim',
                description='pylab.fontproperties interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabYLim',
                inputs=None, outputs=None, widgetmodule=None, widgetclass=None, lazy=False
                )

py_pylab_PyLabXTicks = Factory(name='PyLabXTicks',
                description='pylab.fontproperties interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabXTicks',
                inputs=None, outputs=None, widgetmodule=None, widgetclass=None, lazy=False
                )

py_pylab_PyLabYTicks = Factory(name='PyLabYTicks',
                description='pylab.fontproperties interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabYTicks',
                inputs=None, outputs=None, widgetmodule=None, widgetclass=None, lazy=False
                )
py_pylab_PyLabGrid = Factory(name='PyLabGrid',
                description='pylab.fontproperties interface.',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabGrid',
                inputs=None, outputs=None, widgetmodule=None, widgetclass=None, lazy=False
                )
py_pylab_PyLabOrigin = Factory(name='PyLabOrigin',
                description='enum origni (lower/upper/none) used by imshow ',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabOrigin',
                inputs=None, outputs=None, widgetmodule=None, widgetclass=None, lazy=False
                )
py_pylab_PyLabAxesDecorator = Factory(name='PyLabAxesDecorator',
                description='todo',
                category='visualization, data processing',
                nodemodule='py_pylab',
                nodeclass='PyLabAxesDecorator',
                inputs=None, outputs=None, widgetmodule=None, widgetclass=None
                )
