from openalea.core.alea import *

pm = PackageManager()
pm.init(verbose=False)

test_names = ['acorr', 'annotation', 'axhline_axvline', 'axhspan_axvspan', 'boxplot', 
    'cohere', 'circle', 'cohere', 'colorbar', 'contour', 'csd', 'ellipse', 'errorbar', 
    'figure', 'fill', 'fill_between', 'grid', 'hexbin', 'hist', 'imshow', 'legend', 
    'loglog', 'mcontour3d', 'mcontourf3d', 'mplot3d', 'patches', 'pcolor', 'pie',  
    'plot', 'polygon', 'polar', 'psd', 'quiver', 'rectangle', 'scatter', 
    'semilogx', 'semilogy', 'specgram', 'stem', 'step', 'tickparams', 'title', 
    'tutorial_plot', 'tutorial_plot_line2d', 'wedge', 'xcorr', 
    'xylabels', 'xylim', 'xyticks']

demo_names = ['polar_scatter', 'polar_demo','labels_demo','cross_spectral_density_windowing','hexbin_and_colorbar','SeveralAxesOnSameFigure','pie_demo','scatter_and_histograms','scatter_demo','Line2D_and_multiplots','test_image.npy','fill_between','patches','plot_demos']


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

