# -*- python -*-
#
#       OpenAlea.Core.Library: OpenAlea Core Library module
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): David Da SILVA <david.da_silva@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#


__doc__="""
Wralea for Catalog.PlotTools 
"""

__license__= "Cecill-C"
__revision__=" $Id$ "


from openalea.core import *
 
#class IPlotableObject(IInterface):
#    """ Interface for Plotable object """
#    __metaclass__ = IInterfaceMetaClass
#    __pytype__ = types.PlotableObjectType
 
 
#class IPlotableObjectWidget(IInterfaceWidget, QtGui.QWidget):
#    """
#    Float spin box widget
#    """
# 
#    # Associate widget with the IPlotableObject
#    __interface__ = IPlotableObject
#    __metaclass__ = make_metaclass()
# 
#    def __init__(self, node, parent, parameter_str, interface):
#        """
#        @param parameter_str : the parameter key the widget is associated to
#        @param interface : instance of interface object
#        """
#        QtGui.QWidget.__init__(self, parent)
#        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)
# 
#        hboxlayout = QtGui.QHBoxLayout(self)
#        self.spin = QtGui.QDoubleSpinBox (self)
#        self.spin.setRange(interface.min, interface.max)
# 
#        hboxlayout.addWidget(self.spin)
# 
#        self.notify(None,None)
#        self.connect(self.spin, QtCore.SIGNAL("valueChanged(double)"), self.valueChanged)
# 
# 
#    def valueChanged(self, newval):
#        self.node.set_input_by_key(self.param_str, newval)
# 
#    def notify(self, sender, event):
#        """ Notification sent by node """
#        try:
#            v = float(self.node.get_input_by_key(self.param_str))
#        except:
#            v = 0.
# 
#        self.spin.setValue(v)


def register_packages(pkgmanager):
    """ Initialisation function
    Return a list of package to include in the package manager.
    This function is called by the package manager when it is updated
    """

    # Base Library

    metainfo = { 'version' : '0.0.1',
                 'license' : 'CECILL-C',
                 'authors' : 'OpenAlea Consortium',
                 'institutes' : 'INRIA/CIRAD',
                 'description' : 'Catalog library.',
                 'url' : 'http://openalea.gforge.inria.fr'
                 }


    package = Package("Catalog.PlotTools", metainfo)

    nf = Factory( name= "Plot2D", 
                  description="Plot a list of 2D plotable objects", 
                  category="Vizualisation", 
                  nodemodule="plotools",
                  nodeclass="Plot2D",
                  inputs=(dict(name='plotObjList', interface=ISequence, showwidget=True),
                          dict(name='title', interface=IStr, value='MyPlot'),
                            dict(name='xlabel', interface=IStr, value='x-axis'),
                            dict(name='ylabel', interface=IStr, value='y-axis'),  ),
                  outputs=()

                )

    package.add_factory(nf)


    
    pkgmanager.add_package(package)



