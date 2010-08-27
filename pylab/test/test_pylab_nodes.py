from openalea.core.alea import *

pm = PackageManager()
pm.init(verbose=False)


def test_pylab_nodes():
    res = run(('openalea.pylab.nodes', 'PyLabRandom'),{},pm=pm)
    assert len(res[0]) == 100

res = test_pylab_nodes()

