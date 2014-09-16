 # -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2013 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
__revision__ = ""

from openalea.vpltk.qt import QtCore, QtGui
from openalea.vpltk.plugin import iter_plugins
from openalea.core import logger
from openalea.oalab.gui.pages import WelcomePage2 as WelcomePage
from openalea.core import settings
from openalea.core.path import path
from openalea.oalab.gui import resources_rc # do not remove this import else icon are not drawn
from openalea.oalab.gui.utils import qicon
from openalea.vpltk.project import ProjectManager, Project
from openalea.oalab.project.projectwidget import SelectCategory
from openalea.oalab.gui.utils import ModalDialog
from openalea.vpltk.model import Model

from openalea.oalab.service.applet import get_applet
from openalea.oalab.service.data import DataFactory, DataClass, DataType, MimeType

from openalea.oalab.session.session import Session

class ParadigmContainer(QtGui.QTabWidget):
    """
    Contains paradigm applets (oalab.paradigm_applet)
    """
    identifier = "WidgetEditorContainer"
    name = "Editor Container"

    def __init__(self, controller, session, parent=None):
        super(ParadigmContainer, self).__init__(parent=parent)
        self.session = Session()
#         self.controller = controller

        self.setTabsClosable(True)
        self.setMinimumSize(100, 100)

        self.applets = []
        self._open_tabs = {}
        self.paradigms = {}
        self._new_file_actions = {}
        self.paradigms_actions = []
        for applet in iter_plugins('oalab.paradigm_applet', debug=self.session.debug_plugins):
            self.paradigms[applet.name] = applet()()

        self._open_objects = {}

        self.projectManager = ProjectManager()

        self.setAccessibleName("Container")
        self.setElideMode(QtCore.Qt.ElideMiddle)

        self.actionNewFile = QtGui.QAction(qicon("new.png"), "New file", self)
        self.actionOpenFile = QtGui.QAction(qicon("open.png"), "Open file", self)
        self.actionSave = QtGui.QAction(qicon("save.png"), "Save File", self)
        self.actionSaveAs = QtGui.QAction(qicon("save.png"), "Save As", self)
        self.actionRun = QtGui.QAction(qicon("run.png"), "Run", self)
        self.actionAnimate = QtGui.QAction(qicon("play.png"), "Animate", self)
        self.actionStep = QtGui.QAction(qicon("step.png"), "Step", self)
        self.actionStop = QtGui.QAction(qicon("pause.png"), "Stop", self)
        self.actionInit = QtGui.QAction(qicon("rewind.png"), "Init", self)
        self.actionCloseCurrent = QtGui.QAction(qicon("closeButton.png"), "Close current tab", self)

        self.actionRunSelection = QtGui.QAction(qicon("run.png"), "Run subpart", self)

        self.actionUndo = QtGui.QAction(qicon("editundo.png"), "Undo", self)
        self.actionRedo = QtGui.QAction(qicon("editredo.png"), "Redo", self)
        self.actionSearch = QtGui.QAction(qicon("editfind.png"), "Search", self)

        self.actionComment = QtGui.QAction(qicon("commentOn.png"), "Comment", self)
        self.actionUnComment = QtGui.QAction(qicon("commentOff.png"), "Uncomment", self)
        self.actionGoto = QtGui.QAction(qicon("next-green.png"), "Go To", self)

        self.actionNewFile.setShortcut(self.tr("Ctrl+N"))
        self.actionOpenFile.setShortcut(
            QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))

        self.actionRunSelection.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+E", None, QtGui.QApplication.UnicodeUTF8))

        self.actionCloseCurrent.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+W", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSearch.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+F", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGoto.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+G", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        # self.actionRun.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+R", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRun.setShortcuts([QtGui.QApplication.translate("MainWindow", "F1", None, QtGui.QApplication.UnicodeUTF8),QtGui.QApplication.translate("MainWindow", "Ctrl+R", None, QtGui.QApplication.UnicodeUTF8)])
        self.actionAnimate.setShortcut(QtGui.QApplication.translate("MainWindow", "F2", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStep.setShortcut(QtGui.QApplication.translate("MainWindow", "F3", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStop.setShortcut(QtGui.QApplication.translate("MainWindow", "F4", None, QtGui.QApplication.UnicodeUTF8))
        self.actionInit.setShortcut(QtGui.QApplication.translate("MainWindow", "F5", None, QtGui.QApplication.UnicodeUTF8))


        self.actionNewFile.triggered.connect(self.new_file)
        self.actionOpenFile.triggered.connect(self.open)
        self.actionSave.triggered.connect(self.save_current)
#         self.actionSaveAs.triggered.connect(self.save_as)
        self.actionRun.triggered.connect(self.run)
        self.actionAnimate.triggered.connect(self.animate)
        self.actionStep.triggered.connect(self.step)
        self.actionStop.triggered.connect(self.stop)
        self.actionInit.triggered.connect(self.init)
        self.actionCloseCurrent.triggered.connect(self.close_current)

        self.actionRunSelection.triggered.connect(self.execute)

        self.actionUndo.triggered.connect(self.undo)
        self.actionRedo.triggered.connect(self.redo)
        self.actionSearch.triggered.connect(self.search)
        self.actionGoto.triggered.connect(self.goto)
        self.actionComment.triggered.connect(self.comment)
        self.actionUnComment.triggered.connect(self.uncomment)

        self.actionAddFile = QtGui.QAction(qicon("bool.png"), "Add to Project", self)
        self.actionAddFile.triggered.connect(self.add_current_file)

        self.actionStop.setEnabled(False)

        self._actions = [
                         ["Project", "Manage", self.actionNewFile, 0],
                         ["Project", "Manage", self.actionAddFile, 1],
                         ["Project", "Manage", self.actionOpenFile, 1],
                         ["Project", "Manage", self.actionSave, 1],
                         ["Project", "Manage", self.actionCloseCurrent, 1],

                         ["Project", "Play", self.actionRun, 0],
                         ["Project", "Play", self.actionAnimate, 0],
                         ["Project", "Play", self.actionStep, 0],
                         ["Project", "Play", self.actionStop, 0],
                         ["Project", "Play", self.actionInit, 0],

                         ["Edit", "Text Edit", self.actionUndo, 0],
                         ["Edit", "Text Edit", self.actionRedo, 0],
                         ["Edit", "Text Edit", self.actionSearch, 0],
                         ["Edit", "Text Edit", self.actionGoto, 0],
                         ["Edit", "Text Edit", self.actionComment, 0],
                         ["Edit", "Text Edit", self.actionUnComment, 0],
                         ["Edit", "Text Edit", self.actionRunSelection, 0],
                         ]
        self.connect_paradigm_container()
        self.extensions = ""
        self.connect(self, QtCore.SIGNAL('tabCloseRequested(int)'), self.autoClose)
        self.connect(self, QtCore.SIGNAL('currentChanged(int)'), self.safe_display_help)

    def connect_paradigm_container(self):
        # Connect actions from self.paradigms to menu (newPython, newLpy,...)
        for applet in self.paradigms.values():
            action = QtGui.QAction(QtGui.QIcon(applet.icon), "New " + applet.default_name, self)
            action.triggered.connect(self.new_file)
            self.paradigms_actions.append(action)
            self._new_file_actions[action] = applet.default_name
            self._actions.append(["Project", "Manage", action, 1],)

    def initialize(self):
        self.reset()

    def project(self):
        return self.projectManager.cproject

    def applet(self, obj, dtype):
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
            applet_class = self.paradigms["Python"]

        # TODO: case Python paradigm does not exists
        return applet_class(name=obj.filename, code=obj.read(), model=obj,
                            filepath=obj.path, editor_container=self, parent=None).instanciate_widget()

    def data_name(self, obj):
        return obj.filename

    def current_data(self):
        tab = self.currentWidget()
        if tab:
            return self._open_tabs[tab]
        else:
            return None

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

            idx = self.addTab(applet, self.data_name(obj))
            if obj.path:
                self.setTabToolTip(idx, obj.path)
            self.setCurrentIndex(idx)
            self._open_objects[obj] = applet
            self._open_tabs[applet] = obj

    def close_current(self):
        self.close()

    def close_data(self, obj):
        if obj in self._open_objects:
            tab = self._open_objects[obj]
            self.close(tab)

    def close(self, tab=None):
        if tab is None:
            tab = self.currentWidget()
        idx = self.indexOf(tab)
        self.removeTab(idx)
        if tab in self._open_tabs:
            obj = self._open_tabs[tab]
            del self._open_objects[obj]
            del self._open_tabs[tab]

        if self.count() == 0:
            if self.project():
                self.addCreateFileTab()
            else:
                self.addDefaultTab()

    def save_current(self):
        self.save()

    def save(self, tab=None):
        if tab is None:
            tab = self.currentWidget()
        if tab is None:
            return
        if tab not in self._open_tabs:
            return

        obj = self._open_tabs[tab]
        code = tab.get_code()
        if isinstance(obj, Model):
            obj.content = code
            obj.save()
        else:
            f = open(obj.path, "w")
            code = str(code).encode("utf8", "ignore")
            f.write(code)
            f.close()
        self.setTabBlack(self.indexOf(tab))

    def new_file(self):
        category = 'model'
        try:
            dtype = self._new_file_actions[self.sender()]
            name = '%s_%s.%s' % (dtype, category, DataClass(MimeType(name=dtype)).extension)
        except KeyError:
            dtype = None
            name = 'new_file.ext'

        category, data = self.add(self.project(), name, code='', dtype=dtype, category=category)
        if data:
            self.open_data(data)

    def add(self, project, name, code, dtype=None, category=None):
        if dtype is None:
            dtypes = [ModelClass.default_name for ModelClass in iter_plugins('oalab.model')]
        else:
            dtypes = [dtype]

        if category:
            categories=[category]
        else:
            categories=Project.category_keys
        selector = SelectCategory(filename=name, categories=categories, dtypes=dtypes)
        dialog = ModalDialog(selector)
        if dialog.exec_():
            category = selector.category()
            filename = selector.name()
            dtype = selector.dtype()
            path = project.path / category / filename
            if path.exists():
                box = QtGui.QMessageBox.information(self, 'Data yet exists',
                    'Data with name %s already exists in this project, just add it' % filename)
                code = None
            data = project.add(category=category, filename=filename, content=code, dtype=dtype)
            if data:
                return category, data
        return None, None

    def add_current_file(self):
        project = self.project()
        if project is None:
            return
        obj = self.current_data()
        if obj is None:
            return

        dtype = DataType(mimetype=obj.mimetype)
        self.add(project, obj.filename, obj.read(), dtype=dtype)

    def setTabRed(self, index=None):
        if index is None:
            index = self.currentIndex()
        if index != -1:
            self.tabBar().setTabTextColor(index, QtCore.Qt.red)

    def setTabBlack(self, index=None):
        if index is None:
            index = self.currentIndex()
        if index != -1:
            self.tabBar().setTabTextColor(index, QtCore.Qt.black)

    def setAllTabBlack(self):
        for index in range(self.count()):
            self.setTabBlack(index)

    def addDefaultTab(self):
        """
        Display a welcome tab if nothing is opened
        """
        pm = get_applet(identifier='ProjectManager')
        if pm :
            actions = [pm.actionNewProj, pm.actionOpenProj]
            welcomePage = WelcomePage(actions=actions, parent=self.parent())
            self.addTab(welcomePage, "Welcome")

    def addCreateFileTab(self):
        """
        Display a tab to select type of file that you can create
        """
        if self.paradigms_actions:
            page = WelcomePage(actions=self.paradigms_actions)
            self.addTab(page, "Create File")
        else:
            self.addDefaultTab()
        self.rmTab("Welcome")

    def rmTab(self, tabname="Welcome"):
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
        self.closeAll()

    def connect_actions(self):
        widget = self.applets[-1].widget()
        menu = self.controller.menu
        if widget:
            if widget.actions():
                for action in widget.actions():
                    # Add actions in PanedMenu
                    menu.addBtnByAction(*action)

    def safe_display_help(self):
        """
        Call focus_change method on widget.applet safely (if it exists well).
        """
        widget = self.currentWidget()
        if widget is not None:
            if hasattr(widget, "display_help"):
                widget.display_help()

    def autoClose(self, n_tab):
        self.close(self.widget(n_tab))

    def closeAll(self):
        n = self.count()
        for i in range(n):
            self.close_current()

    def actions(self):
        """
        :return: list of actions to set in the menu.
        """
        return self._actions

    def mainMenu(self):
        """
        :return: Name of menu tab to automatically set current when current widget
        begin current.
        """
        return "Project"

    def save_all(self):
        """
        Save all opened files
        """
        n = self.count()
        for i in range(n):
            self.setCurrentIndex(i)
            self.save()

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

    def undo(self):
        if hasattr(self.currentWidget(), "undo"):
            self.currentWidget().undo()
            logger.debug("Undo " + self.currentWidget().applet.name)
        else:
            logger.warning("Can't use method Undo in " + self.currentWidget().applet.name)

    def redo(self):
        if hasattr(self.currentWidget(), "redo"):
            self.currentWidget().redo()
            logger.debug("Redo " + self.currentWidget().applet.name)
        else:
            logger.warning("Can't use method Redo in " + self.currentWidget().applet.name)

    def search(self):
        if hasattr(self.currentWidget(), "search"):
            self.currentWidget().search()
            logger.debug("Search " + self.currentWidget().applet.name)
        else:
            logger.warning("Can't use method search in " + self.currentWidget().applet.name)

    def comment(self):
        if hasattr(self.currentWidget(), "comment"):
            self.currentWidget().comment()
            logger.debug("comment " + self.currentWidget().applet.name)
        else:
            logger.warning("Can't use method comment in " + self.currentWidget().applet.name)

    def uncomment(self):
        if hasattr(self.currentWidget(), "uncomment"):
            self.currentWidget().uncomment()
            logger.debug("uncomment " + self.currentWidget().applet.name)
        else:
            logger.warning("Can't use method uncomment in " + self.currentWidget().applet.name)

    def goto(self):
        if hasattr(self.currentWidget(), "goto"):
            self.currentWidget().goto()
            logger.debug("Goto " + self.currentWidget().applet.name)
        else:
            logger.warning("Can't use method Goto in " + self.currentWidget().applet.name)

    def _on_text_changed(self, *args):
        tab = self.sender()
        idx = self.indexOf(tab)
        if idx >= 0:
            self.setTabRed(idx)


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
