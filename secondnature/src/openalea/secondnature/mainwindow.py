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
import traceback

from openalea.core.logger import get_logger

from openalea.secondnature.splittable import CustomSplittable
from openalea.secondnature.managers   import AbstractSourceManager
from openalea.secondnature.layouts    import LayoutManager
from openalea.secondnature.applets    import AppletFactoryManager
from openalea.secondnature.data       import DataFactoryManager
from openalea.secondnature.project    import Project
from openalea.secondnature.project    import ProjectManager
from openalea.secondnature.project    import QActiveProjectManager
from openalea.secondnature.mimetools  import DataEditorSelector
from openalea.secondnature.qtutils    import try_to_disconnect



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
        self.__applets = []

        # -- main menu bar --
        self._mainMenuBar = QtGui.QMenuBar(self)
        self._projectMenu = self._mainMenuBar.addMenu("&Project")
        self.setMenuBar(self._mainMenuBar)

        # -- project menu --
        qpm = QActiveProjectManager()
        self._projectMenu.addAction(qpm.get_action_new())
        self._projectMenu.addAction(qpm.get_action_open())
        self._projectMenu.addAction(qpm.get_action_save())
        self._projectMenu.addAction(qpm.get_action_close())

        # -- a default central widget--
        self.__centralStack = QtGui.QStackedWidget(self)

        # -- status bar --
        self._statusBar  = QtGui.QStatusBar(self)
        self._layoutMode = QtGui.QComboBox(self)
        self._statusBar.addPermanentWidget(self._layoutMode)
        self._layoutMode.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.__currentLayout = None

        # -- add all those guys to the main window (self) --
        self.setMenuBar(self._mainMenuBar)
        self.setStatusBar(self._statusBar)
        self.setCentralWidget(self.__centralStack)

        self.__projMan = ProjectManager()
        if not self.__projMan.has_active_project():
            self.__projMan.new_active_project("New Project")

        # -- connections --
        self.__projMan.active_project_changed.connect(self.__on_active_project_set)
        AppletFactoryManager().applet_created.connect(self.add_applet)
        LayoutManager().item_list_changed.connect(self.__onLayoutListChanged)
        self._layoutMode.activated[int].connect(self.__onLayoutChosen)
        self._layoutMode.currentIndexChanged[int].connect(self.__onLayoutChosen)


    def init_extensions(self):
        AbstractSourceManager.init()
        # --choosing default layout--
        index = self._layoutMode.findText("Default Layout")
        if index >= 0:
            self._layoutMode.setCurrentIndex(index)

    #########################################
    # Active project status change handlers #
    #########################################
    def __on_active_project_set(self, proj, old):
        for applet in self.__applets:
            try_to_disconnect(old.data_added, applet.update_combo_list)
            proj.data_added.connect(applet.update_combo_list)

    def add_applet(self, applet):
        self.__projMan.data_added.connect(applet.update_combo_list)
        self.__applets.append(applet)

    #################################
    # DRAG AND DROP RELATED METHODS #
    #################################
    def __validate_mimedata(self, mimedata):
        good = False
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

    def __on_splitter_drag_enter(self, splittable, event):
        mimeData = event.mimeData()
        if not self.__validate_mimedata(mimeData):
            return

        formats = map(str, mimeData.formats())
        handlers = DataFactoryManager().get_handlers_for_mimedata(formats)
        if len(handlers) > 0:
            event.acceptProposedAction()
        elif mimeData.hasFormat(ProjectManager.mimeformat):
            event.acceptProposedAction()

    def __on_splitter_pane_drop(self, splittable, paneId, event):
        mimeData = event.mimeData()
        if not self.__validate_mimedata(mimeData):
            return

        proj = self.__projMan.get_active_project()
        app = None
        data = None
        content = None
        space = None

        if mimeData.hasUrls():
            formats = mimeData.formats()
            url = str(mimeData.urls()[0].toString())
            dt = DataEditorSelector.mime_type_handler(formats, applet=False)
            if not dt:
                return
            parsedUrl = urlparse.urlparse(url)
            data = dt._open_url_0(parsedUrl)
            if not data:
                return
            app = DataEditorSelector.mime_type_handler([data.mimetype], applet=True)
            if not app:
                return

        elif mimeData.hasFormat(ProjectManager.mimeformat):
            dataIdBytes = mimeData.data(ProjectManager.mimeformat)
            if dataIdBytes:
                dataId, ok = dataIdBytes.toInt()
                if ok and proj:
                    data = proj.get_data(dataId)
                    if data:
                        app = DataEditorSelector.mime_type_handler([data.mimetype], applet=True)

        # -- first try to retreive the content associated to this data --
        # NO_SPACE_CONTENT_TRACKING
        # if proj and data:
        #     content = proj.get_data_property(data, "spaceContent")
        # -- if content is still none, we can always try to create a new content --
        if content is None and data:
            if app:
                content = app._create_space_content_0(data)
        # -- find the space (applet) of the pane or create one if none:
        space = splittable.getContentAt(paneId)
        newSpace = False
        if not space or not space.supports(data):
            newSpace = True
            space = app()
        space.add_content(data, content)

        if newSpace is not None:
            self.__setSpaceAt(splittable, paneId, space)

    ####################################
    # Layout selection related methods #
    ####################################
    def __onLayoutListChanged(self, layoutNames):
        self._layoutMode.blockSignals(True)
        oldDataMap = {}
        current = self._layoutMode.currentText()
        for index in range(self._layoutMode.count()):
            oldDataMap[str(self._layoutMode.itemText(index))] = self._layoutMode.itemData(index)
        self._layoutMode.clear()

        layoutNames.sort()
        for ln in layoutNames:
            self._layoutMode.addItem(ln, oldDataMap.get(ln, QtCore.QVariant()))
        self._layoutMode.adjustSize()

        ind = self._layoutMode.findText(current)
        self._layoutMode.setCurrentIndex(ind)
        self._layoutMode.blockSignals(False)

    def __onLayoutChosen(self, index):
        """Called when a user chooses a layout. Fetches the corresponding
        layout from the registered applications and installs a new splitter
        in the central window."""

        layoutName = self._layoutMode.itemText(index)
        if layoutName is None or layoutName == "":
            return

        data = self._layoutMode.itemData(index).toPyObject()
        if data and isinstance(data, CustomSplittable):
            index = self.__centralStack.indexOf(data)
            if index == -1:
                self.__centralStack.addWidget(data)
            self.__centralStack.setCurrentWidget(data)
        else:
            # convert from QString to python str
            layoutName = str(layoutName)
            # layoutNames encodes the application
            # name and the layout name:
            # they are seperated by a period.
            layout = LayoutManager().get(layoutName)
            if not layout:
                return

            # -- FILL THE LAYOUT WITH WIDGETS DESCRIBED BY THE APPLET MAP --
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
                    traceback.print_exc()
                    continue
                if space:
                    self.__setSpaceAt(newSplit, paneId, space)

            self.__centralStack.addWidget(newSplit)

            self.__centralStack.setCurrentWidget(newSplit)
            self._layoutMode.setItemData(index, QtCore.QVariant(newSplit))

    ######################
    # Pane Menu handlers #
    ######################

    # Each time the user presses the "+" button of a pane a new menu
    # is created and it's actions are bound to new slots created on
    # the fly by the following "__make_*_pane_handler methods.
    # The reason is that otherwise we don't know which pane
    # requests the action. This is rougly equivalent to C++' bind1st.
    # Todo : objectify this

    def __onPaneMenuRequest(self, splittable, paneId, pos):
        proj = self.__projMan.get_active_project()

        pos = splittable.mapToGlobal(pos)
        menu = QtGui.QMenu(splittable)
        menu.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        action = menu.addAction("Empty")
        menu.addSeparator()
        action.triggered.connect(self.__make_clear_pane_handler(splittable, paneId))

        applets    = list(AppletFactoryManager().gather_items().itervalues())
        applets.sort(cmp = lambda x,y:cmp(x.name, y.name))
        for app in applets:
            action = menu.addAction(app.icon, app.name)
            action.setIconVisibleInMenu(True)
            func = self.__make_new_applet_pane_handler(splittable, proj, paneId, app)
            action.triggered.connect(func)
        menu.popup(pos)

    def __make_clear_pane_handler(self, splittable, paneId):
        def on_clear_chosen(checked):
            splittable.takeContentAt(paneId, None)
        func = on_clear_chosen
        return func

    def __make_new_applet_pane_handler(self, splittable, proj, paneId, applet):
        def f(checked):
            space = applet()
            self.__setSpaceAt(splittable, paneId, space)
        return f


    ####################################
    # SPACE CONTENT MANAGEMENT METHODS #
    ####################################
    def __new_splittable(self, skeleton=None):
        if skeleton == None:
            s = CustomSplittable(parent=self.__centralStack)
        else:
            s = CustomSplittable.fromString(skeleton, parent=self.__centralStack)
        s.setContentsMargins(0,0,0,0)

        taken = None
        s.full_sticky_check()
        s.paneMenuRequest.connect(self.__onPaneMenuRequest)
        s.dragEnterEventTest.connect(self.__on_splitter_drag_enter)
        s.dropHandlerRequest.connect(self.__on_splitter_pane_drop)
        return s, taken

    def __setSpaceAt(self, splittable, paneId, space):
        splittable.setContentAt(paneId,
                                space,
                                noTearOffs=True, noToolButton=True)




