

# Load SampleCustomData, associated codecs and register its
from openalea.oalab.testing.mimedata import SampleCustomData
from openalea.oalab.testing.qtunittest import QtTestCase

from openalea.oalab.testing.drag_and_drop import DragAndDropWidget
from openalea.oalab.service.drag_and_drop import add_drop_callback, add_drag_format, encode_to_qmimedata

from PyQt4.QtTest import QTest
from openalea.vpltk.qt import QtGui, QtCore


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

        QTest.mousePress(self.widget.drag, QtCore.Qt.LeftButton, pos=pos, delay=1)
        QTest.mouseMove(self.widget.drop)
        QTest.mouseRelease(self.widget.drop, QtCore.Qt.LeftButton)

        self.pause(2)
