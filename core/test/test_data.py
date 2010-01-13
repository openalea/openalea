"""Data tests"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

from openalea.core.pkgmanager import PackageManager


def test_data():
    """test data"""
    pm = PackageManager()
    pm.init()

    assert pm['pkg_test']['file1.txt']
    assert pm['pkg_test']['file2.txt']
