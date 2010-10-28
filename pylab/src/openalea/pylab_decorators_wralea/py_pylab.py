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
    """Add a legend to the axe. see pylab.legend for details

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

    :Example:

    .. dataflow:: openalea.pylab.test legend
        :width: 40%

        **The openalea.pylab.demo.figure dataflow.**

    .. plot::
        :width: 40%

        from openalea.core.alea import *
        pm = PackageManager()
        run_and_display(('openalea.pylab.test', 'legend'),{},pm=pm )

    .. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
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
    """see pylab.figure for details.

    :param axes:
    :param num:
    :param figsize:
    :param dpi:
    :param facecolor:
    :param edgecolor:
    :param frameon:
    :param subplotpars:

    :Example:

    .. dataflow:: openalea.pylab.test figure
        :width: 40%

        **The openalea.pylab.demo.figure dataflow.**

    .. plot::
        :width: 40%

        from openalea.core.alea import *
        pm = PackageManager()
        run_and_display(('openalea.pylab.test', 'figure'),{},pm=pm )


    .. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
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
        #SPHINX
        #self.fig.canvas.draw()
        return self.fig


class PyLabAxis(Node, CustomizeAxes):
    """axis tuning. See pylab.axis for details

    .. warning:: not for production


    .. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>"""

    def __init__(self):

        Node.__init__(self)
        #self.add_input(name="text", interface=IStr)
        #self.add_input(name="fontdict", interface=IDict, value=None)
        self.add_input(name="fontsize", interface=IFloat, value=12.)
        self.add_input(name="alpha", interface=IFloat(0., 1., step=0.1), value=0.5)
        self.add_input(name="color", interface=IEnumStr(tools.colors.keys()), value='blue')
        self.add_input(name='backgroundcolor', interface=IEnumStr(tools.colors.keys()), value='white')
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


class PyLabXLabel(Node, CustomizeAxes):
    """Add a label on the x-axis. See pylab.xlabel for details

    :param axes: an optional axes where new data will be plotted.
    :param str text:
    :param int fontsize: font size (default 12)
    :param str verticalalignement: (default is top)
    :param str horizontalalignment: (default is center)
    :param dict textproperties: output of a :class:`PyLabFontProperties` Node
    :param dict kwargs: any other key/value pair
    :return: the current axes

    :Example:

    .. dataflow:: openalea.pylab.test xylabels
        :width: 40%

        **The openalea.pylab.test.title dataflow.** Add a title to an existing
        axes.

    .. plot::
        :width: 40%

        from openalea.core.alea import *
        pm = PackageManager()
        run_and_display(('openalea.pylab.test', 'xylabels'),{},pm=pm)

    .. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    """
    def __init__(self):
        Node.__init__(self)
        CustomizeAxes.__init__(self)

        self.add_input(name="axes")

        self.add_input(name="text", interface=IStr, value=None)
        self.add_input(name="fontsize", interface=IFloat, value=12.)
        self.add_input(name="labelpad", interface=IInt, value=None)
        self.add_input(name="verticalalignment", interface=IEnumStr(tools.verticalalignment.keys()),
            value='top')
        self.add_input(name="horizontalalignment", interface=IEnumStr(tools.horizontalalignment.keys()),
            value='center')
        self.add_input(name="text properties", interface=IDict, value={})
        self.add_input(name='kwargs', interface=IDict, value={})

        self.add_output(name="axes")

    def __call__(self, inputs):
        kwds = {}
        for key, value in self.get_input('text properties').iteritems():
            kwds[key]=value

        for key, value in self.get_input('kwargs').iteritems():
            kwds[key] = value

        #input text and fontproperties are overwritten
        kwds['fontsize'] = self.get_input('fontsize')
        kwds['labelpad'] = self.get_input('labelpad')
        kwds['verticalalignment'] = self.get_input('verticalalignment')
        kwds['horizontalalignment'] = self.get_input('horizontalalignment')

        axes = self.get_axes()
        for axe in axes:
            axe.set_xlabel(self.get_input('text'), **kwds)
            axe.get_figure().canvas.draw()
        return axes


class PyLabYLabel(Node, CustomizeAxes):
    """Add a label on the x-axis. See pylab.xlabel for details

    :param text:
    :param fontsize:
    :param verticalalignement:
    :param horizontalalignment:
    :param text properties: output of a :class:`TextProperties` Node

    :Example: See :class:`~openalea.pylab_decorators_wralea.py_pylab.PyLabXLabel`

    .. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    """
    def __init__(self):
        Node.__init__(self)
        CustomizeAxes.__init__(self)

        self.add_input(name="axes")

        self.add_input(name="text", interface=IStr, value=None)
        self.add_input(name="fontsize", interface=IFloat, value=12.)
        self.add_input(name="labelpad", interface=IInt, value=None)
        self.add_input(name="verticalalignment", interface=IEnumStr(tools.verticalalignment.keys()), 
            value='center')
        self.add_input(name="horizontalalignment", interface=IEnumStr(tools.horizontalalignment.keys()), 
            value='right')
        self.add_input(name="text properties", interface=IDict, value={})
        self.add_input(name='kwargs', interface=IDict, value={'rotation':'vertical'})

        self.add_output(name="axes")

    def __call__(self, inputs):
        kwds = {}

        for key, value in self.get_input('text properties').iteritems():
            print key, value
            kwds[key]=value

        for key, value in self.get_input('kwargs').iteritems():
            kwds[key] = value

        kwds['fontsize'] = self.get_input('fontsize')
        kwds['labelpad'] = self.get_input('labelpad')
        kwds['verticalalignment'] = self.get_input('verticalalignment')
        kwds['horizontalalignment'] = self.get_input('horizontalalignment')

        axes = self.get_axes()
        for axe in axes:
            axe.set_ylabel(self.get_input('text'), **kwds)
            axe.get_figure().canvas.draw()
        return axes


class PyLabTitle(Node, CustomizeAxes):
    """Add a title to the current axe. See pylab.title for details

    :param axes:
    :param str text:
    :param int fontsize: (default 12)
    :param str color: (default black)
    :param dict kwargs: (defaut {})

    :Example:

    .. dataflow:: openalea.pylab.test title
        :width: 40%

        **The openalea.pylab.test.title dataflow.** Add a title to an existing
        axes.

    .. plot::
        :width: 40%

        from openalea.core.alea import *
        pm = PackageManager()
        run_and_display(('openalea.pylab.test', 'title'),{},pm=pm)

    .. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    """

    def __init__(self):
        from matplotlib import font_manager
        Node.__init__(self)
        CustomizeAxes.__init__(self)

        self.add_input(name="axes")
        self.add_input(name="text", interface=IStr, value=None)
        self.add_input(name="fontsize", interface=IFloat, value=12)
        self.add_input(name="color", interface=IEnumStr(tools.colors.keys()), value='black')
        self.add_input(name='kwargs', interface=IDict, value={})

        self.add_output(name='axes')

    def __call__(self, inputs):
        kwds = {}
        kwds['fontsize'] = self.get_input('fontsize')
        kwds['color'] = self.get_input('color')
        for key, value in self.get_input('kwargs').iteritems():
            kwds[key]=value

        text = self.get_input('text')

        axes = self.get_axes()
        for axe in axes:
            axe.set_title(text, **kwds)
            axe.get_figure().canvas.draw()

        return self.get_input('axes')



class PyLabTextProperties(Node):
    """Create a TextProperties dict. See pylab.Text for details.

    .. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    """
    def __init__(self):
        Node.__init__(self)
        self.add_input(name='alpha',    interface=IFloat(0,1,0.1), value=1)
        self.add_input(name='color',    interface=IEnumStr(tools.colors.keys()), value='k')
        self.add_input(name='fontproperties', interface=IDict, value={'family':'sans-serif',
            'size':12, 'stretch':'normal', 'style':'normal', 'weight':'normal',
            'variant':'normal'})
        self.add_input(name='horizontalalignment', interface=IEnumStr(tools.horizontalalignment.keys()), value='left')
        self.add_input(name='rotation', interface=IFloat(-180,180,10), value=0)
        self.add_input(name='verticalalignment', interface=IEnumStr(tools.verticalalignment.keys()), value='baseline')
        self.add_input(name='kwargs',   interface=IDict, value = {
            #'agg_filter': None,
#            'animated': False,
#            'axes': None,
#            'clip_box': None,
#            'clip_on': True,
#            'clip_path': None,
#            'contains': None,
#            'figure': None,
#            'gid': None,
#            'path_effects': None,
#            'picker': None,
#            'rasterized': None,
#            'rotation_mode': None,
#            'snap': None,
#            'text': '',
#            'transform': None,
            'url': None,
#            'visible': True,
            'zorder': 3})

        self.add_output(name='kwds', interface=IDict, value={})

    def __call__(self,inputs):
        kwds = {}

        for input in self.input_desc:
            if input['name'] != 'kwargs':
                kwds[input['name']] = self.get_input(input['name'])
            else:
                # the kwargs
                for k,v in self.get_input('kwargs').iteritems():
                    kwds[k] = v

        # finally clear up the fontproperties dictionary and replace it by an instance of font properties.
        from pylab import matplotlib
        from matplotlib.font_manager import FontProperties
        fp = FontProperties(**kwds['fontproperties'])
        kwds['fontproperties'] = fp
        #hack for matplotlib <1.0.0
        del kwds['agg_filter']
        return kwds



class PyLabFontProperties(Node):
    """A Font properties selector. See matplotlib.font_manager.FontProperties for details.

    .. warning:: not to be used alone. Connect this node to a TextProperties node.

    :param str family:
    :param str style:
    :param str weight:
    :param str variant:
    :param str stretch:
    :param str size:
    :param str fname: connect to a file with your fonts
    :param dict kwargs: any other key/value pair

    :return: a dictionary to be used by a FontProperties instance.

    .. seealso:: TextProperties

    .. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    """

    def __init__(self):
        Node.__init__(self)
        self.add_input(name='family', interface=IEnumStr(tools.families.keys()), value='serif')
        self.add_input(name='style', interface=IEnumStr(tools.styles.keys()), value='normal')
        self.add_input(name='variant', interface=IEnumStr(tools.variants.keys()), value='normal')
        self.add_input(name='weight', interface=IEnumStr(tools.weights.keys()), value='normal')
        self.add_input(name='stretch', interface=IEnumStr(tools.streches.keys()), value='normal')
        self.add_input(name='size', interface=IEnumStr(tools.sizes.keys()), value='medium')
        self.add_input(name='fname', interface=IStr, value=None)
        self.add_input(name='kwargs', interface=IDict, value={})
        #self.add_input(name='_init', _init=None)
        #todo style, variant and strethc do not seem to work
        self.add_output(name='kwds', interface=IDict, value={})

    def __call__(self,inputs):
        kwds = {}
        kwds['family'] = self.get_input('family')
        kwds['style'] = self.get_input('style')
        # !!! size must be translated into number.
        from pylab import matplotlib
        from matplotlib import font_manager
        kwds['size'] = font_manager.font_scalings[self.get_input('size')]
        kwds['variant'] = self.get_input('variant')
        kwds['weight'] = self.get_input('weight')
        kwds['stretch'] = self.get_input('stretch')
        for key, value in self.get_input('kwargs').iteritems():
            kwds[key] = value

        return kwds




class PyLabSaveFig(Node):
    """Save the current figure in a file. See pylab.savefig for details. 

    .. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    """
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
        kwds['format']=tools.extensions[self.get_input('format')]
        kwds['transparent']=self.get_input('transparent')
        savefig(self.get_input('fname'), **kwds)


class PyLabShow(Node):
    """This node simply calls pylab.show(), which may be useful sometimes.

    The input and output connectors are not used by the function itself. There
    are present to allow this node to be used in a dataflow. Therefore the
    output is simply set to be the input parameter.

    .. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    """
    def __init__(self):
        Node.__init__(self)
        self.add_input(name='dummy')
        self.add_output(name='dummy')

    def __call__(self, inputs):
        from pylab import show
        show()
        return self.get_input('dummy')

class PyLabColorMap(Node):
    """Plot all colormap


    .. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    """
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
                #print index
                subplot(int(l/2)+l%2+1, 2, index+1)
                #print int(l/2)+l%2, 2, (index+1)/2+(index+1)%2+1
                axis("off")
                imshow(a.transpose(),aspect='auto',cmap=tools.get_cmap(m),origin="lower")
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
        from pylab import get_cmap
        res = get_cmap(maps)
        return res




class PyLabXTicks(Node, CustomizeAxes):
    """Set the tick locations and labels. See pylab.xticks for details.

    :param axes: the current axes to manipulate.
    :param array locs: (default is empty)
    :param array labels: (default is empty)
    :param float orientation:
    :returns: the current axes

    :Example:

    .. dataflow:: openalea.pylab.test xyticks
        :width: 40%

        **The openalea.pylab.test.xyticks dataflow.** play with the ticklabels. Notice
        the xlabel at 2.5 and the ylabel orientation.

    .. plot::
        :width: 40%

        from openalea.core.alea import *
        pm = PackageManager()
        run_and_display(('openalea.pylab.test', 'xyticks'),{},pm=pm)

    .. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
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
            if len(locs) != 0:
                axe.set_xticks(locs)
            labels = self.get_input('labels')
            if len(labels) != 0:
                axe.set_xticklabels(labels, **kwds)
            axe.set_yticklabels([x.get_text() for x in axe.get_yticklabels()], **kwds)
            axe.get_figure().canvas.draw()
        return axes


class PyLabTickParams(Node, CustomizeAxes):
    """Tune the ticks on an axis. See pylab.tick_params for details.

    :param axes: the axes to tune.
    :param str axis: which axis to manipulate ('x', 'y', 'both') (default is 'both')
    :param bool reset: set all parameters to defaults
    :param str which: apply arguments to major ticks only (default is major)
    :param str direction: ['in' | 'out'] Puts ticks inside or outside the axes.
    :param int length: Tick length in points
    :param int width: Tick width in points
    :param int pad: Distance in points between tick and label.
    :param labelsize: (default 12)
    :param labelcolor: (default black)
    :param zorder: (default 0)
    :param bool bottom: default True
    :param bool top:
    :param bool left:
    :param bool right:
    :param bool labelbottom: (default True)
    :param bool labeltop:  (default False)
    :param bool labelleft:  (default True)
    :param bool labelright: (default False)

    :Example:

    .. dataflow:: openalea.pylab.test tickparams
        :width: 40%

        **The openalea.pylab.demo.polar_demo dataflow.** In order to plot a x/y pair of
        vectors into a polar plane, you must use the PyLabAxes node and set the polar to True.
        Indeed, there is no mecanism to set the axes to polar after PyLabPlot has been called.

    .. plot::
        :width: 40%

        from openalea.core.alea import *
        pm = PackageManager()
        run_and_display(('openalea.pylab.test', 'tickparams'),{},pm=pm )

    """
    def __init__(self):
        self.daxis = {'in':'in', 'out':'out', 'both':'both'}
        self.ddirection = {'in':'in', 'out':'out'}
        Node.__init__(self)
        CustomizeAxes.__init__(self)
        self.add_input(name='axes')
        self.add_input(name='axis', interface=IEnumStr(self.daxis.keys()), value='both')
        self.add_input(name='reset', interface=IBool, value=False)
        self.add_input(name='direction', interface=IEnumStr(self.ddirection.keys()), value='in')
        self.add_input(name='length', interface=IInt, value=4)
        self.add_input(name='width', interface=IInt, value=1)
        self.add_input(name='color', interface=IEnumStr(tools.colors.keys()), value='black')
        self.add_input(name='pad', interface=IInt, value=1)
        self.add_input(name='labelsize', interface=IInt, value=12)
        self.add_input(name='labelcolor', interface=IEnumStr(tools.colors.keys()), value='black')
        self.add_input(name='zorder', interface=IInt, value=0)
        self.add_input(name='bottom', interface=IBool, value=False)
        self.add_input(name='top', interface=IBool, value=False)
        self.add_input(name='left', interface=IBool, value=False)
        self.add_input(name='right', interface=IBool, value=False)
        self.add_input(name='labelbottom', interface=IBool, value=True)
        self.add_input(name='labeltop', interface=IBool, value=False)
        self.add_input(name='labelleft', interface=IBool, value=True)
        self.add_input(name='labelright', interface=IBool, value=False)

    def __call__(self, inputs):
        kwds = {}
        kwds['axis'] = self.daxis[self.get_input('axis')]
        kwds['reset'] = self.get_input('reset')
        kwds['direction'] = self.ddirection[self.get_input('direction')]
        kwds['length'] = self.get_input('length')
        kwds['width'] = self.get_input('width')
        kwds['color'] = tools.colors[self.get_input('color')]
        kwds['pad'] = self.get_input('pad')
        kwds['labelsize'] = self.get_input('labelsize')
        kwds['labelcolor'] = tools.colors[self.get_input('labelcolor')]
        kwds['zorder'] = self.get_input('zorder')
        kwds['bottom'] = self.get_input('bottom')
        kwds['top'] = self.get_input('top')
        kwds['left'] = self.get_input('left')
        kwds['right'] = self.get_input('right')
        kwds['labelbottom'] = self.get_input('labelbottom')
        kwds['labeltop'] = self.get_input('labeltop')
        kwds['labelleft'] = self.get_input('labelleft')
        kwds['labelright'] = self.get_input('labelright')

        try:
            from pylab import tick_params
            axes = self.get_axes()
            for axe in axes:
                axe.tick_params(**kwds)
                axe.get_figure().canvas.draw()
            return axes
        except:
            import warnings
            warnings.warn('\nWARNING: tickparams not available on your system. Consider installing a maplotlib version>=1')
            return self.get_axes()

class PyLabYTicks(Node, CustomizeAxes):
    """Set the tick locations and labels. See pylab.xticks for details.

    :param axes: the current axes to manipulate.
    :param array locs: (default is empty)
    :param array labels: (default is empty)
    :param float orientation:
    :returns: the current axes

    :Example: see :class:`~openalea.pylab_decorators_wralea.py_pylab.PyLabXTicks`

    .. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
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
            if len(locs) != 0:
                axe.set_yticks(locs)
            labels = self.get_input('labels')
            if len(labels) != 0:
                axe.set_yticklabels(labels)
            axe.set_yticklabels([x.get_text() for x in axe.get_yticklabels()], **kwds)
            axe.get_figure().canvas.draw()
        return axes


class PyLabXLim(Node, CustomizeAxes):
    """VisuAlea version of pylab.xlim

    :param axes:
    :param xmin:
    :param xmax:
    :param kwargs:

    :return: modified axes

    :Example:

    .. dataflow:: openalea.pylab.test xylim
        :width: 40%

        **The openalea.pylab.test.xylim dataflow.** Add a title to an existing
        axes.

    .. plot::
        :width: 40%

        from openalea.core.alea import *
        pm = PackageManager()
        run_and_display(('openalea.pylab.test', 'xylim'),{},pm=pm)

    .. note:: xmin must be less than xmax

    .. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>

    """
    def __init__(self):
        Node.__init__(self)
        CustomizeAxes.__init__(self)
        self.add_input(name='axes')
        self.add_input(name='xmin', interface=IFloat, value=0. )
        self.add_input(name='xmax', interface=IFloat, value=0. )
        self.add_input(name='kwargs', interface=IDict, value={})
        self.add_output(name='axes')

    def __call__(self, inputs):
        kwds = {}
        for key, value in self.get_input('kwargs').iteritems():
            kwds[key] = value
        axes = self.get_axes()
        xmin = self.get_input('xmin')
        xmax = self.get_input('xmax')
        assert xmin<=xmax, 'xmin must be less than xmax'
        if xmin != xmax:
            for axe in axes:
                axe.set_xlim(xmin=xmin, xmax=xmax, **kwds)
                #SPHINX HACK
                axe.get_figure().canvas.draw()
        return axes



class PyLabYLim(Node, CustomizeAxes):
    """VisuAlea version of pylab.ylim

    :param axes:
    :param ymin:
    :param ymax:
    :param kwargs:

    :return: modified axes

    .. seealso:: :class:`~openalea.pylab_decorators_wralea.py_pylab.PyLabXLim`

    .. note:: ymin must be less than ymax

    .. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
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
            #SPHINX HACK
            axe.get_figure().canvas.draw()
        return self.get_input('axes')


class PyLabGrid(Node, CustomizeAxes):
    """Add a grid to an axes. See pylab.grid for details

    :param axes: an input axes
    :param bool b: Set the grid on (default is True)
    :param str which: where to set the lines (default is major ticks)
    :param str linestyle: style of the lines (default is dotted)
    :param str color: color of the lines )(default is black)
    :param float linewidth: width of the lines (default is 1)
    :param dict kwargs: further properties to fully customize the grid

    :returns: the current axes

    :Example:

    .. dataflow:: openalea.pylab.test grid
        :width: 40%

        **The openalea.pylab.demo.polar_demo dataflow.** In order to plot a x/y pair of
        vectors into a polar plane, you must use the PyLabAxes node and set the polar to True.
        Indeed, there is no mecanism to set the axes to polar after PyLabPlot has been called.

    .. plot::
        :width: 40%

        from openalea.core.alea import *
        pm = PackageManager()
        run_and_display(('openalea.pylab.test', 'grid'),{},pm=pm )

    .. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    """
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
        kwds['linestyle']=tools.linestyles[self.get_input("linestyle")]
        kwds['color']=tools.colors[self.get_input("color")]
        kwds['linewidth']=self.get_input("linewidth")
        kwds['b']=self.get_input("b")
        kwds['which']=self.get_input("which")

        axes = self.get_axes()
        for axe in axes:
            axe.grid(**kwds)
            axe.get_figure().canvas.draw()
        return self.get_input('axes')


class PyLabOrigin(Node):
    """Set the origin. See pylab.imshow for instance.

    .. warning: not yet for production
    .. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    """
    def __init__(self):
        Node.__init__(self)
        self.add_input(name='origin', interface=IEnumStr(origins), value=None)
        self.add_output(name='output', interface=IDict, value={})

    def __call__(self, inputs):
        kwds = {}
        kwds['origin'] = self.get_input('origin')
        return (kwds ,)


class PyLabAxes(Node):
    """Create an axes. See pylab.axes for details.

    This node is useful if you want to create a polar axes.

    :param input: an optional input axes
    :param bool clean: clear the axe if True (default is True)
    :param float left: left boundary limit of the axes (default is 0.12)
    :param float bottom: bottom boundary limit of the axes (default is 0.12)
    :param float width: width of the axes (default is 0.78)
    :param float height: height of the axes (default is 0.78)
    :param str axisbg: color of the axes background
    :param bool frameon: set the frame on (default is True)
    :param bool polar: set the axes in polar mode (default is False)
    :param str xscale: set the x axes scale (default is linear)
    :param str yscale: set the y axes scale (default is linear)
    :param str xticks: set the xticks (default is auto)
    :param str xticks: set the yticks (default is auto)
    :param dict kwargs: more arguments may be provided as a dictionary

    :return: the current axes

    :Example:

    .. dataflow:: openalea.pylab.demo polar_demo
        :width: 40%

        **The openalea.pylab.demo.polar_demo dataflow.** In order to plot a x/y pair of
        vectors into a polar plane, you must use the PyLabAxes node and set the polar to True.
        Indeed, there is no mecanism to set the axes to polar after PyLabPlot has been called.

    .. plot::
        :width: 40%

        from openalea.core.alea import *
        pm = PackageManager()
        run_and_display(('openalea.pylab.demo', 'polar_demo'),{},pm=pm )

    .. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    """

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
    """a simple code to clear a figure. See pylab.clf  for details

    :param axes: an axes to clear
    :return: the current axes

    .. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    """
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
    """Node to connect patches or axes decorators to an axes

    :param axes: the axe to complete
    :param whatever: a connector to use for connecting other nodes that add patches or
        decorators such as title and labels.

    :return: the current axes

    .. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    """
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
            if this != None:
                try:
                    gca().add_patch(this)
                    gca().get_figure().canvas.draw()
                except:
                    raise ValueError('an invalid object is connected to AxesDecorator. Only patches and artist object accepted for now.')
        return self.get_input("axes")




class PyLabBox(Node):
    """See pylab.box for details

    .. warning: not yet for production

    :param axes: an input pylab.axes
    :param on' boolean to turn on or off the box of the current axe

    :return: the current axes

    .. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    """
    def __init__(self):
        Node.__init__(self)
        self.add_input(name='axes')
        self.add_input(name='on', interface=IBool, value=True)
        self.add_output(name='output')

    def __call__(self, inputs):
        from pylab import box, gca
        box(self.get_input('on'))
        gca().get_figure().canvas.draw()
        return self.get_input('axes')
