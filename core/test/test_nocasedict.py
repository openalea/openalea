from openalea.core.nocasedict import NoCaseDict

def test_dict():
    
    d = NoCaseDict()
    d['AbC'] = 3
    assert d['aBc'] == 3
    print d

test_dict()
