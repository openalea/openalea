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


from openalea.oalab.testing.mimedata import SampleCustomData
from openalea.oalab.testing.qtunittest import QtTestCase

from openalea.oalab.testing.drag_and_drop import DragAndDropWidget
from openalea.oalab.service.drag_and_drop import add_drop_callback, add_drag_format, encode_to_qmimedata

from Qt import QtGui, QtCore, QtTest

class TestCase(QtTestCase):

    def setUp(self):
        self.init()

    def tearDown(self):
        self.finalize()

    def test_custom_data_drop(self):
        self.widget = DragAndDropWidget()

        index = self.widget.drag.model.index(1, 0)
        pos = self.widget.drag.visualRect(index).center()
        pos = self.widget.drag.mapFromGlobal(pos)
        self.widget.drag.setCurrentIndex(index)

        QtTest.QTest.mousePress(self.widget.drag, QtCore.Qt.LeftButton, pos=pos, delay=1)
        QtTest.QTest.mouseMove(self.widget.drop)
        QtTest.QTest.mouseRelease(self.widget.drop, QtCore.Qt.LeftButton)

        self.pause(2)

#
# test_drag_and_drop.py ends here
