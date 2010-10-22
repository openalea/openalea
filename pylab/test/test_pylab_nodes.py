from openalea.core.alea import *

pm = PackageManager()
pm.init(verbose=False)

test_names = ['acorr', 'boxplot', 'cohere', 'colorbar', 'contour', 'csd', 'errorbar', 'fill', 'hexbin', 'hist', 'imshow', 'loglog', 'pcolor', 'pie',  'plot', 'polar', 'psd', 'quiver', 'scatter', 'specgram', 'stem', 'step', 'xcorr']

demo_names = ['polar_demo','labels_demo','cross_spectral_density_windowing','hexbin_and_colorbar','SeveralAxesOnSameFigure','pie_demo','scatter_and_histograms','scatter_demo','Line2D_and_multiplots','test_image.npy','fill_between','patches','plot_demos']


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

