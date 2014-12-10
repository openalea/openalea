
import unittest
from openalea.core.path import tempdir, path
from openalea.core.service.data import DataFactory, MimeType


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

        d1 = DataFactory(path=filepath, default_content=default_content)
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
        d2 = DataFactory(path=get_data('image.tiff'))
        assert d2.path.name == 'image.tiff'

        # Cannot set content because data yet exists
        # Case mimetype is not defined
        with self.assertRaises(ValueError) as cm:
            d3 = DataFactory(path=get_data('image.tiff'), default_content=b'')
        msg = "got multiple values for content (parameter and 'image.tiff')"
        self.assertEqual(cm.exception.message, msg)

        # Path is a directory and not a file
        empty_dir = self.tmpdir / "empty"
        empty_dir.mkdir()  # No need to remove it after test. Parent dir will be removed in tearDown

        with self.assertRaises(ValueError) as cm:
            d4 = DataFactory(path=empty_dir, default_content=b'')
        msg = "'%s' exists but is not a file" % empty_dir
        self.assertEqual(cm.exception.message, msg)

        d5 = DataFactory(path=self.tmpdir / "doesnotexist" / "image.tiff", default_content=default_content)
        assert d5.exists() == False
        assert d5._content == default_content

    def test_mimetype(self):
        self.assertEqual(MimeType('test.py'), 'text/x-python')
        self.assertEqual(MimeType(name='py'), 'text/x-python')
        self.assertEqual(MimeType(name='python'), 'text/x-python')
        self.assertEqual(MimeType(name='Python'), 'text/x-python')
        self.assertEqual(MimeType('image.tiff'), 'image/tiff')

    def test_DataClass(self):
        from openalea.core.data import Data, PythonFile

        d = DataFactory(path='test.dat')
        self.assertIsInstance(d, Data)

        d = DataFactory(path='test.py')
        self.assertIsInstance(d, PythonFile)

        d = DataFactory(path='test.py', dtype='data')
        self.assertIsInstance(d, Data)

        with self.assertRaises(ValueError) as cm:
            DataFactory('model.py', mimetype='image/tiff', dtype='Python')
        msg = "dtype 'Python' (text/x-python) and mimetype 'image/tiff' are not compatible"
        self.assertEqual(cm.exception.message, msg)

        # Case file do not exists on disk ...
        # Only dtype is available
        d = DataFactory(path=self.tmpdir / 'test.py', dtype='Python')
        self.assertEqual(d.mimetype, 'text/x-python')

        # Only mimetype is available
        d = DataFactory(path=self.tmpdir / 'test.py', mimetype='text/x-python')
        self.assertEqual(d.mimetype, 'text/x-python')

    def test_arrange_data_args(self):
        # arrange_data_args is not a public function, please do not use it outside service.data
        from openalea.core.service.data import arrange_data_args
        path1 = get_data('model.py')
        path2 = 'test.ext'
        self.assertEqual(arrange_data_args(path1, None, None), (path1, 'text/x-python'))

        self.assertEqual(arrange_data_args(path2, None, None), (path2, None))
        self.assertEqual(arrange_data_args(path2, 'text/x-python', None), (path2, 'text/x-python'))
        self.assertEqual(arrange_data_args(path2, None, 'Python'), (path2, 'text/x-python'))
