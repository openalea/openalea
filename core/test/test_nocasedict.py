from openalea.core.pkgdict import PackageDict

def test_dict():
    
    d = PackageDict()
    d['AbC'] = 3
    assert d['aBc'] == 3
    print d

test_dict()
