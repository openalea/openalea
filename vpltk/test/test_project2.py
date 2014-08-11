
import unittest
from openalea.core.path import tempdir, path
from openalea.vpltk.project.project2 import Project

def get_data(filename):
    return path(__file__).parent.abspath() / 'data' / filename

class TestProject(unittest.TestCase):

    def setUp(self):
        self.tmpdir = tempdir()
        self.project = Project('test', projectdir=self.tmpdir)

    def tearDown(self):
        self.project = None
        self.tmpdir.rmtree()

    def test_path_incompatibility(self):
        from openalea.oalab.service import new_data

        model = new_data('model', get_data('model.py'))
        model2 = self.project.add('model', model)
        assert model is not model2
        assert model2.path == self.project.path / 'model' / 'model.py'

        model = new_data('model', filename='model.py')
        model = self.project.add('model', model)
        assert model.path == self.project.path / 'model' / 'model.py'

    def test_add_data(self):

        # Create new data from scratch
        d1 = self.project.add('data', filename='image_1.tiff', content=b'')
        assert d1.path.name == 'image_1.tiff'
        assert d1.name == 'image_1'

        # Create new data and get content and name from existing file
        d2 = self.project.add('data', path=get_data('image_2.tiff'))
        assert d2.path.name == 'image_2.tiff'
        assert d2.name == 'image_2'

        # Create new data with explicit name and get content from existing file
        d3 = self.project.add('data', path=get_data('image_2.tiff'), name='image_3')
        assert d3.name == 'image_3'
        assert d3.path.name == 'image_3.tiff'

        # Create new data with explicit filename and get content from existing file
        # Warning: in this test, extension is changed
        d4 = self.project.add('data', path=get_data('image.jpg'), filename='image_4.jpeg')
        assert d4.name == 'image_4'
        assert d4.path.name == 'image_4.jpeg'

        for data in [d1, d2, d3, d4]:
            assert data.path.parent == self.project.path / 'data'

        assert len(self.project.data) == 4



    def test_add_exceptions(self):

        # Case of path passed doesn't exist
        with self.assertRaises(ValueError) as cm:
            self.project.add('data', path='/do/not/exist.err')

        msg = "ValueError: path '/do/not/exist.err' doesn't exists"
        self.assertEqual(cm.exception.message, msg)
        assert(len(self.project.data) == 0)


        # Case datatype is not defined
        with self.assertRaises(ValueError) as cm:
            self.project.add('data', name='image_1')

        msg = "ValueError: datatype is not defined"
        self.assertEqual(cm.exception.message, msg)
        assert(len(self.project.data) == 0)

        # Case user give an existing path and a content
        with self.assertRaises(ValueError) as cm:
            self.project.add('data', path=get_data('image.jpg'), content=b'')

        msg = "ValueError: 'content' and 'path' are mutually exclusive"
        self.assertEqual(cm.exception.message, msg)
        assert(len(self.project.data) == 0)

        # Add an object twice
        self.project.add('data', filename='image.png')
        with self.assertRaises(ValueError) as cm:
            self.project.add('data', filename='image.png')

        msg = "ValueError: data 'image.png' already exists in project 'test'"
        self.assertEqual(cm.exception.message, msg)



    def test_add_model(self):

        m1 = self.project.add('model', name='model_1', datatype='python', content='print 1')
        assert m1.code == 'print 1'
        assert m1.name == 'model_1'
        assert str(m1.filename) == 'model_1.py'
        assert m1.path == self.project.path / 'model' / 'model_1.py'

        m2 = self.project.add('model', filename='model_2.py', content='print 2')
        assert m2.code == 'print 2'
        assert m2.name == 'model_2'
        assert str(m2.filename) == 'model_2.py'
        assert m2.path == self.project.path / 'model' / 'model_2.py'


        sample = get_data('model.py')
        f = open(sample)
        code = f.read()
        f.close()

        m3 = self.project.add('model', path=sample, name='model_3')
        assert m3.name == 'model_3'
        assert str(m3.filename) == 'model_3.py'
        assert m3.path == self.project.path / 'model' / 'model_3.py'
        assert m3.code == code

        m4 = self.project.add('model', name='model_1', datatype='py', content='print 1')
        assert m4.code == 'print 1'
        assert m4.name == 'model_1'
        assert str(m4.filename) == 'model_1.py'
        assert m4.path == self.project.path / 'model' / 'model_1.py'


        # Check object is a valid model
        for model in [m1, m2, m3, m4]:
            assert hasattr(model, 'run')
            assert model.datatype == 'python'


    def test_load(self):
        project = Project('test_project_lpy', projectdir='data')
        assert len(project.model) == 1
        assert len(project.cache) == 4
        assert len(project.startup) == 1

        lpy = project.model['noise_branch-2d']
        assert lpy.extension == 'lpy'

#     def test_save(self):
#
#         proj = self.project
#         proj.add("model", filename="plop.py", content="print 'hello world'")
#         proj.save()
#
#         assert len(proj.model) == 1
#
#         proj2 = Project('test', self.tmpdir)
#
#         assert len(proj2.model) == 1
#         # assert len(proj2.control) == 2
#         # assert proj2.control["my_integer"] == 42
#         # assert proj2.control["my_float"] == 3.14
#         assert proj2.model["plop"].code == "print 'hello world'"
#
#         pm.close('test')


    def test_add_script(self):
        self.project.add("model", filename="1.py", content="blablabla")
        self.project.add("model", filename="2.py", content="blablabla2")
#         self.project.add("model", filename="2.py", content="blablabla2")
        assert len(self.project.models()) == 2


    def test_rename(self):
        self.project.add("model", filename="1.py", content="blablabla")

        model1_path = self.project.path / 'model' / '1.py'
        model2_path = self.project.path / 'model' / '2.py'

        assert model1_path.isfile()

        self.project.rename("model", "1", "2")
        assert len(self.project.src) == 1
        assert self.project.model["2"].code == "blablabla"

        # Old bug, path lost extension at rename
        model2_badpath = self.project.path / 'model' / '2'
        assert model2_badpath.exists() is False
        assert model2_path.isfile()


    def test_rename_project(self):
        self.project.add("model", filename="1.py", content="blablabla")
        self.project.rename("project", "test", "test2")
        assert self.project.name == "test2"

