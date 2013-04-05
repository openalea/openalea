from openalea.vpltk.qt import QtGui
from openalea.core.alea import *
from openalea.visualea.dataflowview import GraphicalGraph

app = QtGui.QApplication([])

pm = PackageManager()
pm.init()
pkg = pm['openalea.pylab.demo']


for this in ['SeveralAxesOnSameFigure']:
    factory = pkg.get_factory(this)
    node = factory.instantiate()

    #run_and_display(('openalea.pylab.test', 'hist'),{},pm=pm)

    view = GraphicalGraph.create_view(node)
    view.show()
    #QtGui.QPixmap.grabWindow(GtGui.QApplication.desktop().winId()).save('%s.png' % this, 'png')

    filename = 'dataflow_%s.png' % this

    # Get current workspace
    # Retreive the user layout
    rect = view.scene().sceneRect()
    matrix = view.matrix()
    rect = matrix.mapRect(rect)
    
    pixmap = QtGui.QPixmap(rect.width(), rect.height())
    pixmap.fill()
    painter = QtGui.QPainter(pixmap)
    painter.setRenderHint(QtGui.QPainter.Antialiasing)
    view.update()
    view.render(painter)
    #view.scene().render(painter)
    painter.end()
    pixmap.save(filename)

    view.close()
#app.exec_()
