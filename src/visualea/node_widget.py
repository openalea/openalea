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


class IFloatWidget(QtGui.QWidget, NodeWidget):
    """
    Float spin box widget
    """

    def __init__(self, node, parent, parameter_str):
        """
        @param parameter_str : the parameter key the widget is associated to
        """

        NodeWidget.__init__(self, node)
        QtGui.QWidget.__init__(self, parent)

        self.param_str = parameter_str

        hboxlayout = QtGui.QHBoxLayout(self)
        hboxlayout.setMargin(3)
        hboxlayout.setSpacing(5)

        self.label = QtGui.QLabel(self)
        self.label.setText(parameter_str)
        hboxlayout.addWidget(self.label)

        self.spin = QtGui.QDoubleSpinBox (self)
        self.spin.setRange(-2**15, 2**15)

        hboxlayout.addWidget(self.spin)

        self.spin.setValue(self.node.get_input_by_key(self.param_str))

        self.connect(self.spin, QtCore.SIGNAL("valueChanged(double)"), self.valueChanged)

        
    def valueChanged(self, newval):

        self.node.set_input_by_key(self.param_str, newval)
        
    def notify(self):
        """ Notification sent by node """
        try:
            v = float(self.node.get_input_by_key(self.param_str))
        except:
            v = 0.
            
        self.spin.setValue(v)
        

class IIntWidget(QtGui.QWidget, NodeWidget):
    """
    integer spin box widget
    """

    def __init__(self, node, parent, parameter_str):
        """
        @param parameter_str : the parameter key the widget is associated to
        """

        NodeWidget.__init__(self, node)
        QtGui.QWidget.__init__(self, parent)

        self.param_str = parameter_str

        hboxlayout = QtGui.QHBoxLayout(self)
        hboxlayout.setMargin(3)
        hboxlayout.setSpacing(5)


        self.label = QtGui.QLabel(self)
        self.label.setText(parameter_str)
        hboxlayout.addWidget(self.label)

        self.spin = QtGui.QSpinBox (self)
        self.spin.setRange(-2**15, 2**15)

        hboxlayout.addWidget(self.spin)

        self.spin.setValue(self.node.get_input_by_key(self.param_str))

        self.connect(self.spin, QtCore.SIGNAL("valueChanged(int)"), self.valueChanged)

        
    def valueChanged(self, newval):

        self.node.set_input_by_key(self.param_str, newval)
        
        
    def notify(self):
        """ Notification sent by node """

        try:
            v = int(self.node.get_input_by_key(self.param_str))
        except:
            v = 0
        self.spin.setValue(v)



class IBoolWidget(QtGui.QWidget, NodeWidget):
    """
    integer spin box widget
    """

    def __init__(self, node, parent, parameter_str):
        """
        @param parameter_str : the parameter key the widget is associated to
        """

        NodeWidget.__init__(self, node)
        QtGui.QWidget.__init__(self, parent)

        self.param_str = parameter_str

        hboxlayout = QtGui.QHBoxLayout(self)
        hboxlayout.setMargin(3)
        hboxlayout.setSpacing(5)

        self.checkbox = QtGui.QCheckBox (parameter_str, self)

        hboxlayout.addWidget(self.checkbox)

        self.notify()
        self.connect(self.checkbox, QtCore.SIGNAL("stateChanged(int)"), self.stateChanged)

        
    def stateChanged(self, state):

        if(state == QtCore.Qt.Checked):
            self.node.set_input_by_key(self.param_str, True)
        else:
            self.node.set_input_by_key(self.param_str, False)
            
        
        
    def notify(self):
        """ Notification sent by node """

        try:
            ischecked = bool(self.node.get_input_by_key(self.param_str))
        except:
            ischecked = False

        if(ischecked):
            self.checkbox.setCheckState(QtCore.Qt.Checked)
        else:
            self.checkbox.setCheckState(QtCore.Qt.Unchecked)


class IStrWidget(QtGui.QWidget, NodeWidget):
    """
    Line Edit widget
    """

    def __init__(self, node, parent, parameter_str):
        """
        @param parameter_str : the parameter key the widget is associated to
        """

        NodeWidget.__init__(self, node)
        QtGui.QWidget.__init__(self, parent)

        self.param_str = parameter_str

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
        
        
    def notify(self):
        """ Notification sent by node """

        self.subwidget.setText(str(self.node.get_input_by_key(self.param_str)))
        


class IFileStrWidget(IStrWidget):
    """
    File name Line Edit Widget
    """

    def __init__(self, node, parent, parameter_str):
        """
        @param parameter_str : the parameter key the widget is associated to
        """

        IStrWidget.__init__(self, node, parent, parameter_str)

        self.button = QtGui.QPushButton("...", self)
        self.hboxlayout.addWidget(self.button)

        self.connect(self.button, QtCore.SIGNAL("clicked()"), self.button_clicked)

    def button_clicked(self):
        
        result = QtGui.QFileDialog.getOpenFileName(self, "Select File", QtCore.QDir.homePath() )
    
        if(result):
            self.subwidget.setText(str(self.node.get_input_by_key(self.param_str)))
            self.node.set_input_by_key(self.param_str, str(result))
        
            

class DefaultNodeWidget(QtGui.QWidget, NodeWidget):
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
               types.NoneType : None
              }
    

    def __init__(self, node, parent):

        NodeWidget.__init__(self, node)
        QtGui.QWidget.__init__(self, parent)

        self.widgets = []

        vboxlayout = QtGui.QVBoxLayout(self)
        vboxlayout.setMargin(3)
        vboxlayout.setSpacing(2)

        for param in node.factory.parameters:
            param_type = node.get_input_interface_by_key(param) 

            wclass= self.type_map.get(param_type,None)

            if(wclass):
                widget = wclass(node, self, param)
                vboxlayout.addWidget(widget)
                self.widgets.append(widget)

        # If there is no subwidget, add the name
        if( len(self.widgets) == 0):
            label = QtGui.QLabel(self)
            label.setText(self.node.factory.description)

            vboxlayout.addWidget(label)



    def notify(self):
        """ Function called by observed objects """
        
        def call_notify(p) :
            p.notify()
            
        map(call_notify, self.widgets)
