
import unittest
from openalea.core.service.model import ModelClass, ModelFactory
from openalea.core.model import Model, PythonModel


class TestProject(unittest.TestCase):

    def test_model_class(self):

        mclass = ModelClass(mimetype='text/x-python')
        self.assertEqual(mclass, PythonModel)

        mclass = ModelClass(dtype='Python')
        self.assertEqual(mclass, PythonModel)

        self.assertIn(PythonModel, ModelClass())

        mclass = ModelClass(mimetype='text/unknown')
        self.assertEqual(mclass, Model)

    def test_model_factory(self):
        m = ModelFactory(name='MyModel', mimetype='text/x-python')
        self.assertIsInstance(m, PythonModel)
        self.assertEqual(m.name, "MyModel")
