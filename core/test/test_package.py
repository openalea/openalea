__license__ = "Cecill-C"
__revision__ = " $Id$ "

from openalea.core.package import *
from openalea.core.node import gen_port_list
import os, shutil


def test_package():
    metainfo = {'version': '0.0.1',
              'license': 'CECILL-C',
              'authors': 'OpenAlea Consortium',
              'institutes': 'INRIA/CIRAD',
              'description': 'Base library.',
              'url': 'http://openalea.gforge.inria.fr',
              'icon': ''}

    package = Package("Test", metainfo)
    assert package != None


class TestUserPackage():
    def setUp(self):
        os.mkdir("tstpkg")

    def tearDown(self):
        shutil.rmtree("tstpkg")

    def test_case_1(self):

        metainfo = {'version': '0.0.1',
                  'license': 'CECILL-C',
                  'authors': 'OpenAlea Consortium',
                  'institutes': 'INRIA/CIRAD',
                  'description': 'Base library.',
                  'url': 'http://openalea.gforge.inria.fr',
                  'icon': ''}

        path = os.path.join(os.path.curdir, "tstpkg")
        mypackage = UserPackage("DummyPkg", metainfo, path)


        factory = mypackage.create_user_node("TestFact",
                                             "category test",
                                             "this is a test",
                                             gen_port_list(3),
                                             gen_port_list(2))
        assert path in factory.search_path
        assert len(factory.inputs)==3
        assert len(factory.outputs)==2

        assert os.path.exists("tstpkg/TestFact.py")
        execfile("tstpkg/TestFact.py")

        mypackage.write()
        assert os.path.exists("tstpkg/__wralea__.py")
        assert os.path.exists("tstpkg/__init__.py")
        execfile("tstpkg/__wralea__.py")

        # Test_clone_package
        path = os.path.join(os.path.curdir, "clonepkg")
        pkg2 = UserPackage("ClonePkg", metainfo, path)
        print pkg2.wralea_path


        # todo this is not working !!
        from openalea.core.pkgmanager import PackageManager
        pm = PackageManager()
        pm.add_wralea_path(path, pm.temporary_wralea_paths)
        pm.init()
        pkg2.clone_from_package(mypackage)
        pkg2.write()

        assert len(pkg2) == 1
        assert len(pkg2["TestFact"].inputs) == 3
        assert id(pkg2["TestFact"]) != id(mypackage["TestFact"])
        assert os.path.exists(path)
        assert os.path.exists(os.path.join(path, '__wralea__.py'))
        assert os.path.exists(os.path.join(path, '__init__.py'))
        assert os.path.exists(os.path.join(path, 'TestFact.py'))
