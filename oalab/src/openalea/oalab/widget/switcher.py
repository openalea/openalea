
import weakref
from openalea.vpltk.qt import QtGui, QtCore


class WidgetSwitcher(QtGui.QWidget):

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)
        self._previous = None

        self._layout = QtGui.QHBoxLayout(self)

        p = QtGui.QSizePolicy

    def set_widget(self, widget_class, *args, **kwargs):
        """
        This method switch attribute dele
        """
        if self._previous:
            previous = self._previous()
            self._layout.removeWidget(previous)
            previous.setParent(None)
            previous.close()
            self._previous = None
            del previous

        widget = widget_class(*args, **kwargs)
        p = QtGui.QSizePolicy
        widget.setSizePolicy(p(p.MinimumExpanding, p.MinimumExpanding))
        widget.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self._layout.addWidget(widget)
        self._previous = weakref.ref(widget)
