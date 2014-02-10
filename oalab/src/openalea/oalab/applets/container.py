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
from openalea.vpltk.qt.compat import from_qvariant, to_qvariant
from openalea.oalab.applets.lpy import LPyApplet
from openalea.oalab.applets.python import PythonApplet
from openalea.oalab.applets.r import RApplet
from openalea.oalab.applets.visualea import VisualeaApplet
from openalea.core import logger
from openalea.core.path import path
from openalea.vpltk.project.script import Scripts

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
        self.paradigms[PythonApplet.default_name] = PythonApplet
        self.paradigms[LPyApplet.default_name] = LPyApplet
        self.paradigms[VisualeaApplet.default_name] = VisualeaApplet
        self.paradigms[RApplet.default_name] = RApplet
        
        
        
        self.setAccessibleName("Container")
        
        self.actionSave = QtGui.QAction(QtGui.QIcon(":/images/resources/save.png"),"Save", self)
        self.actionRun = QtGui.QAction(QtGui.QIcon(":/lpy_images/resources/lpy/run.png"),"Run", self)
        self.actionAnimate = QtGui.QAction(QtGui.QIcon(":/lpy_images/resources/lpy/play.png"),"Animate", self)
        self.actionStep = QtGui.QAction(QtGui.QIcon(":/lpy_images/resources/lpy/step.png"),"Step", self)
        self.actionStop = QtGui.QAction(QtGui.QIcon(":/lpy_images/resources/lpy/pause.png"),"Stop", self)
        self.actionInit = QtGui.QAction(QtGui.QIcon(":/lpy_images/resources/lpy/rewind.png"),"Init", self)
        
        self.actionRunSelection = QtGui.QAction(QtGui.QIcon(":/lpy_images/resources/lpy/run.png"),"Run subpart", self)
        
        self.actionUndo = QtGui.QAction(QtGui.QIcon(":/lpy_images/resources/lpy/editundo.png"),"Undo", self)
        self.actionRedo = QtGui.QAction(QtGui.QIcon(":/lpy_images/resources/lpy/editredo.png"),"Redo", self)
        self.actionSearch = QtGui.QAction(QtGui.QIcon(":/lpy_images/resources/lpy/editfind.png"),"Search", self)
        
        self.actionComment = QtGui.QAction(QtGui.QIcon(":/images/resources/commentOn.png"),"Comment",self)
        self.actionUnComment = QtGui.QAction(QtGui.QIcon(":/images/resources/commentOff.png"),"Uncomment",self) 
        self.actionGoto = QtGui.QAction(QtGui.QIcon(":/lpy_images/resources/lpy/next-green.png"),"Go To",self) 
       
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
        
        self._actions = [["Simulation","Play",self.actionRun,0],
                         ["Simulation","Play",self.actionAnimate,0],
                         ["Simulation","Play",self.actionStep,0],
                         ["Simulation","Play",self.actionStop,0],
                         ["Simulation","Play",self.actionInit,0],
                         ["Simulation","Text Edit",self.actionSave,0], 
                         ["Simulation","Text Edit",self.actionUndo,1],
                         ["Simulation","Text Edit",self.actionRedo,1],
                         ["Simulation","Text Edit",self.actionRunSelection,0], 
                         ["Simulation","Text Edit",self.actionSearch,1],
                         ["Simulation","Text Edit",self.actionGoto,1],          
                         ["Simulation","Text Edit",self.actionComment,1],
                         ["Simulation","Text Edit",self.actionUnComment,1]]
                                    
        QtCore.QObject.connect(self, QtCore.SIGNAL('tabCloseRequested(int)'),self.autoClose)

        self.reset()

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
        while self.count() > 0 :
            wid = self.widget(0)
            self.removeTab(0)
            del wid
        self.clear()

        if self.session.project:
            self.addCreateFileTab()
        else:
            self.addDefaultTab()
    
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
        logger.debug("New tab. Type: " + applet_type + ". Name: " + tab_name)
        self.rmTab("Welcome")
        self.rmTab("Create File")
        
        # TODO : permit to add more than one script...
        # existing_tabs = list()
        # for name in self.session.project.scripts:
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
        
        if Applet is not None:            
            self.applets.append(Applet(session=self.session, controller=self.controller, parent=self.parent(), name=tab_name, script=script))
            
    
        self.addTab(self.applets[-1].widget(), tab_name)
        self.setCurrentWidget(self.applets[-1].widget())
        self.applets[-1].widget().name = tab_name
        
        self.controller.connect_actions(self.applets[-1].widget(), self.controller.menu)
        QtCore.QObject.connect(self, QtCore.SIGNAL('currentChanged(int)'),self.focusChange)
        self.setTabBlack()
        
    def focusChange(self):
        if self.currentWidget():
            self.currentWidget().applet.focus_change()
        
    def closeTab(self):
        """
        Close current tab
        """
        if self.session.current_is_script():
            ez_name = self.tabText(self.currentIndex())
            self.session.project.rm_script_by_ez_name(ez_name)
            self.controller.project_manager._tree_view_change()
        
        self.removeTab(self.currentIndex())
        if self.count() == 0:
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
        Save all opened scripts
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
        self.controller.project_manager.update_from_widgets()
        try:
            self.currentWidget().applet.run_selected_part()
            logger.debug("Run selected part " + self.currentWidget().applet.name)
        except:
            logger.debug("Can't run selected part " + self.currentWidget().applet.name)
        
    def run(self):
        self.controller.project_manager.update_from_widgets()
        self.currentWidget().applet.run()
        logger.debug("Run " + self.currentWidget().applet.name)
        
    def animate(self):
        self.controller.project_manager.update_from_widgets()
        self.currentWidget().applet.animate()
        logger.debug("Animate " + self.currentWidget().applet.name)
        
    def step(self):
        self.controller.project_manager.update_from_widgets()
        self.currentWidget().applet.step()
        logger.debug("Step " + self.currentWidget().applet.name)
        
    def stop(self):
        self.controller.project_manager.update_from_widgets()
        self.currentWidget().applet.stop()
        logger.debug("Stop " + self.currentWidget().applet.name)
        
    def reinit(self):
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

class CreateFilePage(QtGui.QWidget):
    """
    Welcome page in the applet container.
    Permit to open an existing project,
    or to create a new one,
    or to work on scripts outside projects.
    """
    def __init__(self, session, controller, parent=None):
        super(CreateFilePage, self).__init__(parent=parent)
        
        self.session = session
        self.controller = controller
        layout = QtGui.QGridLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)
        
        max_size = QtCore.QSize(100,80)
        min_size = QtCore.QSize(100,80)
              
        text = QtGui.QLabel("Select type of file to add:")
        newPython = QtGui.QToolButton()
        newPython.setDefaultAction(self.controller.project_manager.actionNewPython)
        newPython.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        #newPython.setMaximumSize(max_size)  
        newPython.setMinimumSize(min_size)         
        newR = QtGui.QToolButton()
        newR.setDefaultAction(self.controller.project_manager.actionNewR)
        newR.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        #newR.setMaximumSize(max_size)  
        newR.setMinimumSize(min_size) 
        newLPy = QtGui.QToolButton()
        newLPy.setDefaultAction(self.controller.project_manager.actionNewLPy)
        newLPy.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        #newLPy.setMaximumSize(max_size)  
        newLPy.setMinimumSize(min_size)         
        newWorkflow = QtGui.QToolButton()
        newWorkflow.setDefaultAction(self.controller.project_manager.actionNewWorkflow)
        newWorkflow.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        #newWorkflow.setMaximumSize(max_size)  
        newWorkflow.setMinimumSize(min_size)       
        text2 = QtGui.QLabel("You can add a file from your computer:")  
        importFile = QtGui.QToolButton()
        importFile.setDefaultAction(self.controller.project_manager.actionImportFile)
        importFile.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        #importFile.setMaximumSize(max_size)  
        importFile.setMinimumSize(min_size)         
        
        layout.addWidget(text,0,0,1,-1)
        layout.addWidget(newPython,1,0)
        layout.addWidget(newLPy,2,0)
        layout.addWidget(newWorkflow,1,1)
        layout.addWidget(newR,2,1)
        layout.addWidget(text2,3,0,1,-1)
        layout.addWidget(importFile,4,0,1,-1)
        
        self.setLayout(layout)

        # fake methods, like if we have a real applet
        class FakeApplet(object):
            def __init__(self):
                self.name = "create_file_page"
            def focus_change(self):
                pass
            def run(self):
                pass
            def animate(self):
                pass
            def step(self):
                pass
            def stop(self):
                pass
            def reinit(self):
                pass
        self.applet = FakeApplet()        
    
        logger.debug("Open create_file Page")



class WelcomePage(QtGui.QWidget):
    """
    Welcome page in the applet container.
    Permit to open an existing project,
    or to create a new one,
    or to work on scripts outside projects.
    """
    def __init__(self, session, controller, parent=None):
        super(WelcomePage, self).__init__(parent=parent)
        
        self.session = session
        self.controller = controller
        layout = QtGui.QGridLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)
        
        max_size = QtCore.QSize(200,60)
        min_size = QtCore.QSize(200,60)
        
        #messageBegin = QtGui.QLabel("Would you like")
        #messageNew = QtGui.QLabel("* to create a new:")
        #messageOpen =QtGui.QLabel("* to open an existing:")        
        
        newBtn = QtGui.QPushButton(QtGui.QIcon(":/images/resources/openalealogo.png"),"New Project")
        newBtn.setMaximumSize(max_size)  
        newBtn.setMinimumSize(min_size)         
        newSvnBtn = QtGui.QPushButton(QtGui.QIcon(":/images/resources/svn.png"),"Versionned Project (SVN)")
        newSvnBtn.setMaximumSize(max_size)  
        newSvnBtn.setMinimumSize(min_size)  
        newGitBtn = QtGui.QPushButton(QtGui.QIcon(":/images/resources/git.png"),"Versionned Project (Git)")
        newGitBtn.setMaximumSize(max_size)  
        newGitBtn.setMinimumSize(min_size)  
        newScriptBtn = QtGui.QPushButton(QtGui.QIcon(":/images/resources/Python-logo.png"),"New File")
        newScriptBtn.setMaximumSize(max_size)  
        newScriptBtn.setMinimumSize(min_size)
        
        openBtn = QtGui.QPushButton(QtGui.QIcon(":/images/resources/openalealogo.png"),"Open Project")
        openBtn.setMaximumSize(max_size)    
        openBtn.setMinimumSize(min_size)
        openSvnBtn = QtGui.QPushButton(QtGui.QIcon(":/images/resources/svn.png"),"Versionned Project (SVN)")
        openSvnBtn.setMaximumSize(max_size) 
        openSvnBtn.setMinimumSize(min_size)
        openGitBtn = QtGui.QPushButton(QtGui.QIcon(":/images/resources/git.png"),"Versionned Project (Git)")
        openGitBtn.setMaximumSize(max_size) 
        openGitBtn.setMinimumSize(min_size)
        openScriptBtn = QtGui.QPushButton(QtGui.QIcon(":/images/resources/Python-logo.png"),"Open File")
        openScriptBtn.setMaximumSize(max_size)  
        openScriptBtn.setMinimumSize(min_size)
        
        restoreSessionBtn = QtGui.QPushButton(QtGui.QIcon(":/images/resources/open.png"),"Restore Previous Session")
        restoreSessionBtn.setMaximumSize(QtCore.QSize(412,60))  
        restoreSessionBtn.setMinimumSize(QtCore.QSize(412,60))
                
        QtCore.QObject.connect(newBtn, QtCore.SIGNAL("clicked()"),self.new)
        QtCore.QObject.connect(newSvnBtn, QtCore.SIGNAL("clicked()"),self.newSvn)
        QtCore.QObject.connect(newGitBtn, QtCore.SIGNAL("clicked()"),self.newGit)
        QtCore.QObject.connect(newScriptBtn, QtCore.SIGNAL("clicked()"),self.newScript)
        QtCore.QObject.connect(openBtn, QtCore.SIGNAL("clicked()"),self.open)
        QtCore.QObject.connect(openSvnBtn, QtCore.SIGNAL("clicked()"),self.openSvn)
        QtCore.QObject.connect(openGitBtn, QtCore.SIGNAL("clicked()"),self.openGit)
        QtCore.QObject.connect(openScriptBtn, QtCore.SIGNAL("clicked()"),self.openScript)
        
        QtCore.QObject.connect(restoreSessionBtn, QtCore.SIGNAL("clicked()"),self.restoreSession)
        
        layout.addWidget(newBtn,0,0)
        layout.addWidget(openBtn,1,0)
        
        layout.addWidget(newScriptBtn,0,1)
        layout.addWidget(openScriptBtn,1,1)
        
        layout.addWidget(restoreSessionBtn,2,0,2,2)
        
        self.setLayout(layout)

        # fake methods, like if we have a real applet
        class FakeApplet(object):
            def __init__(self):
                self.name = "welcome_page"
            def focus_change(self):
                pass
            def run(self):
                pass
            def animate(self):
                pass
            def step(self):
                pass
            def stop(self):
                pass
            def reinit(self):
                pass
        self.applet = FakeApplet()        
    
        logger.debug("Open Welcome Page")
    
    def new(self):
        self.session._is_proj = True
        self.session._is_script = False
        self.controller.project_manager.new()
        logger.debug("New Project from welcome page")
        
    def newSvn(self):
        self.controller.project_manager.newSvn()    
        
    def newGit(self):
        self.controller.project_manager.newGit()   
        
    def newScript(self):
        self.session._is_proj = False
        self.session._is_script = True
        self.controller.project_manager.newPython()
        logger.debug("New Script from welcome page")
          
    def open(self):
        self.session._is_proj = True
        self.session._is_script = False
        self.controller.project_manager.open()
        logger.debug("Open Project from welcome page")
        
    def openSvn(self):
        self.controller.project_manager.openSvn()
        
    def openGit(self):
        self.controller.project_manager.openGit()

    def openScript(self):
        self.session._is_proj = False
        self.session._is_script = True
        self.controller.project_manager.openPython()
        logger.debug("Open Script from welcome page")
        
    def restoreSession(self):
        settings = QtCore.QSettings("OpenAlea", "OpenAleaLaboratory")
        proj = from_qvariant(settings.value("session"))
        if proj is None:
            logger.debug("Can't restore previous session. May be it is empty")
        elif proj.is_project():
            self.session._is_proj = True
            self.session._is_script = False
            name = path(proj.path).abspath()/proj.name
            self.controller.project_manager.open(name)
            logger.debug("Restore previous session. (project)")
        elif proj.is_script():
            self.session._is_proj = False
            self.session._is_script = True
            self.session._project = Scripts()
            for p in proj:
                self.controller.project_manager.importFile(filename=p)
            
            self.controller.project_manager._project_changed()
            #self.controller.project_manager.importFile(filename=fname, extension="*.py")
            logger.debug("Restore previous session. (scripts)")

class SelectExtensionPage(QtGui.QWidget):
    """
    Welcome page in the applet container.
    Permit to select the extension to work with. 
    
    
    UNUSED today
    """
    def __init__(self, session, controller, parent=None):
        super(SelectExtensionPage, self).__init__(parent=parent)
        
        self.session = session
        self.controller = controller
        layout = QtGui.QGridLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)

        text = QtGui.QLabel("Select an extension")
        minilab = QtGui.QPushButton(QtGui.QIcon(":/images/resources/openalealogo.png"),"MiniLab")
        messageminilab = QtGui.QLabel("MiniLab is a minimal environnement with only a text editor and a shell.")
        lab3d = QtGui.QPushButton(QtGui.QIcon(":/images/resources/openalealogo.png"),"3DLab")
        messagelab3d = QtGui.QLabel("3DLab is an environnement to work on 3D Objects.")
        plantlab = QtGui.QPushButton(QtGui.QIcon(":/images/resources/openalealogo.png"),"PlantLab")
        messageplantlab = QtGui.QLabel("PlantLab is an environnement to work on entire plant.")
        tissuelab = QtGui.QPushButton(QtGui.QIcon(":/images/resources/openalealogo.png"),"TissueLab")
        messagetissuelab = QtGui.QLabel("TissueLab is an environnement to work on tissue part of plants.")        
        
        QtCore.QObject.connect(minilab, QtCore.SIGNAL("clicked()"),self.mini)
        QtCore.QObject.connect(lab3d, QtCore.SIGNAL("clicked()"),self.lab3d)
        QtCore.QObject.connect(plantlab, QtCore.SIGNAL("clicked()"),self.plant)
        QtCore.QObject.connect(tissuelab, QtCore.SIGNAL("clicked()"),self.tissue)
                
        layout.addWidget(text,0,0,1,-1)
        layout.addWidget(minilab,1,0)
        #layout.addWidget(messageminilab,0,1)
        layout.addWidget(lab3d,1,1)
        #layout.addWidget(messagelab3d,1,1)
        layout.addWidget(plantlab,2,0)
        #layout.addWidget(messageplantlab,2,1)
        layout.addWidget(tissuelab,2,1)
        #layout.addWidget(messagetissuelab,3,1)
        #layout.addWidget(openproject,4,0)
        #layout.addWidget(messageopenproject,4,1)
        #layout.addWidget(restoresession,4,1)
        #layout.addWidget(messagerestoresession,5,1)
        
        self.setLayout(layout)

        # fake methods, like if we have a real applet
        class FakeApplet(object):
            def __init__(self):
                self.name = "welcome_page"
            def focus_change(self):
                pass
            def run(self):
                pass
            def animate(self):
                pass
            def step(self):
                pass
            def stop(self):
                pass
            def reinit(self):
                pass
        self.applet = FakeApplet()        
    
        logger.debug("Open Select Extension Page")

    def mini(self):
        # TODO
        print "mini"
        #mainwindow.changeExtension(self, extension="mini")
    
    def lab3d(self):
        # TODO
        print "lab3d"
        
    def plant(self):
        # TODO
        print "plant"
        
    def tissue(self):
        # TODO
        print "tissue"
