###############################################################################
# -*- python -*-
#
#       pylab function implementation
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA
#
#       File author(s): Thomas Cokelaer <Thomas.Cokelaer@inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

__doc__="""axes decorators from pylab"""

__license__= "Cecill-C"
__revision__=" $Id$ "

#//////////////////////////////////////////////////////////////////////////////


from openalea.core import Node
from openalea.core import Factory, IFileStr, IInt, IBool, IFloat, \
    ISequence, IEnumStr, IStr, IDirStr, ITuple3, IDict

import pylab
from openalea.core.external import add_docstring
from openalea.pylab import tools
from openalea.pylab.tools import CustomizeAxes




class PyLabLegend(Node, CustomizeAxes):
    """VisuAlea version of pylab.legend

    :param *shadow*: draw a shadow behind legend. 
    :param *location*: legend location. See :class:`Locations` 
    :param *numpoints*: the number of points in the legend for line
    :param *markercolor*:
    :param *fancybox*: draw a frame with a round fancybox
    :param *ncol*: number of columns. default is 1
    :param *mode*: if mode is "expand", the legend will be horizontally expanded
    :param *title*: the legend title
    :param *prop*: connect an optional :class`PyLabFontProperties` object to customise further
    
    .. todo::   *scatterpoints*: integer, *scatteroffsets*: , markerscale*: expand
      *bbox_to_anchor* ,  *bbox_transform*
        borderpad, labelspacing, handlelength,andletextpad,  borderaxespad,  columnspacing

    :author: Thomas Cokelaer
    """
    def __init__(self):
        Node.__init__(self)
        CustomizeAxes.__init__(self)
        
        self.add_input(name='axes')
        self.add_input(name="shadow", interface=IBool, value=False)
        self.add_input(name="location", interface=IEnumStr(tools.locations.keys()), value=0)
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
        # pylab options
        kwds['loc'] = self.get_input('location')
        kwds['numpoints'] = self.get_input('numpoints')
        kwds['fancybox'] = self.get_input('fancybox')
        kwds['markerscale'] = self.get_input('markerscale')
        kwds['shadow'] = self.get_input('shadow')
        kwds['ncol'] = self.get_input('ncol')
        kwds['mode'] = self.get_input('mode')
        kwds['title'] = self.get_input('title')
        kwds['prop'] = self.get_input('prop')

        axes = self.get_axes()
        for axe in axes:
            axe.legend(**kwds)
            axe.get_figure().canvas.draw()
        return self.get_input('axes')

class PyLabFigure(Node):
    """pylab.figure interface

    Create figure

    :authors: Thomas Cokelaer
    """
    def __init__(self):
        Node.__init__(self)
        self.add_input(name="axes", interface=ISequence, value=[])
        self.add_input(name="num", interface=IInt, value=1)
        self.add_input(name="figsize", interface=ISequence, value=(8, 6))
        self.add_input(name="dpi", interface=IFloat, value=80.)
        self.add_input(name="facecolor", interface=IEnumStr(tools.colors.keys()), value='white')
        self.add_input(name="edgecolor", interface=IEnumStr(tools.colors.keys()), value='black')
        self.add_input(name="frameon", interface=IBool, value=True)
        self.add_input(name="subplotpars", interface=ISequence, value=None)
        self.add_input(name="kwds", interface=IDict, value={})

        self.add_output(name="kwds", interface=IDict, value={})

    def __call__(self, inputs):
        from pylab import figure
        from copy import deepcopy
        try:
            kwds = self.get_input('kwds')
        except:
            kwds = {}
        kwds['num'] = self.get_input('num')
        kwds['edgecolor']=self.get_input('edgecolor')
        kwds['frameon']=self.get_input('frameon')
        kwds['subplotpars']=self.get_input('subplotpars')

        c = self.get_input('axes')
        if type(c) != list:
            c = [c]
        if len(c) == 0:
            return None


        fignum = c[0].figure.number
        self.fig = figure(fignum)
        self.fig.set_facecolor(self.get_input('facecolor'))
        self.fig.set_edgecolor(self.get_input('edgecolor'))
        self.fig.set_frameon(self.get_input('frameon'))
        self.fig.set_dpi(self.get_input('dpi'))
        self.fig.canvas.draw()
        return self.fig


class PyLabAxis(Node, CustomizeAxes):

    def __init__(self):
        Node.__init__(self)
        CustomizeAxes.__init__(self)

        self.add_input(name="axes")

        self.add_input(name='type', interface=IEnumStr(tools.axis.keys()), value='normal')
        self.add_input(name='xmin', interface=IFloat(step=0.1), value=0.)
        self.add_input(name='xmax', interface=IFloat(step=0.1), value=1.)
        self.add_input(name='ymin', interface=IFloat(step=0.1), value=0.)
        self.add_input(name='ymax', interface=IFloat(step=0.1), value=1.)

        self.add_input(name='kwargs', interface=IDict, value={})

        self.add_output(name="axes")

    def __call__(self, inputs):

        kwds = {}
        type = self.get_input('type')
        kwds['xmin'] = self.get_input('xmin')
        kwds['xmax'] = self.get_input('xmax')
        kwds['ymin'] = self.get_input('ymin')
        kwds['ymax'] = self.get_input('ymax')

        axes = self.get_axes()
        for axe in axes:
            if type=='manual':
                axe.axis(**kwds)
            else:
                axe.axis(type, **kwds)
            axe.get_figure().canvas.draw()

        return self.get_input('axes')
 




class PyLabTextOptions(Node):

    def __init__(self):

        Node.__init__(self)
        #self.add_input(name="text", interface=IStr)
        #self.add_input(name="fontdict", interface=IDict, value=None)
        self.add_input(name="fontsize", interface=IFloat, value=12.)
        self.add_input(name="alpha", interface=IFloat(0., 1., step=0.1), value=0.5)
        self.add_input(name="color", interface=IEnumStr(tools.colors.keys()), value='blue')
        self.add_input(name='backgroundcolor', interface=IEnumStr(colors.keys()), value='white')
        self.add_input(name='rotation', interface=IFloat, value='horizontal')
        #self.add_input(name="withdash", interface=IBool, value=False)
        self.add_input(name="kwargs", interface=IDict, value={})
        self.add_input(name="fontproperties", interface=IDict, value={})

        self.add_output(name="kwargs", interface=IDict, value=None)


    def __call__(self, inputs):
        from pylab import text
        from matplotlib.font_manager import FontProperties as FP
        kwds = {}
        #kwds['text'] = self.get_input('text')
        kwds['fontsize'] = self.get_input('fontsize')
        kwds['alpha'] = self.get_input('alpha')
        kwds['color'] = self.get_input('color')
        kwds['backgroundcolor'] = self.get_input('backgroundcolor')
        kwds['rotation'] = self.get_input('rotation')
        kwds['fontproperties'] = FP(**self.get_input('fontproperties'))
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
      gid: an id string         
      horizontalalignment or ha: [ 'center' | 'right' | 'left' ]         
      label: any string         
      linespacing: float (multiple of font size)         
      lod: [True | False]         
      multialignment: ['left' | 'right' | 'center' ]         
      picker: [None|float|boolean|callable]         
      rasterized: [True | False | None]         
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


class PyLabXLabel(Node, CustomizeAxes):
    """VisuAlea version of pylab.xlabel

    :param text:
    :param fontsize:
    :param verticalalignement:
    :param horizontalalignment:
    :param text properties: output of a :class:`TextProperties` Node
    """
    def __init__(self):
        Node.__init__(self)
        CustomizeAxes.__init__(self)

        self.add_input(name="axes")

        self.add_input(name="text", interface=IStr, value=None)
        self.add_input(name="fontsize", interface=IFloat, value=12.)
        self.add_input(name="labelpad", interface=IInt, value=None)
        self.add_input(name="verticalalignment", interface=IEnumStr(tools.verticalalignment.keys()), value='top')
        self.add_input(name="horizontalalignment", interface=IEnumStr(tools.horizontalalignment.keys()), value='center')
        self.add_input(name="text properties", interface=IDict, value={})
        self.add_input(name='kwargs', interface=IDict, value={})

        self.add_output(name="axes")

    def __call__(self, inputs):
        kwds = {}
        kwds['fontsize'] = self.get_input('fontsize')
        kwds['labelpad'] = self.get_input('labelpad')
        kwds['verticalalignment'] = self.get_input('verticalalignment')
        kwds['horizontalalignment'] = self.get_input('horizontalalignment')
        for key, value in self.get_input('text properties').iteritems():
            kwds[key]=value

        for key, value in self.get_input('kwargs').iteritems():
            kwds[key] = value

        axes = self.get_axes()
        for axe in axes:
            axe.set_xlabel(self.get_input('text'), **kwds)
            axe.get_figure().canvas.draw()
        return axes

class PyLabYLabel(Node, CustomizeAxes):
    """VisuAlea version of axes.set_ylabel or ylabel

    :param text:
    :param fontsize:
    :param verticalalignement:
    :param horizontalalignment:
    :param text properties: output of a :class:`TextProperties` Node
    """
    def __init__(self):
        Node.__init__(self)
        CustomizeAxes.__init__(self)

        self.add_input(name="axes")

        self.add_input(name="text", interface=IStr, value=None)
        self.add_input(name="fontsize", interface=IFloat, value=12.)
        self.add_input(name="labelpad", interface=IInt, value=None)
        self.add_input(name="verticalalignment", interface=IEnumStr(tools.verticalalignment.keys()), value='top')
        self.add_input(name="horizontalalignment", interface=IEnumStr(tools.horizontalalignment.keys()), value='center')
        self.add_input(name="text properties", interface=IDict, value={})
        self.add_input(name='kwargs', interface=IDict, value={})

        self.add_output(name="axes")

    def __call__(self, inputs):
        kwds = {}
        kwds['fontsize'] = self.get_input('fontsize')
        kwds['labelpad'] = self.get_input('labelpad')
        kwds['verticalalignment'] = self.get_input('verticalalignment')
        kwds['horizontalalignment'] = self.get_input('horizontalalignment')
        for key, value in self.get_input('text properties').iteritems():
            kwds[key]=value

        for key, value in self.get_input('kwargs').iteritems():
            kwds[key] = value

        axes = self.get_axes()
        for axe in axes:
            axe.set_ylabel(self.get_input('text'), **kwds)
            axe.get_figure().canvas.draw()
        return axes


class PyLabTitle(Node, CustomizeAxes):

    def __init__(self):
        from matplotlib import font_manager
        Node.__init__(self)
        CustomizeAxes.__init__(self)

        self.add_input(name="axes")

        self.add_input(name="text", interface=IStr, value=None)
        self.add_input(name="fontsize", interface=IFloat, value=12)
        self.add_input(name="color", interface=IEnumStr(tools.colors.keys()), value='black')
        #self.add_input(name="fontproperties", interface=IDict, value=font_manager.FontProperties())
        self.add_input(name='kwargs', interface=IDict, value={})

        self.add_output(name='axes')

    def __call__(self, inputs):
        kwds = {}
        kwds['fontsize'] = self.get_input('fontsize')
        #kwargs['fontproperties'] = self.get_input('fontproperties')
        kwds['color'] = self.get_input('color')
        #if 'text' in kwargs.keys():
        #    self.set_input('text', kwargs['text'], notify=True)
        for key, value in self.get_input('kwargs').iteritems():
            kwds[key]=value

        text = self.get_input('text')

        axes = self.get_axes()
        for axe in axes:
            axe.set_title(text, **kwds)
            axe.get_figure().canvas.draw()

        return self.get_input('axes')






class PyLabFontProperties(Node):

    def __init__(self):
        Node.__init__(self)
        self.add_input(name='family', interface=IEnumStr(tools.families.keys()), value='serif')
        self.add_input(name='style', interface=IEnumStr(tools.styles.keys()), value='normal')
        self.add_input(name='variant', interface=IEnumStr(tools.variants.keys()), value='normal')
        self.add_input(name='weight', interface=IEnumStr(tools.weights.keys()), value='normal')
        self.add_input(name='stretch', interface=IEnumStr(tools.streches.keys()), value='normal')
        self.add_input(name='size', interface=IEnumStr(tools.sizes.keys()), value='medium')
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




class PyLabSaveFig(Node):
    """ should include hanning, ...."""
    def __init__(self):
        from matplotlib.pyplot import rcParams
        Node.__init__(self)

        self.add_input(name='axes')
        self.add_input(name='fname',        interface=IStr, value=None)
        self.add_input(name='transparent',  interface=IBool, value=False)
        self.add_input(name='dpi',          interface=IInt(40,200,1), value=rcParams['figure.dpi'])
        self.add_input(name='facecolor',    interface=IEnumStr(tools.colors.keys()), value='white')
        self.add_input(name='edgecolor',    interface=IEnumStr(tools.colors.keys()), value='w')
        self.add_input(name='orientation',  interface=IEnumStr(tools.orientation_fig.keys()), value='portrait')
        self.add_input(name='papertype',    interface=IEnumStr(tools.papertypes.keys()), value=None)
        self.add_input(name='format',       interface=IEnumStr(tools.extensions.keys()), value='png')
        self.add_input(name='kwargs',       interface=IDict, value={})

    def __call__(self, inputs):
        from pylab import savefig
        kwds = {}
        kwds['dpi'] = self.get_input('dpi')
        kwds['facecolor']=self.get_input('facecolor')
        kwds['edgecolor']= self.get_input('edgecolor')
        kwds['orientation']=self.get_input('orientation')
        kwds['papertype']=self.get_input('papertype')
        kwds['format']=extensions[self.get_input('format')]
        kwds['transparent']=self.get_input('transparent')
        savefig(self.get_input('fname'), **kwds)



class PyLabColorMap(Node):

    def __init__(self):
        Node.__init__(self)
        self.add_input(name='colormap', interface=IEnumStr(tools.cmaps.keys()), value='jet')
        self.add_input(name='show', interface=IBool, value=False)
        self.add_input(name='showall', interface=IBool, value=False)
        self.add_output(name='output')

    def __call__(self, inputs):
        from numpy import outer, arange, ones
        from pylab import figure, axis, imshow, title, show, subplot, text, clf, subplots_adjust
        maps = self.get_input('colormap')
        a=outer(arange(0,1,0.01),ones(10))

        if self.get_input('showall') is True:
            figure(figsize=(10,5))
            clf()
            l = len(tools.cmaps)
            subplots_adjust(top=0.9,bottom=0.05,left=0.01,right=0.99)
            for index, m in enumerate(tools.cmaps):
                print index
                subplot(int(l/2)+l%2+1, 2, index+1)
                print int(l/2)+l%2, 2, (index+1)/2+(index+1)%2+1
                axis("off")
                imshow(a.transpose(),aspect='auto',cmap=get_cmap(m),origin="lower")
                #title(m,rotation=0,fontsize=10)
                text(0.5,0.5, m)
            show()
        elif self.get_input('show') is True:
            figure(figsize=(10,5))
            clf()
            axis("off")
            imshow(a.transpose(),aspect='auto',cmap=get_cmap(maps),origin="lower")
            title(maps,rotation=0,fontsize=10)
            show()
        res = get_cmap(maps)
        return res


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
        self.add_input(name='orientation', interface=IEnumStr(tools.orientations.keys()), value='vertical')
        self.add_input(name='fraction', interface=IFloat(0.,1,0.01), value=0.15)
        self.add_input(name='pad', interface=IFloat(0.,1,0.01), value=0.05)
        self.add_input(name='shrink', interface=IFloat(0.,1,0.01), value=1)
        self.add_input(name='aspect', interface=IFloat(1,100,0.01), value=20)
        self.add_input(name='drawedges', interface=IBool, value=False)
        self.add_input(name='ticks', interface=ISequence, value=[])
        self.add_input(name='format', interface=IStr, value=None)
        self.add_input(name='label', interface=IStr, value=None)
        self.add_input(name='cmap', interface=IEnumStr, value=None)
        self.add_input(name='show', interface=IBool, value=False)
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

        if self.get_input('show'):
            c = colorbar(**kwds)

        if self.get_input('label') is not None:
            c.set_label(self.get_input('label'))

        return kwds




class PyLabXTicks(Node, CustomizeAxes):
    """VisuAlea version of pylab.xticks

    """
    def __init__(self):
        Node.__init__(self)
        CustomizeAxes.__init__(self)

        self.add_input(name='axes')

        self.add_input(name='locs', interface=ISequence, value=[])
        self.add_input(name='labels', interface=ISequence, value=[])
        self.add_input(name='rotation', interface=IFloat, value=0)
        self.add_input(name='kwargs(text properties)', interface=IDict, value={})

        self.add_output(name='axes')

    def __call__(self, inputs):
        kwds = {}
        for key, value in self.get_input('kwargs(text properties)').iteritems():
            kwds[key] = value
        kwds['rotation'] = self.get_input('rotation')

        axes = self.get_axes()

        for axe in axes:
            locs = self.get_input('locs')
            if len(locs) == 0:
                locs = axe.get_xticks()
            axe.set_xticks(locs)

            labels = self.get_input('labels')
            if len(labels) == 0:
                labels = axe.get_xticklabels()
            axe.set_xticklabels(labels,  **kwds)
            axe.get_figure().canvas.draw()
        return axes

class PyLabYTicks(Node, CustomizeAxes):
    """VisuAlea version of pylab.xticks

    """
    def __init__(self):
        Node.__init__(self)
        CustomizeAxes.__init__(self)

        self.add_input(name='axes')

        self.add_input(name='locs', interface=ISequence, value=None)
        self.add_input(name='labels', interface=ISequence, value=None)
        self.add_input(name='rotation', interface=IFloat, value=0)
        self.add_input(name='kwargs(text properties)', interface=IDict, value={})

        self.add_output(name='axes')

    def __call__(self, inputs):
        kwds = {}
        for key, value in self.get_input('kwargs(text properties)').iteritems():
            kwds[key] = value
        kwds['rotation'] = self.get_input('rotation')

        axes = self.get_axes()

        for axe in axes:
            locs = self.get_input('locs')
            if len(locs) == 0:
                locs = axe.get_yticks()
            axe.set_yticks(locs)

            labels = self.get_input('labels')
            if len(labels) == 0:
                labels = axe.get_yticklabels()
            axe.set_yticklabels(labels,  **kwds)
            axe.get_figure().canvas.draw()
        return axes

    
class PyLabXLim(Node, CustomizeAxes):
    """VisuAlea version of pylab.xlim

    :param axes:
    :param xmin:
    :param xmax:
    :param kwargs:
    
    :return: modified axes

    xmin must be less than xmax

    """
    def __init__(self):
        Node.__init__(self)
        CustomizeAxes.__init__(self)
        self.add_input(name='axes')
        self.add_input(name='xmin', interface=IFloat, value=None )
        self.add_input(name='xmax', interface=IFloat, value=None )
        self.add_input(name='kwargs', interface=IDict, value={})
        self.add_output(name='axes')

    def __call__(self, inputs):
        kwds = {}
        for key, value in self.get_input('kwargs').iteritems():
            kwds[key] = value
        axes = self.get_axes()
        xmin = self.get_input('xmin')
        xmax = self.get_input('xmax')
        assert xmin<xmax, 'xmin must be less than xmax'
        for axe in axes:
            axe.set_xlim(xmin=xmin, xmax=xmax, **kwds)
            axe.get_figure().canvas.draw()
        return axes



class PyLabYLim(Node, CustomizeAxes):
    """VisuAlea version of pylab.ylim

    :param axes:
    :param ymin:
    :param ymax:
    :param kwargs:
    
    :return: modified axes

    ymin must be less than ymax
    """
    def __init__(self):
        Node.__init__(self)
        CustomizeAxes.__init__(self)
        self.add_input(name='axes')
        self.add_input(name='ymin', interface=IFloat, value=None )
        self.add_input(name='ymax', interface=IFloat, value=None )
        self.add_input(name='kwargs', interface=IDict, value={})
        self.add_output(name='axes')

    def __call__(self, inputs):
        kwds = {}
        for key, value in self.get_input('kwargs').iteritems():
            kwds[key] = value
        axes = self.get_axes()
        ymin = self.get_input('ymin')
        ymax = self.get_input('ymax')
        assert ymin<ymax, 'ymin must be less than ymax'
        for axe in axes:
            axe.set_ylim(ymin=ymin, ymax=ymax, **kwds)
            axe.get_figure().canvas.draw()
        return self.get_input('axes')


class PyLabGrid(Node, CustomizeAxes):
    def __init__(self):
        Node.__init__(self)
        CustomizeAxes.__init__(self)

        self.add_input(name='axes')
        self.add_input(name='b', interface=IBool, value=True)
        self.add_input(name='which', interface=IEnumStr(tools.which.keys()), value='major')
        self.add_input(name='linestyle', interface=IEnumStr(tools.linestyles.keys()),   value='dotted')
        self.add_input(name='color', interface=IEnumStr(tools.colors.keys()),   value='black')
        self.add_input(name='linewidth', interface=IFloat, value=1.0)
        self.add_input(name='kwargs', interface=IDict, value={})

        self.add_output(name='axes')

    def __call__(self, inputs):
        kwds = {}
        for key, value in self.get_input('kwargs').iteritems():
            kwds[key] = value
        kwds['linestyle']=linestyles[self.get_input("linestyle")]
        kwds['color']=colors[self.get_input("color")]
        kwds['linewidth']=self.get_input("linewidth")
        kwds['b']=self.get_input("b")
        kwds['which']=self.get_input("which")

        axes = self.get_axes()
        for axe in axes:
            axe.grid(**kwds)
            axe.get_figure().canvas.draw()
        return self.get_input('axes')


class PyLabOrigin(Node):

    def __init__(self):
        Node.__init__(self)
        self.add_input(name='origin', interface=IEnumStr(origins), value=None)
        self.add_output(name='output', interface=IDict, value={})

    def __call__(self, inputs):
        kwds = {}
        kwds['origin'] = self.get_input('origin') 
        return (kwds ,)


class PyLabAxes(Node):
    def __init__(self):
        Node.__init__(self)
        #[left, bottom, width,      height]
        self.add_input(name='input')
        self.add_input(name='clear', interface=IBool, value=True)
        self.add_input(name='left',     interface=IFloat(0, 1, 0.01), value=0.12)
        self.add_input(name='bottom',   interface=IFloat(0, 1, 0.01), value=0.12)
        self.add_input(name='width',    interface=IFloat(0, 1, 0.01), value=0.78)
        self.add_input(name='height',   interface=IFloat(0, 1, 0.01), value=0.78)
        self.add_input(name='axisbg',   interface=IEnumStr(tools.colors.keys()), value='white')
        self.add_input(name='frameon',  interface=IBool, value=True)
        self.add_input(name='polar',    interface=IBool, value=False)
        self.add_input(name='xscale',    interface=IEnumStr(tools.scale.keys()), value='linear')
        self.add_input(name='yscale',    interface=IEnumStr(tools.scale.keys()), value='linear')
        self.add_input(name='xticks',    interface=IEnumStr(tools.ticks.keys()), value='auto')
        self.add_input(name='yticks',    interface=IEnumStr(tools.ticks.keys()), value='auto')
        self.add_input(name='kwargs',    interface=IDict, value={})
        self.add_output(name='axes', interface=IDict, value={})

        self.axe = None

    def __call__(self, inputs):
        from pylab import axes, gcf
        kwds = {}
        position = [self.get_input('left'),  self.get_input('bottom'),
                            self.get_input('width'), self.get_input('height')]
        if self.get_input('xticks')=='None':
            kwds['xticks'] = []
        if self.get_input('yticks')=='None':
            kwds['yticks'] = []

        input_axes = self.get_input('input')

        # case of an empty input, we need to create the axes if it does not exist, or clean the existing one.
        if input_axes == None:
            print 'Axes2: input axes is none'
            #this command return the current axe if it exist otherwise it creates a new one
            input_axes = axes(position, polar=self.get_input('polar'))
            if self.get_input('clear')==True:
                input_axes.clear()
            input_axes.set_axis_bgcolor(self.get_input('axisbg'))
            input_axes.set_frame_on(self.get_input('frameon'))
            input_axes.set_xscale(self.get_input('xscale'))
            input_axes.set_yscale(self.get_input('yscale'))
            f = input_axes.get_figure()
            f.canvas.draw()
            return input_axes

        #else
        print 'Axes2: input axes is not none'
        if type(input_axes)!=list: input_axes = [input_axes]

        for axe in input_axes:
            axe.set_position(position)
            axe.set_axis_bgcolor(self.get_input('axisbg'))
            axe.set_frame_on(self.get_input('frameon'))
            axe.set_xscale(self.get_input('xscale'))
            axe.set_yscale(self.get_input('yscale'))
        f = gcf()
        f.canvas.draw()

        return input_axes


class PyLabClearFigure(Node, CustomizeAxes):

    def __init__(self):
        Node.__init__(self)
        CustomizeAxes.__init__(self)

        self.add_input(name="axes")

        self.add_output(name='axes')

    def __call__(self, inputs):

        axes = self.get_axes()
        for axe in axes:
            try:
                f = axe.get_figure()
                f.clf()
            except:
                import warnings
                warnings('a figure could not be selected or deleted.')
            axe.get_figure().canvas.draw()

        return self.get_input('axes')


class PyLabAxesDecorator(Node):
    
    def __init__(self):
        Node.__init__(self)
        self.add_input(name="axes")
        self.add_input(name="whatever", interface=ISequence, value=[])
        self.add_output(name="axes")
        
    def __call__(self, inputs):
        whatever = self.get_input('whatever')
        if type(whatever)!=list:
            whatever = [whatever]
        import matplotlib
        from pylab import gca
        for this in whatever:
            try:
                gca().add_patch(this)
                gca().get_figure().canvas.draw()
            except:
                print 'this object is not accepted bu AxesDecorator!. Skipped'
                print this
        return self.get_input("axes")
        