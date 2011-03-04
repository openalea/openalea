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
from openalea.secondnature.managers import AppletFactoryManager
from openalea.secondnature.project import ProjectManager
from openalea.secondnature.project import Project


sn_logger = get_logger(__name__)

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setMinimumSize(500, 400)
        self.showMaximized()
        self.setWindowTitle("Second Nature")
        self.setWindowFlags(QtCore.Qt.Window)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.logger = sn_logger

        self._mainMenu = QtGui.QMenuBar(self)

        self.__splittable = None
        self.__new_splittable()

        #status bar
        self._statusBar  = QtGui.QStatusBar(self)
        self._layoutMode = QtGui.QComboBox(self)
        self._statusBar.addPermanentWidget(self._layoutMode)
        self._layoutMode.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.__currentLayout = None

        self.setMenuBar(self._mainMenu)
        self.setStatusBar(self._statusBar)
        self.setCentralWidget(self.__splittable)

        pm = ProjectManager()
        if not pm.has_active_project():
            pm.new_active_project("New Project")

        LayoutManager().itemListChanged.connect(self.__onLayoutListChanged)
        self._layoutMode.activated[QtCore.QString].connect(self.__onLayoutChosen)


    def init_extensions(self):
        init_sources()
        # --choosing default layout--
        index = self._layoutMode.findText("Default Layout")
        if index >= 0:
            self._layoutMode.setCurrentIndex(index)
            self._layoutMode.activated[QtCore.QString].emit("Default Layout")

    #################################
    # DRAG AND DROP RELATED METHODS #
    #################################
    def __validate_mimedata(self, mimedata):
        good = False
        fmts = reduce(lambda x,y:str(x)+' '+str(y), mimedata.formats(),"")
#        print fmts
        #self.logger.info("__validate_mimedata formats" + fmts)
        if mimedata.hasFormat("text/uri-list"):
            urls = mimedata.urls()
            # we only support ONE url
            if len(urls) == 1:
                good = True
        elif mimedata.hasFormat(ProjectManager.mimeformat):
            good = True
        if not good:
            self.logger.error("invalid mimedata: "+fmts)
        return good

    def __on_splitter_drag_enter(self, event):
        mimeData = event.mimeData()
        if not self.__validate_mimedata(mimeData):
            return

        handlers = AppletFactoryManager().get_handlers_for_mimedata(mimeData.formats())
        if len(handlers) > 0:
            event.acceptProposedAction()
        elif mimeData.hasFormat(ProjectManager.mimeformat):
            event.acceptProposedAction()

    def __applet_factory_from_mime_formats(self, formats):
        handlers = AppletFactoryManager().get_handlers_for_mimedata(formats)
#        print handlers
        nbHandlers = len(handlers)
        if nbHandlers == 0:
            return
        elif nbHandlers == 1:
            fac = handlers[0]
        elif nbHandlers > 1:
            selector = DocumentEditorSelector( [h.fullname for h in handlers], self )
            if selector.exec_() == QtGui.QDialog.Rejected:
                return
            else:
                facName = selector.get_selected()
                fac = filter(lambda x: x.fullname == facName, handlers)[0]
        return fac


    def __on_splitter_pane_drop(self, paneId, event):
        mimeData = event.mimeData()
        if not self.__validate_mimedata(mimeData):
            return

        proj = ProjectManager().get_active_project()
        fac = None
        doc = None
        space = None

        if mimeData.hasUrls():
            formats = mimeData.formats()
            url = str(mimeData.urls()[0].toString())
            parsedUrl = urlparse.urlparse(url)
            fac = self.__applet_factory_from_mime_formats(formats)
            if fac:
                doc = fac.open_document_and_register_it(parsedUrl)
        elif mimeData.hasFormat(ProjectManager.mimeformat):
            docIdBytes = mimeData.data(ProjectManager.mimeformat)
            if docIdBytes:
                docId, ok = docIdBytes.toInt()
                if ok and proj:
                    doc = proj.get_document(docId)
                    if doc:
                        fac = self.__applet_factory_from_mime_formats([doc.mimetype])

        # first try to retreive the space associated to this document
        if proj and doc:
            space = proj.get_document_property(doc, "space")
        # if space is still none, we can always try to create a new space
        if space is None and doc:
            if fac:
                space = fac(doc)

        if space is not None:
            self.__setSpaceAt(paneId, space)

    ####################################
    # Layout selection related methods #
    ####################################
    def __onLayoutListChanged(self, layoutNames):
        layoutNames.sort()
        self._layoutMode.clear()
        self._layoutMode.addItems(layoutNames)
        if self.__currentLayout:
            ind = self._layoutMode.findText(self.__currentLayout)
        else:
            ind = -1
        self._layoutMode.setCurrentIndex(ind)
        self._layoutMode.adjustSize()

    def __onLayoutChosen(self, layoutName):
        """Called when a user chooses a layout. Fetches the corresponding
        layout from the registered applications and installs a new splitter
        in the central window."""

        if layoutName is None or layoutName == "":
            return

        # convert from QString to python str
        layoutName = str(layoutName)
        # layoutNames encodes the application
        # name and the layout name:
        # they are seperated by a period.
        layout = LayoutManager().get(layoutName)
        if not layout:
            return

        # -- FILL THE LAYOUT WITH WIDGETS DESCRIBED BY THE RESOURCE MAP --
        # create new splittable and retreive objects from previous
        newSplit, taken = self.__new_splittable(layout.skeleton)

        appletmap = layout.appletmap
        afm = AppletFactoryManager()
        for paneId, appletName in appletmap.iteritems():
            appFac = afm.get(appletName)
            if appFac is None:
                self.logger.debug("__onLayoutChosen has None factory for "+appletName)
                continue
            try:
                space  = appFac()
            except Exception, e:
                self.logger.error("__onLayoutChosen cannot display "+ \
                                  appletName+":"+\
                                  e.message)
                continue
            if space:
                self.__setSpaceAt(paneId, space)
        self.__currentLayout = layoutName

    ######################
    # Pane Menu handlers #
    ######################
    # Each time the user presses the "+" button of a pane a new menu
    # is created and it's actions are bound to new slots created on
    # the fly by the following "__make_*_pane_handler methods.
    # The reason is that otherwise we don't know which pane
    # requests the action. This is rougly equivalent to C++' bind1st.
    # Todo : objectify this

    def __onPaneMenuRequest(self, paneId, pos):
        pos = self.__splittable.mapToGlobal(pos)
        menu = QtGui.QMenu(self.__splittable)
        menu.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        action = menu.addAction("Clear")
        action.triggered.connect(self.__make_clear_pane_handler(paneId))

        appletMenu = menu.addMenu("Applets...")
        appFactories = AppletFactoryManager().gather_items()
        appletNames = sorted(appFactories.iterkeys())
        for appName in appletNames:
            action = appletMenu.addAction(appName)
            func = self.__make_new_applet_pane_handler(paneId, appName)
            action.triggered.connect(func)

        pm = ProjectManager()
        proj = pm.get_active_project()
        if proj:
            docMenu = menu.addMenu("Project Documents...")
            for id, doc in proj:
                srcName = doc.name# + " ("+doc.source+")"
                # must escape the ampersand or Qt stips it as a mnemonic
                srcName = srcName.replace("&","&&")
                action = docMenu.addAction(srcName)
                func = self.__make_document_pane_handler(proj, paneId, doc)
                action.triggered.connect(func)
        menu.popup(pos)

    def __make_clear_pane_handler(self, paneId):
        def on_clear_chosen(checked):
            self.__splittable.takeContentAt(paneId, None)
        func = on_clear_chosen
        return func

    def __make_new_applet_pane_handler(self, paneId, appletName):
        def on_applet_chosen(checked):
            fac  = AppletFactoryManager().get(appletName)
            if not fac:
                self.logger.debug("on_applet_chosen has None factory for " + appletName)
            else:
                doc = fac.new_document_and_register_it()
                space = fac(doc)
                if doc is None:
                    self.logger.debug("on_applet_chosen has None document for "+ appletName)
                if space is None:
                    self.logger.debug("on_applet_chosen has None space for " + appletName)
                else:
                    self.__setSpaceAt(paneId, space)

        func = on_applet_chosen
        return func

    def __make_document_pane_handler(self, proj, paneId, doc):
        def on_document_chosen(checked):
            space = proj.get_document_property(doc, "space")
            if space is None:
                self.logger.debug("on_document_chosen has None space for "+doc.name)
            else:
                self.__setSpaceAt(paneId, space)

        func = on_document_chosen
        return func



    ####################################
    # SPACE CONTENT MANAGEMENT METHODS #
    ####################################
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

    def __setSpaceAt(self, paneId, space):
        content, menuList, toolbar = space.content, space.menus, space.toolbar
        if content is not None:
            self.__setContentAt(paneId, content)
        if menuList:
            self.__setMenusAt(paneId, menuList)
        if toolbar is not None:
            self.__setToolbarAt(paneId, toolbar)

    def __setContentAt(self, paneId, content):
        if self.__splittable:
            self.__splittable.setContentAt(paneId,
                                           content,
                                           noTearOffs=True, noToolButton=True)

    def __setMenusAt(self, paneId, menuList):
        pass

    def __setToolbarAt(self, paneId, tb):
        pass






class DocumentEditorSelector(QtGui.QDialog):
    def __init__(self, items, parent=None):
        QtGui.QDialog.__init__(self, parent, QtCore.Qt.WindowOkButtonHint|
                                             QtCore.Qt.WindowCancelButtonHint)
        self.setWindowTitle("Select a tool")
        self.__l = QtGui.QVBoxLayout()
        self.__itemList = QtGui.QListWidget()
        self.__buttons = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|
                                                QtGui.QDialogButtonBox.Cancel)
        self.__l.addWidget(self.__itemList)
        self.__l.addWidget(self.__buttons)
        self.setLayout(self.__l)
        self.__itemList.addItems(items)
        self.__buttons.accepted.connect(self.accept)
        self.__buttons.rejected.connect(self.reject)

    def get_selected(self):
        return self.__itemList.currentItem().text()




