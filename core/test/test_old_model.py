
import unittest
from openalea.core.data import Data
from openalea.core.path import tempdir, path


def debug_parse(self, code):
    self.parsed = True


def get_data(filename):
    return path(__file__).parent.abspath() / 'data' / filename


class TestProject(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempdir()

    def tearDown(self):
        self.tmpdir.rmtree()

    def todo_inmemory_data(self):
        from openalea.core.model import Model
        Model.parse = debug_parse
        Model.parsed = False

        # Check content is parsed
        model = Model(content='Hi ho', filename='model.py')
        assert model.parsed is True
        model.parsed = False

        model = Model(content='Hi ho', filename='model.py')

        # Check content is not parsed because content has not changed
        model.parsed = False
        content = model.read()
        assert model.parsed is False

        # Check content is parsed again because content has been explicitly changed
        model.content = 'captain'
        assert model.parsed is True

    def todo_infile_data(self):
        from openalea.core.data import Model
        # Create a python file
        pyfile = self.tmpdir / 'model.py'
        with open(pyfile, 'w') as f:
            f.write('data 1')

        Model.set_code = debug_parse

        # Check no parse. At this moment we don't want to read content for performance reason
        model = Model(path=pyfile)
        assert hasattr(model, 'parsed') is False

        # To get documentation, Model need to read content
        content = model.read()
        assert model.parsed is True
        model.parsed = False

        # Check that cache works: file don't have changed, no need to read and parse it again
        content = model.read()
        assert model.parsed is False
        assert content == "data 1"

        # Simulate a change
        with open(pyfile, 'w') as f:
            f.write('new data')

        # pyfile has changed, it need to be read again!
        content = model.read()
        assert model.parsed is True
        assert content == "new data"

        model.parsed = False
        model.set_cache_mode(model.NO_CACHE)
        model.read()
        assert model.parsed is True

    def test_edit_same_data(self):
        # True: In memory data with same path and content
        d1 = Data(path=self.tmpdir / 'test.dat')
        d2 = Data(path=self.tmpdir / 'test.dat')
        assert(d1.is_same_data(d2))
        assert(d2.is_same_data(d1))

        # True: In memory data with same name and content
        d1 = Data(filename='test.dat', content='a')
        d2 = Data(filename='test.dat', content='a')
        assert(d1.is_same_data(d2))
        assert(d2.is_same_data(d1))

        # False: In memory Data with same name and different content
        d1 = Data(filename='test.dat', content='a')
        d2 = Data(filename='test.dat', content='b')
        assert(d1.is_same_data(d2) is False)
        assert(d2.is_same_data(d1) is False)

        # False: In memory Data with same path and different content
        d1 = Data(path=self.tmpdir / 'test.dat', content='a')
        d2 = Data(path=self.tmpdir / 'test.dat', content='b')
        assert(d1.is_same_data(d2) is False)
        assert(d2.is_same_data(d1) is False)

        # True: In memory Data with different name and same content
        d1 = Data(filename='test1.dat', content='a')
        d2 = Data(filename='test2.dat', content='a')
        assert(d1.is_same_data(d2))
        assert(d2.is_same_data(d1))

        # True: On disk Data with same path
        d1 = Data(path=get_data('image.tiff'))
        d2 = Data(path=get_data('image.tiff'))
        assert(d1.is_same_data(d2))
        assert(d2.is_same_data(d1))

        # False: On disk Data with different path
        d1 = Data(path=get_data('image.tiff'))
        d2 = Data(path=get_data('model.py'))
        assert(d1.is_same_data(d2) is False)
        assert(d2.is_same_data(d1) is False)

        # False: One on disk other in memory, same filename, same content different path
        # MUST RETURN FALSE
        d1 = Data(path=self.tmpdir / 'model.py', content="print 'hello world'\n")
        d2 = Data(path=get_data('model.py'))
        assert(d1.is_same_data(d2) is False)
        assert(d2.is_same_data(d1) is False)
        self.assertEqual(d1.read(), "print 'hello world'\n")
        self.assertEqual(d2.read(), "print 'hello world'\n")
        self.assertEqual(d1.filename, d2.filename)
