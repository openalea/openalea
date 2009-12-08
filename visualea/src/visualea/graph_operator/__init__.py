# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Daniel Barbeau <daniel.barbeau@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

__license__ = "Cecill-C"
__revision__ = " $Id$ "

from PyQt4 import QtGui, QtCore
from openalea.core.observer import Observed
import dataflow, layout, color, vertex

#################################
# QtEvent handlers for vertices #
#################################


class GraphOperator(Observed, 
                    dataflow.DataflowOperators,
                    layout.LayoutOperators,
                    color.ColorOperators,
                    vertex.VertexOperators):

    def __init__(self, graphView=None, graph=None):
        Observed.__init__(self)
        dataflow.DataflowOperators.__init__(self)
        layout.LayoutOperators.__init__(self)
        color.ColorOperators.__init__(self)
        vertex.VertexOperators.__init__(self)

        self.__main = None

        self.graphView = None
        self.graph     = None
        self.__session = None
        self.__interpreter = None
        self.__pkgmanager = None

        if(graphView):
            self.graphView = graphView
        if(graph):
            self.graph     = graph

    ######################################
    # Get Qt Actions for methods in here #
    ######################################
    def get_action(self, actionName, parent, functionName, *otherSlots):
        action = QtGui.QAction(actionName, parent)
        return self.bind_action(action, functionName, *otherSlots)

    def bind_action(self, action, functionName, *otherSlots):
        func, argcount = self.__get_wrapped(functionName)
        if (argcount) < 2 :
            QtCore.QObject.connect(action, QtCore.SIGNAL("triggered()"), func )
            for f in otherSlots:
                QtCore.QObject.connect(action, QtCore.SIGNAL("triggered()"), f )
        else:
            QtCore.QObject.connect(action, QtCore.SIGNAL("triggered(bool)"), func )
            for f in otherSlots:
                QtCore.QObject.connect(action, QtCore.SIGNAL("triggered(bool)"), f )
        return action

    def unbind_action(self, action, functionName=None, *otherSlots):
        func, argcount = self.__get_wrapped(functionName)
        if(argcount < 2):
            QtCore.QObject.disconnect(action, QtCore.SIGNAL("triggered()"), func )
            for f in otherSlots:
                QtCore.QObject.disconnect(action, QtCore.SIGNAL("triggered()"), f )
        else:
            QtCore.QObject.disconnect(action, QtCore.SIGNAL("triggered(bool)"), func )
            for f in otherSlots:
                QtCore.QObject.disconnect(action, QtCore.SIGNAL("triggered()"), f )
        return action    

    def __add__(self, other):
        self.bind_action(*other)

    def __sub__(self, other):
        self.unbind_action(*other)

    __call__ = get_action    
    
    def __get_wrapped(self, funcname):
        func = getattr(self,funcname,None)
        def wrapped(*args, **kwargs):
            func(*args, **kwargs)
        return wrapped, func.func_code.co_argcount 


    ###########
    # setters #
    ###########
    def set_main(self, main):
        self.__main = main

    def set_graph_view(self, graphView):
        self.graphView = graphView

    def set_graph(self, graph):
        self.graph     = graph

    def set_session(self, session):
        self.__session = session

    def set_interpreter(self, interp):
        self.__interpreter = interp

    def set_package_manager(self, pkgmanager):
        self.__pkgmanager = pkgmanager

    # def get_session(self):
    #     return self.__session

    # def get_interpreter(self):
    #     return self.__interpreter

    # def get_package_manager(self):
    #     return self.__pkgmanager
    def get_session(self):
        try:
            return self.__main.session
        except:
            return self.__session

    def get_interpreter(self):
        try:
            return self.__main.interpreterWidget
        except:
            return self.__interpreter

    def get_package_manager(self):
        try:
            return self.__main.pkgmanager
        except:
            return self.__pkgmanager

    def get_graph_view(self):
        try:
            return self.__main.tabWorkspace.currentWidget()
        except:
            return self.graphView

    def get_graph(self):
        try:
            return self.__main.tabWorkspace.currentWidget().graph()
        except:
            return self.graph
