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
from openalea.core.logger import get_logger
from openalea.secondnature.splittable import CustomSplittable
from openalea.secondnature.managers import init_sources
from openalea.secondnature.managers import LayoutManager
from openalea.secondnature.managers import DocumentWidgetFactoryManager
from openalea.secondnature.managers import ResourceWidgetFactoryManager
from openalea.secondnature.managers import ExtensionManager
from openalea.secondnature.managers import DocumentManager
#from openalea.secondnature.extendable_objects import SingletonWidgetFactory

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setMinimumSize(500, 400)
        self.setWindowTitle("Second Nature")
        self.setWindowFlags(QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.logger = get_logger(__name__)

        self._mainMenu = QtGui.QMenuBar(self)

        self.__splittable = None
        self.__new_splittable()

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
            self.__setMenuAt(paneId, menu)
        if toolbar is not None:
            self.__setToolbarAt(paneId, toolbar)

    def __setContentAt(self, paneId, content):
        if self.__splittable:
            self.__splittable.setContentAt(paneId,
                                           content,
                                           noTearOffs=True, noToolButton=True)

    def __setMenuAt(self, paneId, menu):
        pass

    def __setToolbarAt(self, paneId, tb):
        pass

    def __validate_mimedata(self, mimedata):
        good = False
        for f in mimedata.formats():
            print f
        if mimedata.hasFormat("text/uri-list"):
            good = True
        urls = mimedata.urls()
        # we only support ONE url
        if len(urls) == 1:
            good = True
        if not good:
            fmts = reduce(lambda x,y:str(x)+' '+str(y), mimedata.formats(),"")
            self.logger.debug("invalid mimedata: "+fmts)
        return good

    def __on_splitter_drag_enter(self, event):
        mimeData = event.mimeData()
        if not self.__validate_mimedata(mimeData):
            return
        handlers = DocumentWidgetFactoryManager().get_handlers_for_mimedata(mimeData)
        if len(handlers) > 0:
            event.acceptProposedAction()

    def __on_splitter_pane_drop(self, paneId, event):
        mimeData = event.mimeData()
        if not self.__validate_mimedata(mimeData):
            return

        handlers = DocumentWidgetFactoryManager().get_handlers_for_mimedata(mimeData)
        nbHandlers = len(handlers)
        if nbHandlers == 0:
            return
        elif nbHandlers == 1:
            fac = handlers[0]
        elif nbHandlers > 1:
            fac = None

        url = str(mimeData.urls()[0].toString())
        parsedUrl = urlparse.urlparse(url)
        doc   = fac.open_document(parsedUrl)
        space = fac.get_document_space(doc)

        if None not in {doc, space}:
            self.__register_document(doc, space)
            self.__setSpaceAt(paneId, space)

    def __register_document(self, doc, space):
        if None not in {doc, space}:
            dm = DocumentManager()
            dm.add_document(doc)
            dm.set_document_property(doc, "space", space)

    def __onLayoutChosen(self, layoutName):
        """Called when a user chooses a layout. Fetches the corresponding
        layout from the registered applications and installs a new splitter
        in the central window."""

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

        # -- FILL THE LAYOUT WITH WIDGETS DESCRIBED BY THE RESOURCE MAP --
        resourcemap = layout.resourcemap

        rwfm = ResourceWidgetFactoryManager()
        for paneId, resourceName in resourcemap.iteritems():
            resFac = rwfm.get(resourceName)
            if resFac is None:
                self.logger.debug("__onLayoutChosen has None factory for "+resourceName)
                continue
            res    = resFac.get_resource()
            space  = resFac.get_resource_space(res)
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

        docWidgetFactories = DocumentWidgetFactoryManager().gather_items()
        newMenu = menu.addMenu("New...")
        newWidgetNames = list(docWidgetFactories.iterkeys())
        for widName in newWidgetNames:
            action = newMenu.addAction(widName)
            func = self.__make_new_doc_pane_handler(paneId, widName)
            action.triggered.connect(func)

        resWidgetFactories = ResourceWidgetFactoryManager().gather_items()
        resMenu = menu.addMenu("Tools...")
        newWidgetNames = list(resWidgetFactories.iterkeys())
        for widName in newWidgetNames:
            action = resMenu.addAction(widName)
            func = self.__make_resource_pane_handler(paneId, widName)
            action.triggered.connect(func)

        dm = DocumentManager()
        docMenu = menu.addMenu("Documents...")
        for source, doc in dm:
            srcName = doc.name + " ("+doc.source+")"
            # must escape the ampersand or Qt stips it as a mnemonic
            srcName = srcName.replace("&","&&")
            action = docMenu.addAction(srcName)
            func = self.__make_document_pane_handler(paneId, doc)
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

    def __make_new_doc_pane_handler(self, paneId, widgetName):
        def on_doc_widget_chosen(checked):
            fac  = DocumentWidgetFactoryManager().get(widgetName)
            if not fac:
                self.logger.debug("on_doc_widget_chosen has None factory for " + widgetName)
            else:
                doc = fac.new_document()
                space = fac.get_document_space(doc)
                if doc is None:
                    self.logger.debug("on_res_widget_chosen has None document for "+ widgetName)
                if space is None:
                    self.logger.debug("on_res_widget_chosen has None space for " + widgetName)
                else:
                    self.__register_document(doc, space)
                    self.__setSpaceAt(paneId, space)

        func = on_doc_widget_chosen
        return func

    def __make_resource_pane_handler(self, paneId, widgetName):
        def on_res_widget_chosen(checked):
            fac = ResourceWidgetFactoryManager().get(widgetName)
            if fac is None:
                self.logger.debug("on_res_widget_chosen has None factory for "+ widgetName)
            else:
                res = fac.get_resource()
                space = fac.get_resource_space(res)
                if res is None:
                    self.logger.debug("on_res_widget_chosen has None resource for "+ widgetName)
                if space is None:
                    self.logger.debug("on_res_widget_chosen has None space for "+widgetName)
                else:
                    self.__setSpaceAt(paneId, space)

        func = on_res_widget_chosen
        return func

    def __make_document_pane_handler(self, paneId, doc):
        def on_document_chosen(checked):
            dm = DocumentManager()
            space = dm.get_document_property(doc, "space")
            if space is None:
                self.logger.debug("on_document_chosen has None space for "+doc.source)
            else:
                self.__setSpaceAt(paneId, space)

        func = on_document_chosen
        return func




