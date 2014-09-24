
from openalea.vpltk.qt import QtCore, QtGui

import sys

try:
    workdir = sys.argv[1]
except IndexError:
    print 'usage: script outputdir'
    sys.exit(1)

app = QtGui.QApplication([])

from openalea.oalab.service.qt_control import qt_widget_plugins
from openalea.core.service import interface_names
from openalea.core.control import Control

for iname in interface_names():
    for plugin in qt_widget_plugins(iname):
        if 'responsive' in plugin.edit_shape:
            shapes = ['vline', 'hline', 'large']
        else:
            shapes = plugin.edit_shape
        for shape, size in [
                ('small', (50, 50)),
                ('hline', (200, 30)),
                ('vline', (30, 200)),
                ('large', None),
                ]:
            if shape not in shapes:
                continue

            control = Control('c', iname, widget=plugin.name)
            w_editor_class = plugin.load()
            if issubclass(w_editor_class, QtGui.QWidget):
                w_editor = w_editor_class()
            else:
                w_editor = w_editor_class.edit(control, shape=shape)
            if w_editor :
                widget = QtGui.QWidget()
                widget.setAttribute(QtCore.Qt.WA_DeleteOnClose)
                layout = QtGui.QVBoxLayout(widget)
                layout.setContentsMargins(1, 1, 1, 1)
                if size:
                    widget.setMinimumSize(*size)
                    widget.resize(*size)
                    widget.setMaximumSize(*size)
                else:
                    widget.setMinimumSize(64, 64)
                layout.addWidget(w_editor)
#                 layout.addStretch()
                widget.show()
                widget.raise_()

                x = widget.pos().x()
                y = widget.pos().y()
                w = widget.size().width()
                h = widget.size().height()

                pixmap = QtGui.QPixmap.grabWindow(widget.winId(), 0, 0, w, h)

                filename = '%s/%s_%s_%s.png' % (workdir, iname, plugin.name, shape)
                pixmap.save(filename)

                if shape == 'large':
                    filename = '%s/preview_%s.png' % (workdir, iname)
                    pixmap.save(filename)


                widget.close()

app.exec_()
