
import unittest
from openalea.core.path import tempdir, path
from openalea.oalab.service.data import data


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
        content = b'blob'

        d1 = data(path=filepath, content=content)
        assert d1.path.name == 'new_image.tiff'
        assert d1.name == 'new_image'
        assert filepath.isfile()

        f = filepath.open('rb')
        content2 = f.read()
        f.close()
        assert content == content2

        # Embed existing data  (image.tiff exists)
        d2 = data(path=get_data('image.tiff'))
        assert d2.path.name == 'image.tiff'
        assert d2.name == 'image'

        # Cannot set content because data yet exists
        # Case datatype is not defined
        with self.assertRaises(ValueError) as cm:
            d3 = data(path=get_data('image.tiff'), content=b'')
        msg = "got multiple values for content (parameter and 'image.tiff')"
        self.assertEqual(cm.exception.message, msg)

