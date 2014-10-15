import unittest
import os
import sys

from openalea.core.path import path as Path
from openalea.core.path import tempdir


class MyAlgo(object):

    def __init__(self):
        pass


class MyAlgoPlugin(object):

    def __call__(self):
        return MyAlgo


def install_package():
    tmppath = tempdir()
    pythonpath = tmppath / 'lib'

    sys.path.insert(0, pythonpath)

    testpath = Path(__file__).parent.abspath()
    pythonpath.mkdir()

    sys.path.insert(0, pythonpath / 'tstpkg1-0.1-py2.7.egg')
    PYTHONPATH = os.environ['PYTHONPATH']
    PYTHONPATH = os.pathsep.join([pythonpath, PYTHONPATH])
    os.environ['PYTHONPATH'] = PYTHONPATH

    oldcwd = os.getcwd()
    oldargs = list(sys.argv)
    os.chdir(testpath / 'tstdistrib')
    from setuptools import setup
    setup(
        name="tstpkg1",
        version="0.1",
        packages=['tstpkg1'],

        entry_points={
            'test.c1': [
                'Plugin1 = tstpkg1.plugin:C1Plugin1',
                'Plugin2 = tstpkg1.plugin:C1Plugin2',
            ],
            'test.c2': [
                'Plugin1 = tstpkg1.plugin:C2Plugin1',
                'Plugin2 = tstpkg1.plugin:C2Plugin2',
            ],
        },
        script_args=[
            'install',
            '--install-base=%s' % tmppath,
            '--install-purelib=%s' % pythonpath,
            '--install-platlib=%s' % pythonpath,
            '--install-scripts=%s' % (tmppath / 'bin'),
            '--install-headers=%s' % (tmppath / 'include'),
            '--install-data=%s' % (tmppath / 'share'),
        ]
    )
    os.chdir(oldcwd)
    sys.argv = oldargs

    return tmppath, pythonpath


class TestPluginManager(unittest.TestCase):

    @classmethod
    def setupClass(cls):
        cls.tmppath, cls.pythonpath = install_package()

        import pkg_resources
        dist = list(pkg_resources.find_distributions(cls.pythonpath))[0]
        pkg_resources.working_set.add(dist)

    def setUp(self):
        from openalea.core.plugin.manager import PluginManager
        self.pm = PluginManager()

    def test_autoload(self):
        assert self.pm._plugin == {}
        self.pm.plugins('test.c1')
        assert 'test.c1' in self.pm._plugin

    def test_dynamic_plugin(self):
        pass

    def test_plugin_name(self):
        import tstpkg1.plugin
        import tstpkg1.impl

        # Check manager use plugin name attribute if defined (instead of class name)
        c1plugin1 = self.pm.plugin('test.c1', 'MyPlugin1')
        assert c1plugin1 is tstpkg1.plugin.C1Plugin1

        # Check there is no conflict if two plugins with same alias (in setup.py) but in different categories
        # Check plugin name use class name if no attribute "name"
        c2plugin1 = self.pm.plugin('test.c2', 'C2Plugin1')
        assert c2plugin1 is tstpkg1.plugin.C2Plugin1

    def test_new_instance(self):
        import tstpkg1.impl

        objc1c1 = self.pm.instance('test.c1', 'MyPlugin1')
        assert objc1c1
        assert isinstance(objc1c1, tstpkg1.impl.C1Class1)

        objc1c2 = self.pm.instance('test.c1', 'MyPlugin2')
        assert objc1c2
        assert isinstance(objc1c2, tstpkg1.impl.C1Class2)

        objc2c1 = self.pm.instance('test.c2', 'C2Plugin1')
        assert objc2c1
        assert isinstance(objc2c1, tstpkg1.impl.C2Class1)

        objc2c2 = self.pm.instance('test.c2', 'C2Plugin2')
        assert objc2c1
        assert isinstance(objc2c2, tstpkg1.impl.C2Class2)

        # Check instance return existing instance
        objc1c1_2 = self.pm.instance('test.c1', 'MyPlugin1')
        assert objc1c1 is objc1c1_2
        assert self.pm.instances('test.c1', 'MyPlugin1')[0] is objc1c1_2

    def test_multiple_instance(self):
        # Assert weakref work correctly and plugin instances have been lost
        assert not self.pm.instances('test.c1', 'MyPlugin1')

        objc1c1_0 = self.pm.instance('test.c1', 'MyPlugin1')
        objc1c1_1 = self.pm.new('test.c1', 'MyPlugin1')
        objc1c1_2 = self.pm.new('test.c1', 'MyPlugin1')

        # Assert all object have been created correctly
        assert objc1c1_0
        assert objc1c1_1
        assert objc1c1_2

        # Assert all instances are different as we use new instead of instance
        assert objc1c1_0 is not objc1c1_1
        assert objc1c1_1 is not objc1c1_2

        objc1c2 = self.pm.new('test.c1', 'MyPlugin2')

        assert len(self.pm.instances('test.c1', 'MyPlugin1')) == 3
        assert len(self.pm.instances('test.c1')) == 4

        del objc1c1_2

        assert len(self.pm.instances('test.c1', 'MyPlugin1')) == 2
        assert len(self.pm.instances('test.c1')) == 3

        del objc1c2

        assert len(self.pm.instances('test.c1', 'MyPlugin1')) == 2
        assert len(self.pm.instances('test.c1', 'MyPlugin2')) == 0
        assert len(self.pm.instances('test.c1')) == 2

    @classmethod
    def tearDownClass(cls):
        cls.tmppath.rmtree()
