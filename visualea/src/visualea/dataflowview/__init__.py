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

from PyQt4 import QtGui, QtCore
from openalea.visualea.graph_operator import GraphOperator
from openalea.core import compositenode, node
from openalea.core.pkgmanager import PackageManager # for drag and drop
from openalea.core.node import RecursionError
from openalea.core.algo import dataflow_evaluation as evalmodule
from openalea.grapheditor import qt
#from openalea.grapheditor import baselisteners, qtgraphview, qtutils

import openalea.grapheditor.base




class DataflowView( qt.View ):

    def __init__(self, parent):
        qt.View.__init__(self, parent)

        # -- Configure the drop handlers --
        mimeFormatsMap = {"openalea/nodefactory":self.node_factory_drop_handler,
                          "openalea/data_instance":self.node_datapool_drop_handler}
        self.set_mime_handler_map(mimeFormatsMap)

        self.__annoNotAdded = True
        self.__annoToolBar = anno.AnnotationTextToolbar(None)
        self.__annoToolBar.setSleepOnDisappear(True)

        self.copyRequest.connect(self.on_copy_request)
        self.cutRequest.connect(self.on_cut_request)
        self.pasteRequest.connect(self.on_paste_request)
        self.deleteRequest.connect(self.on_delete_request)

    def get_graph_operator(self):
        operator=GraphOperator(self, self.scene().get_graph())
        operator.vertexType = vertex.GraphicalVertex
        operator.annotationType = anno.GraphicalAnnotation
        operator.edgeType = edge.GraphicalEdge
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
        operator = self.get_graph_operator()
        operator(fName="graph_paste")()
        a.accept = True

    def on_delete_request(self, view, scene, a):
        operator = self.get_graph_operator()
        operator(fName="graph_remove_selection")()
        a.accept = True

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
            mess = QtGui.QMessageBox.warning(self, "Error",
                                             "A graph cannot be contained in itself.")
            return None


    def __check_factory(self, factory):
            # -- Check if no other instance of this factory is opened --
            operator = self.get_graph_operator()
            session = operator.get_session()
            for ws in session.workspaces:
                if factory == ws.factory:
                    res = QtGui.QMessageBox.warning(self, "Other instances are already opened!",
                                                    "You are trying to insert a composite node that has already been opened.\n" +\
                                                    "Doing this might cause confusion later on.\n" +\
                                                    "Do you want to continue?",
                                                    QtGui.QMessageBox.Ok | QtGui.QMessageBox.Cancel)
                    if res == QtGui.QMessageBox.Cancel:
                        return False
                    else:
                        break
            return True


    def node_factory_drop_handler(self, event):
        """ Drag and Drop from the PackageManager """
        if (event.mimeData().hasFormat("openalea/nodefactory")):
            # -- retreive the data from the event mimeData --
            pieceData = event.mimeData().data("openalea/nodefactory")
            dataStream = QtCore.QDataStream(pieceData, QtCore.QIODevice.ReadOnly)
            package_id = QtCore.QString()
            factory_id = QtCore.QString()
            dataStream >> package_id >> factory_id

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
            event.accept()


    def node_datapool_drop_handler(self, event):
        # Drag and Drop from the DataPool
        if(event.mimeData().hasFormat("openalea/data_instance")):
            # -- retreive the data from the event mimeData --
            pieceData = event.mimeData().data("openalea/data_instance")
            dataStream = QtCore.QDataStream(pieceData, QtCore.QIODevice.ReadOnly)
            data_key = QtCore.QString()
            dataStream >> data_key
            data_key = str(data_key)

            # -- find node factory --
            pkgmanager = PackageManager()
            pkg = pkgmanager["system"]
            factory = pkg.get_factory("pool reader")

            # -- instantiate the new node at the given position --
            position = self.mapToScene(event.pos())
            node = self.__drop_from_factory(factory, [position.x(), position.y()])
            if node:
                node.set_input(0, data_key)
                node.set_caption("pool ['%s']"%(data_key,))
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()

    ##############################################
    # Handling keyboard events on the graph view #
    ##############################################
    def keyPressEvent(self, e):
        qt.View.keyPressEvent(self, e)
        if not e.isAccepted():
            if e.key() == QtCore.Qt.Key_Space:
                self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)

    def keyReleaseEvent(self, e):
        key = e.key()
        if key == QtCore.Qt.Key_Space:
            self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)

    #########################
    # Handling mouse events #
    #########################
    def mouseMoveEvent(self, e):
        items = self.items(e.pos())
        annotations = [i for i in items if isinstance(i, anno.GraphicalAnnotation)]
        if len(annotations) > 0 :
            firstAnno = annotations[0]
            if self.__annoNotAdded:
                self.scene().addItem(self.__annoToolBar)
                self.__annoNotAdded = False
            self.__annoToolBar.wakeup()
            pos = firstAnno.sceneBoundingRect().topLeft()
            pos.setY(pos.y() - self.__annoToolBar.rect().height()/self.matrix().m22())
            self.__annoToolBar.setPos(pos)
            self.__annoToolBar.set_annotation(firstAnno)
            self.__annoToolBar.appear()
        else:
            if not self.__annoNotAdded and self.__annoToolBar not in items:
                #self.__annoToolBar.set_annotation(None)
                self.__annoToolBar.disappear()

        qt.View.mouseMoveEvent(self, e)

    ###########################################
    # Handling context menu on the graph view #
    ###########################################
    def contextMenuEvent(self, event):
        if(self.itemAt(event.pos())):
            QtGui.QGraphicsView.contextMenuEvent(self, event)
            return

        operator=GraphOperator(self)
        menu = qt.AleaQMenu(self)
        menu.addAction(operator("Add Annotation", menu, "graph_add_annotation"))

        # -- Evaluator submenu --
        evaluatorSubmenu = menu.addMenu("Evaluator")
        classlist = evalmodule.__evaluators__
        classlist.sort()
        selectitem = None
        for c in classlist:
            action = operator(c, evaluatorSubmenu, "graph_set_evaluator_"+c)
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
    mdict  = graphModel.get_ad_hoc_dict()

    #graphical data init.
    mdict.simulate_full_data_change(graphView, graphModel)

    #other attributes init (composite node is subclass of node)
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
        if(vertex.__class__.__dict__.has_key("__graphitem__")): vtype = "annotation"
        elif isinstance(vertex, compositenode.CompositeNodeOutput):
            vtype = "outNode"
            doNotify = True if len(vertex.input_desc) else False
        elif isinstance(vertex, compositenode.CompositeNodeInput) :
            vtype = "inNode"
            doNotify = True if len(vertex.output_desc) else False
        else: pass
        if doNotify:
            graphView.notify(graphModel, ("vertex_added", (vtype, vertex)))

    for eid in graphModel.edges():
        (src_id, dst_id) = graphModel.source(eid), graphModel.target(eid)
        etype=None
        src_port_id = graphModel.local_id(graphModel.source_port(eid))
        dst_port_id = graphModel.local_id(graphModel.target_port(eid))

        nodeSrc = graphModel.node(src_id)
        nodeDst = graphModel.node(dst_id)
        src_port = nodeSrc.output_desc[src_port_id]
        dst_port = nodeDst.input_desc[dst_port_id]

        edgedata = "default", eid, src_port, dst_port
        graphView.notify(graphModel, ("edge_added", edgedata))

    #make the sceneRect a tad bigger
    sceneRect = graphView.sceneRect()
    sceneRect.adjust(-50, -50, 50, 50)
    graphView.setSceneRect( sceneRect )


GraphicalGraph = openalea.grapheditor.qt.QtGraphStrategyMaker( graphView            = DataflowView,
                                                               vertexWidgetMap      = {"vertex":vertex.GraphicalVertex,
                                                                                       "annotation":anno.GraphicalAnnotation,
                                                                                       "inNode":vertex.GraphicalInVertex,
                                                                                       "outNode":vertex.GraphicalOutVertex},
                                                               edgeWidgetMap        = {"default":edge.GraphicalEdge,
                                                                                       "floating-default":edge.FloatingEdge},
                                                               graphViewInitialiser = initialise_graph_view_from_model,
                                                               adapterType          = adapter.GraphAdapter )


