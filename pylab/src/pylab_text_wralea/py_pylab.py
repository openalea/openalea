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


cmaps=['autumn','bone', 'cool','copper','flag','gray','hot','hsv','jet','pink', 'prism', 'spring', 'summer', 'winter'] 

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




class PyLabRandom(Node):
    """pylab.random interface

    Returns uniform random distribution array between a
    minimum (0.)  and maximum value (1)

    :param length: length of the random array
    :param min: min value (default is 0.)
    :param max: max value  (default is 1)

    :authors: Thomas Cokelaer
    """
    def __init__(self):
        #from pylab import random
        #self.__doc__ += random.__doc__
        Node.__init__(self)
        self.add_input(name="length", interface = IInt, value=100)
        self.add_input(name="min", interface = IFloat, value=0.)
        self.add_input(name="max", interface = IFloat, value=1.)
        self.add_output(name="result")

    def __call__(self, inputs):
        from pylab import random
        m = self.get_input("min")
        M = self.get_input("max")
        n = self.get_input("length")

        if m and M:
            res = m + (M-m)* random(n)
        else:
            res = random(n)

        return(res,)


class PyLabAbsolute(Node):
    """pylab.absolute interface

    Returns absolute values of the input data

    :authors: Thomas Cokelaer
    """
    def __init__(self):
        #from pylab import absolute
        #self.__doc__+=absolute.__doc__
        Node.__init__(self)
        self.add_input(name="data")
        self.add_output(name="result")

    def __call__(self, inputs):
        from pylab import absolute
        data = self.get_input("data")
        return (absolute(data),)



class PyLabLegend(Node):
    """to be done"""

    def __init__(self):
        Node.__init__(self)
        self.add_input(name="legend on", interface=IBool, value=True)
        self.add_input(name="shadow", interface=IBool, value=False)
        self.add_input(name="location", interface=IEnumStr(locations.keys()), value=0)
        self.add_input(name="numpoints", interface=IInt, value=2)
        self.add_input(name="markerscale", interface=IFloat(0.1,10,0.1), value=1)
        self.add_input(name="fancybox", interface=IBool, value=True)
        self.add_input(name="ncol", interface=IInt(1,10), value=1)
        self.add_input(name="mode", interface=IEnumStr({'None':'None','Expanded':'exapanded'}), value=None)
        self.add_input(name="title", interface=IStr, value=None)
        #rodo scatterpoints
        #borderpad          the fractional whitespace inside the legend border
        #    labelspacing       the vertical space between the legend entries
        #    handlelength       the length of the legend handles
        #    handletextpad      the pad between the legend handle and text
        #    borderaxespad      the pad between the axes and legend border
        #    columnspacing      the spacing between columns
        #borderaxespad
        self.add_input(name="prop", interface=IDict, value={})
        #p = pylab.matplotlib.font_manager.FontProperties(size=26)

        self.add_output(name="kwds", interface=IDict, value={})

    def __call__(self, inputs):
        from pylab import legend
        kwds = {}
        # !!!this one is not pylab option
        kwds['legend on'] = self.get_input('legend on')
        # pylab options
        kwds['loc'] = self.get_input('location')
        kwds['numpoints'] = self.get_input('numpoints')
        kwds['loc'] = self.get_input('location')
        kwds['fancybox'] = self.get_input('fancybox')
        kwds['markerscale'] = self.get_input('markerscale')
        kwds['shadow'] = self.get_input('shadow')
        kwds['ncol'] = self.get_input('ncol')
        kwds['mode'] = self.get_input('mode')
        kwds['title'] = self.get_input('title')
        kwds['prop'] = self.get_input('prop')

        return kwds

class PyLabFigure(Node):
    """pylab.figure interface

    Create figure

    :authors: Thomas Cokelaer
    """
    def __init__(self):
        Node.__init__(self)
        self.add_input(name="num", interface=IInt, value=1)
        self.add_input(name="figsize", interface=ITuple3, value=(8, 6))
        self.add_input(name="dpi", interface=IFloat, value=80.)
        self.add_input(name="facecolor", interface=IEnumStr(colors.keys()), value='white')
        self.add_input(name="edgecolor", interface=IEnumStr(colors.keys()), value='black')

        self.add_output(name="kwds", interface=IDict, value={})

    def __call__(self, inputs):
        from pylab import figure
        kwds={}
        kwds['num']=self.get_input('num')
        kwds['figsize']=self.get_input('figsize')
        kwds['facecolor']=self.get_input('facecolor')
        kwds['edgecolor']=self.get_input('edgecolor')
        kwds['dpi']=self.get_input('dpi')
        #fig = figure(**kwds)
        return kwds


class PyLabLine2D(Node):

    def __init__(self):
        Node.__init__(self)

        self.add_input(name="xdata")
        self.add_input(name="ydata", value=None)
        self.add_input(name="linestyle", interface=IEnumStr(linestyles.keys()), value='solid')
        self.add_input(name="color", interface=IEnumStr(colors.keys()),value='blue')
        self.add_input(name="marker", interface=IEnumStr(markers.keys()),value='circle')
        self.add_input(name="markersize", interface=IInt, value=10)
        self.add_input(name="markeredgewidth", interface=IFloat(0.,10,0.1) , value=None)
        self.add_input(name="markeredgecolor", interface=IEnumStr(colors.keys()), value='None')
        self.add_input(name="linewidth", interface=IFloat, value=1.)
        self.add_input(name="fillstyle", interface=IEnumStr(fillstyles.keys()), value='full')
        self.add_input(name="label", interface=IStr, value=None)
        self.add_input(name="alpha", interface=IFloat(0.,1., step=0.1), value=1.0)

        self.add_output(name="line2d")

    def __call__(self, inputs):
        from pylab import Line2D
        xdata=self.get_input('xdata')
        ydata=self.get_input('ydata')
        #why?
        if ydata is None:
            print 'a'
            ydata = xdata
            xdata = range(0, len(ydata))
        output = Line2D(
            xdata=xdata,
            ydata=ydata,
            linestyle=linestyles[self.get_input('linestyle')],
            color=colors[self.get_input('color')],
            marker=markers[self.get_input('marker')],
            label=self.get_input('label'),
            markersize=self.get_input('markersize'),
            markeredgecolor=colors[self.get_input('markeredgecolor')],
            markeredgewidth=self.get_input('markeredgewidth'),
            linewidth=self.get_input('linewidth'),
            fillstyle=self.get_input('fillstyle'),
            alpha=self.get_input('alpha'),
        )
        return (output, )

"""
antialiased=None, 
dash_capstyle=None,
solid_capstyle=None, 
dash_joinstyle=None,
solid_joinstyle=None,
pickradius=5,
drawstyle=None,
 markevery=None,
**kwargs)

      animated: [True | False]         
      antialiased or aa: [True | False]         
      axes: an :class:`~matplotlib.axes.Axes` instance         
      clip_box: a :class:`matplotlib.transforms.Bbox` instance         
      clip_on: [True | False]         
      clip_path: [ (:class:`~matplotlib.path.Path`,         :class:`~matplotlib.transforms.Transform`) |         :class:`~matplotlib.patches.Patch` | None ]         
      contains: a callable function         
      dash_capstyle: ['butt' | 'round' | 'projecting']         
      dash_joinstyle: ['miter' | 'round' | 'bevel']         
      dashes: sequence of on/off ink in points         
      data: 2D array         
      drawstyle: [ 'default' | 'steps' | 'steps-pre' | 'steps-mid' | 'steps-post' ]         
      figure: a :class:`matplotlib.figure.Figure` instance         
      gid: an id string         
      lod: [True | False]         
      markerfacecolor or mfc: any matplotlib color         
      markevery: None | integer | (startind, stride)
      picker: float distance in points or callable pick function         ``fn(artist, event)``         
      pickradius: float distance in points 
      rasterized: [True | False | None]         
      snap: unknown
      solid_capstyle: ['butt' | 'round' |  'projecting']         
      solid_joinstyle: ['miter' | 'round' | 'bevel']         
      transform: a :class:`matplotlib.transforms.Transform` instance         
      url: a url string         
      visible: [True | False]         
      zorder: any number         

"""

class PyLabAxes(Node):
    def __init__(self):
        Node.__init__(self)
        self.add_input(name='axisbg', interface=IEnumStr(colors.keys()), value='white')
        self.add_input(name='frameon', interface=IBool, value=True)
        self.add_input(name='polar', interface=IBool, value=False)
        #sharex    otherax        current axes shares xaxis attribute with otherax
        #sharey    otherax        current axes shares yaxis attribute with otherax
        #self.add_output(name='axes')
        self.add_output(name='kwds', interface=IDict, value={})

    def __call__(self, inputs):
        from pylab import axes
        kwds = {}
        kwds['axisbg'] = self.get_input('axisbg')
        kwds['frameon'] = self.get_input('frameon')
        kwds['polar'] = self.get_input('polar')
        #aa = axes(**kwds)
        return kwds

class PyLabAxis(Node):

    def __init__(self):
        Node.__init__(self)
        self.add_input(name='type', interface=IEnumStr(axis.keys()), value='normal')
        self.add_input(name='xmin', interface=IFloat(step=0.1), value=0.)
        self.add_input(name='xmax', interface=IFloat(step=0.1), value=1.)
        self.add_input(name='ymin', interface=IFloat(step=0.1), value=0.)
        self.add_input(name='ymax', interface=IFloat(step=0.1), value=1.)
        self.add_output(name='kwds', interface=IDict, value={})

    def __call__(self, inputs):
        from pylab import axis
        kwds = {}
        kwds['type'] = self.get_input('type')
        kwds['xmin'] = self.get_input('xmin')
        kwds['xmax'] = self.get_input('xmax')
        kwds['ymin'] = self.get_input('ymin')
        kwds['ymax'] = self.get_input('ymax')
        #aa = axes(**kwds)
        return kwds




class PyLabTextOptions(Node):

    def __init__(self):

        Node.__init__(self)
        #self.add_input(name="text", interface=IStr)
        #self.add_input(name="fontdict", interface=IDict, value=None)



class PyLabTextOptions(Node):

    def __init__(self):

        Node.__init__(self)
        #self.add_input(name="text", interface=IStr)
        #self.add_input(name="fontdict", interface=IDict, value=None)
        self.add_input(name="fontsize", interface=IFloat, value=12.)
        self.add_input(name="alpha", interface=IFloat(0., 1., step=0.1), value=0.5)
        self.add_input(name="color", interface=IEnumStr(colors.keys()), value='blue')
        self.add_input(name='backgroundcolor', interface=IEnumStr(colors.keys()), value='white')
        #self.add_input(name="withdash", interface=IBool, value=False)
        self.add_input(name="kwargs", interface=IDict, value={})

        self.add_output(name="kwargs", interface=IDict, value=None)


    def __call__(self, inputs):
        from pylab import text
        kwds = {}
        #kwds['text'] = self.get_input('text')
        kwds['fontsize'] = self.get_input('fontsize')
        kwds['alpha'] = self.get_input('alpha')
        kwds['color'] = self.get_input('color')
        kwds['backgroundcolor'] = self.get_input('backgroundcolor')
        for key, value in self.get_input('kwargs').iteritems():
            try:
                kwds[key] = value
            except:
                print 'key already defined. skip it'
                pass

        #res = text(0,0, self.get_input('text'), **kwds)

        return ( kwds,)

""" 
      animated: [True | False]         
      axes: an :class:`~matplotlib.axes.Axes` instance         
      backgroundcolor: any matplotlib color         
      bbox: rectangle prop dict         
      clip_box: a :class:`matplotlib.transforms.Bbox` instance         
      clip_on: [True | False]    i
 clip_on: [True | False]         
      clip_box: a :class:`matplotlib.transforms.Bbox` instance         
      clip_on: [True | False]         
      clip_path: [ (:class:`~matplotlib.path.Path`,         :class:`~matplotlib.transforms.Transform`) |         :class:`~matplotlib.patches.Patch` | None ]         
      color: any matplotlib color         
      contains: a callable function         
      family or fontfamily or fontname or name: [ FONTNAME | 'serif' | 'sans-serif' | 'cursive' | 'fantasy' | 'monospace' ]         
      figure: a :class:`matplotlib.figure.Figure` instance         
      fontproperties or font_properties: a :class:`matplotlib.font_manager.FontProperties` instance         
      gid: an id string         
      horizontalalignment or ha: [ 'center' | 'right' | 'left' ]         
      label: any string         
      linespacing: float (multiple of font size)         
      lod: [True | False]         
      multialignment: ['left' | 'right' | 'center' ]         
      picker: [None|float|boolean|callable]         
      rasterized: [True | False | None]         
      rotation: [ angle in degrees | 'vertical' | 'horizontal' ]         
      rotation_mode: unknown
      size or fontsize: [ size in points | 'xx-small' | 'x-small' | 'small' | 'medium' | 'large' | 'x-large' | 'xx-large' ]         
      snap: unknown
      stretch or fontstretch: [ a numeric value in range 0-1000 | 'ultra-condensed' | 'extra-condensed' | 'condensed' | 'semi-condensed' | 'normal' | 'semi-expanded' | 'expanded' | 'extra-expanded' | 'ultra-expanded' ]         
      style or fontstyle: [ 'normal' | 'italic' | 'oblique']         
      text: string or anything printable with '%s' conversion.         
      transform: :class:`~matplotlib.transforms.Transform` instance         
      url: a url string         
      variant or fontvariant: [ 'normal' | 'small-caps' ]         
      verticalalignment or va or ma: [ 'center' | 'top' | 'bottom' | 'baseline' ]         
      visible: [True | False]         
      weight or fontweight: [ a numeric value in range 0-1000 | 'ultralight' | 'light' | 'normal' | 'regular' | 'book' | 'medium' | 'roman' | 'semibold' | 'demibold' | 'demi' | 'bold' | 'heavy' | 'extra bold' | 'black' ]         
      zorder: any number         
"""


class PyLabPolar(Node):

    def __init__(self):
        Node.__init__(self)
        self.add_input(name="r")
        self.add_input(name="theta")
        self.add_input(name="kwargs", interface = IDict, value = {})
        self.add_output(name="figure")

    def __call__(self, inputs):
        from pylab import polar, show
        kwargs = self.get_input('kwargs')
        fig = polar(self.get_input('r'), self.get_input('theta'), **kwargs)
        show()
        return (fig,)


class PyLabXLabel(Node):

    def __init__(self):
        Node.__init__(self)
        self.add_input(name="text", interface=IStr, value=None)
        self.add_input(name="fontsize", interface=IFloat, value=12.)
        self.add_input(name="verticalalignment", interface=IEnumStr(verticalalignment.keys()), value='top')
        self.add_input(name="horizontalalignment", interface=IEnumStr(horizontalalignment.keys()), value='center')
        self.add_input(name="kwargs", interface=IDict, value={})

        self.add_output(name='kwargs', interface=IDict, value={})

    def __call__(self, inputs):
        from pylab import xlabel, hold

        kwargs = {}
        kwargs['fontsize'] = self.get_input('fontsize')
        kwargs['verticalalignment'] = self.get_input('verticalalignment')
        kwargs['horizontalalignment'] = self.get_input('horizontalalignment')
        for key, value in self.get_input('kwargs').iteritems():
            kwargs[key]=value

        #xlabel(self.get_input('text'), **kwargs)
        kwargs['text'] = self.get_input('text')

        return kwargs

class PyLabYLabel(Node):

    def __init__(self):
        Node.__init__(self)
        self.add_input(name="text", interface=IStr, value=None)
        self.add_input(name="fontsize", interface=IFloat, value=12.)
        self.add_input(name="verticalalignment", interface=IEnumStr(verticalalignment.keys()), value='top')
        self.add_input(name="horizontalalignment", interface=IEnumStr(horizontalalignment.keys()), value='center')
        self.add_input(name="kwargs", interface=IDict, value={})

        self.add_output(name='kwargs', interface=IDict, value={})

    def __call__(self, inputs):
        from pylab import ylabel, hold

        kwargs = {}
        kwargs['fontsize'] = self.get_input('fontsize')
        kwargs['verticalalignment'] = self.get_input('verticalalignment')
        kwargs['horizontalalignment'] = self.get_input('horizontalalignment')
        for key, value in self.get_input('kwargs').iteritems():
            kwargs[key]=value

        #ylabel(self.get_input('text'), **kwargs)
        kwargs['text'] = self.get_input('text')
        return kwargs


class PyLabTitle(Node):

    def __init__(self):
        from matplotlib import font_manager
        Node.__init__(self)
        self.add_input(name="text", interface=IStr, value=None)
        self.add_input(name="fontsize", interface=IFloat, value=12)
        self.add_input(name="color", interface=IEnumStr(colors.keys()), value='black')
        #self.add_input(name="fontproperties", interface=IDict, value=font_manager.FontProperties())
        self.add_input(name='kwargs', interface=IDict, value={})

        self.add_output(name='output', interface=IDict, value={})

    def __call__(self, inputs):
        from pylab import title

        kwargs = {}
        kwargs['fontsize'] = self.get_input('fontsize')
        #kwargs['fontproperties'] = self.get_input('fontproperties')
        kwargs['color'] = self.get_input('color')
        if 'text' in kwargs.keys():
            self.set_input('text', kwargs['text'], notify=True)
        for key, value in self.get_input('kwargs').iteritems():
            kwargs[key]=value

        #print self.get_input('text')
        #print kwargs
        #title(self.get_input('text'), **kwargs)
        kwargs['text'] = self.get_input('text')
        return kwargs






class PyLabRectangle(Node):
    def __init__(self):
        Node.__init__(self)

        self.add_input(name='alpha', interface=IFloat(0.,1.), value=1.0)
        self.add_input(name='facecolor', interface=IEnumStr(colors.keys()), value='blue')
        self.add_input(name='edgecolor', interface=IEnumStr(colors.keys()), value='black')
        self.add_input(name='linestyle', interface=IEnumStr(linestyles.keys()), value='solid')

        self.add_input(name='kwargs', interface=IDict, value={})

        self.add_output(name='output', interface=IDict, value={})

    def __call__(self, inputs):
        kwds = {}
        kwds['alpha'] = self.get_input('alpha')
        kwds['facecolor'] = self.get_input('facecolor')
        kwds['edgecolor'] = self.get_input('edgecolor')
        kwds['linestyle'] = self.get_input('linestyle')
        for key,value in self.get_input('kwargs'):
            kwds[key]=value
        return (kwds)

    """

      animated: [True | False]         
      antialiased or aa: [True | False]  or None for default         
      axes: an :class:`~matplotlib.axes.Axes` instance         
      clip_box: a :class:`matplotlib.transforms.Bbox` instance         
      clip_on: [True | False]         
      clip_path: [ (:class:`~matplotlib.path.Path`,         :class:`~matplotlib.transforms.Transform`) |         :class:`~matplotlib.patches.Patch` | None ]         
      color: matplotlib color arg or sequence of rgba tuples
      contains: a callable function         
      figure: a :class:`matplotlib.figure.Figure` instance         
      fill: [True | False]         
      gid: an id string         
      hatch: [ '/' | '\\' | '|' | '-' | '+' | 'x' | 'o' | 'O' | '.' | '*' ]         
      label: any string         
      linewidth or lw: float or None for default         
      lod: [True | False]         
      picker: [None|float|boolean|callable]         
      rasterized: [True | False | None]         
      snap: unknown
      transform: :class:`~matplotlib.transforms.Transform` instance         
      url: a url string         
      visible: [True | False]         
      zorder: any number        
    """



class PyLabFontProperties(Node):

    def __init__(self):
        Node.__init__(self)
        self.add_input(name='family', interface=IEnumStr(families.keys()), value='serif')
        self.add_input(name='style', interface=IEnumStr(styles.keys()), value='normal')
        self.add_input(name='variant', interface=IEnumStr(variants.keys()), value='normal')
        self.add_input(name='weight', interface=IEnumStr(weights.keys()), value='normal')
        self.add_input(name='stretch', interface=IEnumStr(streches.keys()), value='normal')
        self.add_input(name='size', interface=IEnumStr(sizes.keys()), value='medium')
        #todo size could be number, similarly for stretch and weight
        #self.add_input(name='fname', fname=None)
        #self.add_input(name='_init', _init=None)
        #todo style, variant and strethc do not seem to work
        self.add_output(name='kwds', interface=IDict, value={})

    def __call__(self,inputs):
        kwds = {}
        kwds['family'] = self.get_input('family')
        kwds['style'] = self.get_input('style')
        kwds['size'] = self.get_input('size')
        kwds['variant'] = self.get_input('variant')
        kwds['weight'] = self.get_input('weight')
        kwds['stretch'] = self.get_input('stretch')

        return kwds




class Windowing(Node):
    """ should include hanning, ...."""
    def __init__(self):
        pass

    def __call__(self, inputs):
        pass

class PyLabColorBar(Node):

    """ should include colornap and colorbar options"""
    def __init__(self):

        Node.__init__(self)
        orientations = {'vertical':'vertical','orientation':'orientation'}
        self.add_input(name='orientation', interface=IEnumStr(orientations.keys()), value='vertical')
        self.add_input(name='fraction', interface=IFloat(0.,1,0.01), value=0.15)
        self.add_input(name='pad', interface=IFloat(0.,1,0.01), value=0.05)
        self.add_input(name='shrink', interface=IFloat(0.,1,0.01), value=1)
        self.add_input(name='aspect', interface=IFloat(1,100,0.01), value=20)
        self.add_input(name='drawedges', interface=IBool, value=False)
        self.add_input(name='ticks', interface=ISequence, value=[])
        self.add_input(name='format', interface=IStr, value=None)
        self.add_output(name='kwargs', interface=IDict, value={})

    def __call__(self, inputs):
        from pylab import colorbar
        kwds = {}
        kwds['fraction'] = self.get_input('fraction')
        kwds['orientation'] = self.get_input('orientation') #no need for dictionary conversion since key==value
        kwds['pad'] = self.get_input('pad')
        kwds['shrink'] = self.get_input('shrink')
        kwds['aspect'] = self.get_input('aspect')
        kwds['drawedges'] = self.get_input('drawedges')
        if len(self.get_input('ticks'))>0:
            kwds['ticks'] = self.get_input('ticks')
        kwds['format'] = self.get_input('format')
        c = colorbar(**kwds)


        return kwds
