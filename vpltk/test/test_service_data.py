
import unittest
from openalea.core.path import tempdir, path
from openalea.oalab.service.data import data, datatype


def get_data(filename):
    return path(__file__).parent.abspath() / 'data' / filename

class TestProject(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempdir()

    def tearDown(self):
        self.tmpdir.rmtree()

    def test_new_data(self):

        # Create new data from scratch (image_1.tiff doesn't exist)
        filepath = self.tmpdir / 'new_image.tiff'
        default_content = b'blob'

        d1 = data(path=filepath, default_content=default_content)
        assert d1.path.name == 'new_image.tiff'
        assert filepath.isfile()
        assert d1.exists() is True
        # To check if memory has been freed
        assert d1._content is None

        f = filepath.open('rb')
        content2 = f.read()
        f.close()
        assert default_content == content2

        # Embed existing data  (image.tiff exists)
        d2 = data(path=get_data('image.tiff'))
        assert d2.path.name == 'image.tiff'

        # Cannot set content because data yet exists
        # Case datatype is not defined
        with self.assertRaises(ValueError) as cm:
            d3 = data(path=get_data('image.tiff'), default_content=b'')
        msg = "got multiple values for content (parameter and 'image.tiff')"
        self.assertEqual(cm.exception.message, msg)

        # Path is a directory and not a file
        empty_dir = self.tmpdir/"empty"
        empty_dir.mkdir()  # No need to remove it after test. Parent dir will be removed in tearDown

        with self.assertRaises(ValueError) as cm:
            d4 = data(path=empty_dir, default_content=b'')
        msg = "'%s' exists but is not a file" % empty_dir
        self.assertEqual(cm.exception.message, msg)

        d5 = data(path=self.tmpdir/"doesnotexist"/"image.tiff", default_content=default_content)
        assert d5.exists() == False
        assert d5._content == default_content

    def test_datatype(self):
        self.assertEqual(datatype('test.py'), 'text/x-python')
        self.assertEqual(datatype(name='py'), 'text/x-python')
        self.assertEqual(datatype(name='python'), 'text/x-python')
        self.assertEqual(datatype(name='Python'), 'text/x-python')
        self.assertEqual(datatype('image.tiff'), 'image/tiff')


    def test_dataclass(self):
        from openalea.vpltk.datamodel.data import Data
        from openalea.vpltk.datamodel.python import PythonModel

        d = data(path='test.dat')
        self.assertIsInstance(d, Data)

        d = data(path='test.py')
        self.assertIsInstance(d, PythonModel)

        d = data(path='test.py', dtype='data')
        self.assertIsInstance(d, Data)

