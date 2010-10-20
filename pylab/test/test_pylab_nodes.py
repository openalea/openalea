from openalea.core.alea import *

pm = PackageManager()
pm.init(verbose=False)

test_names = ['acorr', 'boxplot', 'cohere', 'contour', 'csd', 'errorbar', 'fill', 'hexbin', 'hist', 'loglog', 'pcolor', 'pie',  'plot', 'polar', 'psd', 'quiver', 'scatter', 'specgram', 'stem', 'step']

demo_names = ['imshow', 'polar_demo','labels demo','cross spectral density and windowing','hexbin and colorbar','SeveralAxesOnSameFigure','pie demo','scatter and histograms','scatter demo','Line2D and multi plot','test_image.npy','fill_between','patches','plot demos']


datasets = ['PyLabBivariateNormal']


def test_datasets():
    for i in range(0, len(datasets)):
        yield check,'datasets', datasets[i]

def test_tests():
    for i in range(0, len(test_names)):
        yield check,'test', test_names[i]

def test_demos():
    for i in range(0, len(demo_names)):
        yield check,'demo', demo_names[i]

def check(wralea, name):
    res = run(('openalea.pylab.%s' % wralea, name),{},pm=pm)
    from pylab import close
    close('all')

