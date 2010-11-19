# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2006-2010 INRIA - CIRAD - INRA
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
import base as graphOpBase
from PyQt4 import QtGui, QtCore
from openalea.core.compositenode import CompositeNode
from openalea.visualea.util import busy_cursor, exception_display, open_dialog
from openalea.visualea.dialogs import DictEditor, ShowPortDialog, NodeChooser

from openalea.core import observer, node
import compositenode_inspector

INSPECTOR_EDGE_OFFSET = 15

class VertexOperators(graphOpBase.Base):
    __vertexWidgetMap__ = weakref.WeakKeyDictionary()
    __compositeWidgetMap__ = weakref.WeakKeyDictionary()

    def __init__(self, master):
        graphOpBase.Base.__init__(self, master)
        # ---reference to the widget of this vertex---
        self._vertexWidget = None

    def vertex_composite_inspect(self):
        from openalea.visualea.dataflowview import GraphicalGraph
        master = self.master
        vertex = master.vertexItem().vertex()
        view   = master.get_graph_view()
        if not isinstance(vertex, CompositeNode):
            return

        widget= VertexOperators.__compositeWidgetMap__.get(vertex, None)
        if(widget):
            if(widget.isVisible()):
                widget.raise_ ()
                widget.activateWindow ()
            else:
                widget.show()
            return
        else:
            widget = compositenode_inspector.CompositeInspector.create_view(vertex, parent = view)
            VertexOperators.__compositeWidgetMap__[vertex] = widget

            ###################################
            # -- Let's fix the window size -- #
            ###################################
            scRectF = widget.scene().itemsBoundingRect()
            tl      = scRectF.topLeft()
            # -- check the rect doesn't have crazy negative values or too close to screen edge
            # -- or else we loose window or window decorations.
            scRectF.moveTo(INSPECTOR_EDGE_OFFSET, INSPECTOR_EDGE_OFFSET*2)

            scRect     = scRectF.toRect()
            screenGeom = QtGui.QApplication.instance().desktop().screenGeometry(widget)
            if screenGeom.contains(scRect):
                widget.setGeometry(scRect)
            else:
                if scRect.width() > screenGeom.width():
                    ratio    = screenGeom.width() / scRectF.width()*0.75
                    scRect.setWidth(ratio*scRect.width())
                if scRect.height() > screenGeom.height():
                    ratio    = screenGeom.height() / scRectF.height()*0.75
                    scRect.setHeight(ratio*scRect.height())
                widget.setGeometry(scRect)
            ##################
            # -- Finished -- #
            ##################

            widget.set_operators(master.__main__.operator, master)
            widget.setWindowTitle("Inspecting " + vertex.get_caption())
            widget.show_entire_scene()
            widget.show()

    @exception_display
    @busy_cursor
    def vertex_run(self):
        master = self.master
        master.get_graph().eval_as_expression(master.vertexItem().vertex().get_id())

    def vertex_open(self):
        master = self.master
        vertex = master.vertexItem().vertex()
        vwidget = VertexOperators.__vertexWidgetMap__.get(vertex, None)
        if(vwidget):
            if(vwidget.isVisible()):
                vwidget.raise_ ()
                vwidget.activateWindow ()
            else:
                vwidget.show()
            return

        # Create the dialog.
        # NOTE: WE REQUEST THE MODEL TO CREATE THE DIALOG
        # THIS IS NOT DESIRED BECAUSE IT COUPLES THE MODEL
        # TO THE UI.
        factory = vertex.get_factory()
        if(not factory) : return
        innerWidget = factory.instantiate_widget(vertex, None)
        if(not innerWidget) : return
        if (innerWidget.is_empty()):
            innerWidget.close()
            del innerWidget
            return

        title = innerWidget.windowTitle()
        if title == "":
            title = factory.get_id()

        VertexOperators.__vertexWidgetMap__[vertex] = open_dialog(master.get_graph_view(),
                                                                  innerWidget,
                                                                  title,
                                                                  False)


    def vertex_remove(self):
        master = self.master
        master.get_graph_scene().remove_vertex(master.vertexItem().vertex())


    def vertex_reset(self):
        self.master.vertexItem().vertex().reset()


    @classmethod
    def vertex_observer_copy(cls, oldVertex, newVertex):
        """ Copies attributes from old vertex to new vertex, including listeners."""
        oldVertex.copy_to(newVertex)

    @exception_display
    @busy_cursor
    def vertex_replace(self):
        """ Replace a node by an other """
        master  = self.master
        adapter = master.get_graph_scene().get_adapter()
        dialog = NodeChooser(master.get_graph_view())
        vItem = master.vertexItem()
        dialog.search('', vItem.vertex().get_nb_input(),
                      vItem.vertex().get_nb_output())
        ret = dialog.exec_()
        if(not ret): return

        factory = dialog.get_selection()
        oldVertex = vItem.vertex()
        newVertex = factory.instantiate()
        adapter.replace_vertex(oldVertex, newVertex)
        self.vertex_observer_copy(oldVertex, newVertex)


    def vertex_reload(self):
        """ Reload the vertex """
        # Reload package
        master = self.master
        vItem = master.vertexItem()
        factory = vItem.vertex().factory
        package = factory.package
        if(package):
            package.reload()

        # Reinstantiate the vertex
        newVertex = factory.instantiate()
        oldVertex = vItem.vertex()
        master.get_graph().set_actor(oldVertex.get_id(), newVertex)
        self.vertex_observer_copy(oldVertex, newVertex)


    def vertex_set_caption(self):
        """ Open a input dialog to set node caption """

        n = self.master.vertexItem().vertex()
        (result, ok) = QtGui.QInputDialog.getText(None, "Node caption", "",
                                   QtGui.QLineEdit.Normal, n.caption)
        if(ok):
            n.caption = str(result) #I HATE PROPERTIES, REALLY!


    def vertex_show_hide_ports(self):
        """ Open port show/hide dialog """
        editor = ShowPortDialog(self.master.vertexItem().vertex(), self.master.get_graph_view())
        editor.exec_()


    def vertex_mark_user_app(self, val):
        master = self.master
        master.get_graph().set_continuous_eval(master.vertexItem().vertex().get_id(), bool(val))


    def vertex_set_lazy(self, val):
        self.master.vertexItem().vertex().lazy = val #I DO HATE PROPERTIES, REALLY!


    def vertex_block(self, val):
        self.master.vertexItem().vertex().block = val #I DEFINITELY DO HATE PROPERTIES, REALLY!


    def vertex_edit_internals(self):
        """ Edit node internal data """
        master = self.master
        editor = DictEditor(master.vertexItem().vertex().internal_data, self.master.get_graph_view())
        ret = editor.exec_()

        if(ret):
            for k in editor.modified_key:
                master.vertexItem().vertex().set_data(k, editor.pdict[k])


