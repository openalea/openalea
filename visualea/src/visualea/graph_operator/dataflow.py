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

from openalea.vpltk.qt import qt
from openalea.visualea.graph_operator.base import Base

from openalea.visualea.util import open_dialog, exception_display, busy_cursor
from openalea.visualea.dialogs import NewGraph, FactorySelector
from openalea.visualea.dialogs import IOConfigDialog

from openalea.core.compositenode import CompositeNodeFactory
from openalea.core.pkgmanager import PackageManager
from openalea.core import export_app
from openalea.core.algo import dataflow_evaluation as evalmodule
from compositenode_inspector import InspectorView


class DataflowOperators(Base):

    @exception_display
    @busy_cursor
    def graph_run(self):
        master = self.master
        sc = master.get_graph_scene()
        view, = sc.views()
        mw = view.parent().parent().parent().parent().parent().parent()
        graph = master.get_graph()

        prov = graph.eval_as_expression(record_provenance=mw._record_provenance)
        mw.session.provenance = prov


    def graph_reset(self):
        master = self.master
        widget = master.get_sensible_parent()
        ret = qt.QtGui.QMessageBox.question(widget,
                                         "Reset Workspace",
                                         "Reset will delete all input values.\n" + \
                                             "Continue ?\n",
                                         qt.QtGui.QMessageBox.Yes,
                                         qt.QtGui.QMessageBox.No,)
        if(ret == qt.QtGui.QMessageBox.No):
            return
        master.get_graph().reset()


    def graph_invalidate(self):
        self.master.get_graph().invalidate()


    def graph_remove_selection(self, items=None):
        master = self.master
        def cmp(a,b):
            """edges need to be deleted before any other element"""
            if type(a) == master.edgeType and type(b) == master.vertexType : return -1
            if type(a) == type(b) : return 0
            return 1

        scene = master.get_graph_scene()
        if(not items): items = scene.get_selected_items()
        if(not items): return
        items.sort(cmp)
        for i in items:
            if isinstance(i, master.vertexType):
                if scene.get_adapter().is_vertex_protected(i.vertex()): continue
                scene.remove_vertex(i.vertex())
            elif isinstance(i, master.edgeType):
                scene.remove_edge((i.srcBBox().vertex(), i.srcBBox()),
                                  (i.dstBBox().vertex(), i.dstBBox()) )
            elif isinstance(i, master.annotationType):
                scene.remove_vertex(i.annotation())


    def graph_group_selection(self):
        """Export selected nodes in a new factory"""
        master = self.master
        widget = master.get_sensible_parent()
        graph  = master.get_graph()
        scene  = master.get_graph_scene()

        # FIRST WE PREPARE THE USER INTERFACE STUFF
        # ------------------------------------------
        # Get default package id
        default_factory = graph.factory
        if(default_factory and default_factory.package):
            pkg_id = default_factory.package.name
            name = default_factory.name + "_grp_" + str(len(default_factory.package))
        else:
            pkg_id = None
            name = ""

        pm = master.get_package_manager()
        dialog = NewGraph("Group Selection", pm, widget,
                          io=False, pkg_id=pkg_id, name=name)
        ret = dialog.exec_()
        if(not ret): return

        # NOW WE DO THE HARD WORK
        # -----------------------
        factory = dialog.create_cnfactory(pm)
        items = scene.get_selected_items(master.vertexType)
        if(not items): return None

        pos = scene.get_selection_center(items)
        def cmp_x(i1, i2):
            return cmp(i1.scenePos().x(), i2.scenePos().x())
        items.sort(cmp=cmp_x)

        # Instantiate the new node:
        itemIds = [i.vertex().get_id() for i in items]
        graph.to_factory(factory, itemIds, auto_io=True)
        newVert = factory.instantiate([graph.factory.get_id()])

        # Evaluate the new connections:
        def evaluate_new_connections(newGraph, newGPos, idList):
            newId    = scene.add_vertex(newGraph, [newGPos.x(), newGPos.y()])
            newEdges = graph.compute_external_io(idList, newId)
            for edges in newEdges:
                scene.add_edge((edges[0], edges[1]),
                                 (edges[2], edges[3]))
            self.graph_remove_selection(items)

        def correct_positions(newGraph):
            _minX = _minY = float("inf")
            for vid in newGraph.vertices():
                if vid in (newGraph.id_in, newGraph.id_out): continue
                node = newGraph.node(vid)
                _nminX, _nminY = node.get_ad_hoc_dict().get_metadata("position")
                _minX= min(_minX, _nminX)
                _minY= min(_minY, _nminY)
            for vid in newGraph.vertices():
                if vid in (newGraph.id_in, newGraph.id_out): continue
                pos = newGraph.node(vid).get_ad_hoc_dict().get_metadata("position")
                # the 50 is there to have a margin at the top and right of the
                # nodes.
                pos[0] = pos[0] - _minX + 50
                pos[1] = pos[1] - _minY + 50

        if newVert:
            #to prevent too many redraws during the grouping we queue events then process
            #them all at once.
            scene.queue_call_notifications(evaluate_new_connections, newVert, pos, itemIds)
            correct_positions(newVert)


        try:
            factory.package.write()
        except AttributeError, e:
            mess = qt.QtGui.QMessageBox.warning(widget, "Error",
                                             "Cannot write Graph model on disk. :\n"+
                                             "You try to write in a System Package:\n")
        master.notify_listeners(("graphoperator_graphsaved", scene, factory))



    def graph_add_annotation(self, position=None):
        scene = self.master.get_graph_scene()

        # Add new node
        pkgmanager = PackageManager()
        pkg        = pkgmanager["System"]
        factory    = pkg.get_factory("annotation")

        realGraph = scene.get_graph()
        node  = factory.instantiate([realGraph.factory.get_id()])
        node.get_ad_hoc_dict().set_metadata("visualStyle", 1)
        scene.add_vertex(node, position=[position.x(), position.y()])


    def graph_copy(self):
        """ Copy Selection """
        master = self.master
        scene = master.get_graph_scene()
        s = scene.get_selected_items( (master.vertexType, master.annotationType) )
        if(not s): return

        s = [i.vertex().get_id() for i in s]
        master.get_clipboard().clear()
        master.get_graph().to_factory(master.get_clipboard(), s, auto_io=False)

    def graph_cut(self):
        """ Cut selection """
        master = self.master
        self.graph_copy()
        self.graph_remove_selection()

    def graph_paste(self, position=None):
        """ Paste from clipboard """
        master = self.master
        scene  = master.get_graph_scene()
        cnode = master.get_clipboard().instantiate()

        min_x = min_y = float("inf")
        for vid in cnode:
            if vid in (cnode.id_in, cnode.id_out): continue
            pos = cnode.node(vid).get_ad_hoc_dict().get_metadata("position")
            min_x = min(pos[0], min_x); min_y = min(pos[1], min_y)


        def lam(n):
            x = n.get_ad_hoc_dict().get_metadata("position")
            x[0] = x[0]-min_x + position.x()+10
            x[1] = x[1]-min_y + position.y()+10
            n.get_ad_hoc_dict().set_metadata("position", x)

        modifiers = [("position", lam)]
        scene.clearSelection()
        scene.select_added_items(True)
        scene.queue_call_notifications(master.get_clipboard().paste,
                                       master.get_graph(),
                                       modifiers,
                                       meta=True)


    def graph_close(self):
       # Try to save factory if widget is a graph
        master = self.master
        scene  = master.get_graph_scene()
        widget = master.get_sensible_parent()
        if isinstance(widget, InspectorView):
            # print "Forbidden in CompositeNodeInspector"
            return

        try:
            modified = master.get_graph().graph_modified
            if(modified):
                # Generate factory if user want
                ret = qt.QtGui.QMessageBox.question(widget, "Close Workspace",
                                                 "Graph has been modified.\n"+
                                                 "Do you want to report modification "+
                                                 "in the model ?\n",
                                                 qt.QtGui.QMessageBox.Yes,
                                                 qt.QtGui.QMessageBox.No,)

                if(ret == qt.QtGui.QMessageBox.Yes):
                    self.graph_export_to_factory()

        except Exception, e:
            print "graph_close exception", e
            pass

        #update any interested guy
        master.notify_listeners(("graphoperator_graphclosed", scene))


    def graph_export_to_factory(self):
        """Export workspace to its factory"""
        master = self.master
        scene  = master.get_graph_scene()
        widget = master.get_sensible_parent()

        # Get a composite node factory
        graph = master.get_graph()

        #check if no other instance of this factory is opened
        siblings = master.get_siblings()
        for ws in siblings:
            if graph != ws and graph.factory == ws.factory:
                res = qt.QtGui.QMessageBox.warning(widget, "Other instances are opened!",
                """You are trying to save a composite node that has been opened multiple times.
                Doing this may discard changes done in the other intances.
                Do you want to continue?""",
                                                qt.QtGui.QMessageBox.Ok | qt.QtGui.QMessageBox.Cancel)
                if res == qt.QtGui.QMessageBox.Cancel:
                    return
                else:
                    break

        dialog = FactorySelector(graph.factory, widget)

        # Display Dialog
        ret = dialog.exec_()
        if(ret == 0): return None
        factory = dialog.get_factory()

        graph.to_factory(factory, None)
        graph.factory = factory
        graph.set_caption(factory.name)

        try:
            factory.package.write()
        except AttributeError, e:
            mess = qt.QtGui.QMessageBox.warning(widget, "Error",
                                             "Cannot write Graph model on disk. :\n"+
                                             "Trying to write in a System Package!\n")
        master.notify_listeners(("graphoperator_graphsaved", scene, factory))

    def graph_export_script(self):
        master = self.master
        widget = master.get_sensible_parent()
        composite_node = master.get_graph()
        scr = composite_node.to_script()

        filename = qt.QtGui.QFileDialog.getSaveFileName(
            widget, "Export to script",  qt.QtCore.QDir.homePath(), "Python file (*.py)")

        filename = str(filename)
        if not filename:
            return
        elif '.' not in filename:
            filename += '.py'

        with open(filename, "w") as file:
            file.write(scr)

    def graph_export_png(self):
        """ Export current workspace to an image """

        master = self.master
        scene  = master.get_graph_scene()
        widget = master.get_sensible_parent()

        filename = qt.QtGui.QFileDialog.getSaveFileName(widget,
                                                     "Export png image",
                                                     qt.QtCore.QDir.homePath(),
                                                     "PNG Image (*.png)")

        filename = str(filename)
        if not filename:
            return
        elif '.' not in filename:
            filename += '.png'

        mg = 10
        scene.update()
        source  = scene.itemsBoundingRect()
        canvas  = scene.itemsBoundingRect().adjusted(-mg, -mg, mg, mg)
        target  = scene.itemsBoundingRect()
        pixmap  = qt.QtGui.QPixmap(canvas.width(), canvas.height())
        painter = qt.QtGui.QPainter(pixmap)

        target.moveTo(mg, mg)
        pixmap.fill()
        painter.setRenderHint(qt.QtGui.QPainter.Antialiasing)
        scene.render(painter, target, source)
        painter.end()
        pixmap.save(filename)

    def graph_export_svg(self):
        """ Export current workspace to an image """

        master = self.master
        scene  = master.get_graph_scene()
        widget = master.get_sensible_parent()

        filename = qt.QtGui.QFileDialog.getSaveFileName(widget,
                                                     "Export svg image",
                                                     qt.QtCore.QDir.homePath(),
                                                     "SVG Image (*.svg)")

        filename = str(filename)
        print "graph_export_svg", filename
        if not filename:
            return
        elif '.' not in filename:
            filename += '.png'

        mg = 10
        scene.update()
        source  = scene.itemsBoundingRect()
        canvas  = scene.itemsBoundingRect().adjusted(-mg, -mg, mg, mg)
        target  = scene.itemsBoundingRect()
        target.moveTo(mg, mg)

        svg_gen = qt.QtSvg.QSvgGenerator()
        svg_gen.setFileName(filename)
        svg_gen.setSize(canvas.toRect().size())

        painter = qt.QtGui.QPainter(svg_gen)
        painter.setRenderHint(qt.QtGui.QPainter.Antialiasing)
        scene.render(painter, target, source)
        painter.end()


    def graph_configure_io(self):
        """ Configure workspace IO """
        master = self.master
        widget = master.get_sensible_parent()
        graph  = master.get_graph()
        dialog = IOConfigDialog(graph.input_desc,
                                graph.output_desc,
                                parent=widget)
        ret = dialog.exec_()

        if(ret):
            graph.set_io(dialog.inputs, dialog.outputs)


    def graph_reload_from_factory(self):
        """ Reload a tab node """
        master = self.master
        scene  = master.get_graph_scene()
        widget = master.get_sensible_parent()
        if isinstance(widget, InspectorView):
            # print "Forbidden in CompositeNodeInspector"
            return

        graph = master.get_graph()
        name  = graph.factory.name

        if(graph.graph_modified):
            # Show message
            ret = qt.QtGui.QMessageBox.question(widget, "Reload workspace '%s'"%(name),
                                             "Reloading will discard recent changes on " +
                                             "workspace '%s'.\nContinue?"%(name),
                                             qt.QtGui.QMessageBox.Yes, qt.QtGui.QMessageBox.No,)

            if(ret == qt.QtGui.QMessageBox.No):
                return

        oldGraph = graph
        newGraph = graph.factory.instantiate()

        scene.clear()
        scene.set_graph(newGraph)
        scene.initialise_from_model()
        master.notify_listeners(("graphoperator_graphreloaded", scene, newGraph, oldGraph))


    def __get_current_factory(self, name):
        """ Build a temporary factory for current workspace
        Return (node, factory)
        """
        master = self.master
        tempfactory = CompositeNodeFactory(name = name)
        graph = master.get_graph()
        graph.to_factory(tempfactory)
        return (graph, tempfactory)


    def graph_preview_application(self, name="Preview"):
        """ Open Application widget """
        master = self.master
        widget = master.get_sensible_parent()
        if isinstance(widget, InspectorView):
            # print "Forbidden in CompositeNodeInspector"
            return

        graph, tempfactory = self.__get_current_factory(name)
        from openalea.visualea.dataflowview import GraphicalGraph
        w = GraphicalGraph.create_view(graph, parent=widget, clone=True)
        w.setWindowFlags(qt.QtCore.Qt.Window)
        w.setWindowTitle('Preview Application')
        w.show()
        return graph, tempfactory


    def graph_export_application(self):
        """ Export current workspace composite node to an Application """
        master = self.master
        widget = master.get_sensible_parent()
        if isinstance(widget, InspectorView):
            # print "Forbidden in CompositeNodeInspector"
            return

        # Get Filename
        filename = qt.QtGui.QFileDialog.getSaveFileName(
            widget, "Python Application",
            qt.QtCore.QDir.homePath(), "Python file (*.py)")

        filename = str(filename)
        if(not filename):
            return

        # Get Application Name
        result, ok = qt.QtGui.QInputDialog.getText(widget, "Application Name", "",
                                                qt.QtGui.QLineEdit.Normal, "")
        if(not ok):
            return

        name = str(result)
        if(not name) : name = "OpenAlea Application"

        graph, tempfactory = self.__get_current_factory(name)
        #export_app comes from openalea.core
        export_app.export_app(name, filename, tempfactory)


# -- don't look :) i'm just dynamically adding methods!
def add_graph_eval_setters():
    def make_setter(evaluator):
        def setter(self):
            master = self.master
            master.get_graph().eval_algo = evaluator
        return setter
    for c in evalmodule.__evaluators__:
        setattr(DataflowOperators, "graph_set_evaluator_"+c, make_setter(c))


add_graph_eval_setters()

