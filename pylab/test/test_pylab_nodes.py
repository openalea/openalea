from openalea.core.alea import *

pm = PackageManager()
pm.init(verbose=False)

names = ['acorr', 'boxplot', 'cohere', 'contour', 'csd', 'errorbar', 'fill', 'hexbin', 'hist', 'loglog', 'pcolor', 'pie', 'plot', 'polar', 'psd', 'quiver', 'scatter', 'specgram', 'stem', 'step']

def test_all():
    for i in range(0, len(names)):
        yield check,names[i]

def check(name):
    res = run(('openalea.pylab.test', name),{},pm=pm)

