

from openalea.core.data import PythonFile
from openalea.core.model import PythonModel
from openalea.core.path import tempdir

from openalea.oalab.paradigm.container import ParadigmContainer
from openalea.oalab.testing.qtunittest import QtTestCase
from openalea.vpltk.qt import QtGui, QtCore

from PyQt4.QtTest import QTest

SAMPLE_CODE = "# sample"


class TestCaseParadigmEditor(QtTestCase):

    def setUp(self):
        self.init()
        self.tmpdir = tempdir()

        self.model = PythonModel(name='func')
        self.model.set_code(SAMPLE_CODE)
        self.data = PythonFile(content=SAMPLE_CODE, path=self.tmpdir / "test.py")

    def tearDown(self):
        self.tmpdir.rmtree()
        self.finalize()

    def test_open_data(self):
        self.widget = ParadigmContainer()
        self.widget.open_data(self.data)

    def test_apply_and_save(self):
        self.widget = ParadigmContainer()
        self.widget.open_data(self.data)

        memory_code = "# How are you ?"
        hdd_code = "# Fine!"

        pyqode = self.widget.currentWidget()

        pyqode.setPlainText(memory_code)

        # Unchanged because data has not been saved
        self.assertEquals(self.data.content, SAMPLE_CODE)

        # APPLY: change data object but do not save on disk
        self.widget.apply()
        # Changed in memory but not on disk
        self.assertFalse(self.data.path.exists())
        self.assertEquals(self.data.content, memory_code)

        pyqode.setPlainText(hdd_code)
        self.widget.save()
        # SAVE: change data object and save to disk
        with open(self.data.path, 'r') as f:
            disk_code = f.read()
        self.assertEquals(self.data.content, hdd_code)
        self.assertEquals(disk_code, hdd_code)
