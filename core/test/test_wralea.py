__license__ = "Cecill-C"
__revision__ = " $Id$ "

from openalea.core import *


def register_packages(pkgmanager):

    metainfo={'version': '0.0.1',
              'license': 'CECILL-C',
              'authors': 'OpenAlea Consortium',
              'institutes': 'INRIA/CIRAD',
              'description': 'TESTS.',
              'url': 'http://openalea.gforge.inria.fr'}


    package1 = Package("Test", metainfo)

    # Test buitin
    nf = Factory(name="sum",
                 nodeclass="sum",
          inputs=(dict(name='in', interface=None), ),
          outputs=(dict(name='out', interface=None), ),
                  )

    package1.add_factory(nf)

    # user function
    nf = Factory(name= "userfunc",
                 nodeclass = "userfunc",
                 nodemodule = "moduletest",
                 )

    package1.add_factory(nf)

    # user class
    nf = Factory(name= "userclass",
                 nodeclass = "userclass",
                 nodemodule = "moduletest",
                 )

    package1.add_factory(nf)

    pkgmanager.add_package(package1)


from openalea.core.pkgmanager import PackageManager


def test_register():
    """Test register"""
    pkgmanager = PackageManager()

    register_packages(pkgmanager)

    assert "test" in pkgmanager.keys()

    pkg = pkgmanager["Test"]

    assert "sum" in pkg.keys()
    assert "userclass" in pkg.keys()
    assert "userfunc" in pkg.keys()

    fact = pkg["sum"]
    node = fact.instantiate()
    assert (node.get_nb_input() == 1) and (node.get_nb_output() == 1)

    fact = pkg["userfunc"]
    node = fact.instantiate()
    assert (node.get_nb_input() == 2) and (node.get_nb_output() == 1)

    fact = pkg["userclass"]
    node = fact.instantiate()
    assert (node.get_nb_input() == 2) and (node.get_nb_output() == 1)
