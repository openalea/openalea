"""NoCaseDict tests"""

__license__ = "Cecill-C"
__revision__ = " $Id: test_nocasedict.py 1586 2009-01-30 15:56:25Z cokelaer $ "

from openalea.core.pkgdict import PackageDict


def test_dict():
    """Test packageDict"""
    d = PackageDict()
    d['AbC'] = 3
    assert d['aBc'] == 3
    print d


if __name__=="__main__":
    test_dict()
