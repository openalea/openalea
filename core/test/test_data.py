from openalea.core.pkgmanager import PackageManager

def test_data():
    pm = PackageManager()
    pm.init()

    assert pm['pkg_test']['file1.txt']
    assert pm['pkg_test']['file2.txt']
