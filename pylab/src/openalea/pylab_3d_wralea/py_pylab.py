###############################################################################
# -*- python -*-
#
#       VisuAlea implemtation of pylab.mplot3d
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA
#
#       File author(s): Thomas Cokelaer <thomas.cokelaer@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

__doc__="""VisuAlea implementation of pylab.mplot3d
"""

__license__= "Cecill-C"
__revision__=" $Id: py_stat.py 7897 2010-02-09 09:06:21Z cokelaer $ "

#//////////////////////////////////////////////////////////////////////////////


from openalea.core import Node
from openalea.core import Factory, IFileStr, IInt, IBool, IFloat, \
    ISequence, IEnumStr, IStr, IDirStr, ITuple3, IDict


from openalea.pylab_plotting_wralea.py_pylab import Plotting
from openalea.pylab import tools





class PyLabPlot3D(Plotting):
    """Plot 3D data. See mpl_toolkits.mplot3d.Axes3D.plot for details.

    :param *x*: the x coordinates of vertices
    :param *y*: the y coordinates of vertices
    :param *z*: the z values
    :param str marker: a valid matplotlib marker (e.g., [ '+' | '*']).
    :param markersize: default is 10
    :param color:
    :param linestyle:
    :param dict kwargs:  Connect a :class:`~openalea.pylab_plotting_wralea.py_pylab.PyLabLine2D` 
        to customize the curve.
    :param int figure: figure id

    :Example:

    .. dataflow:: openalea.pylab.test mplot3d
        :width: 50%

        **The `openalea.pylab.mplot3d.PyLab3D` dataflow.** Three `randn` nodes provides
        x, y and z arrays, which have normal distributions. The PyLabPlot3D allows to 
        visualize the data in 3D. The figure can be manipulated to look around the data in 
        a 3D view.

    .. plot::
        :width: 50%

        from openalea.core.alea import *
        pm = PackageManager()
        run_and_display(('openalea.pylab.test', 'mplot3d'),{},pm=pm )

    .. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    """
    def __init__(self):
        inputs = [
                    {'name':'x',            'interface':None,                           'value':None},
                    {'name':'y',            'interface':None,                           'value':None},
                    {'name':'z',            'interface':None,                           'value':None},
                    {'name':'marker',       'interface':IEnumStr(tools.markers.keys()),       'value':'circle'},
                    {'name':'markersize',   'interface':IFloat,                         'value':10},
                    {'name':'linestyle',    'interface':IEnumStr(tools.linestyles.keys()),    'value':'solid'},
                    {'name':'color',        'interface':IEnumStr(tools.colors.keys()),        'value':'blue'},
                    {'name': 'kwargs', 'interface':IDict, 'value':{}},
        ]
        Plotting.__init__(self, inputs)

    def __call__(self, inputs):
        from pylab import cla, plot, Line2D
        from mpl_toolkits.mplot3d import Axes3D

        self.figure()
        self.axes()
        ax = Axes3D(self.fig)
        #ax.clear()
        kwds = {}

        line2d = self.get_input('kwargs')
        if type(line2d) == Line2D:
            kwds = self.get_input('kwargs').properties()
        else:
            for key, value in self.get_input('kwargs').iteritems():
                kwds[key] = value

        for x in ['axes', 'children',  'path','xdata', 'ydata', 'data','transform',
                          'xydata','transformed_clip_path_and_affine']:
            del kwds[x]


        kwds['markersize']=self.get_input("markersize")
        kwds['marker']=tools.markers[self.get_input("marker")]
        kwds['linestyle']=tools.linestyles[self.get_input("linestyle")]
        kwds['color']=tools.colors[self.get_input("color")]



        x = self.get_input('x')
        y = self.get_input('y')
        z = self.get_input('z')
        res = ax.plot(x,y,z, **kwds)

        self.update_figure('3d')
        return ax


class PyLabContour3D(Plotting):
    """Plot 3D data. See mpl_toolkits.mplot3d.Axes3D.contour3d for details.

    :param array x: *x* data
    :param array y: *y* data
    :param array z: *z* data
    :param int levels: number of levels
    :param dict kwargs: 
    :param int figure: figure id

    :Example:

    .. dataflow:: openalea.pylab.test mcontour3d
        :width: 50%

        **The openalea.pylab.test.mcontour3d dataflow.**

    .. plot::
        :width: 50%

        from openalea.core.alea import *
        pm = PackageManager()
        run_and_display(('openalea.pylab.test', 'mcontour3d'),{},pm=pm )


    .. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    """
    def __init__(self):
        inputs = [
                    {'name':'x', 'interface':None, 'value':None},
                    {'name':'y', 'interface':None, 'value':None},
                    {'name':'z', 'interface':None, 'value':None},
                    {'name':'levels', 'interface':IInt, 'value':10},
                    {'name':'kwargs', 'interface':IDict, 'value':{}},
        ]
        Plotting.__init__(self, inputs)

    def __call__(self, inputs):
        from pylab import cla,contour
        from mpl_toolkits.mplot3d import Axes3D

        self.figure()
        self.axes()
        ax = Axes3D(self.fig)
        #ax.clear()
        kwds = {}
        for key, value in self.get_input('kwargs').iteritems():
            kwds[key] = value
        x = self.get_input('x')
        y = self.get_input('y')
        z = self.get_input('z')
        levels = self.get_input('levels')
        ax.contour(x,y,z, levels=levels,  **kwds)

        self.update_figure('3d')
        return ax


class PyLabContourf3D(Plotting):
    """Plot 3D data. See mpl_toolkits.mplot3d.Axes3D.contourf3d for details.

    :param array x: *x* data
    :param array y: *y* data
    :param array z: *z* data
    :param int levels: number of levels
    :param dict kwargs: 
    :param int figure: figure id

    :Example:

    .. dataflow:: openalea.pylab.test mcontourf3d
        :width: 50%

        **The openalea.pylab.test.mcontourf3d dataflow.**

    .. plot::
        :width: 50%

        from openalea.core.alea import *
        pm = PackageManager()
        run_and_display(('openalea.pylab.test', 'mcontourf3d'),{},pm=pm)


    .. sectionauthor:: Thomas Cokelaer <Thomas.Cokelaer@sophia.inria.fr>
    """
    def __init__(self):
        inputs = [
                    {'name':'x',            'interface':None,                           'value':None},
                    {'name':'y',            'interface':None,                           'value':None},
                    {'name':'z',            'interface':None,                           'value':None},
                    {'name':'kwargs', 'interface':IDict, 'value':{}},
        ]
        Plotting.__init__(self, inputs)

    def __call__(self, inputs):
        from pylab import cla,contourf
        from mpl_toolkits.mplot3d import Axes3D

        self.figure()
        self.axes()
        ax = Axes3D(self.fig)
        #ax.clear()
        kwds = {}
        for key, value in self.get_input('kwargs').iteritems():
            kwds[key] = value
        x = self.get_input('x')
        y = self.get_input('y')
        z = self.get_input('z')

        ax.contourf(x,y,z, **kwds)

        self.update_figure('3d')
        return ax
