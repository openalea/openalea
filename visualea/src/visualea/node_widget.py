# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2006 - 2007 INRIA - CIRAD - INRA  
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
################################################################################

__doc__="""
Default Node Widget
"""

__license__= "CeCILL V2"
__revision__=" $Id$"



import sys
import os
import weakref

from PyQt4 import QtCore, QtGui
from openalea.core.interface import InterfaceWidgetMap, IInterfaceMetaClass
from openalea.core.observer import lock_notify, AbstractListener
from gui_catalog import *
import types



class SignalSlotListener(AbstractListener):
    """ Listener with QT Signal/Slot support """

    def __init__(self):
        
        # Create a QObject if necessary
        if(not isinstance(self, QtCore.QObject)):
            self.obj = QtCore.QObject()
            self.qobj = weakref.ref(self.obj)
        else:
            self.qobj = weakref.ref(self)
        
            
        self.qobj().connect(self.qobj(), QtCore.SIGNAL("notify"), self.notify)


    def call_notify (self, sender, event=None):
        """
        This function is called by observed object
        @param sender : the observed object which send notification
        @param event : the data associated to the notification
        """
        
        try:
            self.qobj().emit(QtCore.SIGNAL("notify"), sender, event)
        except Exception, e:
            print "Cannot emit Qt Signal : ", e
            self.notify(sender, event)






###############################################################################

class NodeWidget(SignalSlotListener):
    """
    Base class for node instance widgets.
    """

    def __init__(self, node):
        """ Init the widget with the associated node """
        
        self.__node = node

        SignalSlotListener.__init__(self)
        # register to observed node
        self.initialise(node)


    def get_node(self):
        """ Return the associated node """
        return self.__node


    def set_node(self, node):
        """ Define the associated node """
        self.__node = node

    node = property(get_node, set_node)


    def notify(self, sender, event):
        """
        This function is called by the Observed objects
        and must be overloaded
        """
        pass
    

    def is_empty(self):
        return False


    def set_autonomous(self):
        """ 
        Set the widget autonomous (i.e add run/exit button) 
        """
        return

   

class DefaultNodeWidget(NodeWidget, QtGui.QWidget):
    """
    Default implementation of a NodeWidget.
    It displays the node contents.
    """

    type_map = InterfaceWidgetMap()
    
    @lock_notify
    def __init__(self, node, parent):
        """ Constructor """

        QtGui.QWidget.__init__(self, parent)
        NodeWidget.__init__(self, node)
        self.setMinimumSize(100, 20)

        self.widgets = []

        vboxlayout = QtGui.QVBoxLayout(self)
        vboxlayout.setMargin(3)
        vboxlayout.setSpacing(2)

        self.empty = True
        
        for i,desc in enumerate(node.input_desc):
            # Hidden state
            h = node.is_port_hidden(i)
            if(h) :
                self.widgets.append(None)
                continue
            
            name = desc['name']
            interface = desc.get('interface', None)

            # interface class or instance ?
            if(type(interface) == IInterfaceMetaClass):
                interface = interface()
            
            wclass = self.type_map.get(interface.__class__, None)

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
            widget = self.widgets[input_index]
            if widget and not widget.is_notification_locked():

                widget.notify(sender, event)
                widget.update_state()
                

    def is_empty(self):
        return bool(self.empty)

