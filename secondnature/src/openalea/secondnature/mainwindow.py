





from PyQt4 import QtGui, QtCore

from openalea.visualea.splitterui import RubberBandScrollArea, SplittableUI, DraggableWidget
from openalea.secondnature.applications import Extension


class CustomSplittable(SplittableUI):

    paneMenuRequest = QtCore.pyqtSignal(int, QtCore.QPoint)

    def _raise_overlays(self, paneId):
        SplittableUI._raise_overlays(self, paneId)
        tb  = self._g.get_property(paneId, "toolButtonWidget")
        tb.raise_()

    def _split_parent(self, paneId, direction, amount):
        w = SplittableUI._split_parent(self, paneId, direction, amount)
        self._remove_toolbutton(paneId)
        return w

    def _install_child(self, paneId, widget, **kwargs):
        w = SplittableUI._install_child(self, paneId, widget, **kwargs)
        if not kwargs.get("noToolButton", False):
            self._install_toolbutton(paneId)
        return w

    def _uninstall_child(self, paneId):
        w = SplittableUI._uninstall_child(self, paneId)
        self._remove_toolbutton(paneId)
        return w

    def _install_toolbutton(self, paneId):
        g = self._g
        toolbutton = CustomSplittable.ToolButton(paneId, self)
        toolbutton.show()
        toolbutton.clicked.connect(self.paneMenuRequest)
        g.set_property(paneId, "toolButtonWidget", toolbutton)

    def _remove_toolbutton(self, paneId):
        g = self._g
        if not g.has_property(paneId, "toolButtonWidget"):
            return
        toolbut = g.pop_property(paneId, "toolButtonWidget")
        toolbut.close()


    class ToolButton(QtGui.QWidget, DraggableWidget):

        clicked = QtCore.pyqtSignal(int, QtCore.QPoint)
        __ideal_height__ = 10

        def __init__(self, refVid, parent):
            QtGui.QWidget.__init__(self, parent)
            DraggableWidget.__init__(self)
            self.vid = refVid
            self.setFixedHeight(self.__ideal_height__)
            self.setFixedWidth(self.__ideal_height__)

        def mouseReleaseEvent(self, event):
            ret = DraggableWidget.mouseReleaseEvent(self, event)
            if self.rect().contains(event.pos()):
                self.clicked.emit(self.vid, self.mapToParent(event.pos()))
            return ret

        def paintEvent(self, event):
            painter = QtGui.QPainter(self)
            painter.setRenderHint(QtGui.QPainter.Antialiasing)

            if self._hovered:
                brush   = QtGui.QBrush(QtGui.QColor(120,190,255,200))
            else:
                brush   = QtGui.QBrush(QtGui.QColor(120,190,255,70))
            painter.setBrush(brush)

            pen = painter.pen()
            pen.setColor(QtGui.QColor(0,0,0,255))
            pen.setWidth(1)
            painter.setPen(pen)

            adj = pen.width()
            rect = self.contentsRect().adjusted(adj,adj,-adj,-adj)
            painter.drawEllipse(rect)

            center = rect.center()
            x = center.x()+adj
            y = center.y()+adj
            ls = [QtCore.QPoint(x, rect.top()+1+adj),
                  QtCore.QPoint(x, rect.bottom()-1),
                  QtCore.QPoint(rect.left()+1+adj, y),
                  QtCore.QPoint(rect.right()-1, y)]
            painter.drawLines(ls)


    class GeometryComputingVisitor(SplittableUI.GeometryComputingVisitor):
        def visit(self, vid):
            igF, igS = SplittableUI.GeometryComputingVisitor.visit(self, vid)
            if not self.g.has_children(vid):
                geom = self.geomCache[vid]
                tb = self.g.get_property(vid, "toolButtonWidget")
                th = CustomSplittable.ToolButton.__ideal_height__
                if geom.height() <  th or geom.width() < th:
                    tb.hide()
                else:
                    tb.show()

                tb.move(geom.left()+1, geom.top()+1)
                return False, False #don't ignore first or second child
            return igF, igS




class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setMinimumSize(500, 400)
        self.setWindowTitle("Second Nature")
        self.setWindowFlags(QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self._mainMenu = QtGui.QMenuBar(self)

        self.__splittable = None
        self.__new_splittable()

        #store temporary action for pane menu
        self.__menuActions = {}

        #status bar
        self._statusBar  = QtGui.QStatusBar(self)
        self._layoutMode = QtGui.QComboBox(self)
        self._statusBar.addPermanentWidget(self._layoutMode)

        self.setMenuBar(self._mainMenu)
        self.setStatusBar(self._statusBar)
        self.setCentralWidget(self.__splittable)

        Extension.q.applicationListChanged.connect(self.__onExtensionListChange)
        self._layoutMode.activated[QtCore.QString].connect(self.__onLayoutChosen)
        Extension.entry_point_init()


    def __new_splittable(self, skeleton=None):
        if skeleton == None:
            s = CustomSplittable(parent=None)
        else:
            s = CustomSplittable.fromString(skeleton, parent=None)
        s.setContentsMargins(0,0,0,0)

        taken = None
        if self.__splittable is not None:
            # -- prevent deletion of C++ side of widgets by QObject mecanism --
            taken = self.__splittable.takeAllContents(reparent=self)
            self.__splittable.hide()

        self.__splittable = s
        self.setCentralWidget(s)
        s.paneMenuRequest.connect(self.__onPaneMenuRequest)
        s.dragEnterEventTest.connect(self.__on_splitter_drag_enter)
        s.dropHandlerRequest.connect(self.__on_splitter_pane_drop)
        return s, taken

    def __onExtensionListChange(self):
        layouts = Extension.get_layout_names()
        self._layoutMode.clear()
        self._layoutMode.addItems(layouts)
        self._layoutMode.setCurrentIndex(-1)

    def __setContentAt(self, paneId, content):
        if self.__splittable:
            self.__splittable.setContentAt(paneId,
                                           content,
                                           noTearOffs=True, noToolButton=True)

    def __on_splitter_drag_enter(self, event):
        # we only support ONE url
        urls = event.mimeData().urls()
        if len(urls) == 0:
            return
        url = str(urls[0].toString())
        if Extension.has_url_handler(url):
            event.acceptProposedAction()

    def __on_splitter_pane_drop(self, paneId, event):
        # we only support ONE url
        urls = event.mimeData().urls()
        if len(urls) == 0:
            return
        url = str(urls[0].toString())

        if url == "":
            return

        obj, editor = Extension.create_editor_for(url, self.__splittable)
        dm = DocumentManager()
        dm.watch(obj, url, editor)
        self.__setContentAt(paneId, editor)

    def __onLayoutChosen(self, layoutName):
        """Called when a user chooses a layout. Fetches the corresponding
        layout from the registered applications and installs a new splitter
        in the central window."""
        # -- CHECKS TO DO THIS SAFELY! --
        if layoutName is None or layoutName == "":
            return

        layoutName = str(layoutName)   # convert from QString to python str

        # layoutNames encodes the application name and the layout name:
        # they are seperated by a period.
        appName, layout = layoutName.split(".")
        app             = Extension.get_application(appName)

        if app is None:
            return

        layout = app.layouts().get(layout)
        if not layout:
            return

        # -- CHANGE THE LAYOUT --
        newSplit, taken = self.__new_splittable(layout.skeleton)

        # -- FILL THE LAYOUT WITH WIDGETS DESCRIBED BY THE WIDGET MAP --
        widgetmap = layout.widgetmap

        for paneId, widgetName in widgetmap.iteritems():
            app, widgetName = widgetName.split(".")
            app = Extension.get_application(app)
            wid = app.create_widget(widgetName)
            if wid:
                if wid.widget is not None:
                    self.__setContentAt(paneId, wid.widget)




    ######################
    # Pane Menu handlers #
    ######################
    def __onPaneMenuRequest(self, paneId, pos):
        pos = self.__splittable.mapToGlobal(pos)
        menu = QtGui.QMenu(self.__splittable)
        menu.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        action = menu.addAction("Empty")
        action.triggered.connect(self.__make_clear_pane_handler(paneId))

        widMenu = menu.addMenu("Controlers")
        widgetNames = Extension.get_widget_names()
        for widName in widgetNames:
            action = widMenu.addAction(widName)
            func = self.__make_widget_pane_handler(paneId, widName)
            action.triggered.connect(func)

        docMenu = menu.addMenu("Documents")
        dm = DocumentManager()
        for data, doc in dm:
            action = docMenu.addAction(doc.url)
            func = self.__make_document_pane_handler(paneId, doc.url)
            action.triggered.connect(func)
        menu.popup(pos)

    # Each time the user pressed the "+" button of a pane a new menu
    # is created and it's actions are bound to new slots create on
    # the fly by the following "__make_*_pane_handler.
    # The reason is that otherwise we don't know which pane
    # requests the action. This is rougly equivalent to C++' bind1st.
    def __make_clear_pane_handler(self, paneId):
        def on_clear_chosen(checked):
            self.__splittable.takeContentAt(paneId, None)
        func = on_clear_chosen
        return func


    def __make_widget_pane_handler(self, paneId, widgetName):
        def on_widget_chosen(checked):
            app, widName = widgetName.split(".")
            app = Extension.get_application(app)
            wid = app.create_widget(widName)
            if wid:
                widget = wid.widget
                if widget is not None:
                    self.__setContentAt(paneId, widget)
        func = on_widget_chosen
        return func

    def __make_document_pane_handler(self, paneId, url):
        def on_document_chosen(checked):
            dm = DocumentManager()
            doc = dm[url]
            widget = doc.editor
            if widget is not None:
                self.__setContentAt(paneId, widget)
        func = on_document_chosen
        return func





from openalea.core.metaclass import make_metaclass
from openalea.core.singleton import ProxySingleton

class DocumentManager(QtCore.QObject):
    """"""
    class Document(object):
        """"""
        def __init__(self, url, editor, obj):
            self.__url    = url
            self.__editor = editor
            self.__obj    = obj

        url    = property(lambda x:x.__url)
        editor = property(lambda x:x.__editor)
        obj    = property(lambda x:x.__obj)

        @url.setter
        def url(self, value): self.__url=value
        @editor.setter
        def editor(self, value): self.__editor=value
        @obj.setter
        def obj(self, value): self.__obj=value

    __metaclass__ = make_metaclass((ProxySingleton,),
                                   (QtCore.pyqtWrapperType,))

    def __init__(self):
        QtCore.QObject.__init__(self)
        self.__documents = {}
        self.__urlToDoc  = {}

    def watch(self, obj, url, editor):
        doc = DocumentManager.Document(url, editor, obj)
        self.__documents[obj] = doc
        self.__urlToDoc[url] = doc

    def discard(self, obj):
        del self.__documents[obj]

    def __getitem__(self, url):
        return self.__urlToDoc[url]

    def __iter__(self):
        return self.__documents.iteritems()
