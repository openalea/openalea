"""Alias tests"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

from openalea.core.pkgmanager import PackageManager


def test_load():
    """test_load: load directory in PackageManager"""
    pkgman = PackageManager()
    pkgman.load_directory("pkg")
    assert pkgman["pkg_test"]
    assert pkgman["pkg_alias"]==pkgman["pkg_test"]


def test_alias():
    """test_alias: aliases in PackageManager"""
    pkgman = PackageManager()
    pkgman.load_directory("pkg")

    assert pkgman["pkg_test"]["file2.txt"]
    assert pkgman["pkg_test"]["file2.txt"] is pkgman["pkg_test"]["f"]
    assert pkgman["pkg_test"]["file2.txt"] is pkgman["pkg_test"]["g"]
    assert pkgman["pkg_test"]["file1.txt"]
    assert pkgman["pkg_test"]["aliasf1"] is pkgman["pkg_test"]["file1.txt"]


