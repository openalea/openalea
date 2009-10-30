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

import weakref
from PyQt4 import QtGui, QtCore
from openalea.core.settings import Settings
from openalea.grapheditor import qtgraphview
from openalea.visualea.util import open_dialog
from openalea.visualea.dialogs import DictEditor, ShowPortDialog, NodeChooser

#################################
# QtEvent handlers for vertices #
#################################


class GraphOperator(QtCore.QObject):
    def __init__(self, parent, vertexItem, graph=None, vertex=None):
        QtCore.QObject.__init__(self)
        self.parent = weakref.ref(parent)
        self.vertexItem = weakref.ref(vertexItem)
        if(graph): self.graph=weakref.ref(graph)
        if(vertex): self.vertex=weakref.ref(vertex)
        #used when a vertex has been opened
        self._vertexWidget=None

    ###WHAT ???? I HAVE TO DO THIS TO
    ###CORRECTLY BIND AN OPERATOR'S
    ###METHODS TO A QT SIGNAL....
    ###WHY???????????????????????????
    def __get_wrapped(self, funcname):
        def wrapper(*args):
            getattr(self,funcname,None)(*args)
        return wrapper

    def get_action(self, actionName, parent, functionName):
        action = QtGui.QAction(actionName, parent)
        QtCore.QObject.connect(action, QtCore.SIGNAL("triggered()"),
                               self.__get_wrapped(functionName))
        return action

    def __call__(self, actionName, parent, functionName):
        return self.get_action(actionName, parent, functionName)

    ######################
    # The actual methods #
    ######################

    def run_vertex(self):
        self.graph().graph().eval_as_expression(self.vertex().get_id())        

    def open_vertex(self):
        if(self._vertexWidget):
            if(self._vertexWidget.isVisible()):
                self._vertexWidget.raise_ ()
                self._vertexWidget.activateWindow ()
            else:
                self._vertexWidget.show()
            return

        factory = self.vertex().get_factory()
        if(not factory) : return
        # Create the dialog. 
        # NOTE: WE REQUEST THE MODEL TO CREATE THE DIALOG
        # THIS IS NOT DESIRED BECAUSE IT COUPLES THE MODEL
        # TO THE UI.
        innerWidget = factory.instantiate_widget(self.vertex(), None)
        if(not innerWidget) : return 
        if (innerWidget.is_empty()):
            innerWidget.close()
            del innerWidget
            return

        self._vertexWidget = open_dialog(self.parent(), innerWidget, factory.get_id(), False)

    def remove_vertex(self):
        self.graph().remove_vertex(self.vertex().get_id())

    def reset_vertex(self):
        self.vertex().reset()


    def replace_vertex_by(self):
        """ Replace a node by an other """
        
        self.dialog = NodeChooser(self.parent())
        self.dialog.search('', self.vertex().get_nb_input(), self.vertex().get_nb_output())
        ret = self.dialog.exec_()

        if(not ret): return
        
        factory = self.dialog.get_selection()
        newnode = factory.instantiate()
        self.graph().replace_vertex(self.vertex(), newnode)


    def reload_vertex(self):
        """ Reload the vertex """

        # Reload package
        factory = self.vertex().factory
        package = factory.package
        if(package):
            package.reload()

        # Reinstantiate the vertex
        newvertex = factory.instantiate()
        self.graph().graph().set_actor(self.vertex().get_id(), newvertex)
        newvertex.internal_data.update(self.vertex().internal_data)
        self.vertexItem().set_observed(newvertex)
        self.vertexItem().initialise_from_model()


    def set_vertex_caption(self):
        """ Open a input dialog to set node caption """

        n = self.vertex()
        (result, ok) = QtGui.QInputDialog.getText(None, "Node caption", "",
                                   QtGui.QLineEdit.Normal, n.caption)
        if(ok):
            n.caption = str(result) #I HATE PROPERTIES ACTUALLY!



def vertexMouseDoubleClickEvent(self, event):
    if event.button()==QtCore.Qt.LeftButton:
        # Read settings
        try:
            localsettings = Settings()
            str = localsettings.get("UI", "DoubleClick")
        except:
            str = "['open']"

        view = self.scene().views()[0]
        operator=GraphOperator(view, self, graph=self.graph, vertex=self.vertex())

        if('open' in str):
            operator.open_vertex()
        elif('run' in str):
            operator.run_vertex()


def vertexContextMenuEvent(self, event):
    """ Context menu event : Display the menu"""
    view = self.scene().views()[0]
    operator=GraphOperator(view, self, graph=self.graph, vertex=self.vertex())
    menu = QtGui.QMenu(view)

    menu.addAction(operator("Run",             menu, "run_vertex"))
    menu.addAction(operator("Open Widget",     menu, "open_vertex"))
    menu.addSeparator()
    menu.addAction(operator("Delete",          menu, "remove_vertex"))
    menu.addAction(operator("Reset",           menu, "reset_vertex"))
    menu.addAction(operator("Replace By",      menu, "replace_vertex_by"))
    menu.addAction(operator("Reload",          menu, "reload_vertex"))
    menu.addSeparator()
    menu.addAction(operator("Caption",         menu, "set_vertex_caption"))
#     menu.addAction(operator("Show/Hide ports", menu, "show_hide_vertex_port"))
# #     self.scene().connect(action, QtCore.SIGNAL("triggered()"), self.show_ports)
#     menu.addSeparator()

#     action = operator("Mark as User Application", menu, "mark_user_app_vertex")
#     action.setCheckable(True)
#     action.setChecked( bool(self.vertex().user_application))
#     menu.addAction(action)
# #     self.scene().connect(action, QtCore.SIGNAL("triggered(bool)"), self.set_user_application)


#     actionoperator("Lazy", menu, "set_lazy_vertex")
#     action.setCheckable(True)
#     action.setChecked(self.vertex().lazy)
# #     self.scene().connect(action, QtCore.SIGNAL("triggered(bool)"), self.set_lazy)
#     menu.addAction(action)

#     actionoperator("Block", menu, "block_vertex")
#     action.setCheckable(True)
#     action.setChecked(self.subnode.block)
# #     self.scene().connect(action, QtCore.SIGNAL("triggered(bool)"), self.set_block)
#     menu.addAction(action)

#     menu.addAction(operator("Internals", menu, "set_vertex_internals")
# #     self.scene().connect(action, QtCore.SIGNAL("triggered()"), self.set_internals)

    menu.move(event.screenPos())
    menu.show()
#     del menu
    event.accept()










qtgraphview.QtGraphViewVertex.set_event_handler("mouseDoubleClickEvent", 
                                                vertexMouseDoubleClickEvent)
qtgraphview.QtGraphViewVertex.set_event_handler("contextMenuEvent", 
                                                vertexContextMenuEvent)
