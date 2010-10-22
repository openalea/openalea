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
    """VisuAlea version of mpl_toolkits.mplot3d, a line 3d plotter

    :param *x*: the x data, a 1D array
    :param *y*: the y data, a 1D array
    :param *z*: the z data, a 1D array
    :param *marker*:
    :param *markersize*:
    :param *linestyle*:
    :param *color*:

    .. todo:: a mechanism of line3d for full customisation + allow several xyz entries
  
    .. plot::

        from openalea.core.alea import *
        pm = PackageManager()
        run_and_display(('openalea.pylab.test', 'mplot3d'),{},pm=pm)
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
        ]
        Plotting.__init__(self, inputs)

    def __call__(self, inputs):
        from pylab import cla,plot
        from mpl_toolkits.mplot3d import Axes3D

        self.figure()
        self.axes()
        ax = Axes3D(self.fig)
        #ax.clear()
        kwds = {}
        kwds['markersize']=self.get_input("markersize")
        kwds['marker']=tools.markers[self.get_input("marker")]
        kwds['linestyle']=tools.linestyles[self.get_input("linestyle")]
        kwds['color']=tools.colors[self.get_input("color")]
        x = self.get_input('x')
        y = self.get_input('y')
        z = self.get_input('z')
        ax.plot(x,y,z, **kwds)

        self.properties()
        return ax


class PyLabContour3D(Plotting):
    """not for production!! For testing and showing contour3d possibilities.
    
    
    .. plot::

        from openalea.core.alea import *
        pm = PackageManager()
        run_and_display(('openalea.pylab.test', 'mcontour3d'),{},pm=pm)
        
    """
    def __init__(self):
        inputs = [
                    {'name':'x',            'interface':None,                           'value':None},
                    {'name':'y',            'interface':None,                           'value':None},
                    {'name':'z',            'interface':None,                           'value':None},
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
        x = self.get_input('x')
        y = self.get_input('y')
        z = self.get_input('z')
        ax.contour(x,y,z, **kwds)

        self.properties()
        return ax

class PyLabContourf3D(Plotting):
    """not for production!! For testing and showing contour3d possibilities.
    
    
    .. plot::

        from openalea.core.alea import *
        pm = PackageManager()
        run_and_display(('openalea.pylab.test', 'mcontourf3d'),{},pm=pm)

    """
    def __init__(self):
        inputs = [
                    {'name':'x',            'interface':None,                           'value':None},
                    {'name':'y',            'interface':None,                           'value':None},
                    {'name':'z',            'interface':None,                           'value':None},
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
        x = self.get_input('x')
        y = self.get_input('y')
        z = self.get_input('z')
        ax.contourf(x,y,z, **kwds)

        self.properties()
        return ax
