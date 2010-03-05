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
    ISequence, IEnumStr, IStr, IDirStr

colors = {
    'blue':'b',
    'green':'g',
    'red':'r',
    'cyan':'c',
    'magenta':'m',
    'yellow':'y',
    'black':'k',
    'white':'w',}

markers = {
    'point marker':'.',
    'pixel marker':',',
    'circle marker':'o',
    'triangle_down marker':'v',
    'triangle_up marker':'^',
    'triangle_left marker':'<',
    'triangle_right marker':'>',
    'tri_down marker':'1',
    'tri_up marker':'2',
    'tri_left marker':'3',
    'tri_right marker':'4',
    'square marker':'s',
    'pentagon marker':'p',
    'star marker':'*',
    'hexagon1 marker':'h',
    'hexagon2 marker':'H',
    'plus marker':'+',
    'x marker':'x',
    'diamond marker':'D',
    'thin_diamond marker':'d',
    'vline marker':'|',
    'hline marker':'_'}

linestyles = {
    'None':'',
    'solid line style':'-',
    'dashed line style':'--',
    'dash-dot line style': '-.',
    'dotted line style':':'
    }


#//////////////////////////////////////////////////////////////////////////////
class PyLabPlot(Node):
    """pylab.plot interface

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
        #self.__doc__+=plot.__doc__

        self.add_input(name="x")
        self.add_input(name="y", value=None)
        self.add_input(name="label", interface = IStr, value=None)
        self.add_input(name="marker", interface = IEnumStr(markers.keys()),
            value = 'circle marker')
        self.add_input(name="markersize", interface = IFloat, value = 10)
        self.add_input(name="linestyle", interface = IEnumStr(linestyles.keys()),
            value = 'solid line style')
        self.add_input(name="color", interface = IEnumStr(colors.keys()),
            value='blue')
        self.add_input(name="xlabel", interface = IStr, value = "")
        self.add_input(name="ylabel", interface = IStr, value = "")
        self.add_input(name="title", interface = IStr, value = "")
        self.add_input(name="grid", interface = IBool, value = True)
        self.add_output(name="figure")

    def __call__(self, inputs):
        x = self.get_input("x")
        ys = self.get_input("y")
        from pylab import plot, show, clf, xlabel, ylabel, hold, title, grid
        clf()
        if ys is not None:
            fig = plot(x,ys,
                    markersize=self.get_input("markersize"),
                    marker=markers[self.get_input("marker")],
                    linestyle=linestyles[self.get_input("linestyle")],
                    color=colors[self.get_input("color")],
                    label=self.get_input("label"))
        else:
            fig = plot(x,
                markersize=self.get_input("markersize"),
                marker=markers[self.get_input("marker")],
                linestyle=linestyles[self.get_input("linestyle")],
                color=colors[self.get_input("color")],
                label=self.get_input("label"))

        xlabel(self.get_input("xlabel"))
        ylabel(self.get_input("ylabel"))
        title(self.get_input("title"))
        grid(self.get_input("grid"))
        show()
        return (fig,)



class PyLabHist(Node):
    """pylab.hist interface

    :param x: input data
    :param bins: binning number (default is 10)
    :param facecolor: blue by default
    :param normed:
    :param log:
    :param histtype:
    :param orientation:
    :param align:

    :param xlabel: none by default
    :param ylabel: none by default
    :param title: none by default

    .. todo::

        range=None
        bottom=None,
        rwidth=None,

    :authors: Thomas Cokelaer
    """

    def __init__(self):
        from pylab import hist
        Node.__init__(self)
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
        self.add_input(name="xlabel", interface = IStr, value = "")
        self.add_input(name="ylabel", interface = IStr, value = "")
        self.add_input(name="title", interface = IStr, value = "")
        self.add_input(name="grid", interface = IBool, value = True)
        self.add_input(name="normed", interface = IBool, value = False)
        self.add_input(name="log", interface = IBool, value = False)
        self.add_input(name="facecolor", interface = IEnumStr(colors.keys()), value = 'blue')
        self.add_input(name="histtype", interface = IEnumStr(self.histtype.keys()), value='bar')
        self.add_input(name="orientation", interface = IEnumStr(self.orientation.keys()), value='vertical')
        self.add_input(name="align", interface = IEnumStr(self.align.keys()), value='mid')
        #self.add_input(name="kwargs", interface = IStr, value='')
        self.add_input(name="cumulative", interface = IBool, value=False)
        self.add_output(name="figure")

    def __call__(self, inputs):
        from pylab import show, clf, xlabel, ylabel, hold, title, grid, hist
        clf()
        x = self.get_input("x")
        try:
            fig = hist(x,
                bins=self.get_input("bins"),
                normed=self.get_input("normed"),
                facecolor=colors[self.get_input("facecolor")],
                log=self.get_input("log"),
                orientation=self.get_input("orientation"),
                histtype=self.get_input("histtype"),
                align=self.get_input("align"),
                cumulative=self.get_input("cumulative"),
                #**self.get_input("kwargs")
                )
        except ValueError,e:
            print e

        xlabel(self.get_input("xlabel"))
        ylabel(self.get_input("ylabel"))
        title(self.get_input("title"))
        grid(self.get_input("grid"))
        show()
        return (fig,)

 #range=None   bottom=None,    rwidth=None,



class PyLabAcorr(Node):
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
        #self.__doc__+=hist.__doc__

        # acorr options
        self.add_input(name="x")
        self.add_input(name="maxlags", interface = IInt, value=10)
        self.add_input(name="normed", interface = IBool, value = False)
        self.add_input(name="usevlines", interface = IBool, value = True)

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

        xlabel(self.get_input("xlabel"))
        ylabel(self.get_input("ylabel"))
        title(self.get_input("title"))
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



class PyLabScatter(Node):
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
        #self.__doc__+=plot.__doc__

        self.add_input(name="x")
        self.add_input(name="y", value=None)
        self.add_input(name="sizes", value=20)
        self.add_input(name="colors", value='r')

        self.add_input(name="label", interface = IStr, value=None)
        self.add_input(name="marker", interface = IEnumStr(markers.keys()),
            value = 'circle marker')
        self.add_input(name="color", interface = IEnumStr(colors.keys()),
            value='blue')


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

        xlabel(self.get_input("xlabel"))
        ylabel(self.get_input("ylabel"))
        title(self.get_input("title"))
        grid(self.get_input("grid"))
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
        self.add_input(name="sym", interface = IEnumStr(markers.keys()),
            value = 'plus marker')
        self.add_input(name="vert", interface = IInt,  value = 1)

        self.add_input(name="xlabel", interface = IStr, value = "")
        self.add_input(name="ylabel", interface = IStr, value = "")
        self.add_input(name="title", interface = IStr, value = "")
        self.add_input(name="grid", interface = IBool, value = True)

        self.add_output(name="figure")

    def __call__(self, inputs):
        x = self.get_input("x")
        from pylab import boxplot ,show, clf, xlabel, ylabel, hold, title, grid
        clf()
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



