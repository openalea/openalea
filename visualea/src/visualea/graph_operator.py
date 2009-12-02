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
from openalea.grapheditor import qtgraphview
from openalea.grapheditor import dataflowview
from openalea.core.observer import Observed
from openalea.core.compositenode import CompositeNodeFactory
from openalea.core import export_app
from openalea.visualea.util import open_dialog, exception_display, busy_cursor
from openalea.visualea.dialogs import NewGraph, NewPackage, FactorySelector
from openalea.visualea.dialogs import DictEditor, ShowPortDialog, NodeChooser
from openalea.visualea.dialogs import IOConfigDialog, PreferencesDialog, NewData

#################################
# QtEvent handlers for vertices #
#################################


class GraphOperator(Observed):
    __slots__=[]

    def __init__(self, graphView, graph):
        Observed.__init__(self)
        self.graphView = weakref.ref(graphView)
        self.graph     = weakref.ref(graph)

        self._vertexWidget = None


    ######################################
    # Get Qt Actions for methods in here #
    ######################################
    ###WHAT ???? I HAVE TO DO THIS TO
    ###CORRECTLY BIND AN OPERATOR'S
    ###METHODS TO A QT SIGNAL....
    ###WHY???????????????????????????
    def get_action(self, actionName, parent, functionName, *otherSlots):
        action = QtGui.QAction(actionName, parent)
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
    
    __call__ = get_action

    def __get_wrapped(self, funcname):
        func = getattr(self,funcname,None)
        def wrapper(*args):
            func(*args)
        return wrapper, func.func_code.co_argcount 




    ####################################
    # The actual methods -- For graphs #
    ####################################
    def set_session(self, session):
        self.__session = session

    def set_interpreter(self, interp):
        self.__interpreter = interp

    def set_package_manager(self, pkgmanager):
        self.__pkgmanager = pkgmanager

    @exception_display
    @busy_cursor
    def graph_run(self):
        self.graph().eval_as_expression()

    def graph_reset(self):
        ret = QtGui.QMessageBox.question(self, 
                                         "Reset Workspace",
                                         "Reset will delete all input values.\n" + \
                                             "Continue ?\n",
                                         QtGui.QMessageBox.Yes, 
                                         QtGui.QMessageBox.No,)
            
        if(ret == QtGui.QMessageBox.No):
            return

        self.graph().reset() #check what this does signal-wise

    def graph_invalidate(self):
        self.graph().invalidate() #check what this does signal-wise
        
    
    def graph_set_selection_color(self):
        items = self.graphView().get_selected_items()
        if(not items): return

        color = QtGui.QColorDialog.getColor( QtGui.QColor(100,100,100,255), 
                                             self.graphView())
        if not color.isValid():
            return

        color = [color.red(), color.green(), color.blue()]
        for i in items:
            if not isinstance(i, qtgraphview.QtGraphViewVertex): continue
            try:
                i.vertex().get_ad_hoc_dict().set_metadata("user_color", color)
                i.vertex().get_ad_hoc_dict().set_metadata("use_user_color", True)
            except Exception, e:
                print "graph_set_selection_color exception", e
                pass   

    def graph_remove_selection(self, items=None):
        if(not items):
            items = self.graphView().get_selected_items(vertices=False)
        if(not items): return
        for i in items:
            if isinstance(i, dataflowview.strat_vertex.GraphicalVertex):
                if self.graph().is_vertex_protected(i.vertex()): continue
                self.graph().remove_vertex(i.vertex())
            elif isinstance(i, dataflowview.strat_edge.GraphicalEdge):
                self.graph().remove_edge((i.src().vertex(), i.src()),
                                         (i.dst().vertex(), i.dst()) )
            elif isinstance(i, dataflowview.strat_anno.GraphicalAnnotation):
                self.graph().remove_vertex(i.annotation())

    def graph_group_selection(self):
        """
        Export selected node in a new factory
        """
        widget = self.graphView()
        index  = widget.parent().indexOf(widget)

        # Get default package id
        default_factory = self.graph().factory
        if(default_factory and default_factory.package):
            pkg_id = default_factory.package.name
            name = default_factory.name + "_grp_" + str(len(default_factory.package))
        else:
            pkg_id = None
            name = ""

        dialog = NewGraph("Group Selection", self.__pkgmanager, widget, 
                          io=False, pkg_id=pkg_id, name=name)
        ret = dialog.exec_()

        if(not ret): return
        
        factory = dialog.create_cnfactory(self.__pkgmanager)

        items = widget.get_selected_items()
        if(not items): return None
        
        pos = widget.get_selection_center(items)

        # Instantiate the new node
        itemids = [i.vertex().get_id() for i in items]
        self.graph().to_factory(factory, itemids, auto_io=True)
        newVert = factory.instantiate([self.graph().factory.get_id()])
        if newVert:
            widget.setEnabled(False)
            newId = self.graph().add_vertex(newVert, [pos.x(), pos.y()])
#            newVert.simulate_construction_notifications()
            newEdges = self.graph().compute_external_io(newVert, newId)
            for edges in newEdges:
                self.graph().add_edge((edges[0], edges[1]), 
                                      (edges[2], edges[3]))
            self.graph_remove_selection(items)
            widget.setEnabled(True)
        
        try:
            factory.package.write()
        except AttributeError, e:
            mess = QtGui.QMessageBox.warning(self, "Error",
                                             "Cannot write Graph model on disk. :\n"+
                                             "You try to write in a System Package:\n")
        self.notify_listeners(("graphoperator_newfactory", factory))

        
    def graph_copy(self):
        """ Copy Selection """
        if(self.__interpreter.hasFocus()):
            try:
                self.__interpreter.copy()
            except:
                pass
        else:
            s = self.graphView().get_selected_items()
            s = [i.vertex().get_id() for i in s]
            if(not s): return 
            self.__session.clipboard.clear()
            self.graph().to_factory(self.__session.clipboard, s, auto_io=False)

    def graph_cut(self):
        if(self.__interpreter.hasFocus()):
            try:
                self.__interpreter.copy()
            except:
                pass
        else:
            self.graph_copy()
            self.graph_remove_selection()

    def graph_paste(self):
        """ Paste from clipboard """
        if(self.__interpreter.hasFocus()):
            try:
                self.__interpreter.paste()
            except:
                pass
        else:
            widget = self.graphView()
            index  = widget.parent().indexOf(widget)

            # Get Position from cursor
            position = widget.mapToScene(
                widget.mapFromGlobal(widget.cursor().pos()))
            widget.select_added_elements(True)
            
            cnode = self.__session.clipboard.instantiate()

            min_x = min([cnode.node(vid).get_ad_hoc_dict().get_metadata("position")[0] for vid in cnode if vid not in (cnode.id_in, cnode.id_out)])
            min_y = min([cnode.node(vid).get_ad_hoc_dict().get_metadata("position")[1] for vid in cnode if vid not in (cnode.id_in, cnode.id_out)])
            print min_x, min_y

            def lam(n):
                x = n.get_ad_hoc_dict().get_metadata("position")
                x = [x[0]-min_x + position.x()+30, x[1]-min_y + position.y()+30]
                n.get_ad_hoc_dict().set_metadata("position", x)
            
            modifiers = [("position", lam)]
            new_ids = self.__session.clipboard.paste(self.graph(), 
                                                     modifiers, 
                                                     meta=True)

    def graph_close(self):
       # Try to save factory if widget is a graph
        widget = self.graphView()
        index  = widget.parent().indexOf(widget)

        try:
            modified = self.graph().graph_modified
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
        self.__session.close_workspace(index, False)
        widget.parent().removeWidget(widget)
        widget.close()

    def graph_export_to_factory(self):
        """
        Export workspace index to its factory
        """
        widget = self.graphView()
        index  = widget.parent().indexOf(widget)

        # Get a composite node factory
        dialog = FactorySelector(self.graph().factory, widget)
            
        # Display Dialog
        ret = dialog.exec_()
        if(ret == 0): return None
        factory = dialog.get_factory()

        self.graph().to_factory(factory, None)
        self.graph().factory = factory
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
        widget = self.graphView()

        dialog = IOConfigDialog(self.graph().input_desc,
                                self.graph().output_desc,
                                parent=widget)
        ret = dialog.exec_()

        if(ret):
            self.graph().set_io(dialog.inputs, dialog.outputs)
            widget.rebuild_scene()


    def graph_reload_from_factory(self):
        """ Reload a tab node givin its index"""
        widget = self.graphView()
        index  = widget.parent().indexOf(widget)

        name = self.graph().factory.name

        if(self.graph().graph_modified):
            # Show message
            ret = QtGui.QMessageBox.question(wigdet, "Reload workspace '%s'"%(name),
                                             "Reload will discard recent changes on "\
                                                 + "workspace '%s'.\n"%(name)+
                                             "Continue ?\n",
                                             QtGui.QMessageBox.Yes, QtGui.QMessageBox.No,)
            
            if(ret == QtGui.QMessageBox.No):
                return


        newGraph = self.graph().factory.instantiate()
        widget.set_graph(newGraph)
        widget.rebuild_scene()
        self.__session.workspaces[index] = newGraph

    def __get_current_factory(self, name):
        """ Build a temporary factory for current workspace
        Return (node, factory)
        """
        
        tempfactory = CompositeNodeFactory(name = name)
        self.graph().to_factory(tempfactory)
        
        return (self.graph().graph(), tempfactory)
    
    def graph_preview_application(self):
        """ Open Application widget """
        widget = self.graphView()
        
        graph, tempfactory = self.__get_current_factory("Preview")
        widget.deaf()
        w = qtgraphview.QtGraphView(widget.parent(), graph)
        widget.deaf(False)
        #w = tempfactory.instantiate_widget(node, widget, autonomous=True)

        open_dialog(widget, w, 'Preview Application')


    def graph_export_application(self):
        """ Export current workspace composite node to an Application """
        widget = self.graphView()

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
        
        graph, tempfactory = self.__get_current_factory(name)
        widget.deaf()
        w = qtgraphview.QtGraphView(widget.parent(), graph)
        widget.deaf(False)
        
        #export_app comes from openalea.core
        export_app.export_app(name, filename, tempfactory) 
        

    ######################################
    # The actual methods -- For vertices #
    ######################################
    def set_vertex_item(self, vertexItem):
        self.vertexItem = weakref.ref(vertexItem)        

    def vertex_run(self):
        self.graph().eval_as_expression(self.vertexItem().vertex().get_id())        

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

        self._vertexWidget = open_dialog(self.graphView(), innerWidget, factory.get_id(), False)

    def vertex_remove(self):
        self.graph().remove_vertex(self.vertexItem().vertex())

    def vertex_reset(self):
        self.vertexItem().vertex().reset()

    def vertex_replace(self):
        """ Replace a node by an other """
        
        self.dialog = NodeChooser(self.graphView())
        self.dialog.search('', self.vertexItem().vertex().get_nb_input(), 
                           self.vertexItem().vertex().get_nb_output())
        ret = self.dialog.exec_()

        if(not ret): return
        
        factory = self.dialog.get_selection()
        newnode = factory.instantiate()
        self.graph().replace_vertex(self.vertexItem().vertex(), newnode)

    def vertex_reload(self):
        """ Reload the vertex """

        # Reload package
        factory = self.vertexItem().vertex().factory
        package = factory.package
        if(package):
            package.reload()

        # Reinstantiate the vertex
        newvertex = factory.instantiate()
        self.graph().set_actor(self.vertexItem().vertex().get_id(), newvertex)
        newvertex.internal_data.update(self.vertexItem().vertex().internal_data)
        self.vertexItem().set_observed(newvertex)
        self.vertexItem().initialise_from_model()

    def vertex_set_caption(self):
        """ Open a input dialog to set node caption """

        n = self.vertexItem().vertex()
        (result, ok) = QtGui.QInputDialog.getText(None, "Node caption", "",
                                   QtGui.QLineEdit.Normal, n.caption)
        if(ok):
            n.caption = str(result) #I HATE PROPERTIES, REALLY!

    def vertex_show_hide_ports(self):
        """ Open port show/hide dialog """
        editor = ShowPortDialog(self.vertexItem().vertex(), self.graphView())
        editor.exec_()

    def vertex_mark_user_app(self, val):
        self.graph().set_continuous_eval(self.vertexItem().vertex().get_id(), bool(val))

    def vertex_set_lazy(self, val):
        self.vertexItem().vertex().lazy = val #I HATE PROPERTIES, REALLY!

    def vertex_block(self, val):
        self.vertexItem().vertex().block = val #I HATE PROPERTIES, REALLY!

    def vertex_edit_internals(self):
        """ Edit node internal data """
        editor = DictEditor(self.vertexItem().vertex().internal_data, self.graphView())
        ret = editor.exec_()

        if(ret):
            for k in editor.modified_key:
                self.vertexItem().vertex().set_data(k, editor.pdict[k])

