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


family = {
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


cmaps=['autumn','bone', 'cool','copper','flag','gray','hot','hsv','jet','pink', 'prism', 'spring', 'summer', 'winter'] 

locations={'best' : 0, 
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





def get_kwds_from_line2d(line2d, kwds={}):
    """create a dict from line2d properties
    """
    kwds['color']=line2d.get_color()
    kwds['linestyle']=line2d.get_linestyle()
    kwds['markersize']=line2d.get_markersize()
    kwds['linewidth']=line2d.get_linewidth()
    kwds['marker']=line2d.get_marker()
    kwds['label']=line2d.get_label()
    kwds['alpha']=line2d.get_alpha()
    return kwds

class Title():
    def __init__(self):
        pass

    def title(self, data):
        from pylab import title
        if type(data)==str:
            title(data)
        else:
            try:
                args = data[0]
                kwargs = data[1]
                title(args, **kwargs)
            except:
                print data
                print 'could not convert data into args=data[0], kwargs=data[1]'
                pass

class XLabel():
    def __init__(self):
        pass

    def xlabel(self, data):
        from pylab import xlabel
        if type(data) == str:
            xlabel(data)
        else:
            try:
                args = data[0]
                kwargs = data[1]
                xlabel(args, **kwargs)
            except:
                print data
                print 'could not convert data into args=data[0], kwargs=data[1]'
                pass

class YLabel():
    def __init__(self):
        pass

    def ylabel(self, data):
        from pylab import ylabel
        if type(data) == str:
            ylabel(data)
        else:
            try:
                args = data[0]
                kwargs = data[1]
                ylabel(args, **kwargs)
            except:
                print data
                print 'could not convert data into args=data[0], kwargs=data[1]'
                pass

class Plotting(Node):
    def __init__(self,  inputs):
        Node.__init__(self)
        self._show = True
        self._figure = 1
        self._title = None
        self._ylabel = None
        self._xlabel = None

        for input in inputs:
            self.add_input(**input)

        self.add_input(name="show", interface=IBool, value=True)
        self.add_input(name="xlabel", interface=IStr, value="")
        self.add_input(name="ylabel", interface=IStr, value = "")
        self.add_input(name="title", interface=IStr, value = "")

    def show(self):
        from pylab import show
        if self._show is True:
            show()

    def figure(self):
        from pylab import figure
        figure(self._figure)

    def title(self):
        from pylab import title
        title(self._title)
    
    def xlabel(self):
        from pylab import xlabel
        xlabel(self._xlabel)
    
    def ylabel(self):
        from pylab import ylabel
        ylabel(self._ylabel)
    
    def properties(self):
        self.title()
        self.xlabel()
        self.ylabel()
        self.figure()
        self.show()

class PyLabLogLog(Plotting):

    def __init__(self):
        inputs = [
                    {'name':'x', 'interface':None, 'value':None},
                    {'name':'y', 'interface':None, 'value':None}
        ]
        Plotting.__init__(self, inputs)

    def __call__(self, inputs):
        from pylab import loglog, clf, show, figure,plot
        clf()
        plot(self.get_input('x'), self.get_input('y'))
        self.properties()
        self.title()
        self.xlabel()
        self.ylabel()
        self.figure()
        self.show()


class Labels():
    def __init__(self):
        self.add_input(name="xlabel")
        self.add_input(name="ylabel")
        self.add_input(name="title")
        self.add_input(name="subtitle")


#//////////////////////////////////////////////////////////////////////////////
class PyLabPlot(Node, XLabel, YLabel, Title):
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
        from pylab import plot
        Node.__init__(self)
        YLabel.__init__(self)
        XLabel.__init__(self)
        Title.__init__(self)
        #self.__doc__+=plot.__doc__

        #plot format options
        self.add_input(name="x")
        self.add_input(name="y", value=None)
        self.add_input(name="label",        interface=IStr, value=None)
        self.add_input(name="marker",       interface=IEnumStr(markers.keys()), value='circle')
        self.add_input(name="markersize",   interface=IFloat, value=10)
        self.add_input(name="linestyle",    interface=IEnumStr(linestyles.keys()), value='solid')
        self.add_input(name="color",        interface=IEnumStr(colors.keys()), value='blue')
        #self.add_input(name="axes")

        # standard figure options
        self.add_input(name="xlabel",       interface=IStr, value="")
        self.add_input(name="ylabel",       interface=IStr, value = "")
        self.add_input(name="title",        interface=IStr, value = "")
        self.add_input(name="grid",         interface=IBool, value = True)
        self.add_input(name="legend",       interface=IDict, value={'legend on':True})
        self.add_input(name="show",         interface=IBool, value=True)
        self.add_input(name="figure",       interface=IDict, value={"num":1})
        self.add_input(name="axes",         interface=IDict, value={})

        self.add_output(name='output')

    def __call__(self, inputs):
        from pylab import figure, plot, show, clf, xlabel, ylabel, hold, title, grid, Line2D, legend, axes
        xinputs = self.get_input("x")
        yinputs = self.get_input("y")
        
        clf()
        #figure(**self.get_input('figure'))
        kwds = {}
        kwds['markersize']=self.get_input("markersize")
        kwds['marker']=markers[self.get_input("marker")]
        kwds['linestyle']=linestyles[self.get_input("linestyle")]
        kwds['color']=colors[self.get_input("color")]
        kwds['label']=self.get_input("label")
        print self.get_input("axes")
        fig = figure(**self.get_input("figure"))
        axes(**self.get_input("axes"))
        print kwds
        #kwds['axes']=self.get_input("axes")
        #print self.get_input("axes")

        if xinputs == None:
            raise ValueError('x not set. connect a line2D or array or list')

        # case of an x input without y input. line2D are all manage in this if statement
        if yinputs is None:
            #convert input data to list
            if type(xinputs)!=list:
                xinputs = [xinputs]

            #plot(line2D) and plot([line2D, line2D])
            if type(xinputs[0])==Line2D:
                for x in xinputs:
                    print x
                    line2dkwds = get_kwds_from_line2d(x, kwds)
                    print line2dkwds
                    plot(x.get_xdata(), x.get_ydata(),**line2dkwds)
                    hold(True)
            #plot([x1,None,x2,None, ...) and plot(x1)
            else:
                print 'plot(x), plot([x1,x2,x3])'
                c = enumerate(colors)
                for x in xinputs:
                    try:
                        color = c.next()
                        kwds['color']=color[1]
                    except:
                        print 'no more colors'
                    print kwds
                    plot(x, **kwds)
                    hold(True)

        else:
            #convert input data to list
            if type(yinputs)!=list:
                yinputs = [yinputs]

            if type(xinputs)!=list:
                xinputs = [xinputs]

            if len(xinputs)==1:
                print 'plot(x,y) and plot(x, [y1,y2])'
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
                print 'plot([x1,x2], [y1,y2])'
                # plot([x1,x2], [y1,y2])
                # plot([x1], [y1])
                for x,y in zip(xinputs, yinputs):
                   plot(x, y, **kwds)
                   hold(True)

        print self.get_input("legend").keys()
        if self.get_input("legend")['legend on']==True:
            #does this copy is needed?
            mykwds = self.get_input("legend")
            del mykwds['legend on']
            legend(**mykwds)

        self.ylabel(self.get_input("ylabel"))
        self.xlabel(self.get_input("xlabel"))
        self.title(self.get_input("title"))
        grid(self.get_input("grid"))
        if self.get_input("show") is True:
            show()
        
        return (fig, )

class PyLabHist(Node, YLabel, XLabel, Title):
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
        Node.__init__(self)
        YLabel.__init__(self)
        XLabel.__init__(self)
        Title.__init__(self)
        #self.__doc__+=hist.__doc__

        self.histtype = {
                'bar':'bar',
                'barstacked':'barstacked',
                'step' :'step',
                'stepfilled':'stepfilled'}
        self.orientation = {'horizontal':'horizontal', 'vertical':'vertical'}
        self.align = {'mid':'mid', 'right':'right', 'left':'left'}

        self.add_input(name="x")
        self.add_input(name="bins", interface = IInt, value=10)
        self.add_input(name="facecolor", interface = IEnumStr(colors.keys()), value = 'blue')
        #self.add_input(name="range", interface = ITuple3, value = None)
        self.add_input(name="normed", interface = IBool, value = False)
        self.add_input(name="cumulative", interface = IBool, value=False)
        self.add_input(name="histtype", interface = IEnumStr(self.histtype.keys()), value='bar')
        self.add_input(name="align", interface = IEnumStr(self.align.keys()), value='mid')
        self.add_input(name="orientation", interface = IEnumStr(self.orientation.keys()), value='vertical')
        self.add_input(name="log", interface = IBool, value = False)
        self.add_input(name="grid", interface = IBool, value = True)
        self.add_input(name="figure", interface=IInt, value=1)

        self.add_input(name="xlabel", interface = IStr, value = "")
        self.add_input(name="ylabel", interface = IStr, value = "")
        self.add_input(name="title", interface = IStr, value = "")
        self.add_input(name="show", interface = IBool, value = True)

        self.add_input(name="kwargs", interface = IDict, value={'alpha':1., 'animated':False})
        

        self.add_output(name="counts")
        self.add_output(name="position")
        """
          antialiased or aa: [True | False]  or None for default         
          axes: an :class:`~matplotlib.axes.Axes` instance         
          clip_box: a :class:`matplotlib.transforms.Bbox` instance         
          clip_on: [True | False]         
          clip_path: [ (:class:`~matplotlib.path.Path`,         :class:`~matplotlib.transforms.Transform`) |         :class:`~matplotlib.patches.Patch` | None ]         
          color: matplotlib color arg or sequence of rgba tuples
          contains: a callable function         
          edgecolor or ec: mpl color spec, or None for default, or 'none' for no color         
          facecolor or fc: mpl color spec, or None for default, or 'none' for no color         
          figure: a :class:`matplotlib.figure.Figure` instance         
          fill: [True | False]         
          gid: an id string         
          hatch: [ '/' | '\\' | '|' | '-' | '+' | 'x' | 'o' | 'O' | '.' | '*' ]         
          label: any string         
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
        from pylab import show, clf, xlabel, ylabel, hold, title, grid, hist, figure
        clf()
        figure(self.get_input('figure'))
        kwds={}
        print self.get_input('kwargs')
        #!! facecolor is alrady in the Hist node, so override it if available in kwargs dict
        kwds['facecolor'] = self.get_input('facecolor')
        for key,value in self.get_input('kwargs').iteritems():
            kwds[key] = value

        try:
            res = hist(self.get_input('x'),
                bins=self.get_input("bins"),
                normed=self.get_input("normed"),
                #range=self.get_input("range"),
                log=self.get_input("log"),
                orientation=self.get_input("orientation"),
                figure=self.get_input("figure"),
                histtype=self.get_input("histtype"),
                align=self.get_input("align"),
                cumulative=self.get_input("cumulative"),
                **kwds)
        except ValueError, e:
            res = (None, None)
            print e
            raise ValueError('tttt')

        self.ylabel(self.get_input("ylabel"))
        self.xlabel(self.get_input("xlabel"))
        self.title(self.get_input("title"))

        grid(self.get_input("grid"))
        if self.get_input('show'):
            show()

        return (res[0],res[1])
 #range=None   bottom=None,    rwidth=None,


class PyLabAcorr(Node, Title, XLabel, YLabel):
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
        from pylab import hist
        Node.__init__(self)
        XLabel.__init__(self)
        YLabel.__init__(self)
        Title.__init__(self)
        #self.__doc__+=hist.__doc__

        # acorr options
        self.add_input(name="x")
        self.add_input(name="maxlags", interface = IInt, value=10)
        self.add_input(name="normed", interface = IBool, value = False)
        self.add_input(name="usevlines", interface = IBool, value = True)
        self.add_input(name="kwargs", interface = IDict, value = {})

        # general options
        self.add_input(name="xlabel", interface = IStr, value = "")
        self.add_input(name="ylabel", interface = IStr, value = "")
        self.add_input(name="title", interface = IStr, value = "")
        self.add_input(name="grid", interface = IBool, value = True)

        # output
        self.add_output(name="figure")

    def __call__(self, inputs):
        from pylab import show, clf, xlabel, ylabel, hold, title, grid, acorr
        clf()
        x = self.get_input("x")
        try:
            
            fig = acorr(x,
                maxlags=self.get_input("maxlags"),
                normed=self.get_input("normed"),
                usevlines=self.get_input("usevlines"),
                )
        except ValueError,e:
            print e

        self.xlabel(self.get_input("xlabel"))
        self.ylabel(self.get_input("ylabel"))
        self.title(self.get_input("title"))
        grid(self.get_input("grid"))
        show()
        return (fig,)



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



class PyLabScatter(Node, YLabel, XLabel, Title):
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
        """init docstring"""
        from pylab import plot
        Node.__init__(self)
        XLabel.__init__(self)
        YLabel.__init__(self)
        Title.__init__(self)
        #self.__doc__+=plot.__doc__

        self.add_input(name="x")
        self.add_input(name="y", value=None)
        self.add_input(name="sizes", value=20)
        self.add_input(name="colors", value='r')

        self.add_input(name="label", interface = IStr, value=None)
        self.add_input(name="marker", interface = IEnumStr(markers.keys()), value = 'circle')
        self.add_input(name="color", interface = IEnumStr(colors.keys()),  value='blue')


        self.add_input(name="xlabel", interface = IStr, value = "")
        self.add_input(name="ylabel", interface = IStr, value = "")
        self.add_input(name="title", interface = IStr, value = "")
        
        self.add_input(name="grid", interface = IBool, value = True)
        self.add_input(name="alpha", interface = IFloat, value = 0.5)

        self.add_output(name="figure")

    def __call__(self, inputs):
        x = self.get_input("x")
        y = self.get_input("y")
        sizes = self.get_input("sizes")
        colors = self.get_input("colors")
        from pylab import scatter ,show, clf, xlabel, ylabel, hold, title, grid
        clf()
        fig = scatter(x,y, s=sizes,c=colors,
                marker=markers[self.get_input("marker")],
                alpha=self.get_input("alpha"),
                label=self.get_input("label"))

        grid(self.get_input("grid"))
        self.ylabel(self.get_input("ylabel"))
        self.xlabel(self.get_input("xlabel"))
        self.title(self.get_input("title"))
        show()
        return (fig,)




class PyLabBoxPlot(Node):
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
        from pylab import plot
        Node.__init__(self)
        #self.__doc__+=plot.__doc__

        self.add_input(name="x")
        self.add_input(name="notch", interface=IInt, value=0)
        self.add_input(name="sym", interface = IEnumStr(markers.keys()), value='circle')
        self.add_input(name="vert", interface = IInt,  value = 1)

        self.add_input(name="xlabel", interface = IStr, value = "")
        self.add_input(name="ylabel", interface = IStr, value = "")
        self.add_input(name="title", interface = IStr, value = "")
        self.add_input(name="grid", interface = IBool, value = True)
        self.add_input(name="figure", interface=IInt, value=1)

        self.add_output(name="figure")

    def __call__(self, inputs):
        x = self.get_input("x")
        from pylab import boxplot ,show, clf, xlabel, ylabel, hold, title, grid, figure
        clf()
        figure(self.get_input('figure'))
        fig = boxplot(x, 
                sym=markers[self.get_input("sym")],
                vert=self.get_input("vert"),
                notch=self.get_input("notch"))

        xlabel(self.get_input("xlabel"))
        ylabel(self.get_input("ylabel"))
        title(self.get_input("title"))
        grid(self.get_input("grid"))
        show()
        return (fig,)


class PyLabLegend(Node):
    """to be done"""
    location = {'best':0,
                'upper right': 1, 
                'upper left': 2,
                'lower left': 3,
                'lower right': 4,
                'right': 5,
                'center left': 6,
                'center right': 7,
                'lower center': 8,
                'upper center': 9,
                'center': 10}

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
        self.add_input(name="properties to be done", interface=IDict, value=None)
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
        self.add_input(name="linewidth", interface=IFloat, value=1.)
        self.add_input(name="label", interface=IStr, value=None)
        self.add_input(name="alpha", interface=IFloat(0.,1., step=0.1), value=1.0)

        self.add_output(name="line2d")

    def __call__(self, inputs):
        from pylab import Line2D
        xdata=self.get_input('xdata'),
        ydata=self.get_input('ydata'),
        if ydata is None:
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
            linewidth=self.get_input('linewidth'),
            alpha=self.get_input('alpha'),
        )
        return (output, )

"""
markeredgewidth=None,
markeredgecolor=None, 
markerfacecolor=None, 
fillstyle='full', 
antialiased=None, 
dash_capstyle=None,
solid_capstyle=None, 
dash_joinstyle=None,
solid_joinstyle=None,
pickradius=5,
drawstyle=None,
 markevery=None,
**kwargs)

 alpha: float (0.0 transparent through 1.0 opaque)         
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
      fillstyle: ['full' | 'left' | 'right' | 'bottom' | 'top']         
      gid: an id string         
      linewidth or lw: float value in points         
      lod: [True | False]         
      markeredgecolor or mec: any matplotlib color         
      markeredgewidth or mew: float value in points         
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
      xdata: 1D array         
      ydata: 1D array         
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
        self.add_output(name='axes')
        self.add_output(name='kwds', interface=IDict, value={})

    def __call__(self, inputs):
        from pylab import axes
        kwds = {}
        kwds['axisbg'] = self.get_input('axisbg')
        kwds['frameon'] = self.get_input('frameon')
        kwds['polar'] = self.get_input('polar')
        aa = axes(**kwds)
        return aa, kwds




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



class PyLabPie(Node, Title, XLabel, YLabel):

    def __init__(self):
        Node.__init__(self)
        Title.__init__(self)
        XLabel.__init__(self)
        YLabel.__init__(self)
        self.add_input(name="x")
        self.add_input(name="explode", interface=ISequence, value=None)
        self.add_input(name="colors", interface=IStr, value=None)
        self.add_input(name="labels", interface=ISequence, value=None)
        self.add_input(name="pctdistance", interface=IFloat, value=0.6)
        self.add_input(name="labeldistance", interface=IFloat, value=1.1)
        self.add_input(name="shadow", interface=IBool, value=False)
        self.add_input(name="hold", interface=IBool, value=False)
        self.add_input(name="autopct", interface=IStr, value=None)
        self.add_input(name="figure", interface=IInt, value=1)
        self.add_input(name="show", interface=IBool, value=True)
        self.add_input(name="xlabel", interface = IStr, value = "")
        self.add_input(name="ylabel", interface = IStr, value = "")
        self.add_input(name="title", interface = IStr, value = "")
        self.add_output(name="figure")

    def __call__(self, inputs):
        from pylab import pie, show, clf, figure
        figure(self.get_input('figure'))
        clf()
        kwds = {}
        kwds['explode'] = self.get_input('explode')
        kwds['colors'] = self.get_input('colors')
        kwds['labels'] = self.get_input('labels')
        kwds['pctdistance'] = self.get_input('pctdistance')
        kwds['labeldistance'] = self.get_input('labeldistance')
        kwds['shadow'] = self.get_input('shadow')
        kwds['hold'] = self.get_input('hold')
        kwds['autopct'] = self.get_input('autopct')

        fig = pie(self.get_input('x'), **kwds)

        self.ylabel(self.get_input("ylabel"))
        self.xlabel(self.get_input("xlabel"))
        self.title(self.get_input("title"))

        if self.get_input('show'):
            show()

        return (fig,)


class PyLabShow(Node):

    def __init__(self):
        Node.__init__(self)
        self.add_input(name="all", interface=IDict())

    def __call__(self, inputs):
        from pylab import show, hold
        show()







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

        xlabel(self.get_input('text'), **kwargs)

        return (self.get_input('text'), kwargs, )

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

        ylabel(self.get_input('text'), **kwargs)

        return (self.get_input('text'), kwargs, )


class PyLabTitle(Node):

    def __init__(self):
        Node.__init__(self)
        self.add_input(name="text", interface=IStr, value=None)
        self.add_input(name="fontsize", interface=IFloat, value=12)
        self.add_input(name="color", interface=IEnumStr(colors.keys()), value='black')
        self.add_input(name='kwargs', interface=IDict, value={})

        self.add_output(name='output', interface=IDict, value={})

    def __call__(self, inputs):
        from pylab import title

        kwargs = {}
        kwargs['fontsize'] = self.get_input('fontsize')
        kwargs['color'] = self.get_input('color')
        if 'text' in kwargs.keys():
            self.set_input('text', kwargs['text'], notify=True)
        print self.get_input('kwargs')
        for key, value in self.get_input('kwargs').iteritems():
            kwargs[key]=value

        title(self.get_input('text'), **kwargs)

        return (self.get_input('text'), kwargs)






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






class PyLabBar(Node):

    def __init__(self):
        Node.__init__(self)
        self.add_input(name="height",  value=None)
        self.add_input(name="position",value=None)
        self.add_input(name="show", interface=IBool, value=True)
        self.add_input(name="figure", interface=IInt, value=1)


    def __call__(self, inputs):
        from pylab import bar, hold, show, figure,clf
        figure(self.get_input('figure'))
        clf()
        height = self.get_input('height')
        position = self.get_input('position')

        print position
        print type(position)
        print type(position[0])
        print height

        if type(position[0])==float:
            print 'a'
            width = position[1] - position[0]
            print width
            bar(position[1:], height, width=width)
        else:
            print 'b'
            c = enumerate(colors)
            for x,y in zip(position, height):
                color = c.next()
                print color
                print x
                print y
                #width = x[1]-x[0]
                width=0.1
                bar(x[1:],y, width=width, color=color[1], alpha=0.5)
                hold(True)

        if self.get_input('show') is True:
            show()
