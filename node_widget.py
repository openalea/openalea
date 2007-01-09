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
from core.core import NodeWidget


import types


class FloatNodeWidget(QtGui.QWidget, NodeWidget):
    """
    Float spin box widget
    """

    def __init__(self, node, parent, parameter_str="val"):
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
        hboxlayout.addWidget(self.spin)

        self.spin.setValue(self.node[self.param_str])

        self.connect(self.spin, QtCore.SIGNAL("valueChanged(double)"), self.valueChanged)

        
    def valueChanged(self, newval):

        self.node[self.param_str] = newval
        
    def notify(self):
        """ Notification sent by node """
        try:
            v = float(self.node[self.param_str])
        except:
            v = 0.
            
        self.spin.setValue(v)
        

class IntNodeWidget(QtGui.QWidget, NodeWidget):
    """
    integer spin box widget
    """

    def __init__(self, node, parent, parameter_str="val"):
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
        hboxlayout.addWidget(self.spin)

        self.spin.setValue(self.node[self.param_str])

        self.connect(self.spin, QtCore.SIGNAL("valueChanged(int)"), self.valueChanged)

        
    def valueChanged(self, newval):

        self.node[self.param_str] = newval
        
        
    def notify(self):
        """ Notification sent by node """

        try:
            v = int(self.node[self.param_str])
        except:
            v = 0
        self.spin.setValue(v)


class StrNodeWidget(QtGui.QWidget, NodeWidget):
    """
    Line Edit widget
    """

    def __init__(self, node, parent, parameter_str="val"):
        """
        @param parameter_str : the parameter key the widget is associated to
        """

        NodeWidget.__init__(self, node)
        QtGui.QWidget.__init__(self, parent)

        self.param_str = parameter_str
        hboxlayout.setMargin(3)
        hboxlayout.setSpacing(5)

        hboxlayout = QtGui.QHBoxLayout(self)

        self.label = QtGui.QLabel(self)
        self.label.setText(parameter_str)
        hboxlayout.addWidget(self.label)

        self.subwidget = QtGui.QLineEdit (self)
        hboxlayout.addWidget(self.subwidget)

        self.subwidget.setText(str(self.node[self.param_str]))

        self.connect(self.spin, QtCore.SIGNAL("textChanged(QString)"), self.valueChanged)

        
    def valueChanged(self, newval):

        self.node[self.param_str] = str(newval)
        
        
    def notify(self):
        """ Notification sent by node """

        self.spin.setText(str(self.node[self.param_str]))


class DefaultNodeWidget(QtGui.QWidget, NodeWidget):
    """
    Default implementation of a NodeWidget
    It displays the node contents
    """

    # Map between type and widget
    type_map =    {
        float: FloatNodeWidget,
        int : IntNodeWidget,
        str : StrNodeWidget,
        types.NoneType : None
        }
    

    def __init__(self, node, parent):

        NodeWidget.__init__(self, node)
        QtGui.QWidget.__init__(self, parent)

        self.widgets = []

        vboxlayout = QtGui.QVBoxLayout(self)
        vboxlayout.setMargin(3)
        vboxlayout.setSpacing(2)

        for k in node.keys():

            value = node[k]
            try:
                wclass = self.type_map[type(value)]
            except:
                wclass = None

            if(wclass):
                widget = wclass(node, self, k)
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
