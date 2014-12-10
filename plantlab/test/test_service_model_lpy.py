
import unittest
from openalea.core.service.model import ModelClass, ModelFactory
from openalea.core.model import Model
from openalea.plantlab.lpy import LPyModel

"""
Like core/test/test_service_model but test LPy model class instead of Python model class.
"""


class TestProject(unittest.TestCase):

    def test_model_class(self):

        mclass = ModelClass(mimetype='text/vnd-lpy')
        self.assertEqual(mclass, LPyModel)

        mclass = ModelClass(dtype='LSystem')
        self.assertEqual(mclass, LPyModel)

        self.assertIn(LPyModel, ModelClass())

        mclass = ModelClass(mimetype='text/unknown')
        self.assertEqual(mclass, Model)

    def test_model_factory(self):
        m = ModelFactory(name='MyModel', mimetype='text/vnd-lpy')
        self.assertIsInstance(m, LPyModel)
        self.assertEqual(m.name, "MyModel")
