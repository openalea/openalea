
from openalea.core.pkgmanager import PackageManager


def test_load():
    pkgman = PackageManager()
    pkgman.load_directory("pkg")

    assert pkgman["pkg_test"]
    assert pkgman["pkg_alias"] is pkgman["pkg_test"]
    


def test_alias():
    pkgman = PackageManager()
    pkgman.load_directory("pkg")

    assert pkgman["pkg_test"]["file1.txt"] 
    assert pkgman["pkg_test"]["file1.txt"] is pkgman["pkg_test"]["filealias"]

