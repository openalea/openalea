# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#                       Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the CeCILL v2 License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL_V2-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

__doc__="""
Default Node Widget
"""

__license__= "CeCILL V2"
__revision__=" $Id$"



import sys
import os

from PyQt4 import QtCore, QtGui
from openalea.core.node import NodeWidget
from openalea.core.interface import InterfaceWidgetMap, IInterfaceMetaClass
from gui_catalog import *
import types
  

   

class DefaultNodeWidget(NodeWidget, QtGui.QWidget):
    """
    Default implementation of a NodeWidget.
    It displays the node contents.
    """

    type_map = InterfaceWidgetMap()

    def __init__(self, node, parent):

        NodeWidget.__init__(self, node)
        QtGui.QWidget.__init__(self, parent)
        self.setMinimumSize(100, 20)

        self.widgets = []

        vboxlayout = QtGui.QVBoxLayout(self)
        vboxlayout.setMargin(3)
        vboxlayout.setSpacing(2)

        self.empty = True
        for (name, interface) in node.input_desc:

            if(type(interface) == IInterfaceMetaClass):
                interface = interface()
            
            wclass= self.type_map.get(interface.__class__,None)

            if(wclass):
                widget = wclass(node, self, name, interface)
                widget.update_state()
                vboxlayout.addWidget(widget)
                self.widgets.append(widget)
                self.empty = False
            else:
                self.widgets.append(None)

        # If there is no subwidget, add the name
        if( self.empty ):
            label = QtGui.QLabel(self)
            label.setText(self.node.__class__.__name__+
                          " (No Widget available)")

            vboxlayout.addWidget(label)

    
    def notify(self, sender, event):
        """ Function called by observed objects """

        if(event and event[0] == "input_modified"):
            input_index = event[1]

            widget= self.widgets[input_index]
            if widget and not widget.is_notification_locked(): 
                widget.notify(sender, event)
                widget.update_state()
                

    def is_empty(self):
        return bool(self.empty)

