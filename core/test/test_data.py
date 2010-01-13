"""Data tests"""

__license__ = "Cecill-C"
__revision__ = " $Id: test_data.py 1586 2009-01-30 15:56:25Z cokelaer $ "

from openalea.core.pkgmanager import PackageManager


def test_data():
    """test data"""
    pm = PackageManager()
    pm.init()

    assert pm['pkg_test']['file1.txt']
    assert pm['pkg_test']['file2.txt']
