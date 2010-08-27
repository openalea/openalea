from openalea.core.alea import *

pm = PackageManager()
pm.init(verbose=False)


import pylab

def test_pylab_test_acorr():

    for node in  ['acorr', 'axhline/axvline', 'boxplot', 'errorbar', 'fill', 'plot']:
        res = run(('openalea.pylab.test', node),{},pm=pm)
        pylab.close()
        assert res == []


