from openalea.core.alea import *
from openalea.core.path import path

pm = PackageManager()
pm.init(verbose=False)

def test_shared_data_browser():
    res = run(('openalea.misc.test','shared_data_browser'), {}, pm=pm)
    assert res == []
    res = run(('openalea.misc', 'SharedDataBrowser'), inputs={'package': 'openalea.stat_tool', 'filename': 'meri1.his'}, pm=pm)
    assert path(res[0]).basename() == 'meri1.his'
    res = run(('openalea.misc', 'SharedDataBrowser'), inputs={'package': 'vplants.sequence_analysis', 'filename': 'cafe_ortho1.seq'}, pm=pm)
    assert path(res[0]).basename() == 'cafe_ortho1.seq'
    res = run(('openalea.misc', 'SharedDataBrowser'), inputs={'package': 'alinea.caribu', 'filename': 'filterT.can'}, pm=pm)
    assert path(res[0]).basename() == 'filterT.can'
    res = run(('openalea.misc', 'SharedDataBrowser'),inputs={'package': 'numpy', 'filename': 'something.something'}, pm=pm)
    assert res[0] == None
    res = run(('openalea.misc', 'SharedDataBrowser'),inputs={'package': 'alinea.adel.data', 'filename': 'dimTSoissons.csv'}, pm=pm)
    assert res[0] == None

#if __name__ == "__main__":
#    test_demo_corsican()
#    test_demo_dycorinia()
#    test_stat_tool_tutorial_compound()
#    test_stat_tool_tutorial_convolution()

