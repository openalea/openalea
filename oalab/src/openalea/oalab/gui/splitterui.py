# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2011 INRIA - CIRAD - INRA
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
__revision__ = " $Id: splitterui.py 4222 2014-04-23 09:15:04Z gbaty $ "


"""
Contains the implementation of a recursively splittable UI.
"""

from openalea.vpltk.qt import QtCore, QtGui

try:
    from openalea.core import logger
    myLogger = logger.get_logger("openalea.visualea.splitterui")
    logger.connect_loggers_to_handlers(myLogger, logger.get_handler_names())

    def log(level, msg):
        myLogger.log(level, msg)
except:
    def log(level, msg):
        print "debug messsage", level, msg

from collections import deque


class BinaryTree(object):

    """A quirky binary tree that only implements
    node splitting methods. It also implements a
    visitable Breadth First iterating traversal.

    :Examples:

    >>> g = BinaryTree()
    >>> # fid : first child id, sid : second child id
    >>> fid, sid = g.split_node(0) #first node is always 0
    >>> # now node 0 has two children : 1 and 2
    >>> g.collapse_node(0)
    >>> # now node 0 has no more child.
    """

    #########################################################################
    # Exception definitions - Exception definitions - Exception definitions #
    #########################################################################
    class BadIdException(Exception):

        """Raised when you referred to an id that doesn't have a reason
        to exist in the place you looked for it, eg: if an id doesn't have
        children and you ask for its children, you'll get this. It doesn't
        mean that ID doesn't exist in the Tree
        """

        def __init__(self, vid):
            Exception.__init__(self, "Bad node id: " + str(vid))

    class NonAnteTerminalException(Exception):

        """Raised when trying to collapse a node whose children themselves have children."""

        def __init__(self, vid):
            Exception.__init__(self, "Can only collapse nodes terminal-1: " + str(vid))

    class ParentCompleteException(Exception):

        """You should never see this one. Raised if trying to add a child to a node
        that already has two children. This could just ruin the binary concept eh!"""

        def __init__(self, vid):
            Exception.__init__(self, "Parent already complete: " + str(vid))

    class PropertyException(Exception):

        """Raised when a node doesn't have the property you requested"""

        def __init__(self, vid, key):
            Exception.__init__(self, "No %s for node %d" % (str(key), vid))
    #########################################################################
    # /end Exception definitions - Exception definitions - Exception def... #
    #########################################################################

    class PrintingVisitor(object):

        """ A simple visitor to print node ids as is goes by visiting

        :Examples:
        >>> g = BinaryTree()
        >>> ....
        >>> visitor= BinaryTree.PrintingVisitor()
        >>> g.visit_i_breadth_first(visitor)
        """

        def visit(self, vid):
            print vid
            return False, False  # don't ignore first or second child

    def __init__(self):
        """Construct a BinaryTree"""
        self._toChildren = {}  # toCh #: map parent ids to two child ids
        self._toParents = {}  # toPar #: map childid to parent id
        self._properties = {}  # prop #: map vid to a dictionnary of string->val
        self.__root = 0  # : our starting point
        self.__vid = 1  # : the first vertex that will be added. Gets incremented
        # -- Construct the root node --
        self._properties[0] = {}
        self._toParents[0] = None

    def toString(self, props=[]):
        filteredProps = dict((vid, dict((k, v) for k, v in di.iteritems() if k in props))
                             for vid, di in self._properties.iteritems())
        return repr(self._toChildren) + ", " + repr(self._toParents) + ", " + repr(filteredProps)

    @classmethod
    def _convert_keys_to_int(cls, dic):
        for k in dic.keys():
            if isinstance(k, int):
                continue
            dic[int(k)] = dic[k]
            del dic[k]
        return dic

    @classmethod
    def fromJSON(cls, layout):
        g = cls()
        toPar = layout.get('parents', {})
        toCh = layout.get('children', {})
        props = layout.get('properties', {})

        cls._convert_keys_to_int(toPar)
        cls._convert_keys_to_int(toCh)
        cls._convert_keys_to_int(props)

        g.__vid = max(props.iterkeys()) + 1
        g._toChildren = toCh.copy()
        g._toParents = toPar.copy()
        g._properties = props.copy()
        return g

    @classmethod
    def fromString(cls, rep):
        try:
            tup = eval(rep)
        except:
            return None

        g = cls()
        toCh, toPar, props = tup
        g.__vid = max(props.iterkeys()) + 1
        g._toChildren = toCh.copy()
        g._toParents = toPar.copy()
        g._properties = props.copy()
        return g, tup

    def __contains__(self, vid):
        return vid in self._properties

    def parent(self, vid):
        """Returns the parent of vid.
        :Parameters:
         - `vid` (int) - the id of the vertex whose parent is requested

        Raises BinaryTree.BadIdException if vid is not in the list of children.
        """
        if vid not in self._toParents:
            raise self.__class__.BadIdException(vid)
        return self._toParents[vid]

    def leaves(self):
        return [vid for vid in self._properties if not self.has_children(vid)]

    def children(self, vid):
        """Returns the children of vid.
        :Parameters:
         - `vid` (int) - the id of the vertex whose children are requested

        Raises BinaryTree.BadIdException if vid is not in the list of parents.
        """
        if vid not in self._toChildren:
            raise self.__class__.BadIdException(vid)
        return self._toChildren[vid]

    def has_children(self, vid):
        """Returns true if vid has children.
        :Parameters:
         - `vid` (int) - the id of the vertex to check children for.
        """
        return vid in self._toChildren

    def node_is_first_child(self, vid):
        """Returns true if vid is the first child (left), else false.
        :Parameters:
         - `vid` (int) - the id of the node whose position will be checked

        Raises BinaryTree.BadIdException if vid is not in the list of children.
        """
        if vid == self.__root:
            return True
        if vid not in self._toParents:
            raise self.__class__.BinaryTree.BadIdException(vid)
        par = self._toParents[vid]
        chds = self.children(par)
        return chds.index(vid) == 0

    def split_node(self, vid):
        """Add two children to vid and return their ids.

        Raises BinaryTree.BadIdException if vid is not in the graph."""
        if vid not in self._properties:
            raise self.__class__.BadIdException(vid)
        fid, sid = self.__vid, self.__vid + 1
        self.__vid += 2
        self.__new_node(fid, vid)
        self.__new_node(sid, vid)
        return fid, sid

    def collapse_node(self, vid):
        """Remove children from vid and return their ids.

        Raises BinaryTree.BadIdException if vid is not in the graph.
        Raises BinaryTree.NonAnteTerminalException if children of vid have children."""
        if vid not in self._properties:
            raise self.__class__.BadIdException(vid)
        fid, sid = self._toChildren[vid]
        if fid in self._toChildren or sid in self._toChildren:
            raise self.__class__.NonAnteTerminalException(vid)
        self.__del_node(fid, vid)
        self.__del_node(sid, vid)
        return fid, sid

    def __new_node(self, vid, parent):
        """PRIVATE. Create a new node with id  `vid` and attached to `parent`.

        Raises BinaryTree.ParentCompleteException if parent already has two children"""
        chen = self._toChildren.setdefault(parent, [])
        if len(chen) > 1:
            raise self.__class__.ParentCompleteException(parent)
        chen.append(vid)
        self._toParents[vid] = parent
        self._properties[vid] = {}

    def __del_node(self, vid, parent):
        """PRIVATE. Remove a node with id  `vid` and detach it from `parent`."""
        chen = self._toChildren.setdefault(parent, [])
        if len(chen) == 0:
            return
        chen.remove(vid)
        if len(chen) == 0:
            self._toChildren.pop(parent, None)
        self._toChildren.pop(vid, None)
        self._toParents.pop(vid, None)
        self._properties.pop(vid, None)

    def set_property(self, vid, key, value):
        """Replaces/adds property `key` with value `value` to node `vid`.
        :Parameters:
         - `vid` (int) - id of the vertex
         - `key` (str) - name of the property
         - `value` (object) - the value to store
        """
        if vid not in self._properties:
            raise self.__class__.BadIdException(vid)
        self._properties[vid][key] = value

    def has_property(self, vid, key):
        """Tests if key is a valid property for vid.
        :Parameters:
         - `vid` (int) - id of the vertex
         - `key` (str) - name of the property

        Raises BinaryTree.BadIdException if `vid` is not in graph.
        """
        if vid not in self._properties:
            raise self.__class__.BadIdException(vid)
        return key in self._properties[vid]

    def get_property(self, vid, key):
        """Retreives property `key` from node `vid`.
        :Parameters:
         - `vid` (int) - id of the vertex
         - `key` (str) - name of the property

        Raises BinaryTree.BadIdException if `vid` is not in graph.
        Raises BinaryTree.PropertyException if `key` is not a property of `vid` (ie. if not set yet)
        """
        if vid not in self._properties:
            raise self.__class__.BadIdException(vid)
        if key not in self._properties[vid]:
            raise self.__class__.PropertyException(vid, key)
        return self._properties[vid].get(key)

    def pop_property(self, vid, key):
        """Retreives property `key` and removes it from node `vid`
        :Parameters:
         - `vid` (int) - id of the vertex
         - `key` (str) - name of the property

        Raises BinaryTree.BadIdException if `vid` is not in graph.
        Raises BinaryTree.PropertyException if `key` is not a property of `vid` (ie. if not set yet)
        """
        if vid not in self._properties:
            raise self.__class__.BadIdException(vid)
        if key not in self._properties[vid]:
            raise self.__class__.PropertyException(vid, key)
        return self._properties[vid].pop(key)

    def visit_i_breadth_first(self, visitor=None, node=0):
        """Iteratively (not recursively) traverse the tree. If visitor is given
        visitor.visit(vid) will be called with the current vertex id.

        The visitor should take care not to add/remove nodes of the graph.

        :Parameters:
         - visitor (object) - an instance that implements a visit(vid)
                              method and does whatever it wants next.
         - node (int) - id of the node to start the traversal from.
        """
        nodeStack = deque()
        nodeStack.appendleft(node)
        while not len(nodeStack) == 0:
            currNode = nodeStack.pop()
            ignoreFirst, ignoreSecond = False, False
            if visitor != None:
                ignoreFirst, ignoreSecond = visitor.visit(currNode)
            fid, sid = self._toChildren.get(currNode, (None, None))
            if fid != None and not ignoreFirst:
                nodeStack.appendleft(fid)
            if sid != None and not ignoreSecond:
                nodeStack.appendleft(sid)


class DraggableWidget(object):

    """ A base class that implements the mechanism to drag a widget around.
    Use it as a mixin of QWidget derived  classes.

    When dragging starts the following internal variables are set:
    - self._isMoving : True
    - self._offset   : Distance from cursor position to origin of widget
    - self._oldpos   : Position of cursor at previous move event.
                       Updated at each mouse move event. In parent coordinates
    - self._startpos : Position of cursor at the beginning of the dragging.

    All these attributes are reverted to False/None at the end
    of the drag (when user releases mouse button).
    """

    def __init__(self):
        """Contruct a DraggableWidget. Be sure to call this!"""
        self._isMoving = False
        self._offset = None
        self._oldpos = None
        self._startpos = None
        self._hovered = False
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setAttribute(QtCore.Qt.WA_Hover)

    def _fixGeometry(self, newPt, geom):
        """
        During the mouseMoveEvent the abstract method `_fixGeometry`
        is called. It takes the potentially new position of the widget in parent
        coordinates and the original geometry of self (QtCore.QRect - in parent coordinates)
        and returns another QtCore.QRect (always in parent coordinates)
        and a boolean. If the boolean is not True, the returned geometry will be set
        as the geometry of self.

        Use this _fixGeometry method to validate the potentially new position
        of the widget origin and return the fixed geometry and False.

        Use this _fixGeometry method to just catch dragging events and abuse it,
        to do things when mouse button is down, return the original geometry and True
        """
        return geom, False

    ##############################
    # Qt Event reimplementations #
    ##############################
    def event(self, event):
        typ = event.type()
        if typ == QtCore.QEvent.HoverEnter:
            self._hovered = True
            self.update()
        elif typ == QtCore.QEvent.HoverLeave:
            self._hovered = False
            self.update()
        return QtGui.QWidget.event(self, event)

    def mousePressEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            self._isMoving = True
            # this is in local coordinates
            self._offset = event.pos() - self.contentsRect().topLeft()
            # this is in global coordinates
            self._oldpos = event.pos() - self._offset + self.geometry().topLeft()
            self._startpos = event.pos() - self._offset + self.geometry().topLeft()
        else:
            QtGui.QWidget.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        if self._isMoving:
            geom = self.geometry()
            # newPt is in parent coordinates
            newPt = event.pos() - self._offset + geom.topLeft()
            geom, noChange = self._fixGeometry(newPt, geom)
            if not noChange:
                self.setGeometry(geom)
            self._oldpos = newPt
        else:
            QtGui.QWidget.mouseMoveEvent(self, event)

    def mouseReleaseEvent(self, event):
        if event.buttons() & QtCore.Qt.LeftButton:
            self._isMoving = False
            self._offset = None
            self._offset = None
            self._startpos = None
        else:
            QtGui.QWidget.mouseReleaseEvent(self, event)


class SplittableUI(QtGui.QWidget):

    """A widget that tries to mimic the Blender UI.
    Each pane contains a settable widget."""

    __spacing__ = 4
    __hspacing__ = __spacing__ / 2.0

    # used when serializing (toString) the layout
    # of the splitter to identify which properties
    # of the vertices in the binary tree will be serialized
    reprProps = ["amount", "splitDirection"]

    widgetMenuRequest = QtCore.Signal(QtCore.QPoint, int)
    dragEnterEventTest = QtCore.Signal(object, QtGui.QDragEnterEvent)
    dropHandlerRequest = QtCore.Signal(object, int, QtGui.QDropEvent)

    def __init__(self, parent=None, content=None):
        """Contruct a SplittableUI.
        :Parameters:
         - parent (QtGui.QWidget)  - The parent widget
         - content (QtGui.QWidget) - The widget to display in pane at level 0
        """
        QtGui.QWidget.__init__(self, parent)
        self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        self.setAcceptDrops(True)
        # -- our backbone: --
        self._g = BinaryTree()
        # -- contains geometry information (a vid->QRect mapping) --
        self._geomCache = {}
        # -- initialising the pane at level 0 --
        self._geomCache[0] = self.contentsRect()
        self._install_child(0, content)

    def leaves(self):
        return self._g.leaves()

    def getPlaceHolder(self):
        return None

    def splitPane(self, content, paneId, direction, amount):
        """Split a pane into two.
        The content of paneId will be transfered
        to one of the children. if amount if <0.5 it will be transfered to
        the first child, else to the second.

        :Parameters:
         - `content` (QtGui.QWidget) - A widget to place in the newly create pane
         - `paneId`  (int)           - Id of of the pane to split
         - `direction` (QtCore.Qt.Orientation) - Put the two children side-by-side (QtCore.Qt.Horizontal) or
                                                 on top of each other (QtCore.Qt.Vertical).
         - `amount` (float) - Between 0.0 and 1.0. Determines at what percentage of paneId will happen the split.
        """
        g = self._g
        try:
            fid, sid = g.split_node(paneId)
        except BinaryTree.ParentCompleteException:
            return

        widgetFromParent = self._split_parent(paneId, direction, amount)
        # -- transfer the parent's widget to either child
        # and install container in other child --
        if amount < 0.5:
            self._install_child(sid, widgetFromParent)
            self._install_child(fid, content)
        else:
            self._install_child(fid, widgetFromParent)
            self._install_child(sid, content)

        self.computeGeoms(paneId)
        if content is not None:
            content.show()

    def collapsePane(self, paneId, toSecond=True):
        """Collapse paneId's chhildren into one. The content of one child migrates
        to the paneId, the other is removed from the view and returned.

        The content of paneId will be transfered
        to one of the children. if amount if <0.5 it will be transfered to
        the first child, else to the second.

        :Parameters:
         - `paneId` (int) - Id of the pane to collapse (ie. child divisions will be removed)
         - `toSecond` (bool) - If true, the second child's widget will be removed, the first will
                               take all the space (and the reference to the second is returned).
                               If false, the first child's widget is removed, the second takes all
                               the space and ref to first is returned
        """

        g = self._g

        fid, sid = g.children(paneId)
        # -- retreive widgets, one will move up to parent
        # the other will be returned to caller
        fst_widget = self._uninstall_child(fid)
        sec_widget = self._uninstall_child(sid)

        if toSecond:
            ret = sec_widget
            ins = fst_widget
        else:
            ret = fst_widget
            ins = sec_widget

        self._unsplit_parent(paneId)
        self._install_child(paneId, ins)

        g.collapse_node(paneId)
        self.computeGeoms(paneId)

        if ret is not None:
            ret.hide()
        return ret

    def paneAtPos(self, pos):
        """Returns the pane id at position `pos` in local coordinates."""
        visitor = SplittableUI.PaneIdFindingVisitor(self._g, self._geomCache, pos)
        self._g.visit_i_breadth_first(visitor, node=0)
        return visitor.result

    def contentAtPos(self, pos):
        """Returns the content widget at position `pos` in local coordinates."""
        paneId = self.paneAtPos(pos)
        widget = self._g.get_property(paneId, "widget")
        return widget

    def setContentAt(self, paneId, wid, **kwargs):
        """Sets the content of paneId."""
        g = self._g

        if paneId not in g:
            return None

        # -- if the content is already is self, move it to the new vid --
        oldPaneId = self.hasContent(wid)
        if oldPaneId >= 0:
            self.takeContentAt(oldPaneId, self)

        # -- get the old content --
        widget = self._install_child(paneId, wid, **kwargs)

        self._raise_overlays(paneId)

        self.computeGeoms(paneId)
        return widget

    def computeGeoms(self, baseNode=0):
        """Recompute all the geometry starting at node `baseNode`.
        It is effectively hierarchical."""
        visitor = self.GeometryComputingVisitor(self._g, self._geomCache)
        self._g.visit_i_breadth_first(visitor, baseNode)

    def getContentAt(self, paneId):
        if self._g.has_property(paneId, "widget"):
            wid = self._g.get_property(paneId, "widget")
            return wid

    def getAllContents(self, reparent=None):
        widgets = []
        for vid in self._g._properties.iterkeys():
            wid = self.getContentAt(vid)
            if wid is not None:
                widgets.append(wid)
        return widgets

    def takeContentAt(self, paneId, reparent=None):
        if self._g.has_property(paneId, "widget"):
            wid = self._g.get_property(paneId, "widget")
            self._g.set_property(paneId, "widget", None)
            if wid is not None:
                wid.hide()
                wid.setParent(reparent)
                return wid
        return None

    def takeAllContents(self, reparent=None):
        taken = []
        for vid in self._g._properties.iterkeys():
            wid = self.takeContentAt(vid, reparent)
            if wid is not None:
                taken.append(wid)
        return taken

    def hasContent(self, widget):
        for vid, prop in self._g._properties.iteritems():
            if "widget" in prop and prop["widget"] == widget:
                return vid
        return -1

    #############
    # Internals #
    #############
    def _split_parent(self, paneId, direction, amount):
        g = self._g
        # -- The pane at paneId has been divided : it will not
        # contain a widget anymore (it will be transfered to
        # a child) and it's tear offs will be removed --
        self._remove_tearOffs(paneId)
        hasWid = g.has_property(paneId, "widget")
        widgetFromParent = g.pop_property(paneId, "widget") if hasWid else None
        # -- we must create the splitter handle that separates the children --
        handle = SplittableUI.SplitterHandle(g, paneId, direction, self)
        handle.handleMoved.connect(self._onHandleMoved)
        g.set_property(paneId, "handleWidget", handle)
        # -- we store other properties used for layout computation --
        g.set_property(paneId, "splitDirection", direction)
        g.set_property(paneId, "amount", amount)
        self.__sticky_check(paneId, direction, amount)
        return widgetFromParent

    def _unsplit_parent(self, paneId):
        g = self._g
        # -- paneId is not split anymore
        # -- remove associated widgets
        g.pop_property(paneId, "splitDirection")
        g.pop_property(paneId, "amount")
        h = g.pop_property(paneId, "handleWidget")
        h.close()

    def _install_child(self, paneId, widget, **kwargs):
        g = self._g
        # -- get the old content --
        oldWidget = None
        if g.has_property(paneId, "widget"):
            oldWidget = g.get_property(paneId, "widget")
            if oldWidget is not None:
                oldWidget.hide()

        # -- place the new content --
        if widget is not None:
            widget.setParent(self)
            widget.show()
        g.set_property(paneId, "widget", widget)

        if not kwargs.get("noTearOffs", False):
            self._install_tearOffs(paneId)
        return oldWidget

    def _install_tearOffs(self, paneId):
        """Utility function to create the tear off widgets associated to pane `paneId`."""
        g = self._g
        tearOffs = SplittableUI.TearOff(g, paneId, self, bottom=True),\
            SplittableUI.TearOff(g, paneId, self, bottom=False)
        g.set_property(paneId, "tearOffWidgets", tearOffs)
        for t in tearOffs:
            t.splitRequest.connect(self._onSplitRequest)
            t.collapseRequest.connect(self._onCollapseRequest)

    def _uninstall_child(self, paneId):
        g = self._g
        hasWid = g.has_property(paneId, "widget")
        widget = g.pop_property(paneId, "widget") if hasWid else None
        self._geomCache.pop(paneId, None)
        self._remove_tearOffs(paneId)
        return widget

    def _remove_tearOffs(self, paneId):
        """Utility function to remove the tear off widgets associated to pane `paneId`."""
        if not self._g.has_property(paneId, "tearOffWidgets"):
            return
        parTearOffs = self._g.pop_property(paneId, "tearOffWidgets")
        for t in parTearOffs:
            t.close()

    def _raise_overlays(self, paneId):
        # -- tearoffs would be covered by new widget, let's raise them --
        for t in self._g.get_property(paneId, "tearOffWidgets"):
            t.raise_()
        parent = self._g.parent(paneId)
        if parent is not None:
            handle = self._g.get_property(parent, "handleWidget")
            if handle:
                handle.raise_()

    def __sticky_check(self, paneId, orientation, amount):
        geom = self._geomCache.get(paneId)
        sticky = 0
        if geom:
            refVal = geom.width() if orientation == QtCore.Qt.Horizontal else geom.height()
            sp = SplittableUI.__spacing__
            absAmount = amount * refVal
            sticky = -1 if absAmount <= sp else (1 if absAmount >= (refVal - sp - 1) else 0)
        self._g.set_property(paneId, "sticky", sticky)

    def full_sticky_check(self):
        leaves = self._g.leaves()
        leavesAncestors = set([self._g.parent(leaf) for leaf in leaves])
        for paneId in leavesAncestors:
            if paneId == None:
                continue
            amount = self._g.get_property(paneId, "amount")
            orientation = self._g.get_property(paneId, "splitDirection")
            self.__sticky_check(paneId, orientation, amount)

    ###################
    # Signal handlers #
    ###################
    def _onSplitRequest(self, paneId, orientation, amount):
        """Called by tear offs when a split is requested.
        `paneId` will be split following `orientation` at `amount`*pane-width/height."""
        if self._g.has_children(paneId):
            return
        fake = self.getPlaceHolder()

        if amount == 0.0:
            amount += 0.05
        elif amount == 1.0:
            amount -= 0.05
        self.splitPane(fake, paneId, orientation, amount)

    def _onCollapseRequest(self, paneId, collapseType, direction):
        """Called by tear offs when a collapse is requested.
        `paneId` will collapse following `orientation` at `amount`*pane-width/height."""
        if collapseType == 2:
            print "Cannot handle collapse to foreign nodes yet"
            return
        parent = self._g.parent(paneId)
        siblings = self._g.children(parent)
        if collapseType == SplittableUI.TearOff.CollapseToSecond:
            if self._g.has_children(siblings[1]):
                return
        else:
            if self._g.has_children(siblings[0]):
                return
        self.collapsePane(parent,
                          toSecond=(collapseType == SplittableUI.TearOff.CollapseToSecond))

    def _onHandleMoved(self, paneId, position, orientation, newAmount=None):
        """Called when a handle widget moves. It triggers a recomputation
        of the layout at level `paneId`."""
        if newAmount is None:
            geom = self._geomCache[paneId]
            position = position - geom.topLeft()
            if orientation == QtCore.Qt.Horizontal:
                val = float(position.x())
                topVal = geom.width()
            elif orientation == QtCore.Qt.Vertical:
                val = float(position.y())
                topVal = geom.height()
            newAmount = val / topVal

        self.__sticky_check(paneId, orientation, newAmount)
        self._g.set_property(paneId, "amount", newAmount)
        self.computeGeoms(paneId)

    def _onWidgetMenuRequest(self, point):
        pt = self.mapFromGlobal(point)
        paneId = self.paneAtPos(pt)
        self.widgetMenuRequest.emit(point, paneId)

    def toString(self):
        return self._g.toString(self.reprProps)

    @classmethod
    def fromString(cls, rep, parent=None):
        g, tup = BinaryTree.fromString(rep)

        newWid = cls(parent=parent)
        w0 = newWid._uninstall_child(0)
        if w0:
            w0.setParent(None)
            w0.close()

        newWid._g = g
        visitor = SplittableUI.InitContainerVisitor(g, newWid)
        g.visit_i_breadth_first(visitor)
        newWid._geomCache[0] = newWid.contentsRect()
        newWid.computeGeoms(0)
        return newWid

    ##############################
    # Qt Event reimplementations #
    ##############################
    def resizeEvent(self, event):
        """Reimplemented to call `computeGeoms`."""
        self._geomCache[0] = self.contentsRect()
        self.computeGeoms(baseNode=0)
        QtGui.QWidget.resizeEvent(self, event)

    def dragEnterEvent(self, event):
        """While the user hasn't released the object, this method is called
        to tell qt if the view accepts the object or not."""
        self.dragEnterEventTest.emit(self, event)

    def dropEvent(self, event):
        paneId = self.paneAtPos(event.pos())
        if paneId is None:
            return
        self.dropHandlerRequest.emit(self, paneId, event)

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        QtGui.QWidget.paintEvent(self, event)
        # paintingVisitor = self.DebugPaintingVisitor(self._g, self._geomCache, painter)
        # self._g.visit_i_breadth_first(paintingVisitor)

    ###################################################################################
    # Inner classes not meant to be seen by others - Inner classes not meant to be... #
    ###################################################################################
    class DebugPaintingVisitor(object):

        def __init__(self, graph, geomCache, painter):
            self.g = graph
            self.geomCache = geomCache
            self.painter = painter

        def visit(self, vid):
            if not self.g.has_children(vid):
                # ok, no child, so we probably have a widget and our geometry
                # has already been computed by parent
                geom = self.geomCache[vid]
                color = QtGui.QColor.fromHsv(vid * 10, 125, 125)
                self.painter.fillRect(geom, color)
                self.painter.drawText(geom.center(), str(vid))
            return False, False

    class GeometryComputingVisitor(object):

        """A visitor that browses the graph describing
        the partitioning of the UI and computes the geometries
        of the children widgets"""

        def __init__(self, graph, geomCache):
            self.g = graph
            self.geomCache = geomCache

        def layout_pane(self, geom, vid, widgetSpace=None):
            widget = None
            if self.g.has_property(vid, "widget"):
                widget = self.g.get_property(vid, "widget")
            if widget is not None:
                widgetGeom = widgetSpace or geom
                widget.move(widgetGeom.topLeft())
                widget.resize(widgetGeom.width(), widgetGeom.height())

            th = SplittableUI.TearOff.__ideal_height__
            tearOffB, tearOffT = toffs = self.g.get_property(vid, "tearOffWidgets")
            if geom.height() < th or geom.width() < th:
                if widget:
                    widget.hide()
                for t in toffs:
                    t.hide()
            else:
                if widget:
                    widget.show()
                for t in toffs:
                    t.show()
            tearOffB.move(geom.left() + 1, geom.bottom() + 1 - th)
            tearOffT.move(geom.right() - th + 1, geom.top() + 1)
            return False, False  # don't ignore first or second child

        def visit(self, vid):
            """
            Lays out all the widgets concerning vid.

            At vid we check if it is a terminal node. In that case the vid
            has a content widget (non terminal nodes have no content widget).
            Vid's geometry has already been computed by parent so we set the
            widget's geometry to vid's geometry.
            If it's not a terminal node, then it still has a geometry but not
            content widget. However it does contain a splitter handle that must
            be positionned, and we must compute the sizes of its chlidren.

            Called by the binary tree structure. The order is dependent
            on the tree traversal method used."""

            if not self.g.has_children(vid):
                # ok, no child, so we probably have a widget and our geometry
                # has already been computed by parent
                geom = self.geomCache[vid]
                return self.layout_pane(geom, vid)

            fid, sid = self.g.children(vid)

            sp = SplittableUI.__spacing__
            containerGeom = self.geomCache[vid]

            direction = self.g.get_property(vid, "splitDirection")
            amount = self.g.get_property(vid, "amount")
            sticky = self.g.get_property(vid, "sticky")

            # -- The node has children : it doesn't have a widget
            # but it does have a handle that separates the child widgets
            # we must place it accordingly
            handle = self.g.get_property(vid, "handleWidget")
            hgeom = QtCore.QRect()  # handle.geometry()

            containerWidth = (
                containerGeom.width() - sp) if direction == QtCore.Qt.Horizontal else containerGeom.width()
            containerHeight = (
                containerGeom.height() - sp) if direction == QtCore.Qt.Vertical else containerGeom.height()

            if direction == QtCore.Qt.Horizontal:
                firstHeight = secondHeight = containerHeight
                firstWidth = (containerWidth * amount) if sticky != -1 else 0
                secondWidth = (containerWidth - firstWidth) if sticky != 1 else 0
                firstX, firstY = containerGeom.x(), containerGeom.y()
                secondX, secondY = firstX + firstWidth + sp, firstY
                hgeom.moveLeft(firstX + +firstWidth)
                hgeom.moveTop(firstY)
                hgeom.setHeight(containerHeight)
                hgeom.setWidth(sp)
            else:
                firstWidth = secondWidth = containerWidth
                firstHeight = (containerHeight * amount) if sticky != -1 else 0
                secondHeight = (containerHeight - firstHeight) if sticky != 1 else 0
                firstX, firstY = containerGeom.x(), containerGeom.y()
                secondX, secondY = firstX, firstY + firstHeight + sp
                hgeom.moveTop(firstY + firstHeight)
                hgeom.moveLeft(firstX)
                hgeom.setWidth(containerWidth)
                hgeom.setHeight(sp)
            firstGeom = QtCore.QRect(firstX, firstY, firstWidth, firstHeight)
            secondGeom = QtCore.QRect(secondX, secondY, secondWidth, secondHeight)

            self.geomCache[fid] = firstGeom
            self.geomCache[sid] = secondGeom
            handle.setGeometry(hgeom)
            return False, False  # don't ignore first or second child

    class PaneIdFindingVisitor(object):

        """Visitor that searches which leaf id has pos in geometry"""

        def __init__(self, graph, geomCache, pt):
            self.g = graph
            self.geomCache = geomCache
            self.pt = pt
            self.result = None

        def visit(self, vid):
            """
            """

            if self.g.has_children(vid):
                fid, sid = self.g.children(vid)
            else:
                geom = self.geomCache.get(vid)
                if geom.contains(self.pt):
                    self.result = vid
                return False, False

            firstGeom = self.geomCache.get(fid)
            secondGeom = self.geomCache.get(sid)
            ignoreFirst = not firstGeom.contains(self.pt)
            ignoreSecond = not secondGeom.contains(self.pt)
            return ignoreFirst, ignoreSecond

    class InitContainerVisitor(object):

        """Visitor that searches which leaf id has pos in geometry"""

        def __init__(self, graph, wid):
            self.g = graph
            self.wid = wid

        def visit(self, vid):
            """
            """
            if not self.g.has_children(vid):
                self.wid._install_child(vid, None)
                return False, False

            direction = self.g.get_property(vid, "splitDirection")
            amount = self.g.get_property(vid, "amount")

            self.wid._split_parent(vid, direction, amount)

            return False, False

    class TearOff(QtGui.QWidget, DraggableWidget):

        """A widget drawn at top right and bottom left hand corner of each
        SplittableUI pane and that allows the user to split/collapse panes"""
        splitRequest = QtCore.Signal(int, QtCore.Qt.Orientation, float)
        collapseRequest = QtCore.Signal(int, int, int)

        TearUp = 0  # : The tear direction is upward
        TearRight = 1  # : The tear direction is to the right
        TearDown = 2  # : The tear direction is downward
        TearLeft = 3  # : The tear direction is to the left

        CollapseToSecond = 0  # : Collapse first child to second
        CollapseToFirst = 1  # : Collapse second child to first
        CollapseToForeign = 2  # : Collapse the pane to another that is not sibling

        __ideal_height__ = 10

        def __init__(self, graph, refVid, parent, bottom=False):
            """Contruct the TearOff.
            :Parameters:
             - `graph` (BinaryTree) - the graph that manages the layout
             - `refVid` (int) - the id of the pane this tear off belongs to
             - `parent` (SplitterUI) - The parent splittable ui.
             - `bottom` (bool) - Is this tear off at the bottom left?
            """

            QtGui.QWidget.__init__(self, parent)
            DraggableWidget.__init__(self)
            self._g = graph
            self._vid = refVid
            self._bottom = bottom
            self.setFixedHeight(self.__ideal_height__)
            self.setFixedWidth(self.__ideal_height__)
            self.set_edit_mode()
            self.show()

        def _fixGeometry(self, newPt, geom):
            """ We abuse this _fixGeometry method to find out how
            we are splitting. newPt is the cursor position relative to
            parent. It returns true as it doesn't need to change the geometry of self."""
            df = newPt - self._startpos
            vid = self._vid
            if df.manhattanLength() > 5:
                dx, dy = abs(df.x()), abs(df.y())
                direction = None
                if dx > dy:  # horizontal displacement
                    direction = self.TearLeft if df.x() < 0 else self.TearRight
                else:
                    direction = self.TearUp if df.y() < 0 else self.TearDown

                isFirstChild = self._g.node_is_first_child(vid)
                parent = self._g.parent(vid)
                if direction == self.TearUp and self._bottom:  # split up
                    self.splitRequest.emit(vid, QtCore.Qt.Vertical, 0.95)
                elif direction == self.TearRight and self._bottom:  # split right
                    self.splitRequest.emit(vid, QtCore.Qt.Horizontal, 0.05)
                elif direction == self.TearDown and not self._bottom:  # split down
                    self.splitRequest.emit(vid, QtCore.Qt.Vertical, 0.05)
                elif direction == self.TearLeft and not self._bottom:  # split left
                    self.splitRequest.emit(vid, QtCore.Qt.Horizontal, 0.95)
                elif parent is not None:
                    splitDirection = self._g.get_property(parent, "splitDirection")
                    # -- collapse to second --
                    if direction == self.TearDown  and splitDirection == QtCore.Qt.Vertical   and     self._bottom and     isFirstChild or \
                       direction == self.TearRight and splitDirection == QtCore.Qt.Horizontal and not self._bottom and isFirstChild:
                        self.collapseRequest.emit(vid, self.CollapseToSecond, direction)
                    # -- collapse to first --
                    elif direction == self.TearUp   and splitDirection == QtCore.Qt.Vertical   and not self._bottom and not isFirstChild or \
                            direction == self.TearLeft and splitDirection == QtCore.Qt.Horizontal and self._bottom and not isFirstChild:
                        self.collapseRequest.emit(vid, self.CollapseToFirst, direction)
                    # -- collapse to foreign --
                    else:
                        self.collapseRequest.emit(vid, self.CollapseToForeign, direction)
            return geom, True

        def set_edit_mode(self, mode=True):
            self._edit_mode = mode

        ##############################
        # Qt Event reimplementations #
        ##############################
        def paintEvent(self, event):
            if self._edit_mode is False:
                return
            painter = QtGui.QPainter(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)

            pen = painter.pen()
            if self._hovered:
                brush = QtGui.QBrush(QtGui.QColor(120, 190, 255, 200))
                pen.setColor(QtGui.QColor(255, 255, 255, 255))
            else:
                brush = QtGui.QBrush(QtGui.QColor(120, 190, 255, 70))
                pen.setColor(QtGui.QColor(0, 0, 0, 127))

            painter.setBrush(brush)
            painter.setPen(pen)

            adj = painter.pen().width()
            rect = self.contentsRect().adjusted(adj, adj, -adj, -adj)
            if self._bottom:
                painter.drawConvexPolygon([rect.bottomRight(), rect.bottomLeft(), rect.topLeft()])
            else:
                painter.drawConvexPolygon([rect.topRight(), rect.bottomRight(), rect.topLeft()])

    class SplitterHandle(QtGui.QWidget, DraggableWidget):

        """Basically a reimplementation of QtGui.QSplitterHandle.
        The original one needed a reference to a QtGui.QSplitter.
        """
        handleMoved = QtCore.Signal(object,  object, object)

        def __init__(self, graph, refVid, orientation, parent):
            """Contruct a SplitterHandle.
            :Parameters:
             - `graph` (BinaryTree) - the graph that manages the layout
             - `refVid` (int) - the id of the pane who contains two children seperated by this handle
             - `orientation` (QtCore.Qt.Orientation) - How to layout the splitter :
                               Vertical means that it seperates two vertical siblings (its horizontal)
             - `parent` (SplitterUI) - The parent splittable ui.
            """
            QtGui.QWidget.__init__(self, parent)
            DraggableWidget.__init__(self)
            self._g = graph
            self._refVid = refVid
            self._orientation = orientation
            self._thickness = SplittableUI.__spacing__
            if orientation == QtCore.Qt.Vertical:
                self.setFixedHeight(self._thickness)
                dirString = "x1:0, y1:1, x2:0, y2:0,"
                self.setCursor(QtCore.Qt.SplitVCursor)
            else:
                self.setFixedWidth(self._thickness)
                self.setCursor(QtCore.Qt.SplitHCursor)
                dirString = "x1:0, y1:0, x2:1, y2:0,"

            self.setStyleSheet("background-color: " +
                               "qlineargradient(spread:pad," + dirString +
                               "stop:0 rgba(135,135,135,255), " +
                               "stop:0.3 rgba(155,155,155,255), " +
                               "stop:0.5 rgba(255,255,255,255), " +
                               "stop:0.7 rgba(155,155,155,255), " +
                               "stop:1 rgba(135, 135, 135, 255));")

            self.show()

        def _fixGeometry(self, newPt, geom):
            """Validate newPt and fix geom accordingly"""
            newPt = self.__valid_position(newPt)
            if self._orientation == QtCore.Qt.Vertical:
                geom.setY(newPt.y())
            else:
                geom.setX(newPt.x())
            self.handleMoved.emit(self._refVid, geom.topLeft(), self._orientation)
            return geom, True  # DO NOT MODIFY THE GEOMETRY! IT WILL BE DONE BY THE GRAPH UPDATE

        def __valid_position(self, pt):
            """PRIVATE: checks if pt is within the parent's geometry and returns a pt that
            lies inside."""
            parentGeom = self.parent()._geomCache[self._refVid]
            thk = self._thickness
            if self._orientation == QtCore.Qt.Vertical:
                val = pt.y()
                min_ = parentGeom.top() + thk
                max_ = parentGeom.bottom()
                fix = pt.setY
            else:
                val = pt.x()
                min_ = parentGeom.left() + thk
                max_ = parentGeom.right()
                fix = pt.setX
            if val < min_:
                val = min_
            elif val > max_:
                val = max_
            fix(val)
            return pt

        ##############################
        # Qt Event reimplementations #
        ##############################
        def paintEvent(self, event):
            # -- Required for stylesheets to work. Search for QWidget here:
            # http://doc.qt.nokia.com/latest/stylesheet-reference.html --
            QStyle = QtGui.QStyle
            opt = QtGui.QStyleOption()
            opt.initFrom(self)
            painter = QtGui.QPainter(self)
            self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)

    ###################################################################################
    # /end Inner classes not meant to be seen by others - Inner classes not meant to  #
    ###################################################################################


# Small testing example
if __name__ == "__main__":
    app = QtGui.QApplication(["Muahaha"])
    mw = QtGui.QMainWindow()
    splittable = SplittableUI(parent=mw)
    mw.setCentralWidget(splittable)
    mw.show()
    app.exec_()
