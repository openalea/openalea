
import unittest

from openalea.core.service.control import create_control
from openalea.core.control import Control
from openalea.core.control.serialization import (ControlSaver, ControlLoader, ControlSerializer, ControlDeserializer)
from openalea.core.path import tempdir


class TestControls(unittest.TestCase):

    def compare_controls(self, c1, c2):
        self.assertEqual(c1.name, c2.name)
        self.assertEqual(c1.value, c2.value)
        self.assertEqual(type(c1.interface).__name__, type(c2.interface).__name__)
        self.assertEqual(repr(c1.interface), repr(c2.interface))

    def test_controls(self):

        c1 = Control('a', value=1, constraints=dict(min=1, max=2))
        assert c1.interface.min == 1
        assert c1.interface.max == 2
        assert c1.value == 1
        self.assertEqual(repr(c1.interface), 'IInt(min=1, max=2, step=1)')

        c2 = Control('a', 'IInt', constraints=dict(min=3, max=4))
        assert c2.interface.min == 3
        assert c2.interface.max == 4
        #assert c2.value == 3

        c3 = Control('a', 'IInt', constraints=dict(min=5, max=6))

        c4 = Control('a', 'IInt')
        c5 = Control('a', value=4)

        cb1 = create_control('a', value=1, constraints=dict(min=1, max=2))
        cb2 = create_control('a', 'IInt', constraints=dict(min=3, max=4))
        cb3 = create_control('a', 'IInt', value=0, constraints=dict(min=5, max=6))
        cb4 = create_control('a', 'IInt')
        cb5 = create_control('a', value=4)

        self.compare_controls(c1, cb1)
        self.compare_controls(c2, cb2)
        self.compare_controls(c3, cb3)
        self.compare_controls(c4, cb4)
        self.compare_controls(c5, cb5)

    def test_serialization(self):
        c1 = Control('a', value=1,  constraints=dict(min=1, max=2))
        c2 = Control('a', 'IInt', constraints=dict(min=3, max=4))
        orig = [c1, c2]

        serializer = ControlSerializer()
        it = serializer.serialize(orig)

        deserializer = ControlDeserializer()
        controls = deserializer.deserialize(it)

        assert len(controls) == len(orig)
        for i in range(len(orig)):
            self.compare_controls(orig[i], controls[i])

    def test_load_save(self):
        c1 = Control('a', value=1,  constraints=dict(min=1, max=2))
        c2 = Control('a', 'IStr', 'salut')
        orig = [c1, c2]

        tmp = tempdir()
        saver = ControlSaver()
        saver.save(orig, tmp / 'control.py')

        loader = ControlLoader()
        controls = loader.load(tmp / 'control.py')
        tmp.rmtree()

        assert len(controls) == len(orig)
        for i in range(len(orig)):
            self.compare_controls(orig[i], controls[i])
