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


from openalea.pylab_nodes_wralea.py_pylab import Colors, LineStyles,Markers
from openalea.pylab_nodes_wralea.py_pylab import Plotting






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
    
    """
    def __init__(self):
        self.colors = Colors().colors
        self.linestyles = LineStyles().linestyles
        self.markers = Markers().markers
        inputs = [
                    {'name':'x',            'interface':None,                           'value':None},
                    {'name':'y',            'interface':None,                           'value':None},
                    {'name':'z',            'interface':None,                           'value':None},
                    {'name':'marker',       'interface':IEnumStr(self.markers.keys()),       'value':'circle'},
                    {'name':'markersize',   'interface':IFloat,                         'value':10},
                    {'name':'linestyle',    'interface':IEnumStr(self.linestyles.keys()),    'value':'solid'},
                    {'name':'color',        'interface':IEnumStr(self.colors.keys()),        'value':'blue'},
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
        kwds['marker']=self.markers[self.get_input("marker")]
        kwds['linestyle']=self.linestyles[self.get_input("linestyle")]
        kwds['color']=self.colors[self.get_input("color")]
        x = self.get_input('x')
        y = self.get_input('y')
        z = self.get_input('z')
        plot(x,y,z, **kwds)

        self.properties()
        return ax

