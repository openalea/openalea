"""Some parameters"""


def build_dict(inputs, add_none=False):
    output = {}
    for this in inputs:
        output[this] = this
    if add_none:
        output['None'] = None
    
    return output





arrowstyles = build_dict(['-','->','-[','-|>','<-', '<->','<|-', '<|-|>', 'fancy', 'simple', 'wedge'])   
boxstyles = build_dict(['round', 'round4', 'larrow','rarrow','roundtooth', 'sawtooth', 'square'])
connectionstyles = build_dict(['angle', 'angle3','arc','arc3', 'bar'])
ecs = {'none':'none','':''}
extends = {'neither':'neither', 'both':'both',  'min':'min', 'max':'max' }
fillstyles=['top','full','bottom','left','right']
xycoords = build_dict(['figure points', 'figure pixels', 'figure fraction', 'axes points', 'axes pixels', 'axes fraction', 'data', 'offset points', 'polar'])
which = build_dict(['major', 'minor', 'both'])
spacings = { 'uniform':'uniform','proportional':'proportional'} 
scale = {'linear':'linear', 'log':'log', 'symlog':'symlog'}
ticks= {'auto':'auto', 'None':'None'}
shadings = build_dict(['flat', 'faceted'])
axis = {
    'off':'off',
    'manual':'manual',
    'equal':'equal',
    'tight':'tight',
    'scaled':'scaled',
    'image':'image',
    'auto':'auto',
    'normal':'normal'
    }


detrends = {
    'none':'detrend_none',
    'linear':'detrend_linear',
    'mean':'detrend_mean'
    }

streches = {
    'ultra-condensed':'ultra-condensed',
    'extra-condensed':'extra-condensed',
    'condensed':'condensed',
    'semi-condensed':'semi-condensed',
    'normal':'normal',
    'semi-expanded':'semi-expanded',
    'expanded':'expanded',
    'extra-expanded':'extra-expanded' ,
    'ultra-expanded':'ultra-expanded'
    }

weights = {
    'ultralight':'ultralight',
    'light':'light',
    'normal':'normal',
    'regular':'regular',
    'book':'book',
    'medium':'medium',
    'roman':'roman',
    'semibold':'semibold',
    'demibold':'demibold',
    'demi':'demi',
    'bold':'bold',
    'heavy':'heavy',
    'extra bold':'extra bold',
    'black':'black'
    }


sizes = {
    'xx-small':'xx-small',
    'x-small':'x-small',
    'small':'small',
    'medium':'medium',
    'large':'large',
    'x-large':'x-large',
    'xx-large':'xx-large'
    }

styles = {
    'italic':'italic',
    'normal':'normal',
    'oblique':'oblique'}

variants = {
    'normal':'normal',
    'small-caps':'small-caps'}

families = {
    'serif':'serif',
    'sans-serif':'sans-serif',
    'cursive':'cursive',
    'fantasy':'fantasy',
    'monospace':'monospace'}

horizontalalignment = {
    'center':'center',
    'right':'right' ,
    'left':'left' }

verticalalignment = {
    'center':'center' ,
    'top':'top' ,
    'bottom':'bottom' ,
    'baseline':'baseline'}


origins = {'lower':'lower',
    'upper':'upper',
    'None':None,
    'image':'image'
    }

extensions = {'png':'png',
    'pdf':'pdf',
    'ps':'ps',
    'eps':'eps',
    'svg':'svg'
    }


fillstyles={'top':'top',
    'full':'full',
    'bottom':'bottom',
    'left':'left',
    'right':'right',
    }
orientations = {'vertical':'vertical','horizontal':'horizontal'}

histtype = {'bar':'bar','barstacked':'barstacked',  'step' :'step','stepfilled':'stepfilled'}
        
align = {'mid':'mid', 'right':'right', 'left':'left'}
        
orientation_fig = {
    'portrait':'portrait',
    'landscape':'landscape'}


papertypes = {}
for x in ['letter',
    'legal', 'executive','ledger','a0',
    'a1','a2','a3','a4','a5','a6','a7','a8',
    'a9','a10','b0','b1','b2','b3','b4',
    'b5','b6','b7','b8','b9','b10']:
    papertypes[x] = x
    
            


locations = {
            'best' : 0,
            'upper right'  : 1,
            'upper left'   : 2,
            'lower left'   : 3,
            'lower right'  : 4,
            'right'        : 5,
            'center left'  : 6,
            'center right' : 7,
            'lower center' : 8,
            'upper center' : 9,
            'center'       : 10,}

        
from matplotlib import mlab
windows = {'hanning':mlab.window_hanning,
           'hamming, bartlett, blackman, kaiser (use numpy.window)':None, 
           'none':mlab.window_none}
sides = ['default','onesided','twosided']

from pylab import cm, get_cmap
maps=[m for m in cm.datad if not m.endswith("_r")]
cmaps = {}
for c in maps:
    cmaps[c] = get_cmap(c)
cmaps['None'] = None

angles = ['uv', 'xy']
units= ['width','height','dots','inches','x','y']
pivots = ['tail', 'middle', 'tip']


interpolations = build_dict(['nearest', 'bilinear',
          'bicubic', 'spline16', 'spline36', 'hanning', 'hamming',
          'hermite', 'kaiser', 'quadric', 'catrom', 'gaussian',
          'bessel', 'mitchell', 'sinc', 'lanczos'], add_none=True)
    




aspects = build_dict(['auto', 'equal'], add_none=True)
colors =  {
           'blue':'b',
           'green':'g',
           'red':'r',
           'cyan':'c',
           'magenta':'m',            
           'purple':'purple',
           'yellow':'y',
           'black':'k',
           'white':'w',
           'None':None}
        
        
def get_valid_color(color='blue'):

    if color in colors.keys():
        print '1'
        return colors[color]
    elif type(color)==str:
        if len(color)!=7 or color[0]!='#':
            raise ValueError('hexa string must be like #ffffff')
        print '2', color
        return color
    else:
        print '3',
        from matplotlib.colors import rgb2hex
        try:
            import numpy
            c = rgb2hex(numpy.array(color)/256.)
            print c
            return c
        except:
            raise TypeError('colors must be valid matplotlib symbol, or a string (hex code) or a RGB list/array. %s provided' % color)

from pylab import Line2D
drawstyles = {}
for key,value in Line2D.drawStyles.iteritems():
    drawstyles[value.replace('_draw_','')]=key

linestyles = {}
for key,value in Line2D.lineStyles.iteritems():
    linestyles[value.replace('_draw_','')]=key

markers = {}
for key,value in Line2D.markers.iteritems():
    markers[value.replace('_draw_','')]=key







"""from matplotlib.pyplot import rcParams:
{'agg.path.chunksize': 0,
 'axes.axisbelow': False,
 'axes.color_cycle': ['b', 'g', 'r', 'c', 'm', 'y', 'k'],
 'axes.edgecolor': 'k',
 'axes.facecolor': 'w',
 'axes.formatter.limits': [-7, 7],
 'axes.grid': False,
 'axes.hold': True,
 'axes.labelcolor': 'k',
 'axes.labelsize': 'medium',
 'axes.linewidth': 1.0,
 'axes.titlesize': 'large',
 'axes.unicode_minus': True,
 'axes3d.grid': True,
 'backend': 'Qt4Agg',
 'backend_fallback': True,
 'cairo.format': 'png',
 'contour.negative_linestyle': 'dashed',
 'datapath': '/home/cokelaer/Work/virtualplants/trunk/lib/python2.6/site-packages/matplotlib-1.0.0-py2.6-linux-i686.egg/matplotlib/mpl-data',
 'docstring.hardcopy': False,
 'figure.autolayout': False,
 'figure.dpi': 80,
 'figure.edgecolor': 'w',
 'figure.facecolor': '0.75',
 'figure.figsize': [8.0, 6.0],
 'figure.subplot.bottom': 0.10000000000000001,
 'figure.subplot.hspace': 0.20000000000000001,
 'figure.subplot.left': 0.125,
 'figure.subplot.right': 0.90000000000000002,
 'figure.subplot.top': 0.90000000000000002,
 'figure.subplot.wspace': 0.20000000000000001,
 'font.cursive': ['Apple Chancery',
                  'Textile',
                  'Zapf Chancery',
                  'Sand',
                  'cursive'],
 'font.family': 'sans-serif',
 'font.fantasy': ['Comic Sans MS',
                  'Chicago',
                  'Charcoal',
                  'ImpactWestern',
                  'fantasy'],
 'font.monospace': ['Bitstream Vera Sans Mono',
                    'DejaVu Sans Mono',
                    'Andale Mono',
                    'Nimbus Mono L',
                    'Courier New',
                    'Courier',
                    'Fixed',
                    'Terminal',
                    'monospace'],
 'font.sans-serif': ['Bitstream Vera Sans',
                     'DejaVu Sans',
                     'Lucida Grande',
                     'Verdana',
                     'Geneva',
                     'Lucid',
                     'Arial',
                     'Helvetica',
                     'Avant Garde',
                     'sans-serif'],
 'font.serif': ['Bitstream Vera Serif',
                'DejaVu Serif',
                'New Century Schoolbook',
                'Century Schoolbook L',
                'Utopia',
                'ITC Bookman',
                'Bookman',
                'Nimbus Roman No9 L',
                'Times New Roman',
                'Times',
                'Palatino',
                'Charter',
                'serif'],
 'font.size': 12.0,
 'font.stretch': 'normal',
 'font.style': 'normal',
 'font.variant': 'normal',
 'font.weight': 'normal',
 'grid.color': 'k',
 'grid.linestyle': ':',
 'grid.linewidth': 0.5,
 'image.aspect': 'equal',
 'image.cmap': 'jet',
 'image.interpolation': 'bilinear',
 'image.lut': 256,
 'image.origin': 'upper',
 'image.resample': False,
 'interactive': True,
 'keymap.all_axes': 'a',
 'keymap.back': ['left', 'c', 'backspace'],
 'keymap.forward': ['right', 'v'],
 'keymap.fullscreen': 'f',
 'keymap.grid': 'g',
 'keymap.home': ['h', 'r', 'home'],
 'keymap.pan': 'p',
 'keymap.save': 's',
 'keymap.xscale': ['k', 'L'],
 'keymap.yscale': 'l',
 'keymap.zoom': 'o',
 'legend.borderaxespad': 0.5,
 'legend.borderpad': 0.40000000000000002,
 'legend.columnspacing': 2.0,
 'legend.fancybox': False,
 'legend.fontsize': 'large',
 'legend.handlelength': 2.0,
 'legend.handletextpad': 0.80000000000000004,
 'legend.isaxes': True,
 'legend.labelspacing': 0.5,
 'legend.loc': 'upper right',
 'legend.markerscale': 1.0,
 'legend.numpoints': 2,
 'legend.shadow': False,
 'lines.antialiased': True,
 'lines.color': 'b',
 'lines.dash_capstyle': 'butt',
 'lines.dash_joinstyle': 'round',
 'lines.linestyle': '-',
 'lines.linewidth': 1.0,
 'lines.marker': 'None',
 'lines.markeredgewidth': 0.5,
 'lines.markersize': 6,
 'lines.solid_capstyle': 'projecting',
 'lines.solid_joinstyle': 'round',
 'maskedarray': 'obsolete',
 'mathtext.bf': 'serif:bold',
 'mathtext.cal': 'cursive',
 'mathtext.default': 'it',
 'mathtext.fallback_to_cm': True,
 'mathtext.fontset': 'cm',
 'mathtext.it': 'serif:italic',
 'mathtext.rm': 'serif',
 'mathtext.sf': 'sans\\-serif',
 'mathtext.tt': 'monospace',
 'numerix': 'obsolete',
 'patch.antialiased': True,
 'patch.edgecolor': 'k',
 'patch.facecolor': 'b',
 'patch.linewidth': 1.0,
 'path.simplify': True,
 'path.simplify_threshold': 0.1111111111111111,
 'path.snap': True,
 'pdf.compression': 6,
 'pdf.fonttype': 3,
 'pdf.inheritcolor': False,
 'pdf.use14corefonts': False,
 'plugins.directory': '.matplotlib_plugins',
 'polaraxes.grid': True,
 'ps.distiller.res': 6000,
 'ps.fonttype': 3,
 'ps.papersize': 'letter',
 'ps.useafm': False,
 'ps.usedistiller': False,
 'savefig.dpi': 100,
 'savefig.edgecolor': 'w',
 'savefig.extension': 'auto',
 'savefig.facecolor': 'w',
 'savefig.orientation': 'portrait',
 'svg.embed_char_paths': True,
 'svg.image_inline': True,
 'svg.image_noscale': False,
 'text.color': 'k',
 'text.dvipnghack': None,
 'text.fontangle': 'normal',
 'text.fontsize': 'medium',
 'text.fontstyle': 'normal',
 'text.fontvariant': 'normal',
 'text.fontweight': 'normal',
 'text.hinting': True,
 'text.latex.preamble': [''],
 'text.latex.preview': False,
 'text.latex.unicode': False,
 'text.usetex': False,
 'timezone': 'UTC',
 'tk.pythoninspect': False,
 'tk.window_focus': False,
 'toolbar': 'toolbar2',
 'units': False,
 'verbose.fileo': 'sys.stdout',
 'verbose.level': 'silent',
 'xtick.color': 'k',
 'xtick.direction': 'in',
 'xtick.labelsize': 'medium',
 'xtick.major.pad': 4,
 'xtick.major.size': 4,
 'xtick.minor.pad': 4,
 'xtick.minor.size': 2,
 'ytick.color': 'k',
 'ytick.direction': 'in',
 'ytick.labelsize': 'medium',
 'ytick.major.pad': 4,
 'ytick.major.size': 4,
 'ytick.minor.pad': 4,
 'ytick.minor.size': 2}
"""



class Line2DFactory():
    def __init__(self, line2d):
        self.line2d = line2d
        self.kwds = line2d.properties()
        
    def get_kwds(self, type='standard'):
        if type == 'axhline':
            del self.kwds['transform']


def get_kwds_from_line2d(line2d=None, input_kwds={}, type=None):
    """create a dict from line2d properties
    """
    import copy
    kwds = copy.deepcopy(input_kwds)
    if type=='stem':
        return input_kwds
    if line2d!=None:
        kwds['color']=line2d.get_color()    
        kwds['facecolor']=line2d.get_color()
        kwds['linestyle']=line2d.get_linestyle()
        kwds['linewidth']=line2d.get_linewidth()
        if type!='linecollection':
            kwds['marker']=line2d.get_marker()
            kwds['markersize']=line2d.get_markersize()
            kwds['markeredgewidth']=line2d.get_markeredgewidth()
            kwds['markersize']=line2d.get_markersize()
            kwds['fillstyle']=line2d.get_fillstyle()
            kwds['markeredgecolor']=line2d.get_markeredgecolor()
            kwds['label']=line2d.get_label()
            kwds['alpha']=line2d.get_alpha()
    
    if type=='hist':
        for x in ['color','linestyle','marker','markersize','markeredgewidth','fillstyle','markeredgecolor']:
                try:
                    del kwds[x]
                except:
                    pass
    if type in ['csd', 'psd', 'step', 'polar']:
        try:
            del kwds['facecolor']
        except:
            pass
        
    if type=='specgram':
        for x in s['facecolor','color','linewidth',
                   'linestyle','marker','markersize','markeredgewidth',
                   'fillstyle','markeredgecolor']:
            try:
                del kwds[x]
            except:
                pass

    if type=='plot':
        try:
            del kwds['facecolor']
        except:
            pass

    return kwds





def line2d2kwds(line2d, kwds={}):
    try:
        for key, value in line2d.properties().iteritems():
            kwds[key] = value
    except:
        print 'warning: line2d may not be a valid Line2D object'
        pass
    return kwds


def text2kwds(text, kwds={}):
    try:
        for key, value in text.properties().properties():
            kwds[key] = value
    except:
        print 'warning: text may not be a valid Text object'
        pass
    return kwds

def font2kwds(font, kwds={}):
    pass



class CustomizeAxes(object):
    def __init__(self):
        pass
    
    def get_axes(self):
        axes = self.get_input('axes')
        if axes == None:
            from pylab import gca
            axes = gca()
            return [axes]
        
        if type(axes)!=list:
            axes = [axes]
            for axe in axes:
                import matplotlib
                assert axe.__module__ in [matplotlib.axes.__name__,matplotlib.projections.polar.__name__], 'input must be a valid axes from matplotlib.axes %s given for %s' % (type(axes), axes)
            return axes



parameters = {




}
