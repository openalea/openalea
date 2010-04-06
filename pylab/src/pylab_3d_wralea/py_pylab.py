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
    'None':'None'
    }


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





def get_kwds_from_line2d(line2d, input_kwds={}, type=None):
    """create a dict from line2d properties
    """
    import copy
    kwds = copy.deepcopy(input_kwds)
    if type=='stem':
        return input_kwds
    
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
        del kwds['color']
        del kwds['linestyle']
        del kwds['marker']
        del kwds['markersize']
        del kwds['markeredgewidth']
        del kwds['markersize']
        del kwds['fillstyle']
        del kwds['markeredgecolor']

    if type in ['csd', 'psd', 'step']:
        del kwds['facecolor']

    if type=='specgram':
        del kwds['facecolor']
        del kwds['color']
        del kwds['linewidth']
        del kwds['linestyle']
        del kwds['marker']
        del kwds['markersize']
        del kwds['markeredgewidth']
        del kwds['fillstyle']
        del kwds['markeredgecolor']

    if type=='plot':
        del kwds['facecolor']

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
        if self.colorbar_called == True:
            return
        if type(self.get_input('colorbar'))==bool:
            if self.get_input('colorbar')==True:
                colorbar()
                self.corlorbar_called=True
                self.set_input('colorbar', False)
        else:
            kwds = self.get_input('colorbar')
            colorbar(**kwds)
            self.colorbar_called=True

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
        self.set_input('colorbar', False)
        self.show()



class PlotxyInterface():
    ERROR_NOXDATA = 'No data connected to the x connector. Connect a line2D, an array or a list of line2Ds or arrays'
    ERROR_FAILURE = 'Failed to generate the image. check your entries.'

    def __init__(self):
        pass

    def call(self, plottype, kwds):
        from pylab import hold
        if plottype=='plot':
            from pylab import plot as plot
        elif plottype=='loglog':
            from pylab import loglog as plot
        elif plottype=='semilogx':
            from pylab import semilogx as plot
        elif plottype=='semilogy':
            from pylab import semilogy as plot
        elif plottype=='csd':
            from pylab import csd as plot
        elif plottype=='psd':
            from pylab import psd as plot
        elif plottype=='specgram':
            from pylab import specgram as plot
        elif plottype=='stem':
            from pylab import stem as plot
        elif plottype=='step':
            from pylab import step as plot
        elif plottype=='fill':
            from pylab import fill as plot

        xinputs = self.get_input("x")
        yinputs = self.get_input("y")

        # convert x and y inputs into lists
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
                    print kwds
                    line2dkwds = get_kwds_from_line2d(x, kwds, type=plottype)
                    print line2dkwds
                    #returns the processed data ?
                    if plottype in ['specgram', 'psd']:
                        plot(x.get_ydata(orig=False), **line2dkwds)
                    else:
                        try:
                            plot(x.get_xdata(orig=False), x.get_ydata(orig=False), **line2dkwds)
                        except:
                            print kwds
                            print line2dkwds
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
        pass



class PyLabPlot3D(Plotting):

    def __init__(self):
        """init docstring"""
        inputs = [
                    {'name':'x',            'interface':None,                           'value':None},
                    {'name':'y',            'interface':None,                           'value':None},
                    {'name':'z',            'interface':None,                           'value':None},
                    {'name':'marker',       'interface':IEnumStr(markers.keys()),       'value':'circle'},
                    {'name':'markersize',   'interface':IFloat,                         'value':10},
                    {'name':'linestyle',    'interface':IEnumStr(linestyles.keys()),    'value':'solid'},
                    {'name':'color',        'interface':IEnumStr(colors.keys()),        'value':'blue'},
        ]
        Plotting.__init__(self, inputs)

    def __call__(self, inputs):
        from pylab import cla,plot
        from mpl_toolkits.mplot3d import Axes3D

        #first, we select the figure, we use subplot() that may be overwritten by axes()
        self.figure()
        self.axes()
        ax = Axes3D(self.fig)
        cla()
        kwds = {}
        kwds['markersize']=self.get_input("markersize")
        kwds['marker']=markers[self.get_input("marker")]
        kwds['linestyle']=linestyles[self.get_input("linestyle")]
        kwds['color']=colors[self.get_input("color")]
        x = self.get_input('x')
        y = self.get_input('y')
        z = self.get_input('z')
        plot(x,y,z, **kwds)

        self.properties()
        return ax

