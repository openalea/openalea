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
from openalea.vpltk.project import ProjectManager
from openalea.oalab.service.applet import get_applet
from openalea.oalab.project.projectwidget import SelectCategory
from openalea.oalab.gui.utils import ModalDialog

class TextData(object):
    default_name = "text"
    default_file_name = "text"
    pattern = ""
    extension = ""
    icon = ""

    def __init__(self, name="", code="", filepath="", category=None, *args, **kwargs):
        """
        :param name: name of the model (name of the file?)
        :param code: code of the model, can be a string or an other object
        :param filepath: path to save the model on disk
        """
        self.name = name
        self.filepath = filepath
        self.code = code
        self.category = category
        self.execute = self.step = self.animate = self.init = self.run
        self.ns = {}

    def __call__(self, *args, **kwargs):
        self.run(*args, **kwargs)

    def __eq__(self, other):
        return self.code == other.code and self.name == other.name and self.category == other.category

    def run(self, *args, **kargs):
        from openalea.oalab.service.ipython import get_interpreter
        interpreter = get_interpreter()
        return interpreter.runcode(self.code)


class DataContainer(dict):
    """
    Temporary waiting for real dataobject implementation in project
    """
    def __contains__(self, other):
        for obj in self:
            if obj == other:
                return True
        return False

    def __getitem__(self, key):
        try:
            return dict.__getitem__(self, key)
        except KeyError, e:
            for obj in self:
                if obj == key:
                    return dict.__getitem__(self, obj)
            raise e

class ParadigmContainer(QtGui.QTabWidget):
    """
    Contains paradigm applets (oalab.paradigm_applet)
    """
    identifier = "WidgetEditorContainer"
    name = "Editor Container"

    def __init__(self, session, controller, parent=None):
        super(ParadigmContainer, self).__init__(parent=parent)
        self.session = session
        self.controller = controller

        self.setTabsClosable(True)
        self.setMinimumSize(100, 100)

        self.applets = []
        self._open_tabs = {}
        self.paradigms = {}
        self._new_file_actions = {}
        self.paradigms_actions = []
        for applet in iter_plugins('oalab.paradigm_applet', debug=self.session.debug_plugins):
            self.paradigms[applet.name] = applet()()

        self._open_objects = DataContainer()

        self.projectManager = ProjectManager()

        self.setAccessibleName("Container")
        self.setElideMode(QtCore.Qt.ElideMiddle)

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

        self.actionOpenFile.setShortcut(
            QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))

        self.actionRunSelection.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+E", None, QtGui.QApplication.UnicodeUTF8))
        
        self.actionCloseCurrent.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+W", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSearch.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+F", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGoto.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+G", None, QtGui.QApplication.UnicodeUTF8))
        #self.actionSave.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        # self.actionRun.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+R", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRun.setShortcuts([QtGui.QApplication.translate("MainWindow", "F1", None, QtGui.QApplication.UnicodeUTF8),QtGui.QApplication.translate("MainWindow", "Ctrl+R", None, QtGui.QApplication.UnicodeUTF8)])
        self.actionAnimate.setShortcut(QtGui.QApplication.translate("MainWindow", "F2", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStep.setShortcut(QtGui.QApplication.translate("MainWindow", "F3", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStop.setShortcut(QtGui.QApplication.translate("MainWindow", "F4", None, QtGui.QApplication.UnicodeUTF8))
        self.actionInit.setShortcut(QtGui.QApplication.translate("MainWindow", "F5", None, QtGui.QApplication.UnicodeUTF8))

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

        self._actions = [["Project", "Manage", self.actionOpenFile, 1],
                         ["Project", "Manage", self.actionSave, 1],
                         ["Project", "Manage", self.actionAddFile, 1],
#                          ["Project", "Manage", self.actionSaveAs, 1],
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
                         ["Project", "Manage", self.actionCloseCurrent, 1],
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
        return applet_class(name=obj.name, code=obj.code, model=obj,
                            filepath=obj.filepath, editor_container=self, parent=None).instanciate_widget()

    def data(self, category, name):
        project = self.project()
        if category == 'model':
            obj = project.get(category, name)
            # GBY: dont understand why get can return list
            if isinstance(obj, list):
                obj = obj[0]
            dtype = obj.default_name
        else:
            code = project.get(category, name)
            dtype = None
            obj = TextData(name, code, filepath=project.path / category / name)
        obj.category = category
        return obj, dtype

    def data_name(self, obj):
        if obj.category in ('model', 'external'):
            name = obj.name
        else:
            name = '%s/%s' % (obj.category, obj.name)
        return name

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
            name = '.../%s/%s' % (filepath.parent.name, filepath.name)
            f = open(filepath, 'r')
            code = f.read()
            f.close()
            obj = TextData(name, code, filepath, category='external')
            self.open_data(obj, dtype=None)

    def open_project_data(self, category=None, name=None):
        project = self.project()
        if project:
            obj, dtype = self.data(category, name)
            self.open_data(obj, dtype)

    def open_data(self, obj, dtype=None):
        # Check if object is yet open else create applet
        if obj in self._open_objects:
            tab = self._open_objects[obj]
            self.setCurrentWidget(tab)
        else:
            applet = self.applet(obj, dtype)

            idx = self.addTab(applet, self.data_name(obj))
            if obj.filepath:
                self.setTabToolTip(idx, obj.filepath)
            self.setCurrentIndex(idx)
            self._open_objects[obj] = applet
            self._open_tabs[applet] = obj

    def close_current(self):
        self.close()

    def close_project_data(self, category=None, name=None):
        obj, dtype = self.data(category, name)
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

        project = self.project()
        obj = self._open_tabs[tab]
        category = obj.category
        code = tab.get_code()

        if category == 'external':
            f = open(obj.filepath, "w")
            code = str(code).encode("utf8", "ignore")
            f.write(code)
            f.close()
        elif category == 'model':
            obj.code = code
            project.save()
        elif category in ('startup', 'doc', 'lib'):
            getattr(project, category)[obj.filepath.name] = code
            project.save()

    def new_file(self):
        try:
            dtype = self._new_file_actions[self.sender()]
        except KeyError:
            return
        category = 'model'
        name = '%s_%s' % (dtype, category)
        category, name = self.add(self.project(), name, code='', dtype=dtype, category=category)
        if name:
            self.open_project_data(category, name)

    def add(self, project, name, code, dtype=None, category=None):
        models = {}
        if category is None:
            categories = ['model', 'startup', 'doc', 'lib']
        else:
            categories = [category]

        if dtype:
            dtypes = [dtype]
        else:
            dtypes = None
        selector = SelectCategory(filename=name, categories=categories, dtypes=dtypes)
        dialog = ModalDialog(selector)
        if dialog.exec_():
            category = selector.category()
            filename = selector.name()
            dtype = selector.dtype()
            ret = project.add(category=category, name=filename, value=code, dtype=dtype)
            if ret:
                return category, filename
        return None, None

    def add_current_file(self):
        project = self.project()
        if project is None:
            return
        obj = self.current_data()
        if obj is None:
            return

        if obj.category == 'external':
            name = obj.filepath.name
            category = None
            dtype = None
        else:
            name = obj.name
            category = obj.category
            dtype = obj.default_name

        category, name = self.add(project, name, obj.code, dtype=dtype, category=category)
        if name:
            self.close_current()
            self.open_project_data(category, name)

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
