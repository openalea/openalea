
import unittest

from openalea.core.service.interface import interface_class, guess_interface


class TestProject(unittest.TestCase):

    def test_interface_class(self):
        from openalea.core.interface import IInt, IFloat

        self.assertIs(interface_class('IInt'), IInt)
        self.assertIs(interface_class('int'), IInt)
        self.assertIs(interface_class(int), IInt)

        self.assertIs(interface_class('IFloat'), IFloat)
        self.assertIs(interface_class('float'), IFloat)
        self.assertIs(interface_class(float), IFloat)

    def test_guess_interface(self):
        assert 'IInt' in guess_interface(1)
        assert 'IFloat' in guess_interface(1.)
