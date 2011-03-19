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

from openalea.secondnature.managers import AbstractSourceManager
from openalea.secondnature.layouts  import LayoutManager
from openalea.secondnature.applets  import AppletFactoryManager
from openalea.secondnature.data     import DataTypeManager

from openalea.secondnature.project import Project
from openalea.secondnature.project import ProjectManager
from openalea.secondnature.project import QActiveProjectManager

from openalea.secondnature.mimetools import DataEditorSelector

from openalea.secondnature.qtutils import try_to_disconnect



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

        # main menu bar
        self._mainMenuBar = QtGui.QMenuBar(self)
        self._projectMenu = self._mainMenuBar.addMenu("&Project")
        self.setMenuBar(self._mainMenuBar)

        # project menu
        qpm = QActiveProjectManager()
        self._projectMenu.addAction(qpm.get_action_new())
        self._projectMenu.addAction(qpm.get_action_open())
        self._projectMenu.addAction(qpm.get_action_save())
        self._projectMenu.addAction(qpm.get_action_close())

        # a default central widget
        self.__splittable = None
        self.__new_splittable()

        # status bar
        self._statusBar  = QtGui.QStatusBar(self)
        self._layoutMode = QtGui.QComboBox(self)
        self._statusBar.addPermanentWidget(self._layoutMode)
        self._layoutMode.setSizeAdjustPolicy(QtGui.QComboBox.AdjustToContents)
        self.__currentLayout = None

        # add all those guys to the main window (self)
        self.setMenuBar(self._mainMenuBar)
        self.setStatusBar(self._statusBar)
        self.setCentralWidget(self.__splittable)

        self.__projMan = ProjectManager()
        if not self.__projMan.has_active_project():
            self.__projMan.new_active_project("New Project")

        # -- connections --
        self.__projMan.active_project_changed.connect(self.__on_active_project_set)
        AppletFactoryManager().applet_created.connect(self.add_applet)
        LayoutManager().item_list_changed.connect(self.__onLayoutListChanged)
        self._layoutMode.activated[QtCore.QString].connect(self.__onLayoutChosen)


    def init_extensions(self):
        AbstractSourceManager.init()
        # --choosing default layout--
        index = self._layoutMode.findText("Default Layout")
        if index >= 0:
            self._layoutMode.setCurrentIndex(index)
            self._layoutMode.activated[QtCore.QString].emit("Default Layout")

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

    def __on_splitter_drag_enter(self, event):
        mimeData = event.mimeData()
        if not self.__validate_mimedata(mimeData):
            return

        formats = map(str, mimeData.formats())
        handlers = DataTypeManager().get_handlers_for_mimedata(formats)
        if len(handlers) > 0:
            event.acceptProposedAction()
        elif mimeData.hasFormat(ProjectManager.mimeformat):
            event.acceptProposedAction()

    def __on_splitter_pane_drop(self, paneId, event):
        mimeData = event.mimeData()
        if not self.__validate_mimedata(mimeData):
            return

        proj = self.__projMan.get_active_project()
        app = None
        data = None
        space = None

        if mimeData.hasUrls():
            formats = mimeData.formats()
            url = str(mimeData.urls()[0].toString())
            dt = DataEditorSelector.mime_type_handler(formats, applet=False)
            if not dt:
                return
            parsedUrl = urlparse.urlparse(url)
            data = dt.open_url(parsedUrl)
            if not data:
                return
#            self.__register_data(data)
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

        # first try to retreive the space associated to this data
        if proj and data:
            space = proj.get_data_property(data, "space")
        # if space is still none, we can always try to create a new space
        if space is None and data:
            if app:
                space = app(data)
                proj.set_data_property(data, "space", space)

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
        proj = self.__projMan.get_active_project()

        pos = self.__splittable.mapToGlobal(pos)
        menu = QtGui.QMenu(self.__splittable)
        menu.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        action = menu.addAction("Clear")
        action.triggered.connect(self.__make_clear_pane_handler(paneId))


        appletMenu   = menu.addMenu("Applet...")
        applets    = list(AppletFactoryManager().gather_items().itervalues())

        applets.sort(cmp = lambda x,y:cmp(x.name, y.name))
        for app in applets:
            action = appletMenu.addAction(app.icon, app.name)
            action.setIconVisibleInMenu(True)
            func = self.__make_new_applet_pane_handler(proj, paneId, app)
            action.triggered.connect(func)
        menu.popup(pos)

    def __make_clear_pane_handler(self, paneId):
        def on_clear_chosen(checked):
            self.__splittable.takeContentAt(paneId, None)
        func = on_clear_chosen
        return func

    def __make_new_applet_pane_handler(self, proj, paneId, applet):
        def f(checked):
            space = applet()
            self.__setSpaceAt(paneId, space)
        return f


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
        s.full_sticky_check()
        s.paneMenuRequest.connect(self.__onPaneMenuRequest)
        s.dragEnterEventTest.connect(self.__on_splitter_drag_enter)
        s.dropHandlerRequest.connect(self.__on_splitter_pane_drop)
        return s, taken

    def __setSpaceAt(self, paneId, space):
        self.__setContentAt(paneId, space)

    def __setContentAt(self, paneId, content):
        if self.__splittable:
            self.__splittable.setContentAt(paneId,
                                           content,
                                           noTearOffs=True, noToolButton=True)




