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
    'purple':'purple',
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
    if type!='hist':
        kwds['color']=line2d.get_color()
    else:
        kwds['facecolor']=line2d.get_color()
    if type!='hist':
        kwds['linestyle']=line2d.get_linestyle()
    kwds['linewidth']=line2d.get_linewidth()
    if type!='linecollection' and type!='hist':
        kwds['marker']=line2d.get_marker()
        kwds['markersize']=line2d.get_markersize()
        kwds['markeredgewidth']=line2d.get_markeredgewidth()
        kwds['markersize']=line2d.get_markersize()
        kwds['fillstyle']=line2d.get_fillstyle()
        kwds['markeredgecolor']=line2d.get_markeredgecolor()
    kwds['label']=line2d.get_label()
    kwds['alpha']=line2d.get_alpha()
    return kwds



class Plotting(Node):

    ERROR_NOXDATA = 'No data connected to the x connector. Connect a line2D, an array or a list of line2Ds or arrays'
    ERROR_FAILURE = 'Failed to generate the image. check your entries.'

    def __init__(self,  inputs={}):
        Node.__init__(self)
        self._show = True
        self._title = None
        self._ylabel = None
        self._xlabel = None

        for input in inputs:
            self.add_input(**input)

        self.add_input(name="show",   interface=IBool, value=True)
        self.add_input(name="grid",   interface=IBool, value=True)
        self.add_input(name="subplot",interface=IInt(1,20,1), value=1)
        self.add_input(name="xlabel", interface=IStr,  value="")
        self.add_input(name="ylabel", interface=IStr,  value = "")
        self.add_input(name="title",  interface=IStr,  value = "")
        self.add_input(name="figure", interface=IInt(1,20,1), value=1)
        self.add_input(name='legend', interface=IBool, value=True)
        self.add_input(name='colorbar', interface=IBool, value=False)
        self.add_input(name='axes',   interface=IDict, value={})
        self.add_input(name='axis',   interface=IDict, value={'type':'normal', 'xmin':None, 'xmax':None, 'ymin':None, 'ymax':None})

        self.add_output(name='output')
        self.colorbar_called = False
        self.subplot_call = 1
        self.axes_shown = None
        self.fig = None

    def colorbar(self):
        from pylab import colorbar
        print self.colorbar_called
        if self.colorbar_called == True:
            return
        if type(self.get_input('colorbar'))==bool:
            if self.get_input('colorbar')==True:
                colorbar()
                self.corlorbar_called=True
        else:
            kwds = self.get_input('colorbar')
            colorbar(**kwds)
            self.corlorbar_called=True

    def show(self):
        from pylab import show
        if self.get_input('show'):
            show()

    def grid(self):
        from pylab import grid
        grid(self.get_input('grid'))

    def figure(self):
        from pylab import figure
        args = self.get_input('figure')
        if type(args)==int:
            fig = figure(args)
        else:
            fig = figure(**args)

        self.fig = fig

    def axes(self):
        if self.axes_shown is not None:
            try:
                self.fig.delaxes(self.axes_shown)
            except:
                pass
        if len(self.get_input('axes'))>0:
            from pylab import axes
            import copy
            args = self.get_input('axes')
            kwds = copy.deepcopy(args)
            #using axes([], ...) does not have the same behaviour as axes(position=[], ...)
            del kwds['position']
            self.axes_shown = axes(args['position'], **kwds)
        else:
            self.axes_shown = None

    def axis(self):
        from pylab import axis
        import copy
        kwds = copy.deepcopy(self.get_input('axis'))
        type = kwds['type']
        del kwds['type']
        if type!='manual':
            axis(type)
        else:
            print 'b'
            print kwds
            axis(**kwds)

    def title(self):
        from pylab import title
        try:
            import copy
            text = self.get_input('title')['text']
            kwds = copy.deepcopy(self.get_input('title'))
            del kwds['text']
            title(text, **kwds)
        except:
            title(self.get_input('title'))

    def xlabel(self):
        from pylab import xlabel
        try:
            import copy
            text = self.get_input('xlabel')['text']
            kwds = copy.deepcopy(self.get_input('xlabel'))
            del kwds['text']
            xlabel(text, **kwds)
        except:
            xlabel(self.get_input('xlabel'))

    def ylabel(self):
        from pylab import ylabel
        try:
            import copy
            text = self.get_input('ylabel')['text']
            kwds = copy.deepcopy(self.get_input('ylabel'))
            del kwds['text']
            ylabel(text, kwds)
        except:
            ylabel(self.get_input('ylabel'))

    def legend(self):
        from pylab import legend
        args = self.get_input('legend')
        if type(args)==bool:
            if args:
                legend()
        else:
            legend(**args)

    def error(self, message):
        from pylab import text
        text(0., 0.6, message, backgroundcolor='red')

    def subplot(self):
        from pylab import subplot

        try:
            row = self.get_input('subplot')[0]
            column = self.get_input('subplot')[1]
            number = self.get_input('subplot')[2]
            kwds = self.get_input('subplot')[3]
        except:
            row = 1
            column = 1
            number = 1
            kwds = {}
        # this is a hack to prevent colorbar to add-on in an axes when called several times
        # calling subplot(2,1,1) or subplot(111) 
        if self.subplot_call == 1:
            subplot(row, column, number, **kwds)
            self.subplot_call = 2
        else:
            subplot(int(str(row)+str(column)+str(number)), **kwds)
            self.subplot_call = 1


    def properties(self):
        self.legend()
        self.title()
        self.xlabel()
        self.ylabel()
        self.grid()
        self.axis()
        self.colorbar()
        self.show()

class PyLabPlot(Plotting):
    """pylab.plot interface

    if x is an array, y should be an array as well or a list of array (assuming
    they all have the same x). All must have the same length.

    if x is a line2D, y is not used.

    x can also be a list of Line2D objects.

    if x is made of Line2D, their format strings are used (label, color, linewidth...)
    Otherwise, the default values (in pylabplot) are used.

    :param x: either an array or a PyLabLine2D object or a list of PyLabLine2D objects.
    :param x: either an array or list of arrays
    :param label: None by default
    :param marker: circle marker by default
    :param linestyle: solid line by default
    :param color: blue by default
    :param xlabel: none by default
    :param ylabel: none by default
    :param title: none by default

    .. todo:: case where there are several y entries and/or x
    :authors: Thomas Cokelaer
    """
    def __init__(self):
        """init docstring"""
        inputs = [
                    {'name':'x',            'interface':None,                           'value':None},
                    {'name':'y',            'interface':None,                           'value':None},
                    {'name':'marker',       'interface':IEnumStr(markers.keys()),       'value':'circle'},
                    {'name':'markersize',   'interface':IFloat,                         'value':10},
                    {'name':'linestyle',    'interface':IEnumStr(linestyles.keys()),    'value':'solid'},
                    {'name':'color',        'interface':IEnumStr(colors.keys()),        'value':'blue'},
        ]
        Plotting.__init__(self, inputs)

    def __call__(self, inputs):
        from pylab import plot, cla,  hold,  Line2D
        xinputs = self.get_input("x")
        yinputs = self.get_input("y")

        #first, we select the figure, we use subplot() that may be overwritten by axes()
        self.figure()
        #self.subplot()
        self.axes()
        cla()
        kwds = {}
        kwds['markersize']=self.get_input("markersize")
        kwds['marker']=markers[self.get_input("marker")]
        kwds['linestyle']=linestyles[self.get_input("linestyle")]
        kwds['color']=colors[self.get_input("color")]
        print kwds
        if xinputs == None:
            raise ValueError(self.ERROR_NOXDATA)
        if type(xinputs)!=list:
            xinputs = [xinputs]
        if type(yinputs)!=list:
            yinputs = [yinputs]

        # case of an x input without y input. line2D are all manage in this if statement
        if yinputs[0]==None:
            #plot(line2D) and plot([line2D, line2D])
            if type(xinputs[0])==Line2D:
                for x in xinputs:
                    line2dkwds = get_kwds_from_line2d(x, kwds)
                    #returns the processed data ?
                    plot(x.get_xdata(orig=False), x.get_ydata(orig=False),**line2dkwds)
                    hold(True)
            #plot([x1,None,x2,None, ...) and plot(x1)
            else:
                c = enumerate(colors)
                for x in xinputs:
                    try:
                        color = c.next()
                        kwds['color']=color[1]
                    except:
                        print 'no more colors'
                    plot(x, **kwds)
                    hold(True)

        else:
            if len(xinputs)==1 and len(yinputs)!=1:
                # plot(x,y) and plot(x, [y1,y2])
                c = enumerate(colors)
                for y in yinputs:
                    try:
                        color = c.next()
                        kwds['color']=color[1]
                    except:
                        print 'no more colors'
                    plot(xinputs[0], y, **kwds)
                    hold(True)
            else:
                if len(xinputs)!=len(yinputs):
                    print 'warning more x inputs than y inputs. correct the connectors'
                # plot([x1,x2], [y1,y2])
                # plot([x1], [y1])
                for x,y in zip(xinputs, yinputs):
                   plot(x, y, **kwds)
                   hold(True)

        self.properties()



class PyLabLogLog(PyLabPlot):
    """
    status: 80% completed

    .. todo:: this documentsation, add subsx/subsy nonposx and basex options
    """
    def __init__(self):
        PyLabPlot.__init__(self)
        """*basex*/*basey*: scalar > 1
        base of the *x*/*y* logarithm

      *subsx*/*subsy*: [ None | sequence ]
        the location of the minor *x*/*y* ticks; *None* defaults
        to autosubs, which depend on the number of decades in the
        plot; see :meth:`matplotlib.axes.Axes.set_xscale` /
        :meth:`matplotlib.axes.Axes.set_yscale` for details

      *nonposx*/*nonposy*: ['mask' | 'clip' ]
        non-positive values in *x* or *y* can be masked as
        invalid, or clipped to a very small positive number
        """
    def __call__(self, inputs):
        from pylab import loglog, cla,hold
        xinputs = self.get_input("x")
        yinputs = self.get_input("y")

        #figure(**self.get_input('figure'))
        kwds = {}
        kwds['markersize']=self.get_input("markersize")
        kwds['marker']=markers[self.get_input("marker")]
        kwds['linestyle']=linestyles[self.get_input("linestyle")]
        kwds['color']=colors[self.get_input("color")]

        self.figure()
        self.axes()
        cla()

        if xinputs == None:
            raise ValueError(self.ERROR_NOXDATA)
        if type(xinputs)!=list:
            xinputs = [xinputs]
        if type(yinputs)!=list:
            yinputs = [yinputs]

        # case of an x input without y input. line2D are all manage in this if statement
        if yinputs[0]==None:
            #plot(line2D) and plot([line2D, line2D])
            if type(xinputs[0])==Line2D:
                for x in xinputs:
                    line2dkwds = get_kwds_from_line2d(x, kwds)
                    #returns the processed data ?
                    res =loglog(x.get_xdata(orig=False), x.get_ydata(orig=False),**line2dkwds)
                    hold(True)
            #plot([x1,None,x2,None, ...) and plot(x1)
            else:
                c = enumerate(colors)
                for x in xinputs:
                    try:
                        color = c.next()
                        kwds['color']=color[1]
                    except:
                        print 'no more colors'
                    res =loglog(x, **kwds)
                    hold(True)

        else:
            if len(xinputs)==1:
                # plot(x,y) and plot(x, [y1,y2])
                c = enumerate(colors)
                for y in yinputs:
                    try:
                        color = c.next()
                        kwds['color']=color[1]
                    except:
                        print 'no more colors'
                    res = loglog(xinputs[0], y, **kwds)
                    hold(True)
            else:
                if len(xinputs)!=len(yinputs):
                    print 'warning more x inputs than y inputs. correct the connectors'
                # plot([x1,x2], [y1,y2])
                # plot([x1], [y1])
                for x,y in zip(xinputs, yinputs):
                   res = loglog(x, y, **kwds)
                   hold(True)
        self.properties()

        return res



class PyLabHist(Plotting):
    """pylab.hist interface

    :param x: input data
    :param bins: binning number (default is 10)
    :param facecolor: blue by default
    :param normed:
    :param log:
    :param histtype:
    :param orientation:
    :param align:

    :param xlabel: none by default, could be output of PyLabXLabel
    :param ylabel: none by default, could be output of PyLabYLabel
    :param title: none by default, could be output of PyLabTitle
    
    :param kwargs: should be the outpt of PyLabRectangle or see pylab.hist for options

    .. todo::

        range=None
        bottom=None,
        rwidth=None,

    :authors: Thomas Cokelaer
    """

    def __init__(self):
        self.histtype = {
                'bar':'bar',
                'barstacked':'barstacked',
                'step' :'step',
                'stepfilled':'stepfilled'}
        self.orientation = {'horizontal':'horizontal', 'vertical':'vertical'}
        self.align = {'mid':'mid', 'right':'right', 'left':'left'}
        
        inputs = [
            {'name':'x'},
            {'name':'bins',         'interface':IInt, 'value':10},
            {'name':'facecolor',    'interface':IEnumStr(colors.keys()), 'value':'blue'},
            {'name':'normed',       'interface':IBool, 'value':False},
            {'name':'cumulative',   'interface':IBool, 'value':False},
            {'name':'histtype',     'interface':IEnumStr(self.histtype.keys()), 'value':'bar'},
            {'name':'align',        'interface':IEnumStr(self.align.keys()), 'value':'mid'},
            {'name':'orientation',  'interface':IEnumStr(self.orientation.keys()), 'value':'vertical'},
            {'name':'log',          'interface':IBool,  'value':False},
            {'name':'label',          'interface':IStr,  'value':''}
        ]
        Plotting.__init__(self, inputs)

        #self.add_input(name="range", interface = ITuple3, value = None)

        self.add_input(name="kwargs", interface = IDict, value={'alpha':1., 'animated':False})
        

        self.add_output(name="position")
        self.add_output(name="counts")
        """
          antialiased or aa: [True | False]  or None for default         
          axes: an :class:`~matplotlib.axes.Axes` instance         
          clip_box: a :class:`matplotlib.transforms.Bbox` instance         
          clip_on: [True | False]         
          clip_path: [ (:class:`~matplotlib.path.Path`,         :class:`~matplotlib.transforms.Transform`) |         :class:`~matplotlib.patches.Patch` | None ]         
          contains: a callable function         
          edgecolor or ec: mpl color spec, or None for default, or 'none' for no color         
          fill: [True | False]         
          gid: an id string         
          hatch: [ '/' | '\\' | '|' | '-' | '+' | 'x' | 'o' | 'O' | '.' | '*' ]         
          linestyle or ls: ['solid' | 'dashed' | 'dashdot' | 'dotted']         
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
    def __call__(self, inputs):
        from pylab import cla, hold, hist, Line2D
        self.figure()
        self.axes()
        cla()
        kwds={}
        kwds['bins']=self.get_input("bins")
        kwds['normed']=self.get_input("normed")
        kwds['facecolor']=self.get_input("facecolor")
        kwds['label']=self.get_input("label")
        kwds['log']=self.get_input("log")
        kwds['orientation']=self.orientation[self.get_input("orientation")]
        kwds['figure']=self.get_input("figure")
        kwds['histtype']=self.histtype[self.get_input("histtype")]
        kwds['align']=self.align[self.get_input("align")]
        kwds['cumulative']=self.get_input("cumulative")
        #!! facecolor is alrady in the Hist node, so override it if available in kwargs dict
        for key,value in self.get_input('kwargs').iteritems():
            kwds[key] = value

        xinputs = self.get_input('x')
        if type(xinputs)!=list:
            xinputs = [xinputs]
        try:
            for x in xinputs:
                if type(x)==Line2D:
                    line2dkwds = get_kwds_from_line2d(x, kwds, type='hist')
                    print line2dkwds
                    res = hist(x.get_ydata(orig=False),**line2dkwds)
                else:
                    res = hist(x,**kwds)
            hold(True)
        except ValueError, e:
            res = (None, None)
            print e
            raise ValueError('tttt')

        self.properties()
        return (res, res[1],res[0])
 #range=None   bottom=None,    rwidth=None,


class PyLabAcorr(Plotting):
    """pylab.acorr interface

     Plot the autocorrelation of x. If normed = True, normalize
     the data by the autocorrelation at 0-th lag. x is detrended
     by the detrend callable (default no normalization).

    :param x: the input data
    :param normed: True
    :param detrend:
    :param usevlines:
    :param maxlags:
    :param xlabel: none by default
    :param ylabel: none by default
    :param title: none by default


    :authors: Thomas Cokelaer
    """

    def __init__(self):
        inputs = [
                    {'name':'x', 'interface':None, 'value':None},
                    {'name':"maxlags",   'interface':IInt,  'value':10},
                    {'name':"normed",    'interface':IBool, 'value':False},
                    {'name':"usevlines", 'interface':IBool, 'value':True},
                    {'name':'detrend', 'interface':IEnumStr(detrends.keys()), 'value':'none'},
                    {'name':"kwargs",    'interface':IDict, 'value':{}}
                ]
        Plotting.__init__(self, inputs)

    def __call__(self, inputs):
        from pylab import clf, hold, acorr, Line2D
        import pylab
        self.figure()
        self.axes()
        cla()
        x = self.get_input("x")

        kwds = {}
        kwds['maxlags'] = self.get_input("maxlags")
        kwds['normed'] = self.get_input("normed")
        kwds['usevlines'] = self.get_input("usevlines")
        kwds['detrend'] = getattr(pylab, 'detrend_'+self.get_input('detrend'))

        res = None
        xinputs=self.get_input('x')
        if type(xinputs)!=list:
            xinputs = [xinputs]

        #line2dkwds = get_kwds_from_line2d(x, self.get_input('kwargs'), type='linecollection')
        #returns the processed data ?
        for x in xinputs:
            res =  acorr(x, **kwds)
            hold(True)
        #self.error(self.ERROR_FAILURE)
        self.properties()

        return res



#//////////////////////////////////////////////////////////////////////////////

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



class PyLabScatter(Plotting):
    """pylab.scatter interface

    :param x: the first input data set
    :param y: the second input data set (optional)
    :param label: None by default
    :param marker: circle marker by default
    :param linestyle: solid line by default
    :param color: blue by default
    :param xlabel: none by default
    :param ylabel: none by default
    :param title: none by default

    .. todo:: case where there are several y entries and/or x
    :authors: Thomas Cokelaer
    """
    def __init__(self):
        inputs = [
            {'name':'x',        'value':None},
            {'name':'y',        'value':None},
            {'name':'sizes',    'value':20},
            {'name':'colors',   'value':'r'},
            {'name':"label",    'interface':IStr,       'value':None},
            {'name':"marker",   'interface':IEnumStr(markers.keys()), 'value' : 'circle'},
            {'name':"color",    'interface':IEnumStr(colors.keys()),  'value':'blue'},
            {'name':"alpha",    'interface':IFloat,     'value' : 0.5},
        ]

        Plotting.__init__(self, inputs)


    def __call__(self, inputs):
        from pylab import scatter, cla,  subplot
        x = self.get_input("x")
        y = self.get_input("y")
        sizes = self.get_input("sizes")
        colors = self.get_input("colors")
        self.figure()
        #self.subplot()
        self.axes()
        cla()
        res = scatter(x,y, s=sizes,c=colors,
                marker=markers[self.get_input("marker")],
                alpha=self.get_input("alpha"),
                label=self.get_input("label"))
        self.properties()

        return res




class PyLabBoxPlot(Plotting):
    """pylab.boxplot interface


    :param x: data
    :parma notch: (default 0)
    :param sym: '+'
    :param  vert: 1
    :param  whis: 1.5,
    :param  positions: None
    :param widths:None

    .. todo:: 
    :authors: Thomas Cokelaer
    """
    def __init__(self):
        """init docstring"""
        inputs = [
            {'name':"x"},
            {'name':"notch",    'interface':IInt, 'value':0},
            {'name':"sym",      'interface':IEnumStr(markers.keys()), 'value':'circle'},
            {'name':"vert",     'interface':IInt,  'value':1},
        ]
        Plotting.__init__(self, inputs)
        #self.__doc__+=plot.__doc__

    def __call__(self, inputs):
        x = self.get_input("x")
        from pylab import boxplot, cla, hold
        self.figure()
        self.axes()
        cla()
        res = boxplot(x, 
                sym=markers[self.get_input("sym")],
                vert=self.get_input("vert"),
                notch=self.get_input("notch"))
        self.properties()
        return res



class PyLabLine2D(Node):

    def __init__(self):
        Node.__init__(self)

        self.add_input(name="xdata", value=[])
        self.add_input(name="ydata", value=[])
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
        if len(ydata)==0:
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



class PyLabPie(Plotting):

    def __init__(self):
        inputs = [
            { 'name':'x'},
            {'name':'colors',       'interface':IStr,   'value':None},
            {'name':'labels',       'interface':ISequence, 'value':None},
            {'name':'explode',      'interface':ISequence, 'value':None},
            {'name':'pctdistance',  'interface':IFloat, 'value':0.6},
            {'name':'labeldistance','interface':IFloat, 'value':1.1},
            {'name':'shadow',       'interface':IBool,  'value':False},
            {'name':'hold',         'interface':IBool,  'value':False},
            {'name':'autopct',      'interface':IStr,   'value':None}
        ]

        Plotting.__init__(self, inputs)

    def __call__(self, inputs):
        from pylab import pie, cla
        self.figure()
        self.axes()
        cla()
        kwds = {}
        kwds['explode'] = self.get_input('explode')
        kwds['colors'] = self.get_input('colors')
        kwds['labels'] = self.get_input('labels')
        kwds['pctdistance'] = self.get_input('pctdistance')
        kwds['labeldistance'] = self.get_input('labeldistance')
        kwds['shadow'] = self.get_input('shadow')
        kwds['hold'] = self.get_input('hold')
        kwds['autopct'] = self.get_input('autopct')

        res = pie(self.get_input('x'), **kwds)

        self.properties()
        return res








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


class PyLabBar(Plotting):

    def __init__(self):
        inputs = [
            {'name':'left', 'interface':ISequence, 'value':[]},
            {'name':'height', 'interface':ISequence, 'value':[]}
        ]
        Plotting.__init__(self, inputs)


    def __call__(self, inputs):
        from pylab import bar, hold, cla
        
        self.figure()
        self.axes()
        cla()
        left = self.get_input('left')
        height = self.get_input('height')

        if type(left)!=list:
            left = [left]


        res = None
        if type(left[0])==float:
            print 'a'
            width = left[1] - left[0]
            print width
            print left
            print height
            res = bar(left[1:], height, width=width)
        else:
            print 'b'
            c = enumerate(colors)
            for x,y in zip(left, height):
                color = c.next()
                print color
                print x
                print y
                #width = x[1]-x[0]
                width=0.1
                res = bar(x[1:],y, width=width, color=color[1], alpha=0.5)
                hold(True)
        self.properties()

        return res

class PyLabCohere(Plotting):
    """ A function or a vector of length *NFFT*. To create window
          vectors see :func:`window_hanning`, :func:`window_none`,
          :func:`numpy.blackman`, :func:`numpy.hamming`,
          :func:`numpy.bartlett`, :func:`scipy.signal`,
          :func:`scipy.signal.get_window`, etc. The default is
          :func:`window_hanning`.  If a function is passed as the
          argument, it must take a data segment as an argument and
          return the windowed version of the segment.
    """
    def __init__(self):
        #     window = mlab.window_hanning, noverlap=0, pad_to=None,
        #     sides='default', scale_by_freq=None, **kwargs)
        inputs = [
            {'name':'x',            'interface':None,   'value':None},
            {'name':'y',            'interface':None,   'value':None},
            {'name':'NFFT',         'interface':IInt,   'value':256},
            {'name':'Fs',           'interface':IFloat, 'value':2.},
            {'name':'detrend',      'interface':IEnumStr(detrends.keys()), 'value':'none'},
            #{'name':'window',       'interface':None, 'value':'tobedone'},
            {'name':'noverlap',     'interface':IInt,   'value':0},
            {'name':'pad_to',       'interface':IInt,   'value':None},
            {'name':'sides',        'interface':IEnumStr(sides.keys()), 'value':'default'},
            #{'name':'scale_by_freq','interface':IBool,  'value':True},
            {'name':'Fc',           'interface':IFloat, 'value':0},
            ]

        Plotting.__init__(self, inputs)


    def __call__(self, inputs):
        from pylab import cohere, cla, detrend_none, detrend_linear, detrend_mean, hold
        import pylab
        cla()
        self.figure()
        self.axes()
        cla()
        kwds = {}
        kwds['NFFT'] = self.get_input('NFFT')
        kwds['Fs'] = self.get_input('Fs')
        kwds['detrend'] = getattr(pylab, 'detrend_'+self.get_input('detrend'))
        #kwds['window'] = self.get_input('window')
        kwds['noverlap'] = self.get_input('noverlap')
        kwds['pad_to'] = self.get_input('pad_to')
        kwds['sides'] = self.get_input('sides')
        #kwds['scale_by_freq'] = self.get_input('scale_by_freq')
        kwds['Fc'] = self.get_input('Fc')

        cxy = None
        freq = None
        try:
            cxy, freq = cohere(self.get_input('x'), self.get_input('y'), **kwds)
        except:
            xinputs=self.get_input('x')
            if type(xinputs)!=list:
                xinputs = [xinputs]
            if type(xinputs[0])==Line2D:
                for x in xinputs:
                    line2dkwds = get_kwds_from_line2d(x, kwds)
                    #returns the processed data ?
                    cxy, freq = cohere(x.get_xdata(orig=False), x.get_ydata(orig=False),**line2dkwds)
                    hold(True)

        self.properties()
        return (cxy, freq)


class Windowing(Node):
    """ should include hanning, ...."""
    def __init__(self):
        pass

    def __call__(self, inputs):
        pass


class PyLabSubPlotTool(Node):
    def __init__(self):

        Node.__init__(self)
        self.add_input(name='input')
        self.add_output(name='output')
    def __call___(self, inputs):
        from pylab import subplot_tool 
        #s = subplot_tool()
        return (s)


class PyLabSubPlot(Node):

    def __init__(self):

        Node.__init__(self)
        self.add_input(name='row', interface=IInt, value=1)
        self.add_input(name='col', interface=IInt, value=1)
        self.add_input(name='num', interface=IInt, value=1)
        self.add_input(name='polar', interface=IBool, value=False)
        self.add_output(name='test')

    def __call__(self, inputs):
        #from pylab import subplot
        row = self.get_input('row')
        col = self.get_input('col')
        num = self.get_input('num')
        kwds = {}
        kwds['polar'] = self.get_input('polar')
        #subplot(row, col, num)

        return (row, col, num, kwds)
