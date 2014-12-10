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
from openalea.vpltk.qt import qt
from openalea.visualea.graph_operator.base import Base
from openalea.visualea.graph_operator import compositenode_inspector

from openalea.visualea.util import busy_cursor, exception_display, open_dialog
from openalea.visualea.dialogs import DictEditor, ShowPortDialog, NodeChooser

from openalea.core.compositenode import CompositeNode
from openalea.core import observer, node


INSPECTOR_EDGE_OFFSET = 15


class VertexOperators(Base):
    __compositeWidgetMap__ = weakref.WeakKeyDictionary()

    def vertex_composite_inspect(self):
        master = self.master
        vertex = master.get_vertex_item().vertex()
        parwidget = master.get_sensible_parent()
        if not isinstance(vertex, CompositeNode):
            return

        widget = VertexOperators.__compositeWidgetMap__.get(vertex, None)
        if(widget):
            if(widget.isVisible()):
                widget.raise_()
                widget.activateWindow()
            else:
                widget.show()
            return
        else:
            widget = compositenode_inspector.CompositeInspector.create_view(vertex,
                                                                            parent=parwidget)
            VertexOperators.__compositeWidgetMap__[vertex] = widget

            ###################################
            # -- Let's fix the window size -- #
            ###################################
            scRectF = widget.scene().itemsBoundingRect()
            tl = scRectF.topLeft()
            # -- check the rect doesn't have crazy negative values or too close to screen edge
            # -- or else we loose window or window decorations.
            scRectF.moveTo(INSPECTOR_EDGE_OFFSET, INSPECTOR_EDGE_OFFSET * 2)
            scRect = scRectF.toRect()
            screenGeom = qt.QtGui.QApplication.instance().desktop().screenGeometry(widget)
            ratio = 1.
            if not screenGeom.contains(scRect):
                if scRect.width() > screenGeom.width():
                    ratio = screenGeom.width() / scRectF.width() * 0.75
                    scRect.setWidth(ratio * scRect.width())
                if scRect.height() > screenGeom.height():
                    ratio = screenGeom.height() / scRectF.height() * 0.75
                    scRect.setHeight(ratio * scRect.height())
            widget.resize(scRect.size())
            widget.scale(1. / ratio, 1. / ratio)
            ##################
            # -- Finished -- #
            ##################
            widget.setWindowTitle("Inspecting " + vertex.get_caption())
#            widget.show_entire_scene()
            widget.show()

    @exception_display
    @busy_cursor
    def vertex_run(self):
        master = self.master
        master.get_graph().eval_as_expression(master.get_vertex_item().vertex().get_id())

    def vertex_open(self):
        master = self.master
        widget = master.get_sensible_parent()
        item = master.get_vertex_item()
        vertex = item.vertex()
        vwidget = item.get_editor_instance()
        if(vwidget):
            if(vwidget.isVisible()):
                vwidget.raise_()
                vwidget.activateWindow()
            else:
                vwidget.show()
            return

        # Create the dialog.
        # NOTE: WE REQUEST THE MODEL TO CREATE THE DIALOG
        # THIS IS NOT DESIRED BECAUSE IT COUPLES THE MODEL
        # TO THE UI.
        factory = vertex.get_factory()
        if(not factory):
            return
        innerWidget = factory.instantiate_widget(vertex, None)
        if(not innerWidget):
            return
        if (innerWidget.is_empty()):
            innerWidget.close()
            del innerWidget
            return

        title = innerWidget.windowTitle()
        if title == "":
            title = factory.get_id()

        vwidget = open_dialog(widget,
                              innerWidget,
                              title,
                              False)

        item.set_editor_instance(vwidget)

    def vertex_remove(self):
        master = self.master
        master.get_graph_scene().remove_vertex(master.get_vertex_item().vertex())

    def vertex_reset(self):
        self.master.get_vertex_item().vertex().reset()

    @classmethod
    def vertex_observer_copy(cls, oldVertex, newVertex):
        """ Copies attributes from old vertex to new vertex, including listeners."""
        oldVertex.copy_to(newVertex)

    @exception_display
    @busy_cursor
    def vertex_replace(self):
        """ Replace a node by an other """
        master = self.master
        adapter = master.get_graph_scene().get_adapter()
        widget = master.get_sensible_parent()
        dialog = NodeChooser(widget)
        vItem = master.get_vertex_item()
        dialog.search('', vItem.vertex().get_nb_input(),
                      vItem.vertex().get_nb_output())
        ret = dialog.exec_()
        if(not ret):
            return

        factory = dialog.get_selection()
        oldVertex = vItem.vertex()
        newVertex = factory.instantiate()
        adapter.replace_vertex(oldVertex, newVertex)
        self.vertex_observer_copy(oldVertex, newVertex)

    def vertex_reload(self):
        """ Reload the vertex """
        # Reload package
        master = self.master
        vItem = master.get_vertex_item()
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

        n = self.master.get_vertex_item().vertex()
        (result, ok) = qt.QtGui.QInputDialog.getText(None, "Node caption", "",
                                                     qt.QtGui.QLineEdit.Normal, n.caption)
        if(ok):
            n.caption = str(result)

    def vertex_show_hide_ports(self):
        """ Open port show/hide dialog """
        widget = self.master.get_sensible_parent()
        editor = ShowPortDialog(self.master.get_vertex_item().vertex(), widget)
        editor.exec_()

    def vertex_mark_user_app(self, val):
        master = self.master
        master.get_graph().set_continuous_eval(master.get_vertex_item().vertex().get_id(),
                                               bool(val))

    def vertex_set_lazy(self, val):
        self.master.get_vertex_item().vertex().lazy = val

    def vertex_block(self, val):
        self.master.get_vertex_item().vertex().block = val

    def vertex_edit_internals(self):
        """ Edit node internal data """
        master = self.master
        widget = master.get_sensible_parent()
        editor = DictEditor(master.get_vertex_item().vertex().internal_data, widget)
        ret = editor.exec_()

        if(ret):
            for k in editor.modified_key:
                master.get_vertex_item().vertex().set_data(k, editor.pdict[k])
