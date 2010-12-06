# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
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
###############################################################################
"""Default Node Widget"""

__license__ = "CeCILL V2"
__revision__ = " $Id$"



import sys
import os
import weakref

from PyQt4 import QtCore, QtGui
from openalea.core.interface import InterfaceWidgetMap, IInterfaceMetaClass
from openalea.core.observer import lock_notify, AbstractListener
from openalea.core.traitsui import View, Item, Group
from openalea.visualea.gui_catalog import *
from openalea.visualea.util import busy_cursor, exception_display

import types



class SignalSlotListener(AbstractListener):
    """ Listener with QT Signal/Slot support """

    def __init__(self):
        AbstractListener.__init__(self)
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

    def __init__(self, node, autonomous=False):
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




class DefaultNodeWidget(NodeWidget, QtGui.QWidget):
    """
    Default implementation of a NodeWidget.
    It displays the node contents.
    """

    type_map = InterfaceWidgetMap()

    @lock_notify
    def __init__(self, node, parent, autonomous=False):
        """ Constructor """

        QtGui.QWidget.__init__(self, parent)
        NodeWidget.__init__(self, node)
        self.setMinimumSize(100, 20)


        self.widgets = []
        self.empty = True

        self.vboxlayout = QtGui.QVBoxLayout(self)
        self.vboxlayout.setSizeConstraint(QtGui.QLayout.SetMinimumSize)

        if  node.factory.view is None:
            # we create the widget in default way
            #print node.input_desc
            layout = self.vboxlayout
            layout.setMargin(3)
            layout.setSpacing(2)
            for port in node.input_desc:
                self.place_item( self, port, layout)
        else:
            #if node.factory.view.layout=="-": layout = QtGui.QHBoxLayout(self)
            #elif node.factory.view.layout=="|": layout = QtGui.QVBoxLayout(self)
            #layout.setMargin(3)
            #layout.setSpacing(2)
            #
            ## we use custom view defined by user
            #for i in node.factory.view.content:
            #    self.place( self,  i, layout )
            self.place_group( self, node.factory.view, self.vboxlayout)

        if autonomous:
            self.set_autonomous()



    def set_autonomous(self):
        """ Add Run bouton and close button """

        runbutton = QtGui.QPushButton("Run", self)
        exitbutton = QtGui.QPushButton("Exit", self)
        self.connect(runbutton, QtCore.SIGNAL("clicked()"), self.run)
        self.connect(exitbutton, QtCore.SIGNAL("clicked()"), self.exit)

        buttons = QtGui.QHBoxLayout()
        buttons.addWidget(runbutton)
        buttons.addWidget(exitbutton)
        self.vboxlayout.addLayout(buttons)


    @exception_display
    @busy_cursor
    def run(self):
        self.node.eval()


    def exit(self):
        self.parent().close()


    def place( self, widget,  item, layout ):
        """
        Place
        """
        if isinstance( item, Item ):
            p = self.node.get_input_port( item.name )
            self.place_item( widget, p, layout)

        elif isinstance( item, Group ):
            self.place_group(widget, item, layout)


    def place_item( self,  widget, port,  layout ):
        """
        Place item : ?
        """
        name = port['name']
        interface = port.get_interface()

        ## Hidden state
        ## TODO
        if not port.get('showwidget', not port.is_hidden()):
            self.widgets.append(None)
            return

        # interface class or instance ?
        if(type(interface) == IInterfaceMetaClass):
            interface = interface()

        wclass = self.type_map.get(interface.__class__, None)

        if(wclass):
            #print widget
            widgetT = wclass(self.node, widget, name, interface)
            widgetT.update_state()
            layout.addWidget(widgetT)
            self.widgets.append(widgetT)
            self.empty = False
        else:
            self.widgets.append(None)

        # If there is no subwidget, add the name
        if( self.empty ):
            pass
#             label = QtGui.QLabel(self)
#             label.setText(self.node.__class__.__name__+
#                           " (No Widget available)")

#             layout.addWidget(label)


    def place_group( self, widget, group, layout ):
        """<Short description of the function functionality.>

        <Long description of the function functionality.>

        :param widget: <Description of arg1 meaning>
        :type widget:  <Description of arg1 type>

        :return: <Description of ``return_object`` meaning>
        :raise Exception: <Description of situation raising `Exception`>

        """

        if group.layout=="-" or  group.layout=="|":
            groupW = QtGui.QGroupBox(widget)
            groupW.setTitle(group.label)
            layout.addWidget( groupW )
            if group.layout=="-": nlayout = QtGui.QHBoxLayout(self)
            else: nlayout = QtGui.QVBoxLayout(self)
            groupW.setLayout(nlayout)
        else:
            tab=QtGui.QTabWidget( self )
            layout.addWidget( tab )

        for i in group.content:
            if group.layout=="t":
                groupW = QtGui.QWidget()
                nlayout = QtGui.QVBoxLayout(self)
                groupW.setLayout(nlayout)
                if isinstance( i, Item ):
                    name=self.node.get_input_port( i.name ).get_label()
                else: name=group.label
                tab.addTab(groupW, name)
            self.place(groupW, i, nlayout)


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

