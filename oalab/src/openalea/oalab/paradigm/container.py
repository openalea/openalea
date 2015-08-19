# -*- python -*-
# -*- coding: utf8 -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2013 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#
#       File contributor(s): Guillaume Bâty <guillaume.baty@inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
__revision__ = ""

from openalea.core import logger
from openalea.core import settings
from openalea.core.model import Model
from openalea.core.path import path
from openalea.core.project import Project
from openalea.core.service.data import DataFactory, DataClass, DataType, MimeType
from openalea.core.service.plugin import debug_plugin, plugins
from openalea.oalab.project.dialog import SelectCategory
from openalea.oalab.service.applet import get_applet
from openalea.oalab.utils import ModalDialog
from openalea.oalab.utils import qicon
from openalea.oalab.widget import resources_rc  # do not remove this import else icon are not drawn
from openalea.oalab.widget.pages import WelcomePage
from openalea.vpltk.qt import QtCore, QtGui


class ParadigmContainer(QtGui.QTabWidget):

    """
    Widget to edit and run models.

    Contains paradigm applets (oalab.paradigm_applet)
    """
    identifier = "WidgetEditorContainer"
    name = "Editor Container"

    def __init__(self, parent=None):
        super(ParadigmContainer, self).__init__(parent=parent)

        self.setTabsClosable(True)

        self.applets = []
        self.welcome_actions = []

        self._open_tabs = {}
        self.paradigms = {}
        self._new_file_actions = {}
        self.paradigms_actions = []
        for plugin in plugins('oalab.plugin', criteria=dict(implement='IParadigmApplet')):
            paradigm_applet = debug_plugin('oalab.plugin', func=plugin)
            if paradigm_applet:
                self.paradigms[plugin.name] = paradigm_applet

        self._open_objects = {}

        self.connect(self, QtCore.SIGNAL('tabCloseRequested(int)'), self.auto_close)
        self.connect(self, QtCore.SIGNAL('currentChanged(int)'), self.safe_display_help)

        self.add_default_tab()
        self.fine_tune()

    def fine_tune(self):
        self.setDocumentMode(True)
        # self.setMinimumSize(100, 100)
        self.setAccessibleName("Container")
        self.setElideMode(QtCore.Qt.ElideLeft)

    def initialize(self):
        self.reset()

    def _on_text_changed(self, *args):
        tab = self.sender()
        idx = self.indexOf(tab)
        if idx >= 0:
            self._set_tab_red(idx)

    ###########################################################################
    # Convenience method
    ###########################################################################

    def applet(self, obj, dtype, mimetype=None):
        applet_class = None
        if dtype in self.paradigms:
            # Check in paradigm.default_name
            applet_class = self.paradigms[dtype]
        else:
            # Check in paradigm.extension
            for value in self.paradigms.values():
                if dtype == value.extension:
                    applet_class = value
        if applet_class is None:
            applet_class = self.paradigms["Textual"]

        return applet_class(data=obj).instantiate_widget()

    def data_name(self, obj):
        return obj.filename

    def _tab(self, tab):
        if tab is None:
            return self.currentWidget()
        if tab is None:
            return
        if tab not in self._open_tabs:
            return

    def data(self, tab=None):
        return self._open_tabs[self._tab(tab)]

    ###########################################################################
    # Open/Close data
    ###########################################################################

    def open(self):
        filepath = showOpenFileDialog()
        if filepath:
            filepath = path(filepath)
            obj = DataFactory(path=filepath)
            self.open_data(obj)

    def open_data(self, obj):
        # Check if object is yet open else create applet
        if obj in self._open_objects:
            tab = self._open_objects[obj]
            self.setCurrentWidget(tab)
        else:
            applet = self.applet(obj, obj.default_name)
            if hasattr(applet, 'textChanged'):
                applet.textChanged.connect(self._on_text_changed)

            self.remove_tab("Welcome")
            idx = self.addTab(applet, self.data_name(obj))
            if obj.path:
                self.setTabToolTip(idx, obj.path)
            self.setCurrentIndex(idx)
            self._open_objects[obj] = applet
            self._open_tabs[applet] = obj

    def close(self, tab=None):
        if tab is None:
            tab = self.currentWidget()
        idx = self.indexOf(tab)
        self.removeTab(idx)
        if tab in self._open_tabs:
            obj = self._open_tabs[tab]
            del self._open_objects[obj]
            del self._open_tabs[tab]
            tab.close()

        if self.count() == 0:
            self.add_default_tab()

    def close_current(self):
        self.close()

    def close_data(self, obj):
        if obj in self._open_objects:
            tab = self._open_objects[obj]
            self.close(tab)

    def auto_close(self, n_tab):
        self.close(self.widget(n_tab))

    def close_all(self):
        n = self.count()
        for i in range(n):
            self.close_current()

    ###########################################################################
    # Apply
    ###########################################################################

    def apply(self, tab=None):
        tab = self._tab(tab)
        try:
            applet = tab.applet
        except AttributeError:
            return

        applet.apply()

    def apply_all(self):
        """
        Save all opened files
        """
        n = self.count()
        for i in range(n):
            self.apply(tab=self.widget(i))

    ###########################################################################
    # Save
    ###########################################################################

    def save(self, tab=None):
        self.apply(tab)
        obj = self.data(tab)
        obj.save()
        self._set_tab_black(self.indexOf(tab))

    def save_current(self):
        self.save()

    def save_all(self):
        """
        Save all opened files
        """
        n = self.count()
        for i in range(n):
            self.save(tab=self.widget(i))

    ###########################################################################
    # Tab coloration
    ###########################################################################

    def _set_tab_red(self, index=None):
        if index is None:
            index = self.currentIndex()
        if index != -1:
            self.tabBar().setTabTextColor(index, QtCore.Qt.red)

    def _set_tab_black(self, index=None):
        if index is None:
            index = self.currentIndex()
        if index != -1:
            self.tabBar().setTabTextColor(index, QtCore.Qt.black)

    def set_all_tab_black(self):
        for index in range(self.count()):
            self._set_tab_black(index)

    ###########################################################################
    # Tab management
    ###########################################################################

    def remove_tab(self, tabname="Welcome"):
        """
        Remove the tab named "tabname"

        :param tabname: name of the tab to remove. Default: "Welcome"
        """
        for i in range(self.count()):
            if self.tabText(i) == tabname:
                self.removeTab(i)

    def reset(self):
        """
        Delete all tabs
        """
        self.close_all()

    def set_welcome_actions(self, actions=[]):
        self.welcome_actions = actions

    def add_welcome_tab(self, actions):
        self.remove_tab("Welcome")
        welcomePage = WelcomePage(actions=actions, parent=self.parent(), style=WelcomePage.STYLE_MEDIUM)
        self.addTab(welcomePage, "Welcome")

    def add_default_tab(self):
        self.add_welcome_tab(self.welcome_actions)

    def safe_display_help(self):
        """
        Call focus_change method on widget.applet safely (if it exists well).
        """
        widget = self.currentWidget()
        if widget is not None:
            if hasattr(widget, "display_help"):
                widget.display_help()

    ###########################################################################
    # Run models
    ###########################################################################

    def execute(self):
        self.currentWidget().applet.execute()
        logger.debug("Execute selected part " + self.currentWidget().applet.name)

    def run(self):
        self.currentWidget().applet.run()
        logger.debug("Run " + self.currentWidget().applet.name)

    def animate(self):
        self.currentWidget().applet.animate()
        logger.debug("Animate " + self.currentWidget().applet.name)

    def step(self):
        self.currentWidget().applet.step()
        logger.debug("Step " + self.currentWidget().applet.name)

    def stop(self):
        self.currentWidget().applet.stop()
        logger.debug("Stop " + self.currentWidget().applet.name)

    def init(self):
        self.currentWidget().applet.init()
        logger.debug("Init " + self.currentWidget().applet.name)


def showOpenFileDialog(extension=None, where=None, parent=None):
    if extension is None:
        extension = ""

    if where is not None:
        my_path = path(str(where)).abspath().splitpath()[0]
    else:
        my_path = path(settings.get_project_dir())
    logger.debug("Search to open file with extension " + extension + " from " + my_path)
    fname = QtGui.QFileDialog.getOpenFileName(parent, 'Select File to open',
                                              my_path, "All (*);;Scripts Files (%s)" % extension)
    return fname


class ModelEditorApplet(ParadigmContainer):

    def __init__(self, parent=None):
        ParadigmContainer.__init__(self, parent=parent)
        self._create_actions()
        self._create_connections()

    def _create_actions(self):
        # Create actions
        self.actionRun = QtGui.QAction(qicon("run.png"), "Run", self)
        self.actionAnimate = QtGui.QAction(qicon("play.png"), "Animate", self)
        self.actionStep = QtGui.QAction(qicon("step.png"), "Step", self)
        self.actionStop = QtGui.QAction(qicon("pause.png"), "Stop", self)
        self.actionInit = QtGui.QAction(qicon("rewind.png"), "Init", self)
        self.actionRunSelection = QtGui.QAction(qicon("run.png"), "Run subpart", self)

        self.actionSave = QtGui.QAction(qicon("save.png"), "Save File", self)
        self.actionCloseCurrent = QtGui.QAction(qicon("closeButton.png"), "Close current tab", self)

        # Add shortcuts
        self.actionRunSelection.setShortcut(self.tr("Ctrl+E"))
        self.actionCloseCurrent.setShortcut(self.tr("Ctrl+W"))
        self.actionRun.setShortcuts(["F1", "Ctrl+R"])
        #self.actionInit.setShortcut("F1")
        self.actionAnimate.setShortcut("F2")
        self.actionStep.setShortcut("F3")
        self.actionStop.setShortcut("F4")

        # Store actions
        self._run_actions = [
            self.actionAnimate,
            self.actionInit,
            self.actionRun,
            self.actionRunSelection,
            self.actionStep,
            self.actionStop,
        ]

        # File
        self.actionNewFile = QtGui.QAction(qicon("new.png"), "New file", self)
        self.actionOpenFile = QtGui.QAction(qicon("open.png"), "Open file", self)
        self.actionSaveAs = QtGui.QAction(qicon("save.png"), "Save As", self)

        # Text edit
        self.actionNewFile.setShortcut(self.tr("Ctrl+N"))
        self.actionOpenFile.setShortcut(self.tr("Ctrl+O"))
        self.actionSave.setShortcut(self.tr("Ctrl+S"))

        self._actions = [
            #["Project", "Manage", self.actionNewFile, 0],
            #["Project", "Manage", self.actionOpenFile, 1],

            ["Project", "Play", self.actionRun, 0],
            ["Project", "Play", self.actionAnimate, 0],
            ["Project", "Play", self.actionStep, 0],
            ["Project", "Play", self.actionStop, 0],
            ["Project", "Play", self.actionInit, 0],


        ]

    def _create_connections(self):
        self.currentChanged.connect(self.on_current_tab_changed)

        self.actionRun.triggered.connect(self.run)
        self.actionAnimate.triggered.connect(self.animate)
        self.actionStep.triggered.connect(self.step)
        self.actionStop.triggered.connect(self.stop)
        self.actionInit.triggered.connect(self.init)

        self.actionNewFile.triggered.connect(self.new_file)
        self.actionOpenFile.triggered.connect(self.open)
        self.actionSave.triggered.connect(self.save_current)
        self.actionCloseCurrent.triggered.connect(self.close_current)

        self.actionRunSelection.triggered.connect(self.execute)

    def actions(self):
        """
        :return: list of actions to set in the menu.
        """
        return self._actions

    def toolbar_actions(self):
        return self._actions

    def toolbars(self):

        tb_run = QtGui.QToolBar("Run")
        tb_run.addActions([
            self.actionRun,
            self.actionAnimate,
            self.actionStep,
            self.actionStop,
            self.actionInit,
        ])

        tb_edit = QtGui.QToolBar("Edit")
        tb_edit.addActions([
            self.actionSave,
            self.actionCloseCurrent,
        ])

        return [tb_run, tb_edit]

    def menu_actions(self):
        actions = []
        for menu in self.menus():
            actions += menu.actions()
        return actions

    def menus(self):

        menu_project = QtGui.QMenu("File", self)

        menu_project.addActions([
            self.actionNewFile,
            self.actionOpenFile,
            self.actionSave,
            self.actionCloseCurrent,
        ])

        menu_project.addSeparator()

        menu_project.addActions([
            self.actionRun,
            self.actionAnimate,
            self.actionStep,
            self.actionStop,
            self.actionInit,
        ])

        return [menu_project]

    def on_current_tab_changed(self):
        try:
            runnable = self.currentWidget().applet.runnable()
        except AttributeError:
            runnable = False
        self._set_run_mode(runnable)

    def _set_run_mode(self, mode=True):
        if mode:
            for action in self._run_actions:
                action.setEnabled(True)
        else:
            for action in self._run_actions:
                action.setEnabled(False)

ModelEditorApplet = ParadigmContainer
