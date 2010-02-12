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
from openalea.grapheditor import qtgraphview
from openalea.visualea.util import open_dialog, exception_display, busy_cursor
from openalea.visualea.dialogs import NewGraph, FactorySelector
from openalea.visualea.dialogs import IOConfigDialog
from openalea.core.compositenode import CompositeNodeFactory
from openalea.core import export_app


class DataflowOperators(object):
    @exception_display
    @busy_cursor
    def graph_run(self):
        self.get_graph().eval_as_expression()

    def graph_reset(self):
        ret = QtGui.QMessageBox.question(self, 
                                         "Reset Workspace",
                                         "Reset will delete all input values.\n" + \
                                             "Continue ?\n",
                                         QtGui.QMessageBox.Yes, 
                                         QtGui.QMessageBox.No,)
        if(ret == QtGui.QMessageBox.No):
            return
        self.get_graph().reset() #check what this does signal-wise

    def graph_invalidate(self):
        self.get_graph().invalidate() #TODO : check what this does signal-wise
        
    def graph_remove_selection(self, items=None):
        if(not items):
            items = self.get_graph_view().get_selected_items()
        if(not items): return
        for i in items:
            if isinstance(i, qtgraphview.Vertex):
                if self.get_graph().is_vertex_protected(i.vertex()): continue
                self.get_graph().remove_vertex(i.vertex())
            elif isinstance(i, qtgraphview.Edge):
                self.get_graph().remove_edge((i.srcBBox().vertex(), i.srcBBox()),
                                         (i.dstBBox().vertex(), i.dstBBox()) )
            elif isinstance(i, qtgraphview.Annotation):
                self.get_graph().remove_vertex(i.annotation())

    def graph_group_selection(self):
        """
        Export selected node in a new factory
        """
        widget = self.get_graph_view()

        # FIRST WE PREPARE THE USER INTERFACE STUFF
        # ------------------------------------------
        # Get default package id
        default_factory = self.get_graph().factory
        if(default_factory and default_factory.package):
            pkg_id = default_factory.package.name
            name = default_factory.name + "_grp_" + str(len(default_factory.package))
        else:
            pkg_id = None
            name = ""

        dialog = NewGraph("Group Selection", self.get_package_manager(), widget, 
                          io=False, pkg_id=pkg_id, name=name)
        ret = dialog.exec_()
        if(not ret): return

        # NOW WE DO THE HARD WORK
        # -----------------------
        
        factory = dialog.create_cnfactory(self.get_package_manager())
        items = widget.get_selected_items(qtgraphview.Vertex)
        if(not items): return None
        
        pos = widget.get_selection_center(items)
        def cmp_x(i1, i2):
            return cmp(i1.scenePos().x(), i2.scenePos().x())
        items.sort(cmp=cmp_x)        

        # Instantiate the new node:
        itemIds = [i.vertex().get_id() for i in items]
        self.get_graph().to_factory(factory, itemIds, auto_io=True)
        newVert = factory.instantiate([self.get_graph().factory.get_id()])

        # Evaluate the new connections:
        def evaluate_new_connections(newGraph, newGPos, idList):
            newId    = self.get_graph().add_vertex(newGraph, [newGPos.x(), newGPos.y()])
            newEdges = self.get_graph().compute_external_io(idList, newId)
            for edges in newEdges:
                self.get_graph().add_edge((edges[0], edges[1]), 
                                      (edges[2], edges[3]))
            self.graph_remove_selection(items)

        def correct_positions(newGraph):
            _minX, _minY = None, None
            for vid in newGraph.vertices():
                if vid == newGraph.id_in or vid == newGraph.id_out:
                    continue
                node = newGraph.node(vid)
                if not _minX and not _minY:
                    _minX, _minY = node.get_ad_hoc_dict().get_metadata("position")
                _nminX, _nminY = node.get_ad_hoc_dict().get_metadata("position")
                _minX= min(_minX, _nminX)
                _minY= min(_minY, _nminY)
            for vid in newGraph.vertices():
                if vid == newGraph.id_in or vid == newGraph.id_out:
                    continue
                pos = newGraph.node(vid).get_ad_hoc_dict().get_metadata("position")
                # the 50 is there to have a margin at the top and right of the
                # nodes.
                pos[0] = pos[0] - _minX + 50 
                pos[1] = pos[1] - _minY + 50
                
        if newVert:
            #to prevent too many redraws during the grouping we queue events then process
            #them all at once.
            widget.queue_call_notifications(evaluate_new_connections, newVert, pos, itemIds)
            correct_positions(newVert)

        
        try:
            factory.package.write()
        except AttributeError, e:
            mess = QtGui.QMessageBox.warning(self, "Error",
                                             "Cannot write Graph model on disk. :\n"+
                                             "You try to write in a System Package:\n")
        self.notify_listeners(("graphoperator_newfactory", factory))

        
    def graph_copy(self):
        """ Copy Selection """
        if(self.get_interpreter().hasFocus()):
            try:
                self.get_interpreter().copy()
            except:
                pass
        else:
            s = self.get_graph_view().get_selected_items(qtgraphview.Vertex)
            s = [i.vertex().get_id() for i in s]
            if(not s): return 
            self.get_session().clipboard.clear()
            self.get_graph().to_factory(self.get_session().clipboard, s, auto_io=False)

    def graph_cut(self):
        if(self.get_interpreter().hasFocus()):
            try:
                self.get_interpreter().copy()
            except:
                pass
        else:
            self.graph_copy()
            self.graph_remove_selection()

    def graph_paste(self):
        """ Paste from clipboard """
        if(self.get_interpreter().hasFocus()):
            try:
                self.get_interpreter().paste()
            except:
                pass
        else:
            widget = self.get_graph_view()

            # Get Position from cursor
            position = widget.mapToScene(
                widget.mapFromGlobal(widget.cursor().pos()))
            widget.select_added_elements(True)
            
            cnode = self.get_session().clipboard.instantiate()

            min_x = min([cnode.node(vid).get_ad_hoc_dict().get_metadata("position")[0] for vid in cnode if vid not in (cnode.id_in, cnode.id_out)])
            min_y = min([cnode.node(vid).get_ad_hoc_dict().get_metadata("position")[1] for vid in cnode if vid not in (cnode.id_in, cnode.id_out)])

            def lam(n):
                x = n.get_ad_hoc_dict().get_metadata("position")
                x = [x[0]-min_x + position.x()+30, x[1]-min_y + position.y()+30]
                n.get_ad_hoc_dict().set_metadata("position", x)
            
            modifiers = [("position", lam)]
            widget.scene().clearSelection()
            new_ids = self.get_session().clipboard.paste(self.get_graph(), 
                                                     modifiers, 
                                                     meta=True)


    def graph_close(self):
       # Try to save factory if widget is a graph
        widget = self.get_graph_view()
        index  = widget.parent().indexOf(widget)

        try:
            modified = self.get_graph().graph_modified
            if(modified):
                # Generate factory if user want
                ret = QtGui.QMessageBox.question(widget, "Close Workspace",
                                                 "Graph has been modified.\n"+
                                                 "Do you want to report modification "+
                                                 "in the model ?\n",
                                                 QtGui.QMessageBox.Yes, 
                                                 QtGui.QMessageBox.No,)
            
                if(ret == QtGui.QMessageBox.Yes):
                    self.graph_export_to_factory()

        except Exception, e:
            print "graph_close exception", e
            pass

        # Update session
        self.get_session().close_workspace(index, False)
        widget.parent().removeWidget(widget)
        widget.close()

    def graph_export_to_factory(self):
        """
        Export workspace index to its factory
        """
        widget = self.get_graph_view()
        index  = widget.parent().indexOf(widget)

        # Get a composite node factory
        dialog = FactorySelector(self.get_graph().factory, widget)
            
        # Display Dialog
        ret = dialog.exec_()
        if(ret == 0): return None
        factory = dialog.get_factory()

        self.get_graph().to_factory(factory, None)
        self.get_graph().factory = factory
        caption = "Workspace %i - %s"%(index, factory.name)
        
        widget.parent().parent().setTabText(index, caption)

        try:
            factory.package.write()

        except AttributeError, e:
            mess = QtGui.QMessageBox.warning(self, "Error",
                                             "Cannot write Graph model on disk. :\n"+
                                             "Trying to write in a System Package!\n")
        self.notify_listeners(("graphoperator_newfactory", factory))

    def graph_configure_io(self):
        """ Configure workspace IO """
        widget = self.get_graph_view()

        dialog = IOConfigDialog(self.get_graph().input_desc,
                                self.get_graph().output_desc,
                                parent=widget)
        ret = dialog.exec_()

        if(ret):
            self.get_graph().set_io(dialog.inputs, dialog.outputs)



    def graph_reload_from_factory(self, index=None):
        """ Reload a tab node givin its index"""
        widget = self.get_graph_view()
        if(index is None):
            index  = widget.parent().indexOf(widget)

        name = self.get_graph().factory.name

        if(self.get_graph().graph_modified):
            # Show message
            ret = QtGui.QMessageBox.question(widget, "Reload workspace '%s'"%(name),
                                             "Reload will discard recent changes on "\
                                                 + "workspace '%s'.\n"%(name)+
                                             "Continue ?\n",
                                             QtGui.QMessageBox.Yes, QtGui.QMessageBox.No,)
            
            if(ret == QtGui.QMessageBox.No):
                return


        newGraph = self.get_graph().factory.instantiate()
        widget.set_graph(newGraph)
        widget.rebuild_scene()
        self.get_session().workspaces[index] = newGraph

    def __get_current_factory(self, name):
        """ Build a temporary factory for current workspace
        Return (node, factory)
        """
        
        tempfactory = CompositeNodeFactory(name = name)
        self.get_graph().to_factory(tempfactory)
        
        #self.get_graph() in this case returns an adapter.
        #adapter.graph() returns the real graph.
        return (self.get_graph().graph(), tempfactory)
    
    def graph_preview_application(self, name="Preview"):
        """ Open Application widget """
        widget = self.get_graph_view()
        
        graph, tempfactory = self.__get_current_factory(name)
        w = qtgraphview.View(widget.parent(), graph)
        w.viewport().setEnabled(False)

        open_dialog(widget, w, 'Preview Application')
        return graph, tempfactory


    def graph_export_application(self):
        """ Export current workspace composite node to an Application """
        widget = self.get_graph_view()

        # Get Filename
        filename = QtGui.QFileDialog.getSaveFileName(
            widget, "Python Application", 
            QtCore.QDir.homePath(), "Python file (*.py)")
        
        filename = str(filename)
        if(not filename):
            return

        # Get Application Name
        result, ok = QtGui.QInputDialog.getText(widget, "Application Name", "",
                                                QtGui.QLineEdit.Normal, "")
        if(not ok):
            return

        name = str(result)
        if(not name) : name = "OpenAlea Application"
        
        graph, tempfactory = self.graph_preview_application(name)
        #export_app comes from openalea.core
        export_app.export_app(name, filename, tempfactory) 
        
