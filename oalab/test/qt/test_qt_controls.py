# Version: $Id$
#
#

# Commentary:
#
#

# Change Log:
#
#

# Code:

from Qt import QtWidgets

from openalea.core.service.control import create_control
from openalea.oalab.service.qt_control import qt_editor

instance = QtWidgets.QApplication.instance()
if instance is None:
    app = QtWidgets.QApplication([])

control = create_control('i', 'IInt', 250, dict(min=200, max=300))
widget = qt_editor(control)
# widget.show()
assert control.value == 250
assert widget.value() == 250

#if instance is None:
#     app.exec_()

#
# test_qt_controls.py ends here
