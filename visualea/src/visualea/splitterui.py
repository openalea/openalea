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
__revision__ = " $Id$ "


"""
Contains the implementation of a recusively splittable UI.
"""

from PyQt4 import QtCore, QtGui

class RubberBandScrollArea(QtGui.QScrollArea):
    """ A customized QScrollArea that can be scrolled
    with a middle mouse drag in a blank area.
    Scrolling can be locked to X or Y. (default is not locked)

    Obeys to Qt naming convention.
    """

    def __init__(self, parent=None):
        """ Contruct a RubberBandScrollArea.
        :Parameters:
         - `parent` (QtGui.QWidget) - The parent widget.
        """
        QtGui.QScrollArea.__init__(self, parent)
        self.__scrollY = True
        self.__scrollX = True
        self.__rubberband = False
        self.__oldMousePos = None
        self.__scrollButton = QtCore.Qt.MidButton

    def setYScrollable(self, val):
        """ Sets if the widgets scrolls vertically
        :Parameters:
         - `val` (bool) - False to lock Y scrolling
        """
        self.__scrollY = val

    def setXScrollable(self, val):
        """ Sets if the widgets scrolls horizontally
        :Parameters:
         - `val` (bool) - False to lock X scrolling
        """
        self.__scrollX = val

    def setScrollButton(self, button):
        """ Sets the mouse button that activates scrolling
        to this value.
        :Parameters:
         - `button` (QtCore.Qt.MouseButton) - The button flag
        """
        self.__scrollButton = button

    ###############################
    # Qt events reimplementations #
    ###############################
    def mousePressEvent(self, e):
        """Reimplemented to catch the mouse press button and activate
        rubberband"""
        if e.button() == self.__scrollButton:
            self.__rubberband = True
            self.__oldMousePos = e.pos()
        else:
            QtGui.QScrollArea.mousePressEvent(self,e)

    def mouseMoveEvent(self, e):
        """Reimplemented to scroll the window in rubberband mode.
        It modifies the scrollbar values that will then update
        the viewport.
        """
        if self.__rubberband:
            pos = e.pos()
            df = pos - self.__oldMousePos
            if self.__scrollX:
                sb = self.horizontalScrollBar()
                sb.setValue(sb.value() - df.x())
            if self.__scrollY:
                sb = self.verticalScrollBar()
                sb.setValue(sb.value() - df.y())
            self.__oldMousePos = pos
        else:
            QtGui.QScrollArea.mousePressEvent(self,e)

    def mouseReleaseEvent(self, e):
        """Reimplemented to catch the mouse press button and deactivate
        rubberband"""
        if e.button() == self.__scrollButton:
            self.__rubberband = False
            self.__rubberband = None
        else:
            QtGui.QScrollArea.mousePressEvent(self,e)




class Niche(QtGui.QFrame):
    """A customized QtGui.QFrame that includes a content area and a
    header area. The header holds a static button to the left, and
    a t-constrained RubberBandScrollArea to its right. This area can
    hold a menu bar.

    Obeys to Qt naming convention.
    """

    panelMenuRequest = QtCore.pyqtSignal(QtGui.QWidget)


    ###################################################################################
    # Inner classes not meant to be seen by others - Inner classes not meant to be... #
    ###################################################################################
    class Header(QtGui.QFrame):
        """Implementation of the are that holds the button and toolbar area

        Obeys to Qt naming convention.
        """

        __ideal_height__ = 27 # this is fixed, never got it right otherwise.

        def __init__(self, parent=None, windowsflags=QtCore.Qt.Widget):
            QtGui.QFrame.__init__(self, parent, windowsflags)
            self.__lay = QtGui.QHBoxLayout()
            self.__but = QtGui.QPushButton("Win")
            self.__but.setSizePolicy(QtGui.QSizePolicy.Fixed,QtGui.QSizePolicy.Fixed)
            self.__lay.setContentsMargins(1,1,1,1)
            self.__lay.setSpacing(1)
            self.__lay.addWidget(self.__but)

            self.headerScr = RubberBandScrollArea()
            # -- lock scrolling to X --
            self.headerScr.setYScrollable(False)
            # -- appearance --
            self.headerScr.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.headerScr.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
            self.headerScr.setFrameShape(QtGui.QFrame.NoFrame)
            self.headerScr.setFrameShadow(QtGui.QFrame.Sunken)

            self.__lay.addWidget(self.headerScr)
            self.__fixSize()
            self.setLayout(self.__lay)

        def setToolbar(self, toolbar):
            """Set the widget held by the scrollable
            toolbar area to the right.

            :Parameters:
             - `toolbar` (QtGui.QWidget) - the widget that serves as a toolbar.
            """
            self.headerScr.setWidget(toolbar)
            self.__fixSize()

        def toolbar(self):
            """Retreive the toolbar widget"""
            self.headerScr.widget(toolbar)

        def __fixSize(self):
            """Forces all subwidgets to a decent size. Private."""
            szY = self.__ideal_height__
            self.__but.setFixedSize(QtCore.QSize(szY,szY))
            self.setMaximumHeight(szY+5)
            self.setMinimumHeight(szY+5)
    ###################################################################################
    # /end Inner classes not meant to be seen by others - Inner classes not meant to  #
    ###################################################################################


    def __init__(self, parent=None, windowsflags=QtCore.Qt.Widget):
        """Contructs a Niche.
        :Parameters:
         - `parent` (QtGui.QWidget) - A reference to the parent
         - `windowsflags` (QtCore.Qt.WindowType) - The type of widget to build
        """
        QtGui.QFrame.__init__(self, parent, windowsflags)
        self.setFrameShape(QtGui.QFrame.StyledPanel)
        self.setFrameShadow(QtGui.QFrame.Sunken)

        self.__lay = QtGui.QVBoxLayout()
        self.__lay.setContentsMargins(1,1,1,1)
        self.setLayout(self.__lay)

        self.__header = Niche.Header()

        self.__contentScr = RubberBandScrollArea()
        self.__contentScr.setFrameShape(QtGui.QFrame.NoFrame)
        self.__content = None

        self.__lay.addWidget(self.__header)
        self.__lay.addWidget(self.__contentScr)


    def setContent(self, widget):
        """Set the widget to host within the content pane of the niche
        :Parameters:
         - `widget` (QtGui.QWidget) - The widget to host. The Niche takes ownership
        """
        if self.__content == widget:
            return
        self.__contentScr.setWidget(widget)
        self.__content = widget

    setWidget = setContent

    def content(self):
        """Retreive the hosted widget. Doesn't change ownership"""
        return self.__contentScr.widget()

    def setToolbar(self, toolbar):
        """Set the toolbar of the niche
        :Parameters:
         - toolbar (QtGui.QWidget) - The widgets that serves as toolbar.
        """
        self.__header.setToolbar(toolbar)

    def toolbar(self):
        """Retreive the toolbar widget. Doesn't change ownership"""
        return self.__header.toolbar()



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
            Exception.__init__(self, "Bad node id: "+str(vid))
    class NonAnteTerminalException(Exception):
        """Raised when trying to collapse a node whose children themselves have children."""
        def __init__(self, vid):
            Exception.__init__(self, "Can only collapse nodes terminal-1: "+str(vid))
    class ParentCompleteException(Exception):
        """You should never see this one. Raised if trying to add a child to a node
        that already has two children. This could just ruin the binary concept eh!"""
        def __init__(self, vid):
            Exception.__init__(self, "Parent already complete: "+str(vid))
    class PropertyException(Exception):
        """Raised when a node doesn't have the property you requested"""
        def __init__(self, vid, key):
            Exception.__init__(self, "No %s for node %d"%(str(key), vid))
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


    def __init__(self):
        """Construct a BinaryTree"""
        self._toChildren = {} #: map parent ids to two child ids
        self._toParents  = {} #: map childid to parent id
        self._properties = {} #: map vid to a dictionnary of string->val
        self.__root = 0 #: our starting point
        self.__vid  = 1 #: the first vertex that will be added. Gets incremented
        # -- Construct the root node --
        self._properties[0] = {}
        self._toParents[0] = None

    def parent(self, vid):
        """Returns the parent of vid.
        :Parameters:
         - `vid` (int) - the id of the vertex whose parent is requested

        Raises BinaryTree.BadIdException if vid is not in the list of children.
        """
        if vid not in self._toParents:
            raise BinaryTree.BadIdException(vid)
        return self._toParents[vid]

    def children(self, vid):
        """Returns the children of vid.
        :Parameters:
         - `vid` (int) - the id of the vertex whose children are requested

        Raises BinaryTree.BadIdException if vid is not in the list of parents.
        """
        if vid not in self._toChildren:
            raise BinaryTree.BadIdException(vid)
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
            raise BinaryTree.BadIdException(vid)
        par = self._toParents[vid]
        chds = self.children(par)
        return chds.index(vid)==0

    def split_node(self, vid):
        """Add two children to vid and return their ids.

        Raises BinaryTree.BadIdException if vid is not in the graph."""
        if vid not in self._properties:
            raise BinaryTree.BadIdException(vid)
        fid, sid = self.__vid, self.__vid+1
        self.__vid += 2
        self.__new_node(fid, vid)
        self.__new_node(sid, vid)
        return fid, sid

    def collapse_node(self, vid):
        """Remove children from vid and return their ids.

        Raises BinaryTree.BadIdException if vid is not in the graph.
        Raises BinaryTree.NonAnteTerminalException if children of vid have children."""
        if vid not in self._properties:
            raise BinaryTree.BadIdException(vid)
        fid, sid = self._toChildren[vid]
        if fid in self._toChildren or sid in self._toChildren:
            raise BinaryTree.NonAnteTerminalException(vid)
        self.__del_node(fid, vid)
        self.__del_node(sid, vid)
        return fid, sid

    def __new_node(self, vid, parent):
        """PRIVATE. Create a new node with id  `vid` and attached to `parent`.

        Raises BinaryTree.ParentCompleteException if parent already has two children"""
        chen = self._toChildren.setdefault(parent,[])
        if len(chen) > 1:
            raise BinaryTree.ParentCompleteException(parent)
        chen.append(vid)
        self._toParents [vid] = parent
        self._properties[vid] = {}

    def __del_node(self, vid, parent):
        """PRIVATE. Remove a node with id  `vid` and detach it from `parent`."""
        chen = self._toChildren.setdefault(parent,[])
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
            raise BinaryTree.BadIdException(vid)
        self._properties[vid][key] = value

    def get_property(self, vid, key):
        """Retreives property `key` from node `vid`.
        :Parameters:
         - `vid` (int) - id of the vertex
         - `key` (str) - name of the property

        Raises BinaryTree.BadIdException if `vid` is not in graph.
        Raises BinaryTree.PropertyException if `key` is not a property of `vid` (ie. if not set yet)
        """
        if vid not in self._properties:
            raise BinaryTree.BadIdException(vid)
        if key not in self._properties[vid]:
            raise BinaryTree.PropertyException(vid, key)
        return self._properties[vid].get(key)

    def pop_property(self, vid, key):
        """Retreives property `key`  and removes it from node `vid`
        :Parameters:
         - `vid` (int) - id of the vertex
         - `key` (str) - name of the property

        Raises BinaryTree.BadIdException if `vid` is not in graph.
        Raises BinaryTree.PropertyException if `key` is not a property of `vid` (ie. if not set yet)
        """
        if vid not in self._properties:
            raise BinaryTree.BadIdException(vid)
        if key not in self._properties[vid]:
            raise BinaryTree.PropertyException(vid, key)
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
        while not len(nodeStack)==0:
            currNode = nodeStack.pop()
            if visitor != None:
                visitor.visit(currNode)
            fid, sid = self._toChildren.get(currNode, (None, None))
            if fid != None:
                nodeStack.appendleft(fid)
            if sid != None:
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
        self._isMoving  = False
        self._offset    = None
        self._oldpos    = None
        self._startpos  = None
        self._hovered   = False
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
        of the widget origin and return the fixed the geometry and False.

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
            self._offset   = event.pos() - self.contentsRect().topLeft()
            #this is in global coordinates
            self._oldpos   = event.pos() - self._offset + self.geometry().topLeft()
            self._startpos = event.pos() - self._offset + self.geometry().topLeft()
        else:
            QtGui.QWidget.mousePressEvent(self, event)

    def mouseMoveEvent(self, event):
        if self._isMoving:
            geom = self.geometry()
            #newPt is in parent coordinates
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
            self._offset   = None
            self._offset   = None
            self._startpos = None
        else:
            QtGui.QWidget.mouseReleaseEvent(self, event)



class SplittableUI(QtGui.QWidget):
    """A widget that tries to mimic the Blender UI.
    Each pane contains a `Niche` that in
    turn contents a content pane and a toolbar pane."""

    __spacing__ = 8
    __hspacing__ = __spacing__/2

    def __init__(self, parent=None, content=None):
        """Contruct a SplittableUI.
        :Parameters:
         - parent (QtGui.QWidget) - The parent widget
         - content (QtGui.QWidget) - The widget to display in niche at level 0
        """
        QtGui.QWidget.__init__(self, parent)
        # -- our backbone: --
        self._g = BinaryTree()
        # -- contains geometry information (a vid->QRect mapping) --
        self._geomCache = {}

        # self._pal = 0 # : used during testing

        # -- initialising the pane at level 0 --
        wid = Niche(parent=self)
        self._g.set_property(0, "widget", wid)
        self.__install_tearOffs(0)
        if content is not None:
            wid.setContent(content)
        self._geomCache[0] = self.contentsRect()

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

        # -- The pane at paneId will be divided : it will not
        # contain a widget anymore (it will be transfered to
        # a child) and it's tear offs will be removed --
        self.__remove_tearOffs(paneId)
        widgetFromParent = g.pop_property(paneId, "widget")

        # -- We create a container for the newly created pane --
        container_widget = Niche(parent=self)
        container_widget.setContent(content)

        # -- we must create the splitter handle that separates the children --
        handle = SplittableUI.SplitterHandle(g, paneId, direction, self)
        handle.handleMoved.connect(self._onHandleMoved)

        # -- let's configure the tear offs for child widgets --
        self.__install_tearOffs(fid)
        self.__install_tearOffs(sid)

        # -- transfer the parent's widget to either child
        # and install container in other child --
        if amount < 0.5:
            g.set_property(sid, "widget", widgetFromParent)
            g.set_property(fid, "widget", container_widget)
        else:
            g.set_property(fid, "widget", widgetFromParent)
            g.set_property(sid, "widget", container_widget)

        g.set_property(paneId, "splitDirection", direction)
        g.set_property(paneId, "amount", amount)
        g.set_property(paneId, "handleWidget", handle)

        self.computeGeoms(paneId)
        handle.show()
        container_widget.show()


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
        fst_widget = g.pop_property(fid, "widget")
        sec_widget = g.pop_property(sid, "widget")
        # -- children don't exist anymore, cleanup cache
        self._geomCache.pop(fid, None)
        self._geomCache.pop(sid, None)
        # -- remove tearoffs for children --
        self.__remove_tearOffs(fid)
        self.__remove_tearOffs(sid)

        if toSecond:
            ret = sec_widget
            g.set_property(paneId, "widget", fst_widget)
        else: #to left
            ret = fst_widget
            g.set_property(paneId, "widget", sec_widget)

        # -- paneId is not split anymore
        # -- remove associated widgets
        g.pop_property(paneId, "splitDirection")
        g.pop_property(paneId, "amount")
        h = g.pop_property(paneId, "handleWidget")
        h.setParent(None)
        h.close()
        # -- paneId is dividable again, install tearoffs --
        self.__install_tearOffs(paneId)

        g.collapse_node(paneId)
        self.computeGeoms(paneId)
        ret.setParent(None)
        return ret

    def computeGeoms(self, baseNode=0):
        """Recompute all the geometry starting at node `baseNode`. It is effectively hierarchical."""
        visitor = SplittableUI.GeometryComputingVisitor(self._g, self._geomCache, baseNode)
        self._g.visit_i_breadth_first(visitor, baseNode)

    def __install_tearOffs(self, vid):
        """Utility function to create the tear off widgets associated to pane `vid`."""
        g = self._g
        tearOffs = SplittableUI.TearOff(g, vid, self, bottom=True),SplittableUI.TearOff(g, vid, self, bottom=False)
        g.set_property(vid, "tearOffWidgets", tearOffs)
        for t in tearOffs:
            t.show()
            t.raise_()
            t.splitRequest.connect(self._onSplitRequest)
            t.collapseRequest.connect(self._onCollapseRequest)

    def __remove_tearOffs(self, vid):
        """Utility function to remove the tear off widgets associated to pane `vid`."""
        parTearOffs = self._g.pop_property(vid, "tearOffWidgets")
        for t in parTearOffs:
            t.close()
            t.setParent(None)

    ##############################
    # Qt Event reimplementations #
    ##############################
    def resizeEvent(self, event):
        """Reimplemented to call `computeGeoms`."""
        self._geomCache[0] = self.contentsRect()
        self.computeGeoms(baseNode=0)
        QtGui.QWidget.resizeEvent(self, event)

    ###################
    # Signal handlers #
    ###################
    def _onSplitRequest(self, paneId, orientation, amount):
        """Called by tear offs when a split is requested.
        `paneId` will be split following `orientation` at `amount`*pane-width/height."""
        if self._g.has_children(paneId):
            return
        fake = QtGui.QLabel(self)
        # palette = fake.palette()
        # palette.setColor(QtGui.QPalette.Window, QtGui.QColor.fromHsl(self._pal, 100, 100))
        # fake.setPalette(palette)
        # fake.setMinimumSize(200, 200)
        # self._pal += 10
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
        if collapseType==SplittableUI.TearOff.CollapseToSecond:
            if self._g.has_children(siblings[1]):
                return
        else:
            if self._g.has_children(siblings[0]):
                return
        self.collapsePane(parent,
                          toSecond=(collapseType==SplittableUI.TearOff.CollapseToSecond))

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
            newAmount  = val/topVal
        self._g.set_property(paneId, "amount", newAmount)
        self.computeGeoms(paneId)



    ###################################################################################
    # Inner classes not meant to be seen by others - Inner classes not meant to be... #
    ###################################################################################
    class GeometryComputingVisitor(object):
        """A visitor that browses the graph describing
        the partitioning of the UI and computes the geometries
        of the children widgets"""
        def __init__(self, graph, geomCache, baseNode):
            self.g = graph
            self.geomCache = geomCache

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

            if self.g.has_children(vid):
                fid, sid = self.g.children(vid)
            else:
                # ok, no child, so we probably have a widget and our geometry
                # has already been computed by parent

                widget = self.g.get_property(vid, "widget")
                geom = self.geomCache[vid]
                if widget is not None:
                    widget.setGeometry(geom)

                th = SplittableUI.TearOff.__ideal_height__
                tearOffB,tearOffT = self.g.get_property(vid, "tearOffWidgets")
                if geom.height() <  th or geom.width() < th:
                    tearOffB.hide()
                    tearOffT.hide()
                else:
                    tearOffB.show()
                    tearOffT.show()
                tearOffB.move(geom.left(), geom.bottom()+1-th)
                tearOffT.move(geom.right()-th, geom.top()+1)
                return

            sp = SplittableUI.__spacing__
            containerGeom = self.geomCache[vid]

            direction = self.g.get_property(vid, "splitDirection")
            amount    = self.g.get_property(vid, "amount")

            # -- The node has children : it doesn't have a widget
            # but it does have a handle that separates the widgets
            # we must place it accordingly
            handle = self.g.get_property(vid, "handleWidget")
            hgeom = handle.geometry()

            containerWidth = (containerGeom.width() - sp) if direction == QtCore.Qt.Horizontal else containerGeom.width()
            containerHeight = (containerGeom.height() - sp) if direction == QtCore.Qt.Vertical else containerGeom.height()

            if direction == QtCore.Qt.Horizontal:
                firstHeight = secondHeight = containerHeight
                firstWidth  = containerWidth * amount
                secondWidth = containerWidth - firstWidth
                firstX, firstY = containerGeom.x(), containerGeom.y()
                secondX, secondY = firstX + firstWidth + sp, firstY
                hgeom.moveLeft(firstX++firstWidth)
                hgeom.moveTop(firstY)
                hgeom.setHeight(containerHeight)
            else:
                firstWidth = secondWidth = containerWidth
                firstHeight   = containerHeight * amount
                secondHeight  = containerHeight - firstHeight
                firstX, firstY = containerGeom.x(), containerGeom.y()
                secondX, secondY = firstX, firstY + firstHeight + sp
                hgeom.moveTop(firstY+firstHeight)
                hgeom.moveLeft(firstX)
                hgeom.setWidth(containerWidth)
            firstGeom = QtCore.QRect(firstX, firstY, firstWidth, firstHeight)
            secondGeom = QtCore.QRect(secondX, secondY, secondWidth, secondHeight)

            self.geomCache[fid] = firstGeom
            self.geomCache[sid] = secondGeom
            handle.setGeometry(hgeom)


    class TearOff(QtGui.QWidget, DraggableWidget):
        """A widget drawn at top right and bottom left hand corner of each
        SplittableUI pane and that allows the user to split/collapse panes"""
        splitRequest = QtCore.pyqtSignal(int, QtCore.Qt.Orientation, float)
        collapseRequest = QtCore.pyqtSignal(int, int, int)

        TearUp    = 0 #: The tear direction is upward
        TearRight = 1 #: The tear direction is to the right
        TearDown  = 2 #: The tear direction is downward
        TearLeft  = 3 #: The tear direction is to the left

        CollapseToSecond  = 0 #: Collapse first child to second
        CollapseToFirst   = 1 #: Collapse second child to first
        CollapseToForeign = 2 #: Collapse the pane to another that is not sibling

        __ideal_height__ = 10

        def __init__(self, graph, refVid, parent, bottom=False):
            """Contruct the TearOff.
            :Parameters:
             - `graph` (BinaryTree) - the graph that manages the layout
             - `refVid` (int) - the id of the pane who contains two children seperated by this handle
             - `parent` (SplitterUI) - The parent splittable ui.
             - `bottom` (bool) - Is this tear off at the bottom left?
            """

            QtGui.QWidget.__init__(self, parent)
            DraggableWidget.__init__(self)
            self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            self._g = graph
            self._vid = refVid
            self._bottom=bottom
            self.setFixedHeight(self.__ideal_height__)
            self.setFixedWidth(self.__ideal_height__)

        def _fixGeometry(self, newPt, geom):
            """ We abuse this _fixGeometry method to find out how
            we are splitting. newPt is the cursor position relative to
            parent. It returns true as it doesn't need to change the geometry of self."""
            df = newPt - self._startpos
            vid = self._vid
            if df.manhattanLength() > 5:
                dx, dy = abs(df.x()), abs(df.y())
                direction = None
                if dx > dy: #horizontal displacement
                    direction = self.TearLeft if df.x() < 0 else self.TearRight
                else:
                    direction = self.TearUp if df.y() < 0 else self.TearDown

                isFirstChild   = self._g.node_is_first_child(vid)

                if direction == self.TearUp and self._bottom: #split up
                    self.splitRequest.emit(vid, QtCore.Qt.Vertical, 0.95)
                elif direction == self.TearRight and self._bottom: #split right
                    self.splitRequest.emit(vid, QtCore.Qt.Horizontal, 0.05)
                elif direction == self.TearDown and not self._bottom: #split down
                    self.splitRequest.emit(vid, QtCore.Qt.Vertical, 0.05)
                elif direction == self.TearLeft and not self._bottom: #split left
                    self.splitRequest.emit(vid, QtCore.Qt.Horizontal, 0.95)

                parent = self._g.parent(vid)
                if parent is not None:
                    splitDirection = self._g.get_property(parent, "splitDirection")
                    # -- collapse to second --
                    if direction == self.TearDown  and splitDirection == QtCore.Qt.Vertical   and     self._bottom and     isFirstChild or \
                       direction == self.TearRight and splitDirection == QtCore.Qt.Horizontal and not self._bottom and     isFirstChild:
                        self.collapseRequest.emit(vid, self.CollapseToSecond, direction)
                    # -- collapse to first --
                    elif direction == self.TearUp   and splitDirection == QtCore.Qt.Vertical   and not self._bottom and not isFirstChild or \
                         direction == self.TearLeft and splitDirection == QtCore.Qt.Horizontal and     self._bottom and not isFirstChild:
                        self.collapseRequest.emit(vid, self.CollapseToFirst, direction)
                    # -- collapse to foreign --
                    else:
                        self.collapseRequest.emit(vid, self.CollapseToForeign, direction)
            return geom, True

        ##############################
        # Qt Event reimplementations #
        ##############################
        def paintEvent(self, event):
            painter = QtGui.QPainter(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)

            if self._hovered:
                brush   = QtGui.QBrush(QtGui.QColor(120,190,255,100))
            else:
                brush   = QtGui.QBrush(QtGui.QColor(120,190,255,20))
            painter.setBrush(brush)

            adj = painter.pen().width()
            rect = self.contentsRect().adjusted(adj,adj,-adj,-adj)
            if self._bottom:
                painter.drawConvexPolygon(rect.bottomRight(), rect.bottomLeft(), rect.topLeft())
            else:
                painter.drawConvexPolygon(rect.topRight(), rect.bottomRight(), rect.topLeft())


    class SplitterHandle(QtGui.QWidget, DraggableWidget):
        """Basically a reimplementation of QtGui.QSplitterHandle.
        The original one needed a reference to a QtGui.QSplitter.
        """
        handleMoved = QtCore.pyqtSignal(object,  object, object)

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
            self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            self._g           = graph
            self._refVid      = refVid
            self._orientation = orientation
            self._thickness = SplittableUI.__spacing__
            if orientation == QtCore.Qt.Vertical:
                self.setFixedHeight(self._thickness)
            else:
                self.setFixedWidth(self._thickness)

        def __valid_position(self, pt):
            """PRIVATE: checks if pt is within the parent's geometry and returns a pt that
            lies inside."""
            parentGeom, thk = self.parent()._geomCache[self._refVid], self._thickness
            if self._orientation == QtCore.Qt.Vertical:
                val  = pt.y()
                min_ = parentGeom.top() + thk
                max_ = parentGeom.bottom() - thk
                fix = pt.setY
            else:
                val  = pt.x()
                min_ = parentGeom.left() + thk
                max_ = parentGeom.right() - thk
                fix = pt.setX
            if   val < min_: val = min_
            elif val > max_: val = max_
            fix(val)
            return pt

        def _fixGeometry(self, newPt, geom):
            """Validate newPt and fix geom accordingly"""
            newPt = self.__valid_position(newPt)
            if self._orientation == QtCore.Qt.Vertical:
                geom.setY(newPt.y())
            else:
                geom.setX(newPt.x())
            self.handleMoved.emit(self._refVid, geom.topLeft(), self._orientation)
            return geom, True #DO NOT MODIFY THE GEOMETRY! IT WILL BE DONE BY THE GRAPH UPDATE

        ##############################
        # Qt Event reimplementations #
        ##############################
        def paintEvent(self, event):
            QStyle = QtGui.QStyle
            painter = QtGui.QPainter(self)
            opt = QtGui.QStyleOption(0)
            opt.rect = self.contentsRect()
            opt.palette = self.palette()
            opt.state = QStyle.State_Horizontal if self._orientation==QtCore.Qt.Horizontal \
                        else QStyle.State_None
            if self._hovered: opt.state |= QStyle.State_MouseOver
            if self._isMoving: opt.state |= QStyle.State_Sunken
            if self.isEnabled(): opt.state |= QStyle.State_Enabled
            #painter.fillRect(self.rect(), QtCore.Qt.blue)
            self.style().drawControl(QStyle.CE_Splitter, opt, painter, self)
    ###################################################################################
    # /end Inner classes not meant to be seen by others - Inner classes not meant to  #
    ###################################################################################



#Small testing example
if __name__ == "__main__":
    app = QtGui.QApplication(["Muahaha"])
    mw = QtGui.QMainWindow()
    splittable = SplittableUI(parent=mw)
    mw.setCentralWidget(splittable)
    mw.show()
    app.exec_()




