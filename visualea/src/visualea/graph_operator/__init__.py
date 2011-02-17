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

import weakref
from PyQt4 import QtGui, QtCore
from openalea.core.observer import Observed
from openalea.grapheditor import qtgraphview
from openalea.core.compositenode import CompositeNodeFactory

def do_imports():
    import dataflow, layout, color, vertex, port, anno

class GraphOperator(Observed):

    vertexType     = None
    annotationType = None
    edgeType       = None

    def __init__(self, graph, graphScene=None, clipboard=None, siblings=None):
        Observed.__init__(self)
        do_imports()
        self.__ops = [ dataflow.DataflowOperators(self), layout.LayoutOperators(self),
                       color.ColorOperators(self), vertex.VertexOperators(self),
                       port.PortOperators(self), anno.AnnotationOperators(self) ]

        self.__availableNames = {}

        for operator in self.__ops:
            for meth in dir(operator):
                self.__availableNames[meth] = getattr(operator, meth)

        self.graph          = graph
        self.scene          = graphScene
        self.clipboard      = clipboard or CompositeNodeFactory("Clipboard")
        self.siblings       = siblings or []
        self.__interpreter  = None
        self.__pkgmanager   = None
        self.vertexItem     = None
        self.annotationItem = None
        self.portItem       = None


    ######################################
    # Get Qt Actions for methods in here #
    ######################################
    def get_action(self, actionName=None, parent=None, fName=None, **kwargs):
        if actionName is None and parent is None and fName is not None:
            return self.__get_wrapped(fName, kwargs)[0]
        action = QtGui.QAction(actionName, parent)
        return self.bind_action(action, fName, kwargs)

    def bind_action(self, action, fName, kwargs=None):
        func, argcount = self.__get_wrapped(fName, kwargs)
        #self.unbind_action(action, fName)
        action.triggered.connect(func)
        data = QtCore.QVariant(func)
        action.setData(data)
        return action

    def unbind_action(self, action, fName=None):
        data = action.data()
        if not data.isNull() and data.isValid():
            func = data.toPyObject()
            action.triggered.disconnect(func)
        # this is probably broken! __get_wrapped returns new functions each time
        # func, argcount = self.__get_wrapped(fName)
        # action.triggered.disconnect(func)
        return action

    def __add__(self, other):
        self.bind_action(*other)

    def __sub__(self, other):
        self.unbind_action(*other)

    __call__ = get_action

    def __get_wrapped(self, fName, kwargs=None):
        func = self.__availableNames.get(fName)
        defaults = func.im_func.func_defaults
        if defaults:
            argcount = func.func_code.co_argcount - len(defaults)
        else:
            argcount = func.func_code.co_argcount
        kwargs = kwargs or dict()
        #used for graph_operator methods that don't
        #handle the QAction's boolean sent by trigger
        def wrappedGOPNoBool(*args):
            if self.get_graph() is None : return
            #we receive a boolean from the triggered signal,
            #but we cant handle it
            args = args[1:]
            return func(*args, **kwargs)
        #used for graph_operator methods that DO
        #handle the QAction's boolean sent by trigger
        def wrappedGOPBool(*args):
            if self.get_graph() is None : return
            return func(*args, **kwargs)


        if argcount < 2:
            return wrappedGOPNoBool, argcount
        else:
            return wrappedGOPBool, argcount

    ###########
    # setters #
    ###########
    def set_vertex_item(self, vertexItem):
        self.vertexItem = weakref.ref(vertexItem)

    def set_annotation_item(self, annotationItem):
        self.annotationItem = weakref.ref(annotationItem)

    def set_port_item(self, portitem):
        self.portItem = weakref.ref(portitem)

    ###########
    # getters #
    ###########
    def get_interpreter(self):
        return None

    def get_clipboard(self):
        return self.clipboard

    def get_siblings(self):
        return self.siblings

    def get_package_manager(self):
        from openalea.core.pkgmanager import PackageManager
        return PackageManager()

    def get_sensible_parent(self):
        return QtGui.QApplication.topLevelWidgets()[0]

    def get_graph_scene(self):
        return self.scene

    def get_graph(self):
        scene = self.get_graph_scene()
        if scene:
            return scene.get_graph()
        else:
            return self.graph
