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

__doc__="""pylab nodes related to drawings in a pylab.axes"""
__license__= "Cecill-C"
__revision__=" $Id$ "


from openalea.core import Node
from openalea.core import Factory, IFileStr, IInt, IBool, IFloat, \
    ISequence, IEnumStr, IStr, IDirStr, ITuple3, IDict, ITuple

import pylab
from openalea.pylab import tools
from openalea.pylab.tools import CustomizeAxes


class PyLabFancyArrowDict(Node):
    """Create a dictionary to store arrow key/value pairs.

    This is then passed to an :class:`~openalea.pylab_drawing_wralea.py_pylab.PyLabAnnotate` node.

    :param str arrowstyle:
    :param str connectionstyle: default is 'arc3'
    :param tuple relpos: default is (0.5,0.5)
    :param dict patchA: default is None
    :param dict patchB: default is None
    :param dict shrinkA: default is None
    :param dict shrinkB: default is None
    :param float mutation_scale: default is 1
    :param float mutation_aspect: default is 1
    :param dict pathPatch: default is None
    :param ec: to be done. is it the style?
    :param dict kwargs: default is {}

    :return: a dictionary containing the arrow properties

    .. seealso:: :class:`~openalea.pylab_drawing_wralea.py_pylab.PyLabAnnotate` for a dataflow example.
    """

    def __init__(self):
        Node.__init__(self)

        #self.get_input('axes')

        self.add_input(name='arrowstyle', interface=IEnumStr(tools.arrowstyles.keys()), value='simple')
        self.add_input(name='connectionstyle', interface=IEnumStr(tools.connectionstyles.keys()), value='arc3')
        self.add_input(name='relpos', interface=ITuple, value=(0.5,0.5))
        self.add_input(name='patchA', interface=IDict, value=None)
        self.add_input(name='patchB', interface=IDict, value=None)
        self.add_input(name='shrinkA', interface=IDict, value=None)
        self.add_input(name='shrinkB', interface=IDict, value=None)
        self.add_input(name='mutation_scale', interface=IFloat, value=1)
        self.add_input(name='mutation_aspect', interface=IFloat, value=1)
        self.add_input(name='pathPatch', interface=IDict, value=None)
        self.add_input(name='ec', interface=IEnumStr(tools.linestyles.keys()), value='solid')
        self.add_input(name='kwargs', interface=IDict, value={})
        #todo for connection style, connectionstyle="angle,angleA=0,angleB=-90,rad=10"
        #todo for arrowstyle:head_length=0.4,head_width=0.2 tail_width=0.3,shrink_factor=0.5
        self.add_output(name='dict', interface=IDict, value={})

    def __call__(self, inputs):

        kwds = {}
        kwds['arrowstyle'] = self.get_input('arrowstyle')
        kwds['relpos'] = self.get_input('relpos')
        kwds['connectionstyle'] = self.get_input('connectionstyle')
        kwds['mutation_scale'] = self.get_input('mutation_scale')
        kwds['patchA'] = self.get_input('patchA')
        kwds['patchB'] = self.get_input('patchB')
        kwds['mutation_scale'] = self.get_input('mutation_scale')
        kwds['mutation_aspect'] = self.get_input('mutation_aspect')
        #kwds['ec'] = tools.linestyles[self.get_input('ec')]
        for key, value in self.get_input('kwargs').iteritems():
            kwds[key] = value

        print kwds

        return (kwds,)

class PyLabYAArowDict(Node):
    """Create a dictionary to store yaarow key/value pairs.

    This is then passed to an :class:`~openalea.pylab_drawing_wralea.py_pylab.PyLabAnnotate` node.

    :param float width:
    :param float headwidth:
    :param float frac:
    :param float alpha:
    :param str color:
    :param dict kwargs:

    :return: a dictionary containing the arrow properties

    .. seealso:: :class:`~openalea.pylab_drawing_wralea.py_pylab.PyLabAnnotate` for a dataflow example.

    .. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    """
    # do not call the class but use its args and kwrags for others like BBox
    def __init__(self):
        Node.__init__(self)
        self.add_input(name='width', interface=IFloat(0,100,0.1), value=4)
        #figure, xytip and xybase are not needed
        self.add_input(name='headwidth', interface=IFloat(0,100,0.1), value=12)
        self.add_input(name='frac', interface=IFloat(0,1,0.05), value=0.1)
        self.add_input(name='alpha', interface=IFloat(0,1,0.05), value=1)
        self.add_input(name='color', interface=IEnumStr(tools.colors.keys()), value='blue')
        self.add_input(name='kwargs', interface=IDict, value={})
        self.add_output(name='output', interface=IDict, value = {})

    def __call__(self, inputs):
        kwds = {}
        kwds['width']= self.get_input('width')
        kwds['headwidth']= self.get_input('headwidth')
        kwds['frac']= self.get_input('frac')
        kwds['alpha']= self.get_input('alpha')
        kwds['color']= self.get_input('color')
        return kwds

class PyLabBBox(Node):
    """Create a dictionary to store bbox key/value pairs.

    This is then passed to an :class:`~openalea.pylab_drawing_wralea.py_pylab.PyLabAnnotate` node.

    :param str boxstyle:
    :param float fc:
    :param float pad:

    :return: a dictionary containing the *boxstyle*, *fc* and *pad* keys

    .. seealso:: :class:`~openalea.pylab_drawing_wralea.py_pylab.PyLabAnnotate` for a dataflow example.

    .. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    """

    def __init__(self):
        Node.__init__(self)

        self.add_input(name='boxstyle',interface=IEnumStr(tools.boxstyles.keys()), value='round')
        self.add_input(name='fc',interface=IFloat(0,1,0.1), value=0.8)
        self.add_input(name='pad',interface=IFloat(0,1,0.1), value=0.3)
        self.add_output(name='output', interface=IDict)
        #todo: ec
    def __call__(self, inputs):
        #from pylab import bbox
        kwds = {}
        kwds['boxstyle'] = self.get_input('boxstyle') + ',pad='+str(self.get_input('pad'))
        kwds['fc'] = str(self.get_input('fc'))
        return kwds

class PyLabAnnotate(Node):
    """Annotate the *x*, *y* point *xy* with text. See pylab.annotate for details

    If the dictionary has a key *arrowstyle*, a FancyArrowDict
    instance is created with the given dictionary and is
    drawn. Otherwise, a YAArow patch instance is created and
    drawn. Valid keys for YAArow are

    :param axes: an optional axes where new data will be plotted.
    :param text: the text to add in the axe
    :param tuple xy: a tuple to set the xy coordinates of the arrow's head
    :param tuple xytext: a tuple to set the xy coordinates of the text
    :param str xycoords: type of coordinates used to place xy tuple
    :param str xytext: type of coordinates used to place xytext tuple
    :param dict arrowprops: could be a PyLabYAArrow or PyLabFancyArrowDict dictionary.
    :param dict bbox: bbox where to insert the text. Use PyLabBbox dictionary
    :param dict kwargs:

    .. seealso:: :class:`~openalea.pylab_drawing_wralea.py_pylab.PyLabFancyArrowDict` and
        :class:`~openalea.pylab_drawing_wralea.py_pylab.PyLabYAArowDict`

    :Example:

    .. dataflow:: openalea.pylab.test annotation
        :width: 40%

        **The openalea.pylab.test.annotation dataflow.**

    .. plot::
        :width: 40%

        from openalea.core.alea import *
        pm = PackageManager()
        run_and_display(('openalea.pylab.test', 'annotation'),{},pm=pm)

    .. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    """
    def __init__(self):
        Node.__init__(self)

        self.add_input(name='axes')

        self.add_input(name='text', interface=IStr, value=None)
        self.add_input(name='xy', interface=ITuple, value=(0,0))
        self.add_input(name='xytext', interface=ITuple, value=(0,0))
        self.add_input(name='xycoords', interface=IEnumStr(tools.xycoords.keys()), value='data')
        self.add_input(name='textcoords', interface=IEnumStr(tools.xycoords.keys()), value='data')
        self.add_input(name='arrowprops', interface=IDict, value={'arrowstyle':'->', 'connectionstyle':'arc3'})
        self.add_input(name='bbox', interface=IDict, value=None)
        self.add_input(name='kwargs(text properties)', interface=IDict, value={})
        self.add_output(name='output')

    def __call__(self, inputs):
        from pylab import annotate, gca
        kwds = {}
        kwds = self.get_input('kwargs(text properties)')
        s = self.get_input('text')
        xy = self.get_input('xy')
        xytext = self.get_input('xytext')
        xycoords = self.get_input('xycoords')
        textcoords = self.get_input('textcoords')
        bbox = self.get_input('bbox')

        axe = gca()
        axe.annotate(s, xy, xytext, xycoords=xycoords,
                 textcoords=textcoords,
                 bbox=bbox,
                 arrowprops=self.get_input('arrowprops'), **kwds)
        #SPHINX DATAFLOW bug. Comment this line for a proper rendering
        #axe.get_figure().canvas.draw()
        from pylab import  gca
        gca().get_figure().canvas.draw()

        return self.get_input('axes')


class PyLabAxhline(Node,CustomizeAxes):
    """Draw a horizontal line at *y* from *xmin* to *xmax*. See pylab.axhline for details.

    :param axes: an optional axes where new data will be plotted.
    :param float *y*: the y position
    :param float *xmin*: starting x position
    :param float *xmax*: ending x position
    :param bool *hold*: True by default
    :param dict *kwargs or Line2D*: connect a Line2D object (optional)

    :returns:
        * current axe
        * pylab.axhline output

    .. seealso:: in VisuAlea, see pylab/test/boxplot composite node.

    :Example:

    .. dataflow:: openalea.pylab.test axhline_axvline
        :width: 40%

        **The openalea.pylab.test.axhline/axvline dataflow.**

    .. plot::
        :width: 40%

        from openalea.core.alea import *
        pm = PackageManager()
        run_and_display(('openalea.pylab.test', 'axhline_axvline'),{},pm=pm)

    .. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    """
    def __init__(self):
        Node.__init__(self)
        CustomizeAxes.__init__(self)

        self.add_input(name='axes')
        self.add_input(name='y', interface=IFloat, value=0.5)
        self.add_input(name='xmin', interface=IFloat, value=0.)
        self.add_input(name='xmax', interface=IFloat, value=1.)
        self.add_input(name='hold', interface=IBool, value=True)
        self.add_input(name='kwargs or line2d', interface=IDict, value={'alpha':1.})

        self.add_output(name="axes")
        self.add_output(name="line2d")

    def __call__(self, inputs):
        from pylab import axhline, Line2D


        kwds = {}
        y = self.get_input('y')
        xmin = self.get_input('xmin')
        xmax = self.get_input('xmax')
        hold = self.get_input('hold')

        axes = self.get_axes()

        if type(self.get_input('kwargs or line2d')) == Line2D:
            line2d = self.get_input('kwargs or line2d')
            kwds = line2d.properties()
            for this in ['transform','children','axes','path', 'data', 'xdata', 'ydata', 'xydata','transformed_clip_path_and_affine']:
                del kwds[this]
        else:
            kwds = self.get_input('kwargs or line2d')


        for axe in axes:
            line2d = axhline(y, xmin=xmin, xmax=xmax, hold=hold, **kwds)
            axe.add_line(line2d)
            axe.get_figure().canvas.draw()

        return self.get_input('axes'), line2d




class PyLabAxvline(Node,CustomizeAxes):
    """Draw a vertical line at *y* from *xmin* to *xmax*. See pylab.axhline for details.

    :param axes: an optional axes where new data will be plotted.
    :param float *x*: the x position
    :param float *ymin*: starting y position
    :param float *ymax*: ending y position
    :param int *hold*: True by default
    :param dict *kwargs or Line2D*: connect a Line2D object (optional)

    :returns:
        * current axe
        * pylab.axhline output

    .. seealso:: :class:`~openalea.pylab_drawing_wralea.py_pylab.PyLabAxhline` for
        dataflow example.

    .. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    """
    def __init__(self):
        Node.__init__(self)
        CustomizeAxes.__init__(self)

        self.add_input(name='axes')
        self.add_input(name='x', interface=IFloat, value=0.5)
        self.add_input(name='ymin', interface=IFloat, value=0.)
        self.add_input(name='ymax', interface=IFloat, value=1.)
        self.add_input(name='hold', interface=IBool, value=True)
        self.add_input(name='kwargs or line2d', interface=IDict, value={'alpha':1.})

        self.add_output(name="axes")
        self.add_output(name="line2d")

    def __call__(self, inputs):
        from pylab import axvline, Line2D
        #cleanup

        kwds = {}
        x = self.get_input('x')
        ymin = self.get_input('ymin')
        ymax = self.get_input('ymax')
        hold = self.get_input('hold')

        axes = self.get_axes()

        if type(self.get_input('kwargs or line2d')) == Line2D:
            line2d = self.get_input('kwargs or line2d')
            kwds = line2d.properties()
            for this in ['transform','children','axes','path', 'data', 'xdata', 'ydata', 'xydata','transformed_clip_path_and_affine']:
                del kwds[this]
        else:
            kwds = self.get_input('kwargs or line2d')

        for axe in axes:
            line2d = axvline(x, ymin=ymin, ymax=ymax, hold=hold, **kwds)
            axe.add_line(line2d)
            axe.get_figure().canvas.draw()

        return self.get_input('axes'), line2d

class PyLabAxhspan(Node, CustomizeAxes):
    """Axis Horizontal Span. See pylab.axvspan for details

    Draw a horizontal span (rectangle) from *ymin* to *ymax*.
    With the default values of *xmin* = 0 and *xmax* = 1.

    :param axes: an optional axes where new data will be plotted.
    :param float xmin: starting x position
    :param float xmax: ending x position
    :param float ymin: starting y position
    :param float ymax: ending y position
    :param bool hold: True by default
    :param kwargs: connect a Patch/polygon object (optional) to further customize the span

    :returns:
        * current axe
        * pylab.axhspan output

    :Example:

    .. dataflow:: openalea.pylab.test axhspan_axvspan
        :width: 40%

        **The openalea.pylab.test.axhline/axvline dataflow.**

    .. plot::
        :width: 40%

        from openalea.core.alea import *
        pm = PackageManager()
        run_and_display(('openalea.pylab.test', 'axhspan_axvspan'),{},pm=pm)

    .. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    """
    def __init__(self):
        Node.__init__(self)
        CustomizeAxes.__init__(self)

        self.add_input(name='axes')

        self.add_input(name='ymin', interface=IFloat, value=0)
        self.add_input(name='ymax', interface=IFloat, value=0.5)
        self.add_input(name='xmin', interface=IFloat, value=0)
        self.add_input(name='xmax', interface=IFloat, value=1)
        self.add_input(name='hold', interface=IBool, value=True)
        self.add_input(name='kwargs (Patch)', interface=IDict, value={})
        #self.add_input(name='kwargs or line2d', interface=IDict, value={'alpha':1.})

        self.add_output(name="axes")
    def __call__(self, inputs):
        from pylab import axhspan
        res = axhspan(self.get_input('ymin'), self.get_input('ymax'), xmin=self.get_input('xmin'),
                xmax=self.get_input('xmax'), **self.get_input('kwargs (Patch)'))
        return res


class PyLabAxvspan(Node, CustomizeAxes):
    """Axis Vertical Span. See pylab.axhspan for details

    Draw a vertical span (rectangle) from *xmin* to *xmax*.  With
    the default values of *ymin* = 0 and *ymax* = 1.

    :param float xmin: starting x position
    :param float xmax: ending x position
    :param float ymin: starting y position
    :param float ymax: ending y position
    :param bool hold: True by default
    :param kwargs: connect a Patch/polygon object (optional) to further customize the span

    :returns:
        * current axe
        * pylab.axhspan output

    .. seealso:: :class:`~openalea.pylab_drawing_wralea.py_pylab.PyLabAxhspan` for
        dataflow example.

    .. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    """
    def __init__(self):
        Node.__init__(self)
        CustomizeAxes.__init__(self)

        self.add_input(name='axes')
        self.add_input(name='xmin', interface=IFloat, value=0)
        self.add_input(name='xmax', interface=IFloat, value=0.5)
        self.add_input(name='ymin', interface=IFloat, value=0)
        self.add_input(name='ymax', interface=IFloat, value=1)
        self.add_input(name='hold', interface=IBool, value=True)
        self.add_input(name='kwargs (Patch)', interface=IDict, value={})

        self.add_output(name='axes')

    def __call__(self, inputs):
        from pylab import axvspan
        res = axvspan(self.get_input('xmin'), self.get_input('xmax'), ymin=self.get_input('ymin'),
                ymax=self.get_input('ymax'), **self.get_input('kwargs (Patch)'))
        return res

