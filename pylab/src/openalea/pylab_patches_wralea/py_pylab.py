###############################################################################
# -*- python -*-
#
#       VisuAlea implementation of pylab.matplotlib.patch
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA
#
#       File author(s): Thomas Cokelaer  <Thomas.Cokelaer@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

__doc__="""VisuAlea implementation of pylab.matplotlib.patch
"""

__license__= "Cecill-C"
__revision__=" $Id: py_stat.py 7897 2010-02-09 09:06:21Z cokelaer $ "

#//////////////////////////////////////////////////////////////////////////////


from openalea.core import Node
from openalea.core import Factory, IFileStr, IInt, IBool, IFloat, \
    ISequence, IEnumStr, IStr, IDirStr, ITuple3, IDict


from openalea.pylab import tools


class PyLabPatchDictionary(Node):
    """VisuAlea version of pylab.patch


    .. todo:: finalise the options?
    """
    def __init__(self):
        Node.__init__(self)
        self.add_input(name='alpha', interface=IFloat(0,1,0.1), value=1.)
        self.add_input(name='axes', interface=IDict, value={})
        self.add_input(name='color', interface=IEnumStr(tools.colors.keys()), value='None')
        self.add_input(name='edgecolor', interface=IEnumStr(tools.colors.keys()), value='black')
        self.add_input(name='facecolor', interface=IEnumStr(tools.colors.keys()), value='blue')
        self.add_input(name='figure', interface=IDict, value=None)
        self.add_input(name='fill', interface=IBool, value=True)
        self.add_input(name='label', interface=IStr, value=None)
        self.add_input(name='linestyle', interface=IEnumStr(tools.linestyles.keys()), value='solid')
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
            kwds['color'] = tools.colors[self.get_input('color')] 
        kwds['edgecolor'] = tools.colors[self.get_input('edgecolor')]
        kwds['facecolor'] = tools.colors[self.get_input('facecolor')]
        return kwds



class PyLabCircle(Node):
    """VisuAlea version of Circle

    :param *x*: x coordinate of circle's center
    :param *y*: y coordinate of circle's center
    :param *radius*: radius of the circle
    :param *patch*:  a :class:`PyLabPatchDictionary` object (optional)
    """

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
    """VisuAlea version of Ellipse

    :param *x*: x coordinate of ellipse center
    :param *y*: y coordinate of ellipse center
    :param *width*: width of horizontal axis
    :param *height*: length of vertical axis
    :param *angle*:  rotation in degrees (anti-clockwise)
    :param *patch*:  a :class:`PyLabPatchDictionary` object (optional)
    """
    def __init__(self):
        from matplotlib.patches import Ellipse
        self.__doc__+=Ellipse.__init__.__doc__
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





class PyLabRectangle(Node):
    """VisuAlea version of Rectangle

    :param *x*: x coordinate of lower left rectangle
    :param *y*: y coordinate of lower left rectangle
    :param *width*: width of the rectangle
    :param *height*: height of the rectangle
    :param *patch*:  a :class:`PyLabPatchDictionary` object (optional)
    """
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
    """VisuAlea version of Wedge

    :param *x*: x-coordinate of wedge's center
    :param *y*: y-coordinate of wedge's center
    :param *r*: radius that sweeps *theta1* and *theta2*
    :param *theta1*:
    :param *theta2*:
    :param *width*: if provided, then a partial wedge is drawn from inner radius *r* - *width* to outer radius *r*.
    :param *patch*:  a :class:`PyLabPatchDictionary` object (optional)
    """
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
    """VisuAlea version of Polygon

    :param *x*: array with shape Nx1
    :param *y*: array with shape Nx1.
    :param *closed*: polygon will be closed so the starting and ending points are the same (default is True)
    :param *patch*:  a :class:`PyLabPatchDictionary` object (optional)

    """
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

