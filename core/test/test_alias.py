
from openalea.core.pkgmanager import PackageManager


def test_load():
    pkgman = PackageManager()
    pkgman.load_directory("pkg")

    assert pkgman["pkg_test"]
    assert pkgman["pkg_alias"] is pkgman["pkg_test"]
    


def test_alias():
    pkgman = PackageManager()
    pkgman.load_directory("pkg")

    assert pkgman["pkg_test"]["file2.txt"] 
    assert pkgman["pkg_test"]["file2.txt"] is pkgman["pkg_test"]["f"]
    assert pkgman["pkg_test"]["file2.txt"] is pkgman["pkg_test"]["g"]

    assert pkgman["pkg_test"]["file1.txt"] 
    assert pkgman["pkg_test"]["aliasf1"] is pkgman["pkg_test"]["file1.txt"]
    
def test_catalog():
    pkgman = PackageManager()
    pkgman.init(verbose=False)

    assert pkgman["catalog.data"["int"] is pkgman["openalea.data structure"["int"]
