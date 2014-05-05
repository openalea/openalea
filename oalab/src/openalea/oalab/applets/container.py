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
from openalea.vpltk.plugin import discover, Plugin
from openalea.core import logger
from openalea.oalab.gui.pages import WelcomePage, CreateFilePage
from openalea.core import settings
from openalea.core.path import path
from openalea.oalab.gui import resources_rc # do not remove this import else icon are not drawn

class AppletContainer(QtGui.QTabWidget):
    """
    Contains applets.
    Each tab is an applet.
    """
    identifier = "WidgetEditorContainer"
    name = "Editor Container"    
    
    def __init__(self, session, controller, parent=None):
        super(AppletContainer, self).__init__(parent=parent)
        self.session = session
        self.controller = controller
        self.setTabsClosable(True)
        self.setMinimumSize(100, 100)
        self.applets = list()
        
        self.paradigms = dict()
        self.paradigms_actions = []
        applets = discover('oalab.paradigm_applet')
        for app in applets.values():
            applet = Plugin(app)
            applet = applet.load()
            self.paradigms[applet.default_name] = applet

        self.setAccessibleName("Container")

        self.actionOpenFile = QtGui.QAction(QtGui.QIcon(":/images/resources/open.png"), "Open file", self)

        self.actionSave = QtGui.QAction(QtGui.QIcon(":/images/resources/save.png"),"Save File", self)
        self.actionRun = QtGui.QAction(QtGui.QIcon(":/images/resources/run.png"),"Run", self)
        self.actionAnimate = QtGui.QAction(QtGui.QIcon(":/images/resources/play.png"),"Animate", self)
        self.actionStep = QtGui.QAction(QtGui.QIcon(":/images/resources/step.png"),"Step", self)
        self.actionStop = QtGui.QAction(QtGui.QIcon(":/images/resources/pause.png"),"Stop", self)
        self.actionInit = QtGui.QAction(QtGui.QIcon(":/images/resources/rewind.png"),"Init", self)
        
        self.actionRunSelection = QtGui.QAction(QtGui.QIcon(":/images/resources/run.png"),"Run subpart", self)
        
        self.actionUndo = QtGui.QAction(QtGui.QIcon(":/images/resources/editundo.png"),"Undo", self)
        self.actionRedo = QtGui.QAction(QtGui.QIcon(":/images/resources/editredo.png"),"Redo", self)
        self.actionSearch = QtGui.QAction(QtGui.QIcon(":/images/resources/editfind.png"),"Search", self)
        
        self.actionComment = QtGui.QAction(QtGui.QIcon(":/images/resources/commentOn.png"),"Comment",self)
        self.actionUnComment = QtGui.QAction(QtGui.QIcon(":/images/resources/commentOff.png"),"Uncomment",self) 
        self.actionGoto = QtGui.QAction(QtGui.QIcon(":/images/resources/next-green.png"),"Go To",self)

        self.actionOpenFile.setShortcut(
            QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
       
        self.actionComment.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+W", None, QtGui.QApplication.UnicodeUTF8)) 
        self.actionUnComment.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+J", None, QtGui.QApplication.UnicodeUTF8))
        
        self.actionRunSelection.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+R", None, QtGui.QApplication.UnicodeUTF8))

        self.actionSearch.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+F", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGoto.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+G", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRun.setShortcut(QtGui.QApplication.translate("MainWindow", "F1", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAnimate.setShortcut(QtGui.QApplication.translate("MainWindow", "F2", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStep.setShortcut(QtGui.QApplication.translate("MainWindow", "F3", None, QtGui.QApplication.UnicodeUTF8))
        self.actionStop.setShortcut(QtGui.QApplication.translate("MainWindow", "F4", None, QtGui.QApplication.UnicodeUTF8))
        self.actionInit.setShortcut(QtGui.QApplication.translate("MainWindow", "F5", None, QtGui.QApplication.UnicodeUTF8))

        QtCore.QObject.connect(self.actionOpenFile, QtCore.SIGNAL('triggered(bool)'),self.open_file)

        QtCore.QObject.connect(self.actionSave, QtCore.SIGNAL('triggered(bool)'),self.save)
        QtCore.QObject.connect(self.actionRun, QtCore.SIGNAL('triggered(bool)'),self.run)
        QtCore.QObject.connect(self.actionAnimate, QtCore.SIGNAL('triggered(bool)'),self.animate)
        QtCore.QObject.connect(self.actionStep, QtCore.SIGNAL('triggered(bool)'),self.step)
        QtCore.QObject.connect(self.actionStop, QtCore.SIGNAL('triggered(bool)'),self.stop)
        QtCore.QObject.connect(self.actionInit, QtCore.SIGNAL('triggered(bool)'),self.reinit)
        
        QtCore.QObject.connect(self.actionRunSelection, QtCore.SIGNAL('triggered(bool)'),self.run_selected_part)
        
        QtCore.QObject.connect(self.actionUndo, QtCore.SIGNAL('triggered(bool)'),self.undo)
        QtCore.QObject.connect(self.actionRedo, QtCore.SIGNAL('triggered(bool)'),self.redo)
        QtCore.QObject.connect(self.actionSearch, QtCore.SIGNAL('triggered(bool)'),self.search)
        QtCore.QObject.connect(self.actionGoto, QtCore.SIGNAL('triggered(bool)'),self.goto)
        QtCore.QObject.connect(self.actionComment, QtCore.SIGNAL('triggered(bool)'),self.comment)
        QtCore.QObject.connect(self.actionUnComment, QtCore.SIGNAL('triggered(bool)'),self.uncomment)
        
        self.actionStop.setEnabled(False)
        
        self._actions = [["File", "Manage", self.actionOpenFile, 0],
                         ["File", "Manage",self.actionSave,0],
                         ["Simulation", "Play",self.actionRun,0],
                         ["Simulation", "Play",self.actionAnimate,0],
                         ["Simulation", "Play",self.actionStep,0],
                         ["Simulation", "Play",self.actionStop,0],
                         ["Simulation", "Play",self.actionInit,0],
                         ["Edit", "Text Edit",self.actionUndo,1],
                         ["Edit", "Text Edit",self.actionRedo,1],
                         ["Edit", "Text Edit",self.actionSearch,1],
                         ["Edit", "Text Edit",self.actionGoto,1],
                         ["Edit", "Text Edit",self.actionComment,1],
                         ["Edit", "Text Edit",self.actionUnComment,1],
                         ["Edit", "Text Edit",self.actionRunSelection,0]]
                                    
        QtCore.QObject.connect(self, QtCore.SIGNAL('tabCloseRequested(int)'), self.autoClose)

        self.extensions = ""
        self.connect_paradigm_container()

        self.reset()

    def open_file(self, filename=None, extension=None):
        """
        Open a file.

        If not filename, open a widget to select it.

        If not extension, extension is the list of all available (*.py, *.r, *.lpy, *.wpy)
        """
        if extension is None:
            extension = self.extensions

        if not filename:
            if extension:
                filename = showOpenFileDialog(extension)
            else:
                filename = showOpenFileDialog()

        if filename:
            filename = path(filename).abspath()

            f = open(filename, "r")
            txt = f.read()
            f.close()

            ## here we use tabname to know where to save the file...
            ## TODO use a more complete "file" object which store the code and the filename and use a short tabname
            #tab_name = str(path(filename).splitpath()[-1])
            tab_name = str(path(filename))
            ext = str(path(filename).splitext()[-1])
            ext = ext.split(".")[-1]
            logger.debug("Try to open file named " + tab_name + " . With applet_type " + ext)

            try:
                self.newTab(applet_type=ext, tab_name=tab_name, script=txt)
                # project.add("src", filename, txt)
                logger.debug("Open file named " + tab_name)
            except:
                print "File extension " + ext + " not recognised"
                logger.warning("Can't import file named %s in current project. Unknow extension." % filename)

    def new_file(self, applet_type=None, tab_name=None, script=""):
        """
        Create a new model of type 'applet_type

        :param applet_type: type of applet to add. Can be Workflow, LSystem, Python, R
        """
        if not applet_type:
            button = self.sender()
            applet_type = button.text() # can be Workflow, LSystem, Python, R
            applet_type = applet_type[4:]
            # TODO: this approach is not reliable. If a developer change action name, it breaks the system
            # a better approach should be to define a "newModel" method in IApplet and call it directly
            # for instance in __init__ : action.triggered.connect(applet.newModel)
        Applet = self.paradigms.get(applet_type)
        if not tab_name and Applet:
            tab_name = Applet.default_file_name
        self.newTab(applet_type=applet_type, tab_name=tab_name, script=script)

        ## TODO: how to add a file to a project???
        """
        if self.session.project:
            text = self.applets[-1].widget().get_text()
            self.session.project.add("src", tab_name, text)
            self.controller.update_namespace()
            self._project_changed()"""

    def connect_paradigm_container(self):
        # Connect actions from self.paradigms to menu (newPython, newLpy,...)
        for applet in self.paradigms.values():
            action = QtGui.QAction(QtGui.QIcon(applet.icon), "New " + applet.default_name, self)
            action.triggered.connect(self.new_file)
            self.paradigms_actions.append(action)
            self._actions.append(["File", "Manage", action, 0],)
            self.extensions = self.extensions + applet.pattern + " "

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

        # welcomePage = ProjectSelectorScroll(self.session.project_manager.projects, open_project=self.controller.project_manager.openProject)
        welcomePage = WelcomePage(session = self.session, controller=self.controller, parent=self.parent())
        self.addTab(welcomePage, "Welcome")
        
    def addCreateFileTab(self):
        """
        Display a tab to select type of file that you can create
        """
        page = CreateFilePage(session = self.session, controller=self.controller, parent=self.parent())
        self.addTab(page, "Create File")
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
    
    def openTab(self, applet_type, tab_name, script):
        """
        Open a tab with the widget 'applet_type'
        """
        self.newTab(applet_type=applet_type, tab_name=tab_name, script=script)
            
    def newTab(self, applet_type, tab_name="", script=""):
        """
        Open a tab with the widget 'applet_type'
        
        # TODO : automatize with plugin system
        """
        logger.debug("New tab. Type: " + str(applet_type) + ". Name: " + str(tab_name))
        self.rmTab("Welcome")
        self.rmTab("Create File")
        
        # TODO : permit to add more than one script...
        # existing_tabs = list()
        # for name in self.session.project.src:
        #    existing_tabs.append(name)
        # tab_name = check_if_name_is_unique(tab_name, existing_tabs)

        Applet = None
        
        if self.paradigms.has_key(applet_type):
            # Check in paradigm.default_name
            Applet = self.paradigms[applet_type]
        else:
            # Check in paradigm.extension
            for value in self.paradigms.values():
                if value.extension == applet_type:
                    Applet = value

        if Applet is None:
            if "Python" in self.paradigms.keys():
                Applet = self.paradigms["Python"]

        icon = ""
        if Applet is not None:            
            appl = Applet(session=self.session, controller=self.controller, parent=self.parent(), name=tab_name, script=script)
            self.applets.append(appl)
            icon = Applet.icon
            
            try:
                self.addTab(self.applets[-1].widget(), QtGui.QIcon(icon), tab_name)
                self.setCurrentWidget(self.applets[-1].widget())
                self.applets[-1].widget().name = tab_name

                self.connect_actions()
                QtCore.QObject.connect(self, QtCore.SIGNAL('currentChanged(int)'),self.focusChange)
                self.setTabBlack()
            except IndexError:
                pass

    def connect_actions(self):
        widget = self.applets[-1].widget()
        menu = self.controller.menu
        if widget.actions():
            for action in widget.actions():
                # Add actions in PanedMenu
                menu.addBtnByAction(*action)
        
    def focusChange(self):
        widget = self.currentWidget()
        if widget:
            if hasattr(widget, "applet"):
                widget.applet.focus_change()
        
    def closeTab(self):
        """
        Close current tab
        """       
        self.removeTab(self.currentIndex())
        if self.count() == 0:
            if self.session.current_is_project():
                self.addCreateFileTab()
            else:
                self.addDefaultTab()
        logger.debug("Close tab")
        
    def autoClose(self, n_tab):
        self.setCurrentIndex(n_tab)
        self.closeTab()   
        
    def closeAll(self):
        n = self.count()
        for i in range(n):
            self.closeTab()
        
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
        return "Simulation"     
    
    def save(self,name=None):
        """
        Save current script
        """ 
        if name in (False, None):
            name = self.tabText(self.currentIndex())
        logger.debug("Save model " + str(name))
        self.currentWidget().save(name=name)
    
    def save_all(self):
        """
        Save all opened src
        """
        logger.debug("Save all models")
        n = self.count()
        for i in range(n):
            wid = self.widget(i)
            name = wid.applet.name
            wid.save(name=name)
            try:
                name = self.widget(i).editor.name
            except:
                name = self.widget(i).name
            logger.debug("%s saved."%name)
            self.setTabText(i, name)
                
    def run_selected_part(self):
        if self.controller.project_manager:
            self.controller.project_manager.update_from_widgets()
        try:
            self.currentWidget().applet.run_selected_part()
            logger.debug("Run selected part " + self.currentWidget().applet.name)
        except:
            logger.debug("Can't run selected part " + self.currentWidget().applet.name)
        
    def run(self):
        if self.controller.project_manager:
            self.controller.project_manager.update_from_widgets()
        self.currentWidget().applet.run()
        logger.debug("Run " + self.currentWidget().applet.name)
        
    def animate(self):
        if self.controller.project_manager:
            self.controller.project_manager.update_from_widgets()
        self.currentWidget().applet.animate()
        logger.debug("Animate " + self.currentWidget().applet.name)
        
    def step(self):
        if self.controller.project_manager:
            self.controller.project_manager.update_from_widgets()
        self.currentWidget().applet.step()
        logger.debug("Step " + self.currentWidget().applet.name)
        
    def stop(self):
        if self.controller.project_manager:
            self.controller.project_manager.update_from_widgets()
        self.currentWidget().applet.stop()
        logger.debug("Stop " + self.currentWidget().applet.name)
        
    def reinit(self):
        if self.controller.project_manager:
            self.controller.project_manager.update_from_widgets()
        self.currentWidget().applet.reinit()
        logger.debug("Reinit " + self.currentWidget().applet.name)

    def undo(self):
        try:
            self.currentWidget().undo()
            logger.debug("Undo " + self.currentWidget().applet.name)
        except:
            logger.warning("Can't use method Undo in " + self.currentWidget().applet.name)
        
    def redo(self):
        try:
            self.currentWidget().redo()
            logger.debug("Redo " + self.currentWidget().applet.name)
        except:
            logger.warning("Can't use method Redo in " + self.currentWidget().applet.name)
        
    def search(self):
        try:        
            self.currentWidget().search()
            logger.debug("Search " + self.currentWidget().applet.name)
        except:
            logger.warning("Can't use method search in " + self.currentWidget().applet.name)
        
    def comment(self):
        try:
            self.currentWidget().comment()
            logger.debug("comment " + self.currentWidget().applet.name)
        except:
            logger.warning("Can't use method comment in " + self.currentWidget().applet.name)

    def uncomment(self):
        try:
            self.currentWidget().uncomment()
            logger.debug("uncomment " + self.currentWidget().applet.name)
        except:
            logger.warning("Can't use method uncomment in " + self.currentWidget().applet.name)
        
    def goto(self):
        try:
            self.currentWidget().goto()
            logger.debug("Goto " + self.currentWidget().applet.name)
        except:
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