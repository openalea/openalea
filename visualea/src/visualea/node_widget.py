# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#                       Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the GPL License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.gnu.org/licenses/gpl.txt
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

__doc__="""
Default Node Widget and Subgraph Widget
"""

__license__= "GPL"
__revision__=" $Id$"



import sys
import math

from PyQt4 import QtCore, QtGui
from openalea.core.core import NodeWidget
from openalea.core.interface import *


import types


class IInterfaceWidget(QtGui.QWidget, NodeWidget):
    """ Base class for widget associated to an interface """

    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """
        
        NodeWidget.__init__(self, node)
        QtGui.QWidget.__init__(self, parent)

        self.param_str = parameter_str

        self.update_state()


    def update_state(self):
        """ Enable or disable widget depending of connection status """

        i = self.node.get_input_index(self.param_str)
        state = self.node.get_input_state(i)
        
        if(state == "connected"):
            self.setEnabled(False)
        else:
            self.setEnabled(True)

    


class IFloatWidget(IInterfaceWidget):
    """
    Float spin box widget
    """

    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """

        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)
        
        hboxlayout = QtGui.QHBoxLayout(self)
        hboxlayout.setMargin(3)
        hboxlayout.setSpacing(5)

        self.label = QtGui.QLabel(self)
        self.label.setText(parameter_str)
        hboxlayout.addWidget(self.label)

        self.spin = QtGui.QDoubleSpinBox (self)
        self.spin.setRange(interface.min, interface.max)

        hboxlayout.addWidget(self.spin)

        self.spin.setValue(self.node.get_input_by_key(self.param_str))

        self.connect(self.spin, QtCore.SIGNAL("valueChanged(double)"), self.valueChanged)

        
    def valueChanged(self, newval):

        self.node.set_input_by_key(self.param_str, newval)
        
    def notify(self, sender, event):
        """ Notification sent by node """
        try:
            v = float(self.node.get_input_by_key(self.param_str))
        except:
            v = 0.
            
        self.spin.setValue(v)
        

class IIntWidget(IInterfaceWidget):
    """
    integer spin box widget
    """

    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """

        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)

        hboxlayout = QtGui.QHBoxLayout(self)
        hboxlayout.setMargin(3)
        hboxlayout.setSpacing(5)


        self.label = QtGui.QLabel(self)
        self.label.setText(parameter_str)
        hboxlayout.addWidget(self.label)

        self.spin = QtGui.QSpinBox (self)
        self.spin.setRange(interface.min, interface.max)

        hboxlayout.addWidget(self.spin)

        self.spin.setValue(self.node.get_input_by_key(self.param_str))

        self.connect(self.spin, QtCore.SIGNAL("valueChanged(int)"), self.valueChanged)

        
    def valueChanged(self, newval):

        self.node.set_input_by_key(self.param_str, newval)
        
        
    def notify(self, sender, event):
        """ Notification sent by node """

        try:
            v = int(self.node.get_input_by_key(self.param_str))
        except:
            v = 0
        self.spin.setValue(v)



class IBoolWidget(IInterfaceWidget):
    """
    integer spin box widget
    """

    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """

        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)

        hboxlayout = QtGui.QHBoxLayout(self)
        hboxlayout.setMargin(3)
        hboxlayout.setSpacing(5)

        self.checkbox = QtGui.QCheckBox (parameter_str, self)

        hboxlayout.addWidget(self.checkbox)

        self.notify(node, None)
        self.connect(self.checkbox, QtCore.SIGNAL("stateChanged(int)"), self.stateChanged)

        
    def stateChanged(self, state):

        if(state == QtCore.Qt.Checked):
            self.node.set_input_by_key(self.param_str, True)
        else:
            self.node.set_input_by_key(self.param_str, False)
        
        
    def notify(self, sender, event):
        """ Notification sent by node """

        try:
            ischecked = bool(self.node.get_input_by_key(self.param_str))
        except:
            ischecked = False

        if(ischecked):
            self.checkbox.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkbox.setCheckState(QtCore.Qt.Unchecked)


class IStrWidget(IInterfaceWidget):
    """
    Line Edit widget
    """

    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """

        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)

        self.hboxlayout = QtGui.QHBoxLayout(self)

        self.hboxlayout.setMargin(3)
        self.hboxlayout.setSpacing(5)


        self.label = QtGui.QLabel(self)
        self.label.setText(parameter_str)
        self.hboxlayout.addWidget(self.label)

        self.subwidget = QtGui.QLineEdit (self)
        self.hboxlayout.addWidget(self.subwidget)

        self.subwidget.setText(str(self.node.get_input_by_key(self.param_str)))

        self.connect(self.subwidget, QtCore.SIGNAL("textChanged(QString)"), self.valueChanged)

        
    def valueChanged(self, newval):

        self.node.set_input_by_key(self.param_str, str(newval))
        
        
    def notify(self, sender, event):
        """ Notification sent by node """

        self.subwidget.setText(str(self.node.get_input_by_key(self.param_str)))
        


class IFileStrWidget(IStrWidget):
    """
    File name Line Edit Widget
    """

    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """

        IStrWidget.__init__(self, node, parent, parameter_str, interface)

        self.button = QtGui.QPushButton("...", self)
        self.hboxlayout.addWidget(self.button)

        self.connect(self.button, QtCore.SIGNAL("clicked()"), self.button_clicked)

    def button_clicked(self):
        
        result = QtGui.QFileDialog.getOpenFileName(self, "Select File", QtCore.QDir.homePath() )
    
        if(result):
            self.node.set_input_by_key(self.param_str, str(result))
            
        
class IEnumStrWidget(IInterfaceWidget):
    """ String Enumeration widget """
    
    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """

        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)
                
        self.hboxlayout = QtGui.QHBoxLayout(self)
        self.hboxlayout.setMargin(3)
        self.hboxlayout.setSpacing(5)

        self.label = QtGui.QLabel(self)
        self.label.setText(parameter_str)
        self.hboxlayout.addWidget(self.label)

        self.subwidget = QtGui.QComboBox(self)

        # map between string and combobox index
        self.map_index = {}
        for s in  interface.enum:
            self.subwidget.addItem(s)
            self.map_index[s] = self.subwidget.count() - 1
        
        self.hboxlayout.addWidget(self.subwidget)

        self.connect(self.subwidget,
                     QtCore.SIGNAL("currentIndexChanged(const QString & text)"),
                     self.valueChanged)

        
    def valueChanged(self, newval):

        self.node.set_input_by_key(self.param_str, str(newval))
        
        
    def notify(self, sender, event):
        """ Notification sent by node """

        str = str(self.node.get_input_by_key(self.param_str))
        try:
            index = self.map_index[str]
        except :
            index = -1

        self.subwidget.setCurrentIndex(index)



class IRGBColorWidget(IInterfaceWidget):
    """ RGB Color Widget """

    def __init__(self, node, parent, parameter_str, interface):
        """
        @param parameter_str : the parameter key the widget is associated to
        @param interface : instance of interface object
        """

        IInterfaceWidget.__init__(self, node, parent, parameter_str, interface)

        self.hboxlayout = QtGui.QHBoxLayout(self)
        self.hboxlayout.setMargin(3)
        self.hboxlayout.setSpacing(5)

        self.label = QtGui.QLabel(self)
        self.label.setText(parameter_str)
        self.hboxlayout.addWidget(self.label)

        self.colorwidget = QtGui.QWidget(self)
        self.colorwidget.setAutoFillBackground(True)

        self.colorwidget.setMinimumSize(QtCore.QSize(50,50))
        self.colorwidget.setBackgroundRole(QtGui.QPalette.Window)
        self.colorwidget.mouseDoubleClickEvent = self.widget_clicked
        self.notify(node, None)
        
        self.hboxlayout.addWidget(self.colorwidget)


#         self.button = QtGui.QPushButton("...", self)
#         self.hboxlayout.addWidget(self.button)

#         self.connect(self.button, QtCore.SIGNAL("clicked()"), self.button_clicked)

    def widget_clicked(self,event):
        
        try:
            (r,g,b) = self.node.get_input_by_key(self.param_str)
            oldcolor = QtGui.QColor(r,g,b)
        except:
            oldcolor = QtCore.Qt.White                                        
        
        color = QtGui.QColorDialog.getColor(oldcolor, self)
    
        if(color):
            self.node.set_input_by_key(self.param_str, (color.red(), color.green(), color.blue()))

    def notify(self, sender, event):
        """ Notification sent by node """

        try:
            (r,g,b) = self.node.get_input_by_key(self.param_str)
        except:
            (r,g,b) = (0,0,0)
        
        palette = self.colorwidget.palette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor(r,g,b))
        self.colorwidget.setPalette(palette)
        self.colorwidget.update()
        
  

   

class DefaultNodeWidget(NodeWidget, QtGui.QWidget):
    """
    Default implementation of a NodeWidget.
    It displays the node contents.
    """

    # Map between type and widget
    type_map= {IFloat: IFloatWidget,
               IInt : IIntWidget,
               IStr : IStrWidget,
               IFileStr: IFileStrWidget,
               IBool : IBoolWidget,
               IEnumStr : IEnumStrWidget,
               IRGBColor : IRGBColorWidget,
               types.NoneType : None
              }
    

    def __init__(self, node, parent):

        NodeWidget.__init__(self, node)
        QtGui.QWidget.__init__(self, parent)

        self.widgets = []

        vboxlayout = QtGui.QVBoxLayout(self)
        vboxlayout.setMargin(3)
        vboxlayout.setSpacing(2)

        for (name, interface) in node.input_desc:

            if(type(interface) == types.TypeType):
                interface = interface()
            
            wclass= self.type_map.get(interface.__class__,None)

            if(wclass):
                widget = wclass(node, self, name, interface)
                vboxlayout.addWidget(widget)
                self.widgets.append(widget)

        # If there is no subwidget, add the name
        if( len(self.widgets) == 0):
            label = QtGui.QLabel(self)
            label.setText(self.node.factory.description)

            vboxlayout.addWidget(label)

    
    def notify(self, sender, event):
        """ Function called by observed objects """

        if(event and event[0] == "input_modified"):
            input_index = event[1]

            self.widgets[input_index].notify(sender, event)
            self.widgets[input_index].update_state()
