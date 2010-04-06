###############################################################################
# -*- python -*-
#
#       amlPy function implementation
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA
#
#       File author(s): Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

__doc__="""
amlPy functions
"""

__license__= "Cecill-C"
__revision__=" $Id: py_stat.py 7897 2010-02-09 09:06:21Z cokelaer $ "

#//////////////////////////////////////////////////////////////////////////////


from openalea.core import Node
from openalea.core import Factory, IFileStr, IInt, IBool, IFloat, \
    ISequence, IEnumStr, IStr, IDirStr, ITuple3, IDict

#matplotlib.pyplot.rcParams

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

sides = { 'default':'default',  'onesided':'onesided',  'twosided':'twosided' }

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
    'fantasy':'fantisy',
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

ticks= {'auto':'auto', 'None':'None'}

colors = {
    'blue':'b',
    'green':'g',
    'red':'r',
    'cyan':'c',
    'magenta':'m',
    'yellow':'y',
    'black':'k',
    'white':'w',
    'None':'None'}


from pylab import Line2D

drawstyles = {}
for key,value in Line2D.drawStyles.iteritems():
    drawstyles[value.replace('_draw_','')]=key

# line style --, -., .....
linestyles = {}
for key,value in Line2D.lineStyles.iteritems():
    linestyles[value.replace('_draw_','')]=key

# markers : o, square, ...
markers = {}
for key,value in Line2D.markers.iteritems():
    markers[value.replace('_draw_','')]=key

#pylab.Line2D.filled_markers

fillstyles={'top':'top',
    'full':'full',
    'bottom':'bottom',
    'left':'left',
    'right':'right',
    }

from pylab import cm, get_cmap
maps=[m for m in cm.datad if not m.endswith("_r")]
cmaps = {}
for c in maps:
    cmaps[c] = get_cmap(c)

locations={
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


orientation_fig = {
    'portrait':'portrait',
    'landscape':'landscape'}


papertypes = {
    'letter':'letter',
    'legal':'legal',
    'executive':'executive',
    'ledger':'ledger',
    'a0':'a0',
    'a1':'a1',
    'a2':'a2',
    'a3':'a3',
    'a4':'a4',
    'a5':'a5',
    'a6':'a6',
    'a7':'a7',
    'a8':'a8',
    'a9':'a9',
    'a10':'a10',
    'b0':'b0',
    'b1':'b1',
    'b2':'b2',
    'b3':'b3',
    'b4':'b4',
    'b5':'b5',
    'b6':'b6',
    'b7':'b7',
    'b8':'b8',
    'b9':'b9',
    'b10':'b10'
    }


def get_kwds_from_line2d(line2d, kwds={}, type=None):
    """create a dict from line2d properties
    """
    kwds['color']=line2d.get_color()
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
    return kwds


def line2d2kwds(line2d, kwds={}):
    try:
        for key, value in line2d.properties().properties():
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






class PyLabPatch(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input(name='alpha', interface=IFloat(0,1,0.1), value=1.)
        self.add_input(name='axes', interface=IDict, value={})
        self.add_input(name='color', interface=IEnumStr(colors.keys()), value='None')
        self.add_input(name='edgecolor', interface=IEnumStr(colors.keys()), value='black')
        self.add_input(name='facecolor', interface=IEnumStr(colors.keys()), value='blue')
        self.add_input(name='figure', interface=IDict, value=None)
        self.add_input(name='fill', interface=IBool, value=True)
        self.add_input(name='label', interface=IStr, value=None)
        self.add_input(name='linestyle', interface=IEnumStr(linestyles.keys()), value='solid')
        self.add_input(name='linewidth', interface=IFloat, value=None)

        self.add_output(name='output')
    """animated    [True | False]
antialiased or aa   [True | False] or None for default
axes    an Axes instance
clip_box    a matplotlib.transforms.Bbox instance
clip_on     [True | False]
clip_path   [ (Path, Transform) | Patch | None ]
contains    a callable function
gid     an id string
hatch   [ '/' | '\' | '|' | '-' | '+' | 'x''| 'o' | 'O' | '.' | '*' ]
lod     True  False
picker  [None|float|boolean|callable]
rasterized  [True | False | None]
snap    unknown
transform   Transform instance
url     a url string
visible     [True | False]
zorder  any number
    """
    def __call__(self, inputs):
        kwds = {}
        for x in ['alpha', 'axes', 'figure', 'fill', 'label', 'linestyle', 'linewidth']:
            kwds[x]=self.get_input(x)
        if self.get_input('color')!='None':
            kwds['color'] = colors[self.get_input('color')] 
        kwds['edgecolor'] = colors[self.get_input('edgecolor')]
        kwds['facecolor'] = colors[self.get_input('facecolor')]
        return kwds



class PyLabCircle(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input(name='x', interface=IFloat, value=0)
        self.add_input(name='y', interface=IFloat, value=0)
        self.add_input(name='radius', interface=IFloat, value=5)
        self.add_input(name='patch', interface=IDict, value={})
        self.add_output(name='return',value=None)

    def __call__(self, inputs):
        from pylab import Circle

        c = Circle((self.get_input('x'), self.get_input('y')),
            self.get_input('radius'), **self.get_input('patch'))
        return c

class PyLabEllipse(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input(name='x', interface=IFloat, value=0)
        self.add_input(name='y', interface=IFloat, value=0)
        self.add_input(name='width', interface=IFloat, value=1)
        self.add_input(name='height', interface=IFloat, value=1)
        self.add_input(name='angle', interface=IFloat, value=0)
        self.add_input(name='patch', interface=IDict, value={})
        self.add_output(name='return',value=None)

    def __call__(self, inputs):
        from matplotlib.patches import Ellipse

        c = Ellipse((self.get_input('x'), self.get_input('y')),
            self.get_input('width'), self.get_input('height'), self.get_input('angle'), 
            **self.get_input('patch'))
        return c


class PyLabAddPatches(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input(name='axe', interface=IDict, value=None)
        self.add_input(name='patches', interface=ISequence,  value=[])
        self.add_output(name='return',value=None)

    def __call__(self, inputs):
        from pylab import Circle, draw

        axe = self.get_input('axe')
        if axe is not None:
            patches2add = []
            #if type(self.get_input('patches'))!=list:
            #    patches = list(self.get_input('patches'))
            #else:
            patches = self.get_input('patches')
            for patch in patches:
                axe.add_patch(patch)
            draw()
        #return axe



class PyLabRectangle(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input(name='x', interface=IFloat, value=0)
        self.add_input(name='y', interface=IFloat, value=0)
        self.add_input(name='width', interface=IFloat, value=1)
        self.add_input(name='height', interface=IFloat, value=1)
        self.add_input(name='patch', interface=IDict, value={})
        self.add_output(name='return',value=None)

    def __call__(self, inputs):
        from pylab import Rectangle

        c = Rectangle((self.get_input('x'), self.get_input('y')),
            self.get_input('width'), self.get_input('height'), 
            **self.get_input('patch'))
        return c

class PyLabWedge(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input(name='x', interface=IFloat, value=0)
        self.add_input(name='y', interface=IFloat, value=0)
        self.add_input(name='r', interface=IFloat, value=0)
        self.add_input(name='theta1', interface=IFloat, value=0)
        self.add_input(name='theta2', interface=IFloat, value=0)
        self.add_input(name='width', interface=IFloat(0.01,1,0.01), value=None)
        self.add_input(name='patch', interface=IDict, value={})
        self.add_output(name='return',value=None)

    def __call__(self, inputs):
        from matplotlib.patches import Wedge
        c = Wedge((self.get_input('x'), self.get_input('y')), 
                self.get_input('r'), self.get_input('theta1'), 
                self.get_input('theta2'), self.get_input('width'),
                **self.get_input('patch'))
        return c

class PyLabPolygon(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input(name='x', interface=ISequence, value=[])
        self.add_input(name='y', interface=ISequence, value=[])
        self.add_input(name='closed', interface=IBool, value=True)
        self.add_input(name='patch', interface=IDict, value={})
        self.add_output(name='return',value=None)

    def __call__(self, inputs):
        from pylab import Polygon
        from numpy import array
        #build up a (5,2) shape array from two x,y lists
        a = []
        for x,y in zip(self.get_input('x'), self.get_input('y')):
            a.append((x,y))
        c = Polygon(a, self.get_input('closed'), **self.get_input('patch'))
        return c

