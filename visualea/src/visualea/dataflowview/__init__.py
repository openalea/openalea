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

import vertex
import edge
import anno
import adapter

from Qt import QtCore, QtGui, QtWidgets

from openalea.qt.compat import to_qvariant

from openalea.visualea.graph_operator import GraphOperator

from openalea.core import compositenode, node
from openalea.core.pkgmanager import PackageManager
from openalea.core.node import RecursionError
from openalea.core.algo import dataflow_evaluation as evalmodule
from openalea.core.node import NodeFactory
from openalea.core.compositenode import CompositeNodeFactory

from openalea.grapheditor import qt
import openalea.grapheditor.base

class DataflowView(qt.View):

    def __init__(self, parent, *args, **kwargs):
        qt.View.__init__(self, parent)

        self.__clipboard = None
        self.__siblings = None

        # -- Configure the drop handlers --
        mimeFormatsMap = {node.NodeFactory.mimetype: self.node_factory_drop_handler,
                          compositenode.CompositeNodeFactory.mimetype: self.node_factory_drop_handler,
                          "openalea/data_instance": self.node_datapool_drop_handler,
                          "openalealab/model": self.node_model_factory_drop_handler,
                          "openalealab/control": self.node_control_drop_handler,
                          "openalealab/data": self.node_data_drop_handler,
                          }

        self.set_mime_handler_map(mimeFormatsMap)

        # -- handle the vanishing toolbar --
        self.__noToolBar = kwargs.get("noToolBar", False)

        if not self.__noToolBar:
            self.__annoToolBar = anno.AnnotationTextToolbar(None)
            self.__annoToolBar.setSleepOnDisappear(True)

        self.copyRequest.connect(self.on_copy_request)
        self.cutRequest.connect(self.on_cut_request)
        self.pasteRequest.connect(self.on_paste_request)
        self.deleteRequest.connect(self.on_delete_request)

    def setScene(self, scene):
        # This is called by grapheditor.qtgraphview.set_canvas
        # which is itself called by GraphicalGraph(...) after __init__.
        if scene is not None and not self.__noToolBar:
            scene.addItem(self.__annoToolBar)
        qt.View.setScene(self, scene)

    def set_clipboard(self, cnf):
        self.__clipboard = cnf

    def set_siblings(self, sibs):
        self.__siblings = sibs

    def get_graph_operator(self):
        operator = GraphOperator(graph=self.scene().get_graph(),
                                 graphAdapter=self.scene().get_adapter(),
                                 graphScene=self.scene(),
                                 clipboard=self.__clipboard,
                                 siblings=self.__siblings,
                                 )
        return operator

    def on_copy_request(self, view, scene, a):
        operator = self.get_graph_operator()
        operator(fName="graph_copy")()
        a.accept = True

    def on_cut_request(self, view, scene, a):
        operator = self.get_graph_operator()
        operator(fName="graph_cut")()
        a.accept = True

    def on_paste_request(self, view, scene, a):
        position = view.mapToScene(view.mapFromGlobal(view.cursor().pos()))
        operator = self.get_graph_operator()
        self.setUpdatesEnabled(False)
        operator(fName="graph_paste", position=position)()
        self.setUpdatesEnabled(True)
        self.update()
        a.accept = True

    def on_delete_request(self, view, scene, a):
        operator = self.get_graph_operator()
        operator(fName="graph_remove_selection")()
        a.accept = True

    #######################################################
    # THIS DOESN'T BELONG HERE! OR AT LEAST NOT LIKE THIS #
    #######################################################
    ####################################################
    # Handling the drag and drop events over the graph #
    ####################################################
    def __drop_from_factory(self, factory, pos):
        try:
            scene = self.scene()
            scene.clearSelection()
            scene.select_added_items(True)
            realGraph = scene.get_graph()
            node = factory.instantiate([realGraph.factory.get_id()])
            scene.add_vertex(node, position=pos)
            return node
        except RecursionError:
            mess = QtWidgets.QMessageBox.warning(self, "Error",
                                                "A graph cannot be contained in itself.")
            return None

    def __check_factory(self, factory):
            # -- Check if no other instance of this factory is opened --
        operator = self.get_graph_operator()
        for ws in operator.get_siblings():
            if factory == ws.factory:
                res = QtWidgets.QMessageBox.warning(self, "Other instances are already opened!",
                                                   "You are trying to insert a composite node that has already been opened.\n" +
                                                   "Doing this might cause confusion later on.\n" +
                                                   "Do you want to continue?",
                                                   QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Cancel)
                if res == QtWidgets.QMessageBox.Cancel:
                    return False
                else:
                    break
        return True

    def node_factory_drop_handler(self, event):
        """ Drag and Drop from the PackageManager """
        mimedata = event.mimeData()
        if mimedata.hasFormat(NodeFactory.mimetype) or mimedata.hasFormat(CompositeNodeFactory.mimetype):
            format = NodeFactory.mimetype if mimedata.hasFormat(
                NodeFactory.mimetype) else CompositeNodeFactory.mimetype
            # -- retreive the data from the event mimeData --
            pieceData = event.mimeData().data(format)
            dataStream = QtCore.QDataStream(pieceData, QtCore.QIODevice.ReadOnly)
            package_id = str(dataStream.readString())
            factory_id = str(dataStream.readString())

            # -- find node factory --
            pkgmanager = PackageManager()
            pkg = pkgmanager[str(package_id)]
            factory = pkg.get_factory(str(factory_id))

            # -- see if we can safely open this factory (with user input) --
            if not self.__check_factory(factory):
                return

            # -- instantiate the new node at the given position --
            position = self.mapToScene(event.pos())
            self.__drop_from_factory(factory, [position.x(), position.y()])
            event.setDropAction(QtCore.Qt.MoveAction)
            # event.accept()

    def node_model_factory_drop_handler(self, event):
        """ Drag and Drop from the Model """
        mimedata = event.mimeData()
        if mimedata.hasFormat("openalealab/model"):
            from openalea.oalab.service.mimedata import decode
            # -- retreive the data from the event mimeData --
            model, kwds = decode(str(mimedata.data("openalealab/model")), "openalealab/model", "openalealab/model")
            model_id = model.name

            try:
                # version > August 2014 (Git)
                from openalea.oalab.model.visualea import ModelNodeFactory
            except ImportError:
                try:
                    # Backward compatibility with oalab from svn June 2014
                    from openalea.oalab.model.model import ModelFactory
                except ImportError:
                    event.ignore()
                    return
                else:
                    factory = ModelFactory(model_id)
            else:
                factory = ModelNodeFactory(model_id)
            """
            # -- see if we can safely open this factory (with user input) --
            if not self.__check_factory(factory):
                return"""

            # -- instantiate the new node at the given position --
            position = self.mapToScene(event.pos())
            self.__drop_from_factory(factory, [position.x(), position.y()])
            event.setDropAction(QtCore.Qt.MoveAction)
            # event.accept()

    def node_control_drop_handler(self, event):
        # Drag and Drop from the DataPool
        if(event.mimeData().hasFormat("openalealab/control")):
            # -- retreive the data from the event mimeData --
            pieceData = event.mimeData().data("openalealab/control")
            dataStream = QtCore.QDataStream(pieceData, QtCore.QIODevice.ReadOnly)
            identifier, data_key = str(pieceData).split(';')

            # -- find node factory --
            pkgmanager = PackageManager()
            pkg = pkgmanager["openalea.oalab"]
            factory = pkg.get_factory("control")

            # -- instantiate the new node at the given position --
            position = self.mapToScene(event.pos())
            node = self.__drop_from_factory(factory, [position.x(), position.y()])
            if node:
                node.set_input(0, data_key)
                node.set_caption(data_key)
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()

    def node_data_drop_handler(self, event):
        # Drag and Drop from the DataPool
        if(event.mimeData().hasFormat("openalealab/data")):
            # -- retreive the data from the event mimeData --
            from openalea.oalab.mimedata.builtin import decode_project_item
            data = decode_project_item(
                str(event.mimeData().data("openalealab/data")),
                "openalealab/data",
                "openalealab/data")

            # -- find node factory --
            pkgmanager = PackageManager()
            pkg = pkgmanager["openalea.oalab"]
            factory = pkg.get_factory("data")

            # -- instantiate the new node at the given position --
            position = self.mapToScene(event.pos())
            node = self.__drop_from_factory(factory, [position.x(), position.y()])
            if node:
                node.set_input(0, data.name)
                node.set_caption(unicode(data.name))
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()

    def node_datapool_drop_handler(self, event):
        # Drag and Drop from the DataPool
        if(event.mimeData().hasFormat("openalea/data_instance")):
            # -- retreive the data from the event mimeData --
            pieceData = event.mimeData().data("openalea/data_instance")
            dataStream = QtCore.QDataStream(pieceData, QtCore.QIODevice.ReadOnly)
            data_key = str()
            data_key = str(data_key + dataStream)

            # -- find node factory --
            pkgmanager = PackageManager()
            pkg = pkgmanager["system"]
            factory = pkg.get_factory("pool reader")

            # -- instantiate the new node at the given position --
            position = self.mapToScene(event.pos())
            node = self.__drop_from_factory(factory, [position.x(), position.y()])
            if node:
                node.set_input(0, data_key)
                node.set_caption("pool ['%s']" % (data_key,))
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()

    ##############################################
    # Handling keyboard events on the graph view #
    ##############################################
    def keyPressEvent(self, e):
        qt.View.keyPressEvent(self, e)
        if not e.isAccepted():
            if e.key() == QtCore.Qt.Key_Space:
                self.setDragMode(QtWidgets.QGraphicsView.ScrollHandDrag)

    def keyReleaseEvent(self, e):
        key = e.key()
        if key == QtCore.Qt.Key_Space:
            self.setDragMode(QtWidgets.QGraphicsView.RubberBandDrag)

    #########################
    # Handling mouse events #
    #########################
    def mouseMoveEvent(self, e):
        if not self.__noToolBar:
            # -- the annotation toolbar (color of the text/postit) is positionned
            # here. When the pointer is over an annotation, the annotation is set
            # as the annotation of the annotation toolbar. This correctly puts the
            # toolbar in the right place and reveals it.
            # If the pointer not over an annotation it is hidden unless it is over
            # the toolbar. --
            items = self.items(e.pos())
            annotations = [i for i in items if isinstance(i, anno.GraphicalAnnotation)]
            if len(annotations) > 0:
                firstAnno = annotations[0]
                self.__annoToolBar.wakeup()
                self.__annoToolBar.set_annotation(firstAnno, self)
            # elif not self.__annoToolBar in items :
            #     self.__annoToolBar.set_annotation(None)

        qt.View.mouseMoveEvent(self, e)

    ###########################################
    # Handling context menu on the graph view #
    ###########################################
    def contextMenuEvent(self, event):

        QtWidgets.QGraphicsView.contextMenuEvent(self, event)
        if event.isAccepted():
            return

        scenePos = self.mapToScene(event.pos())

        operator = self.get_graph_operator()
        menu = qt.AleaQMenu(self)
        menu.addAction(operator("Add Annotation", menu,
                                "graph_add_annotation", position=scenePos))

        # -- Evaluator submenu --
        evaluatorSubmenu = menu.addMenu("Evaluator")
        classlist = sorted(evalmodule.__evaluators__)
        selectitem = None
        for c in classlist:
            action = operator(c, evaluatorSubmenu, "graph_set_evaluator_" + c)
            evaluatorSubmenu.addAction(action)
            action.setCheckable(True)
            if c == self.scene().get_graph().eval_algo:
                evaluatorSubmenu.setActiveAction(action)
                action.setChecked(True)

        menu.move(event.globalPos())
        menu.show()
        event.accept()

def initialise_graph_view_from_model(graphView, graphModel):

    # -- do the base node class initialisation --
    mdict = graphModel.get_ad_hoc_dict()

    # graphical data init.
    mdict.simulate_full_data_change(graphView, graphModel)

    # other attributes init (composite node is subclass of node)
    for i in graphModel.input_desc:
        graphView.notify(graphModel, ("input_port_added", i))
    for i in graphModel.output_desc:
        graphView.notify(graphModel, ("output_port_added", i))
    for i in graphModel.map_index_in:
        graphView.notify(graphModel, ("input_modified", i))
    graphView.notify(graphModel, ("caption_modified", graphModel.internal_data["caption"]))
    graphView.notify(graphModel, ("tooltip_modified", graphModel.get_tip()))
    graphView.notify(graphModel, ("internal_data_changed",))

    # -- then the composite node class initialisation --
    ids = graphModel.vertices()
    for eltid in ids:
        vtype = "vertex"
        doNotify = True
        vertex = graphModel.node(eltid)
        if("__graphitem__" in vertex.__class__.__dict__):
            vtype = "annotation"
        elif isinstance(vertex, compositenode.CompositeNodeOutput):
            vtype = "outNode"
            doNotify = True if len(vertex.input_desc) else False
        elif isinstance(vertex, compositenode.CompositeNodeInput):
            vtype = "inNode"
            doNotify = True if len(vertex.output_desc) else False
        else:
            pass
        if doNotify:
            graphView.notify(graphModel, ("vertex_added", (vtype, vertex)))

    for eid in graphModel.edges():
        (src_id, dst_id) = graphModel.source(eid), graphModel.target(eid)
        etype = None
        src_port_id = graphModel.local_id(graphModel.source_port(eid))
        dst_port_id = graphModel.local_id(graphModel.target_port(eid))

        nodeSrc = graphModel.node(src_id)
        nodeDst = graphModel.node(dst_id)
        src_port = nodeSrc.output_desc[src_port_id]
        dst_port = nodeDst.input_desc[dst_port_id]

        edgedata = "default", eid, src_port, dst_port
        graphView.notify(graphModel, ("edge_added", edgedata))


GraphicalGraph = openalea.grapheditor.qt.QtGraphStrategyMaker(graphView=DataflowView,
                                                              vertexWidgetMap={"vertex": vertex.GraphicalVertex,
                                                                               "annotation": anno.GraphicalAnnotation,
                                                                               "inNode": vertex.GraphicalInVertex,
                                                                               "outNode": vertex.GraphicalOutVertex},
                                                              edgeWidgetMap={"default": edge.GraphicalEdge,
                                                                             "floating-default": edge.FloatingEdge},
                                                              graphViewInitialiser=initialise_graph_view_from_model,
                                                              adapterType=adapter.GraphAdapter)
