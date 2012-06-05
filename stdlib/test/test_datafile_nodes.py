'''Test of data file nodes''' 

from openalea.core.alea import *
from openalea.core.path import path

pm = PackageManager()
pm.init(verbose=False)

def test_get_data():
    res = run(('openalea.data file', 'get_data'), inputs={'package': 'alinea.caribu.data', 'filename': 'filterT.can'}, pm=pm)
    assert path(res[0]).basename() == 'filterT.can'
    res = run(('openalea.data file', 'get_data'), inputs={'package': 'openalea.core', 'filename': 'test_image.npy'}, pm=pm)
    assert path(res[0]).basename() == 'test_image.npy'
    res = run(('openalea.data file', 'get_data'), inputs={'package': 'vplants.fractalysis', 'filename': 'mango_f21_L.bgeom'}, pm=pm)
    assert path(res[0]).basename() == 'mango_f21_L.bgeom'
    res = run(('openalea.data file', 'get_data'), inputs={'package': 'openalea.stat_tool', 'filename': 'meri1.his'}, pm=pm)
    assert res[0] == None
    

