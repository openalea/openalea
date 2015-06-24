
from openalea.vpltk.qt import QtGui
from openalea.core.service.control import create_control
from openalea.oalab.service.qt_control import qt_editor

instance = QtGui.QApplication.instance()
if instance is None:
    app = QtGui.QApplication([])


control = create_control('i', 'IInt', 250, dict(min=200, max=300))
widget = qt_editor(control)
# widget.show()
assert control.value == 250
assert widget.value() == 250

#if instance is None:
#     app.exec_()
