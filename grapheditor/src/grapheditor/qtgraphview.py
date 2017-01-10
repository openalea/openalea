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

"""Generic Qt Graph Widget"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

import weakref, types, gc, warnings
from Qt import QtWidgets, QtGui, QtCore
from openalea.qt.compat import from_qvariant
import base, baselisteners, qtutils
import edgefactory

from math import sqrt

#------*************************************************------#
class Element(baselisteners.GraphElementListenerBase):
    """Base class for elements in a qtgraphview.View.

    Implements basic listeners calls for elements of a graph.
    A listener call is the method that is called after the main
    listening method (self.notify) dispatches the events. They
    are specified by interfaces.IGraphViewElement.

    :Listener calls:
     * position_changed(self,  (posx, posy))
     * add_to_view(self, view)
     * remove_from_view(self, view)


    """

    ####################################
    # ----Instance members follow----  #
    ####################################
    def __init__(self, observed=None, graph=None):
        """
        :Parameters:
             - observed (openalea.core.observer.Observed) - The item to observe.
             - graph (ducktype) - The graph owning the item.

        """
        baselisteners.GraphElementListenerBase.__init__(self,
                                                        observed,
                                                        graph)

    #################################
    # IGraphViewElement realisation #
    #################################
    def get_view(self):
        return self.scene()

    def add_to_view(self, view):
        """An element adds itself to the given view"""
        view.addItem(self)

    def remove_from_view(self, view):
        """An element removes itself from the given view"""
        view.removeItem(self)

    def position_changed(self, *args):
        """Updates the item's **graphical** position from
        model notifications. """
        point = QtCore.QPointF(args[0], args[1])
        self.setPos(point)

    def lock_position(self, val=True):
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, not val)

    def default_position(self):
        return [0.0, 0.0]

#------*************************************************------#
class Connector(Element):
    def __init__(self, *args, **kwargs):
        Element.__init__(self, *args, **kwargs)
        self.setFlag(qtutils.ItemSendsGeometryChanges)
        # self.setFlag(ItemSendsScenePositionChanges)
        self.setZValue(1.5)
        self.highlighted = False
        self.__makeConnectionMouseButton = QtCore.Qt.LeftButton
        self.__makeConnectionModifiers = QtCore.Qt.ControlModifier

    def set_connection_button(self, button):
        self.__makeConnectionMouseButton = button

    def set_connection_modifiers(self, modifiers):
        self.__makeConnectionModifiers = modifiers

    def set_highlighted(self, val):
        self.highlighted = val
        self.update()

    def get_scene_center(self):
        pos = self.sceneBoundingRect().center()
        return [pos.x(), pos.y()]

    def notify_position_change(self, pos=None):
        obs = self.get_observed()
        if pos is None:
            pos = self.get_scene_center()
        edges = []
        # the following line is quirky because it relies on core.observer.Observed.listeners
        if hasattr(obs, "listeners"):
            edges = [l() for l in obs.listeners if isinstance(l(), Edge)]
        elif hasattr(self, "fakeParent"): # I am a defaultConnector
            par = self.fakeParent
            scene = par.scene()
            if scene is None:
                return
            observers = scene.get_graphical_edges_connected_to(obs)
            if observers:
                edges = [l() for l in observers if l is not None]
        for e in edges:
            e.notify(obs, ("metadata_changed", "connectorPosition", pos))

    #####################
    # ----Qt World----  #
    #####################
    def itemChange(self, change, value):
        if change & (qtutils.ItemScenePositionHasChanged | qtutils.ItemPositionHasChanged):
            self.notify_position_change()
            return value

    def mousePressEvent(self, event):
        scene = self.scene()
        if (scene and event.buttons() & self.__makeConnectionMouseButton and
            event.modifiers() == self.__makeConnectionModifiers):
            scene._new_edge_start(self.get_scene_center())
        else:
            super(self.__class__, self).mousePressEvent(event)


#------*************************************************------#
def defaultPaint(owner, painter, paintOptions, widget):
    rect = owner.boundingRect()
    painter.drawEllipse(rect)


class Vertex(Element):
    """An abstract graphic item that represents a graph vertex.

    The actual implementation is done in the derived class. What this
    intermediate implementation does is that it provides the basics
    for handling edge creation from one node to the other.
    It also provides a state based pluggable painting system,
    meant to customize the painting from the application side.
    Of course, if it doesn't match your needs you
    can override it completely in your subclass."""


    class InvisibleConnector(QtGui.QGraphicsEllipseItem, Connector):
        size = 10
        def __init__(self, parent, *args, **kwargs):
            QtGui.QGraphicsEllipseItem.__init__(self, 0, 0 , self.size, self.size, None)
            Connector.__init__(self, *args, **kwargs)
            self.setBrush(QtGui.QBrush(QtCore.Qt.darkGreen))
            # Needs to be visible or else won't receive events
            # we override paint in order to hide the item
            self.setVisible(True)
            self.fakeParent = parent



        def position_changed(self, *args):
            """reimplemented to do nothing. otherwise caught
            position changes from the model and ignored
            the position it was forced to"""
            pass

        def paint(self, painter, options, widget):
            pass

        itemChange = qtutils.mixin_method(Connector, QtGui.QGraphicsEllipseItem,
                                  "itemChange")

    ####################################
    # ----Instance members follow----  #
    ####################################
    def __init__(self, vertex, graph, defaultCenterConnector=False):
        """
        :Parameters:
            - vertex - the vertex to observe.
            - graph - the owner of the vertex
        """
        Element.__init__(self, vertex, graph)
        self.__connectors = []
        self.__defaultConnector = None

        self.setZValue(1.0)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(qtutils.ItemSendsGeometryChanges)
        self.__paintStrategy = defaultPaint
        if defaultCenterConnector:
            self.__defaultConnector = Vertex.InvisibleConnector(self, vertex, graph)

    vertex = baselisteners.GraphElementListenerBase.get_observed

    def iter_connectors(self, filter=lambda x:True):
        return (c for c in self.__connectors if filter(c))

    def get_scene_center(self):
        """retrieve the center of the widget on the scene"""
        center = self.sceneBoundingRect().center()
        return [center.x(), center.y()]

    def add_to_view(self, view):
        Element.add_to_view(self, view)
        if self.__defaultConnector:
            self.__defaultConnector.add_to_view(view)

    def remove_from_view(self, view):
        Element.remove_from_view(self, view)
        if self.__defaultConnector:
            self.__defaultConnector.remove_from_view(view)

    def set_highlighted(self, value):
        pass

    def set_painting_strategy(self, strat):
        self.__paintStrategy = strat

    def add_connector(self, connector):
        assert isinstance(connector, Connector)
        self.__connectors.append(connector)

    def remove_connector(self, connector):
        assert isinstance(connector, Connector)
        self.__connectors.remove(connector)

    def notify(self, sender, event):
        if event == "notify_position_change":
            self.notify_position_change()
        else:
            Element.notify(self, sender, event)

    def notify_position_change(self):
        """ Triggers a visual refresh of anything that observes the position
        of the vertex. """
        if self.__defaultConnector:
            center = self.sceneBoundingRect().center()
            self.__defaultConnector.setPos(center.x() - Vertex.InvisibleConnector.size / 2.0,
                                            center.y() - Vertex.InvisibleConnector.size / 2.0)
            self.__defaultConnector.notify_position_change()
        for c in self.__connectors:
            c.notify_position_change()

    #####################
    # ----Qt World----  #
    #####################
    def itemChange(self, change, value):
        """ Used mainly to capture position changes from the QGraphicsScene
        and store it in the model so that it can be saved. """
        sc = self.scene()
        if sc:
            sc.invalidate()

        if change == QtWidgets.QGraphicsItem.ItemVisibleHasChanged:
            self.notify_position_change()

        elif change == qtutils.ItemPositionHasChanged:
            self.deaf(True)
            point = QtCore.QPointF(from_qvariant(value))
            self.store_view_data(position=[point.x(), point.y()])
            self.deaf(False)
            self.notify_position_change()

        return value

    def paint(self, painter, option, widget):
        """Qt-specific call to paint things."""
        if self.__paintStrategy is None:
            self.__paintStrategy = defaultPaint
        self.__paintStrategy(self, painter, option, widget)



#------*************************************************------#
class Edge(Element):
    """Base class for Qt based edges."""

    def __init__(self, edge=None, graph=None, src=None, dst=None):
        Element.__init__(self, edge, graph)
        self.setFlag(QtWidgets.QGraphicsItem.ItemIsSelectable)
        self.setZValue(0.5)
        self.srcPoint = QtCore.QPointF()
        self.dstPoint = QtCore.QPointF()
        self.__edge_creator = self.set_edge_creator(edgefactory.LinearEdgePath())

        self.setPen(QtGui.QPen(QtCore.Qt.black, 2,
                               QtCore.Qt.SolidLine,
                               QtCore.Qt.RoundCap,
                               QtCore.Qt.RoundJoin))

        self.dstBBox = self.srcBBox = None
        if src is not None: self.set_observed_source(src)
        if dst is not None: self.set_observed_destination(dst)
        self.setPath(self.__edge_creator.get_path(self.srcPoint, self.dstPoint))

    edge = baselisteners.GraphElementListenerBase.get_observed

    def initialise_from_model(self):
        pass

    def set_edge_creator(self, creator):
        self.__edge_creator = creator
        self.setPath(self.__edge_creator.get_path(self.srcPoint, self.dstPoint))
        return creator

    def change_observed(self, old, new):
        if old == self.srcBBox():
            self.set_observed_source(new)
        elif old == self.dstBBox():
            self.set_observed_destination(new)
        else:
            Element.change_observed(self, old, new)
        return

    def set_observed_source(self, src):
        if self.srcBBox is None:
            self.srcBBox = baselisteners.BlackBoxModel(self, src)
        else:
            self.srcBBox.clear_observed()
            self.srcBBox(src)

    def set_observed_destination(self, dst):
        if self.dstBBox is None:
            self.dstBBox = baselisteners.BlackBoxModel(self, dst)
        else:
            self.dstBBox.clear_observed()
            self.dstBBox(dst)

    def clear_observed(self, *args):
        self.srcBBox.clear_observed()
        self.dstBBox.clear_observed()
        Element.clear_observed(self, *args)

    def update_line_source(self, *pos):
        self.srcPoint = QtCore.QPointF(*pos)
        path = self.__edge_creator.get_path(self.srcPoint, self.dstPoint)
        self.setPath(path)

    def update_line_destination(self, *pos):
        self.dstPoint = QtCore.QPointF(*pos)
        path = self.__edge_creator.get_path(self.srcPoint, self.dstPoint)
        self.setPath(path)

    def notify(self, sender, event):
        if(event[0] == "metadata_changed"):
            if(event[1] == "connectorPosition"):
                pos = event[2]
                if(sender == self.srcBBox()):
                    self.update_line_source(*pos)
                if(sender == self.dstBBox()):
                    self.update_line_destination(*pos)
            elif(event[1] == "hide" and (sender == self.dstBBox() or sender == self.srcBBox())):
                if event[2]:
                    self.setVisible(False)
                else:
                    self.setVisible(True)

    def remove(self):
        self.graph().remove_edge(self.srcBBox(), self.dstBBox())

    ############
    # Qt World #
    ############
    def shape(self):
        path = self.__edge_creator.shape()
        if not path:
            return QtGui.QGraphicsPathItem.shape(self)
        else:
            return path

    def itemChange(self, change, value):
        """ Callback when item has been modified (move...) """
        # hack to update start and end points:
        if change == QtWidgets.QGraphicsItem.ItemVisibleHasChanged:
            try:
                srcGraphical = filter(lambda x: isinstance(x(), Connector),
                                      self.srcBBox().listeners)[0]()
                dstGraphical = filter(lambda x: isinstance(x(), Connector),
                                      self.dstBBox().listeners)[0]()
                srcGraphical.notify_position_change()
                dstGraphical.notify_position_change()
            except:
                # possible errors :
                # -filter yielded an empty list: index out of range
                # -item 0 of list is a weakref whose refered object has died
                # -other.
                pass

        elif (change == QtWidgets.QGraphicsItem.ItemSelectedChange):
            if(bool(value)):
                color = QtCore.Qt.blue
            else:
                color = QtCore.Qt.black

            self.setPen(QtGui.QPen(color, 2,
                                   QtCore.Qt.SolidLine,
                                   QtCore.Qt.RoundCap,
                                   QtCore.Qt.RoundJoin))

        return QtWidgets.QGraphicsItem.itemChange(self, change, value)


class FloatingEdge(Edge):

    def __init__(self, srcPoint, graph):
        Edge.__init__(self, None, graph, None, None)
        self.srcPoint = QtCore.QPointF(*srcPoint)
        self.dstPoint = QtCore.QPointF(self.srcPoint)

    def notify(self, sender, event):
        return

    def consolidate(self, graph):
        try:
            srcVertex, dstVertex , sItem, dItem = self.get_connections()
            if(srcVertex == None or dstVertex == None):
                return
            self.scene().add_edge(srcVertex, dstVertex)
        except Exception, e:
            pass
            # print "consolidation failed :", type(e), e,\
            # ". Are you sure you plugged the right ports?"
        return

    def get_connections(self):
        # find the vertex items that were activated

        srcVertexItem = self.scene().find_closest_connectable(self.srcPoint, boxsize=2)
        dstVertexItem = self.scene().find_closest_connectable(self.dstPoint, boxsize=2)

        scene = self.scene()

        if(not scene.is_connectable(srcVertexItem) or
            not scene.is_connectable(dstVertexItem)):
            raise Exception("Non connectable types for : " + str(srcVertexItem) + " : " + \
                                str(dstVertexItem))
            return None, None, None, None

        # if the input and the output are on the same vertex...
        if(srcVertexItem == dstVertexItem):
            raise Exception("Nonsense connection : plugging self to self.")

        return srcVertexItem.get_observed(), dstVertexItem.get_observed(), srcVertexItem, dstVertexItem


#------*************************************************------#
class Scene(QtGui.QGraphicsScene, baselisteners.GraphListenerBase):
    """A Qt implementation of GraphListenerBase"""

    __instanceMap__ = weakref.WeakKeyDictionary()

    # A few signals that strangely enough don't exist in QWidget
    focusedItemChanged = QtCore.Signal(QtGui.QGraphicsScene, Element)


    @classmethod
    def make_scene(cls, graph, clone=False, parent=None):
        if graph is not None:
            # if the graph has already a qtgraphview.Scene GraphListener
            # reuse it:
            existingScene = cls.__instanceMap__.get(graph)
            if existingScene is None or clone is True:
                existingScene = Scene(parent)
                cls.__instanceMap__[graph] = existingScene
            return existingScene
        else:
            return Scene(parent)

    def __init__(self, parent):
        QtGui.QGraphicsScene.__init__(self, parent)
        baselisteners.GraphListenerBase.__init__(self)
        self.__selectAdditions = False # select newly added items
        self.__views = set()

        # -- used by upper class to operate snapping to connectors. --
        self._connector_types.add(Connector)


    #############################################################################
    # Functions to correctly cooperate with the View class (reference counting) #
    #############################################################################
    def register_view(self, view):
        self.__views.add(weakref.ref(view))

    def unregister_view(self, view, scene):
        toDiscard = None
        for v in self.__views:
            if v() == view : toDiscard = v; break
        if toDiscard:
            self.__views.remove(toDiscard)
        try: self.get_graph().unregister_listener(view)
        except : pass
        if len(self.__views) == 0: # cleanup before suicide?
            self.clear()

    #################################
    # IGraphListener implementation #
    #################################
    def get_scene(self):
        return self

    def find_closest_connectable(self, pos, boxsize=10.0):
        # creation of a square to find connectables inside.
        if isinstance(pos, QtCore.QPointF) : pos = pos.x(), pos.y()
        rect = QtCore.QRectF((pos[0] - boxsize / 2), (pos[1] - boxsize / 2), boxsize, boxsize)
        dstPortItems = self.items(rect)
        dstPortItems = [item for item in dstPortItems if self.is_connectable(item)]

        distance = float('inf')
        dstPortItem = None
        for item in dstPortItems:
            d = sqrt((item.boundingRect().center().x() - pos[0]) ** 2 +
                        (item.boundingRect().center().y() - pos[1]) ** 2)
            if d < distance:
                distance = d
                dstPortItem = item
        return dstPortItem

    def post_addition(self, element):
        if self.__selectAdditions:
            element.setSelected(True)

    def rebuild(self):
        """ Build the scene with graphic vertex and edge"""
        g = self.get_graph()
        ga = self.get_adapter()
        go = self.get_observable_graph()
        self.clear()
        self.set_graph(g, ga, go)
        self.initialise_from_model()

    def clear(self):
        """ Remove all items from the scene """
        # do not use the following even though it is faster.
        # qt might just delete stuff that is owned by Python.
        # QtGui.QGraphicsScene.clear(self)
        items = self.items()
        for i in items:
            self.removeItem(i) # let gc do the rest.
        baselisteners.GraphListenerBase.clear(self)
        gc.collect()

    ##################
    # QtWorld-Events #
    ##################
    def mouseMoveEvent(self, event):
        if(self._is_creating_edge()):
            pos = event.scenePos()
            pos = [pos.x(), pos.y()]
            self._new_edge_set_destination(*pos)
        QtGui.QGraphicsScene.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        if(self._is_creating_edge()):
            self._new_edge_end()
        QtGui.QGraphicsScene.mouseReleaseEvent(self, event)

    #########################
    # Other utility methods #
    #########################
    def select_added_elements(self, val):
        warnings.warn(DeprecationWarning("Please use self.%s instead" % ("select_added_items",)),
                      stacklevel=2)
        self.select_added_items(val)

    def select_added_items(self, val):
        self.__selectAdditions = val

    def get_items(self, filterType=None, subcall=None):
        """ """
        if filterType and not isinstance(filterType, tuple):
            filterType = filterType,
        return [ (item if subcall is None else subcall(item))
                 for item in self.items() if
                 (True if filterType is None else isinstance(item, filterType))]

    def get_selected_items(self, filterType=None, subcall=None):
        """ """
        if filterType and not isinstance(filterType, tuple):
            filterType = filterType,
        return [ (item if subcall is None else subcall(item))
                 for item in self.items() if item.isSelected() and
                 (True if filterType is None else isinstance(item, filterType))]

    def get_selection_center(self, selection=None):
        """ """
        items = None
        if selection: items = selection
        else: items = self.get_selected_items()

        l = len(items)
        if(l == 0) : return QtCore.QPointF(30, 30)

        sx = sum((i.pos().x() for i in items))
        sy = sum((i.pos().y() for i in items))
        return QtCore.QPointF(float(sx) / l, float(sy) / l)



#------*************************************************------#
def deprecate(methodName, newName=None):
    """create deprecation wrappers"""
    if newName is None : newName = methodName
    def deprecation_wrapper(self, *args, **kwargs):
        warnings.warn(DeprecationWarning("Please use self.scene().%s instead" % (newName,)),
                       stacklevel=2)
        return getattr(self.scene(), newName)(*args, **kwargs)
    return deprecation_wrapper


class View(QtGui.QGraphicsView, baselisteners.GraphViewBase):
    """A View implementing client customisation """

    class AcceptEvent(object):
        def __init__(self):
            self.accept = False

    # A few signals that strangely enough don't exist in QWidget
    closing = QtCore.Signal(QtGui.QGraphicsView, QtGui.QGraphicsScene)

    # Some other signals that can be useful
    copyRequest = QtCore.Signal(QtGui.QGraphicsView, QtGui.QGraphicsScene, AcceptEvent)
    cutRequest = QtCore.Signal(QtGui.QGraphicsView, QtGui.QGraphicsScene, AcceptEvent)
    pasteRequest = QtCore.Signal(QtGui.QGraphicsView, QtGui.QGraphicsScene, AcceptEvent)
    deleteRequest = QtCore.Signal(QtGui.QGraphicsView, QtGui.QGraphicsScene, AcceptEvent)

    ####################################
    # ----Instance members follow----  #
    ####################################
    def __init__(self, parent):
        QtGui.QGraphicsView.__init__(self, parent)
        self.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

        self.__defaultDropHandler = None
        self.__mimeHandlers = {}
        self.__pressHotkeyMap = {}
        self.__releaseHotkeyMap = {}

        # ---Qt Stuff---
#        self.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.setRenderHint(QtGui.QPainter.Antialiasing)
        self.setTransformationAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QtGui.QGraphicsView.AnchorViewCenter)
        self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)

    def setScene(self, scene):
        """ Overload of QGraphicsView.setScene to correctly handle multiple views
        of the same scene using reference counting. """
        self.__scene = scene
        if scene is not None:
            scene.register_view(self)
            self.closing.connect(scene.unregister_view)
        QtGui.QGraphicsView.setScene(self, scene)

    def set_canvas(self, scene):
        self.setScene(scene)

    ##################
    # QtWorld-Events #
    ##################
    def set_mime_handler_map(self, mapping):
        self.__mimeHandlers.update(mapping)

    def set_keypress_handler_map(self, mapping):
        self.__pressHotkeyMap.update(mapping)

    def set_keyrelease_handler_map(self, mapping):
        self.__releaseHotkeyMap = mapping

    def set_default_drop_handler(self, handler):
        self.__defaultDropHandler = handler

    def wheelEvent(self, event):
        delta = -event.delta() / 2400.0 + 1.0
        self.scale_view(delta)

    # ----drag and drop----
    def accept_drop(self, event):
        """ Return the format of the object if a handler is registered for it.
        If not, if there is a default handler, returns True, else returns False.
        """
        for format in self.__mimeHandlers.keys():
            if event.mimeData().hasFormat(format): return format
        return True if self.__defaultDropHandler else False

    def dragEnterEvent(self, event):
        """While the user hasn't released the object, this method is called
        to tell qt if the view accepts the object or not."""
        event.setAccepted(True if self.accept_drop(event) else False)

    def dragMoveEvent(self, event):
        format = self.accept_drop(event)
        if (format):
            event.setDropAction(QtCore.Qt.MoveAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        format = self.accept_drop(event)
        handler = self.__mimeHandlers.get(format)
        if(handler):
            handler(event)
        else:
            self.__defaultDropHandler(event)
        # Do not call the basic implementation
        # as it does a "move" instead of a "copy"
        # and the item is deleted from where it was
        # dragged from :
        # QtGui.QGraphicsView.dropEvent(self, event)

    # ----hotkeys----
    def keyPressEvent(self, event):
        combo = event.modifiers().__int__(), event.key()
        action = self.__pressHotkeyMap.get(combo)
        if(action):
            action(event)
        else:
            QtGui.QGraphicsView.keyPressEvent(self, event)

        if not event.isAccepted():
            key = event.key()
            scene = self.scene()
            acceptEvent = View.AcceptEvent()
            if event.modifiers() == QtCore.Qt.ControlModifier:
                if key == QtCore.Qt.Key_C:
                    self.copyRequest.emit(self, scene, acceptEvent)
                elif key == QtCore.Qt.Key_X:
                    self.cutRequest.emit(self, scene, acceptEvent)
                elif key == QtCore.Qt.Key_V:
                    self.pasteRequest.emit(self, scene, acceptEvent)
            else:
                if key == QtCore.Qt.Key_Delete:
                    self.deleteRequest.emit(self, scene, acceptEvent)
            if acceptEvent.accept:
                event.accept()


    def keyReleaseEvent(self, event):
        combo = event.modifiers().__int__(), event.key()
        action = self.__releaseHotkeyMap.get(combo)
        if(action):
            action(event)
        else:
            QtGui.QGraphicsView.keyReleaseEvent(self, event)

    # ----low level and Qt-Related----
    def closeEvent(self, evt):
        """a big hack to cleanly remove items from the view
        and delete the python objects so that they stop leaking
        on some operating systems"""
        if self.testAttribute(QtCore.Qt.WA_DeleteOnClose):
            self.closing.emit(self, self.scene())
            self.setScene(None)
        return QtGui.QGraphicsView.closeEvent(self, evt)

    #########################
    # Other utility methods #
    #########################
    def scale_view(self, factor):
        self.scale(factor, factor)

    def show_entire_scene (self) :
        """Scale the scene and center it
        in order to display the entire content
        without scrolling.
        """
        self.fitInView(self.scene().itemsBoundingRect(), QtCore.Qt.KeepAspectRatio)

    ######################
    # Deprecated methods #
    ######################
    graph = deprecate("graph")
    set_graph = deprecate("set_graph")
    rebuild_scene = deprecate("rebuild")
    clear_scene = deprecate("clear")
    get_selected_items = deprecate("get_items")
    get_selected_items = deprecate("get_selected_items")
    get_selection_center = deprecate("get_selection_center")
    select_added_elements = deprecate("select_added_elements")
    post_addition = deprecate("post_addition")
    notify = deprecate("notify")



if __debug__:
    import interfaces
    interfaces.IGraphListener.check(Scene)

def QtGraphStrategyMaker(*args, **kwargs):
    _type = base.GraphStrategyMaker(*args, **kwargs)
    _type.__sceneType__ = Scene
    return _type

################################
# SOME DEFAULT IMPLEMENTATIONS #
################################
class DefaultGraphicalEdge(Edge, QtGui.QGraphicsPathItem):
    def __init__(self, edge=None, graph=None, src=None, dest=None):
        QtGui.QGraphicsPathItem.__init__(self, None)
        Edge.__init__(self, edge, graph, src, dest)
        self.set_edge_creator(edgefactory.LinearEdgePath())

    store_view_data = None
    get_view_data = None


class DefaultGraphicalFloatingEdge(QtGui.QGraphicsPathItem, FloatingEdge):
    def __init__(self, srcPoint, graph):
        """ """
        QtGui.QGraphicsPathItem.__init__(self, None)
        FloatingEdge.__init__(self, srcPoint, graph)
        self.set_edge_creator(edgefactory.LinearEdgePath())


class DefaultGraphicalVertex(Vertex, QtGui.QGraphicsEllipseItem):
    circleSize = 10.0 * 2
    def __init__(self, vertex, graph):
        QtGui.QGraphicsEllipseItem .__init__(self, 0, 0, self.circleSize, self.circleSize, None)
        Vertex.__init__(self, vertex, graph, defaultCenterConnector=True)

    mousePressEvent = qtutils.mixin_method(Vertex, QtGui.QGraphicsEllipseItem,
                                   "mousePressEvent")
    itemChange = qtutils.mixin_method(Vertex, QtGui.QGraphicsEllipseItem,
                                      "itemChange")
    paint = qtutils.mixin_method(QtGui.QGraphicsEllipseItem, None,
                         "paint")
