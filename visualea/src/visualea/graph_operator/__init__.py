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

from Qt import QtCore, QtGui, QtWidgets

from openalea.core.observer import Observed
from openalea.core.compositenode import CompositeNodeFactory

from openalea.qt.compat import to_qvariant

class GraphOperator(Observed):

    # These are not filled by dataflowview itself to avoid recursive imports
    # as dataflowview is imported in modules from this package.
    vertexType        = None
    annotationType    = None
    edgeType          = None
    globalInterpreter = None

    def __init__(self, graph, graphScene=None, clipboard=None, siblings=None, interpreter=None, graphAdapter=None):
        Observed.__init__(self)

        do_imports()
        configure_dataflow_types()

        self.__ops = [ dataflow.DataflowOperators(self), layout.LayoutOperators(self),
                       color.ColorOperators(self), vertex.VertexOperators(self),
                       port.PortOperators(self), anno.AnnotationOperators(self) ]

        self.__availableNames = {}

        for operator in self.__ops:
            for meth in dir(operator):
                self.__availableNames[meth] = getattr(operator, meth)

        self.__graph        = graph
        self.__adapter      = graphAdapter
        self.__scene        = graphScene
        self.__clipboard    = clipboard or CompositeNodeFactory("Clipboard")
        self.__siblings     = siblings or []
        self.__interpreter  = interpreter or GraphOperator.globalInterpreter

        # when working on current item these can be set
        self.__vertexItem     = None
        self.__annotationItem = None
        self.__portItem       = None


    ######################################
    # Get Qt Actions for methods in here #
    ######################################
    def get_action(self, actionName=None, parent=None, fName=None, **kwargs):
        if actionName is None and parent is None and fName is not None:
            return self.__get_wrapped(fName, kwargs)[0]
        action = QtWidgets.QAction(actionName, parent)
        return self.bind_action(action, fName, kwargs)

    def bind_action(self, action, fName, kwargs=None):
        func, argcount = self.__get_wrapped(fName, kwargs)
        #self.unbind_action(action, fName)
        action.triggered.connect(func)
        data = to_qvariant(func)
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
    # getters #
    ###########
    def get_interpreter(self):
        return self.__interpreter

    def get_clipboard(self):
        return self.__clipboard

    def get_siblings(self):
        return self.__siblings

    def get_package_manager(self):
        from openalea.core.pkgmanager import PackageManager
        return PackageManager()

    def get_sensible_parent(self):
        # TODO improve this:
        return QtWidgets.QApplication.topLevelWidgets()[0]

    def get_graph_scene(self):
        return self.__scene

    def get_graph(self):
        scene = self.get_graph_scene()
        if scene:
            return scene.get_graph()
        else:
            return self.__graph

    def get_graph_adapter(self):
        scene = self.get_graph_scene()
        if scene:
            return scene.get_adapter()
        else:
            return self.__adapter

    def get_vertex_item(self):
        return self.__vertexItem() if self.__vertexItem else None

    def get_annotation_item(self):
        return self.__annotationItem() if self.__annotationItem else None

    def get_port_item(self):
        return self.__portItem() if self.__portItem else None

    ###########
    # setters #
    ###########
    def set_vertex_item(self, vertexItem):
        self.__vertexItem = weakref.ref(vertexItem)

    def set_annotation_item(self, annotationItem):
        self.__annotationItem = weakref.ref(annotationItem)

    def set_port_item(self, portitem):
        self.__portItem = weakref.ref(portitem)



def do_imports():
    import dataflow, layout, color, vertex, port, anno

def configure_dataflow_types():
    from openalea.visualea.dataflowview import vertex, anno, edge
    GraphOperator.vertexType        = vertex.GraphicalVertex
    GraphOperator.annotationType    = anno.GraphicalAnnotation
    GraphOperator.edgeType          = edge.GraphicalEdge
