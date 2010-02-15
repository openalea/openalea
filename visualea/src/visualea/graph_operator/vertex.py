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
import weakref
from openalea.visualea.util import busy_cursor, exception_display, open_dialog
from openalea.visualea.dialogs import DictEditor, ShowPortDialog, NodeChooser
from openalea.grapheditor import qtgraphview
from openalea.core import observer, node


class VertexOperators(object):
    def __init__(self):
        # ---reference to the widget of this vertex---
        self._vertexWidget = None
        self.vertexItem = None

    def set_vertex_item(self, vertexItem):
        self.vertexItem = weakref.ref(vertexItem)
        

    def vertex_composite_inspect(self):
        widget = qtgraphview.View(self.get_graph_view(), self.vertexItem().vertex())
        widget.setWindowFlags(QtCore.Qt.Window)
        widget.setWindowTitle("Inspecting " + self.vertexItem().vertex().get_caption())        
        widget.show_entire_scene()
        widget.show()
        
    @exception_display
    @busy_cursor
    def vertex_run(self):
        self.get_graph().eval_as_expression(self.vertexItem().vertex().get_id())        

    def vertex_open(self):
        if(self._vertexWidget):
            if(self._vertexWidget.isVisible()):
                self._vertexWidget.raise_ ()
                self._vertexWidget.activateWindow ()
            else:
                self._vertexWidget.show()
            return

        factory = self.vertexItem().vertex().get_factory()
        if(not factory) : return
        # Create the dialog. 
        # NOTE: WE REQUEST THE MODEL TO CREATE THE DIALOG
        # THIS IS NOT DESIRED BECAUSE IT COUPLES THE MODEL
        # TO THE UI.
        innerWidget = factory.instantiate_widget(self.vertexItem().vertex(), None)
        if(not innerWidget) : return 
        if (innerWidget.is_empty()):
            innerWidget.close()
            del innerWidget
            return

        self._vertexWidget = open_dialog(self.get_graph_view(), innerWidget, factory.get_id(), False)

    def vertex_remove(self):
        self.get_graph().remove_vertex(self.vertexItem().vertex())

    def vertex_reset(self):
        self.vertexItem().vertex().reset()

    def vertex_observer_swap(self, oldVertex, newVertex):
        """replaces the actor of a vertex by another one in the views only!
        not model-wise. For that, use vertex_replace, vertex_reload."""
        self.vertexItem().terminate_from_model()  # graphical vertex clears its input and output port
        oldVertex.copy_to(newVertex)
        self.vertexItem().initialise_from_model() # graphical vertex restarts
        #currently, the grapheditor widget maps models with graphical items
        #to track which graphic item to delete when something is being
        #deleted in the model:
        self.get_graph_view()._unregister_widget_from_model(self.vertexItem(), oldVertex)
        self.get_graph_view()._register_widget_with_model(self.vertexItem(), newVertex)

    @exception_display
    @busy_cursor
    def vertex_replace(self):
        """ Replace a node by an other """
        self.dialog = NodeChooser(self.get_graph_view())
        self.dialog.search('', self.vertexItem().vertex().get_nb_input(), 
                           self.vertexItem().vertex().get_nb_output())
        ret = self.dialog.exec_()
        if(not ret): return
        
        factory = self.dialog.get_selection()
        oldVertex = self.vertexItem().vertex()
        newVertex = factory.instantiate()
        self.get_graph().replace_vertex(oldVertex, newVertex)
        self.vertex_observer_swap(oldVertex, newVertex)

    def vertex_reload(self):
        """ Reload the vertex """
        # Reload package
        factory = self.vertexItem().vertex().factory
        package = factory.package
        if(package):
            package.reload()

        # Reinstantiate the vertex
        newVertex = factory.instantiate()
        oldVertex = self.vertexItem().vertex()
        self.get_graph().set_actor(oldVertex.get_id(), newVertex)
        self.vertex_observer_swap(oldVertex, newVertex)        

    def vertex_set_caption(self):
        """ Open a input dialog to set node caption """

        n = self.vertexItem().vertex()
        (result, ok) = QtGui.QInputDialog.getText(None, "Node caption", "",
                                   QtGui.QLineEdit.Normal, n.caption)
        if(ok):
            n.caption = str(result) #I HATE PROPERTIES, REALLY!

    def vertex_show_hide_ports(self):
        """ Open port show/hide dialog """
        editor = ShowPortDialog(self.vertexItem().vertex(), self.get_graph_view())
        editor.exec_()

    def vertex_mark_user_app(self, val):
        self.get_graph().set_continuous_eval(self.vertexItem().vertex().get_id(), bool(val))

    def vertex_set_lazy(self, val):
        self.vertexItem().vertex().lazy = val #I DO HATE PROPERTIES, REALLY!

    def vertex_block(self, val):
        self.vertexItem().vertex().block = val #I DEFINITELY DO HATE PROPERTIES, REALLY!

    def vertex_edit_internals(self):
        """ Edit node internal data """
        editor = DictEditor(self.vertexItem().vertex().internal_data, self.get_graph_view())
        ret = editor.exec_()

        if(ret):
            for k in editor.modified_key:
                self.vertexItem().vertex().set_data(k, editor.pdict[k])

