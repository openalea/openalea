# -*- python -*-
#
#       OpenAlea.SecondNature
#
#       Copyright 2006-2011 INRIA - CIRAD - INRA
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

__license__ = "CeCILL v2"
__revision__ = " $Id$ "


from PyQt4 import QtGui, QtCore

import urlparse

from openalea.secondnature.splittable import CustomSplittable
from openalea.secondnature.managers import init_sources
from openalea.secondnature.managers import LayoutManager
from openalea.secondnature.managers import WidgetFactoryManager
from openalea.secondnature.managers import ExtensionManager
from openalea.secondnature.extendable_objects import SingletonWidgetFactory

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

        LayoutManager().itemListChanged.connect(self.__onLayoutListChanged)
        self._layoutMode.activated[QtCore.QString].connect(self.__onLayoutChosen)

    def init_extensions(self):
        init_sources()

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

    def __onLayoutListChanged(self, layoutNames):
        layoutNames.sort()
        self._layoutMode.clear()
        self._layoutMode.addItems(layoutNames)
        self._layoutMode.setCurrentIndex(-1)

    def __setSpaceAt(self, paneId, space):
        content, menu, toolbar = space.content, space.menu, space.toolbar
        if content is not None:
            self.__setContentAt(paneId, content)
        if menu is not None:
            pass #self.__setMenuAt(paneId, menu)
        if toolbar is not None:
            pass #self.__setToolbarAt(paneId, toolbar)

    def __setContentAt(self, paneId, content):
        if self.__splittable:
            self.__splittable.setContentAt(paneId,
                                           content,
                                           noTearOffs=True, noToolButton=True)
    def __setMenuAt(self, paneId, menu):
        pass

    def __setToolbarAt(self, paneId, tb):
        pass

    def __on_splitter_drag_enter(self, event):
        #this is the hackiest part and concept-grinding bit of the problem
        #whatever that means...
        mimeData = event.mimeData()
        if mimeData.hasUrls():
            # we only support ONE url
            urls = mimeData.urls()
            if len(urls) == 0:
                return
            url = str(urls[0].toString())
            parsedUrl = urlparse.urlparse(url)
            if WidgetFactoryManager().has_handler_for(parsedUrl):
                event.acceptProposedAction()

    def __on_splitter_pane_drop(self, paneId, event):
        #this is the hackiest part and concept-grinding bit of the problem
        #whatever that means...
        mimeData = event.mimeData()
        if mimeData.hasUrls():
            # we only support ONE url
            urls = mimeData.urls()
            if len(urls) == 0:
                return
            url = str(urls[0].toString())

            if url == "":
                return

            parsedUrl = urlparse.urlparse(url)
            data, space = WidgetFactoryManager().create_space(input=parsedUrl)
            if space is not None:
                self.__register_document(data, url, space)
                self.__setSpaceAt(paneId, space)

    def __register_document(self, data, url, space):
        if None not in {data, space}:
            dm = DocumentManager()
            dm.watch(data, url, space)

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
        layout = LayoutManager().get(layoutName)

        if not layout:
            return

        # -- CHANGE THE LAYOUT --
        newSplit, taken = self.__new_splittable(layout.skeleton)

        # -- FILL THE LAYOUT WITH WIDGETS DESCRIBED BY THE WIDGET MAP --
        widgetmap = layout.widgetmap

        for paneId, widgetName in widgetmap.iteritems():
            data, space  = WidgetFactoryManager().create_space(name=widgetName)
            if space:
                self.__setSpaceAt(paneId, space)

    ######################
    # Pane Menu handlers #
    ######################
    def __onPaneMenuRequest(self, paneId, pos):
        pos = self.__splittable.mapToGlobal(pos)
        menu = QtGui.QMenu(self.__splittable)
        menu.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        action = menu.addAction("Empty")
        action.triggered.connect(self.__make_clear_pane_handler(paneId))

        widgetFactories = WidgetFactoryManager().gather_items()

        newMenu = menu.addMenu("New...")
        newWidgetNames = [f for f,v in widgetFactories.iteritems() \
                          if not isinstance(v, SingletonWidgetFactory)]
        for widName in newWidgetNames:
            action = newMenu.addAction(widName)
            func = self.__make_widget_pane_handler(paneId, widName)
            action.triggered.connect(func)

        widMenu = menu.addMenu("Tools...")
        widgetNames = [f for f,v in widgetFactories.iteritems() \
                          if isinstance(v, SingletonWidgetFactory)]
        for widName in widgetNames:
            action = widMenu.addAction(widName)
            func = self.__make_widget_pane_handler(paneId, widName)
            action.triggered.connect(func)

        docMenu = menu.addMenu("Documents...")
        dm = DocumentManager()
        for data, doc in dm:
            action = docMenu.addAction(doc.url)
            func = self.__make_document_pane_handler(paneId, doc.url)
            action.triggered.connect(func)
        menu.popup(pos)

    # Each time the user presses the "+" button of a pane a new menu
    # is created and it's actions are bound to new slots created on
    # the fly by the following "__make_*_pane_handler methods.
    # The reason is that otherwise we don't know which pane
    # requests the action. This is rougly equivalent to C++' bind1st.
    # Todo : objectify this
    def __make_clear_pane_handler(self, paneId):
        def on_clear_chosen(checked):
            self.__splittable.takeContentAt(paneId, None)
        func = on_clear_chosen
        return func

    def __make_widget_pane_handler(self, paneId, widgetName):
        def on_widget_chosen(checked):
            data, space = WidgetFactoryManager().create_space(name=widgetName)
            url = "blabla://sillydomain/"+str(data)
            self.__register_document(data, url, space)
            if space:
                self.__setSpaceAt(paneId, space)

        func = on_widget_chosen
        return func

    def __make_document_pane_handler(self, paneId, url):
        def on_document_chosen(checked):
            dm = DocumentManager()
            doc = dm[url]
            space = doc.editor
            if space is not None:
                self.__setSpaceAt(paneId, space)
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
