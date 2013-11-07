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
from openalea.oalab.applets.lpy import LPyApplet
from openalea.oalab.applets.python import PythonApplet
from openalea.oalab.applets.r import RApplet
from openalea.oalab.applets.visualea import VisualeaApplet
from openalea.core import logger
from openalea.core.path import path

class AppletContainer(QtGui.QTabWidget):
    """
    Contains applets.
    Each tab is an applet.
    """
    def __init__(self, session):
        super(AppletContainer, self).__init__()
        self.session = session # session
        self.setTabsClosable(True)
        self.setMinimumSize(100, 100)
        self.applets = list()
        
        self.actionSave = QtGui.QAction(QtGui.QIcon(":/images/resources/save.png"),"Save", self)
        self.actionRun = QtGui.QAction(QtGui.QIcon(":/lpy_images/resources/lpy/run.png"),"Run", self)
        self.actionAnimate = QtGui.QAction(QtGui.QIcon(":/lpy_images/resources/lpy/play.png"),"Animate", self)
        self.actionStep = QtGui.QAction(QtGui.QIcon(":/lpy_images/resources/lpy/step.png"),"Step", self)
        self.actionStop = QtGui.QAction(QtGui.QIcon(":/lpy_images/resources/lpy/pause.png"),"Stop", self)
        self.actionInit = QtGui.QAction(QtGui.QIcon(":/lpy_images/resources/lpy/rewind.png"),"Init", self)
        
        self.actionRunSelection = QtGui.QAction(QtGui.QIcon(":/lpy_images/resources/lpy/run.png"),"Run selection", self)
        
        self.actionUndo = QtGui.QAction(QtGui.QIcon(":/lpy_images/resources/lpy/editundo.png"),"Undo", self)
        self.actionRedo = QtGui.QAction(QtGui.QIcon(":/lpy_images/resources/lpy/editredo.png"),"Redo", self)
        self.actionSearch = QtGui.QAction(QtGui.QIcon(":/lpy_images/resources/lpy/editfind.png"),"Search", self)
        
        self.actionComment = QtGui.QAction(QtGui.QIcon(":/images/resources/commentOn.png"),"Comment",self)
        self.actionUnComment = QtGui.QAction(QtGui.QIcon(":/images/resources/commentOff.png"),"Uncomment",self) 
       
        self.actionComment.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+W", None, QtGui.QApplication.UnicodeUTF8)) 
        self.actionUnComment.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        
        self.actionRunSelection.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+R", None, QtGui.QApplication.UnicodeUTF8))

        self.actionSearch.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+F", None, QtGui.QApplication.UnicodeUTF8))
        
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
        QtCore.QObject.connect(self.actionComment, QtCore.SIGNAL('triggered(bool)'),self.comment)
        QtCore.QObject.connect(self.actionUnComment, QtCore.SIGNAL('triggered(bool)'),self.uncomment)
        
        self.actionStop.setEnabled(False)
        
        self._actions = ["Simulation",[["Play",self.actionRun,0],
                                    ["Play",self.actionAnimate,0],
                                    ["Play",self.actionStep,0],
                                    ["Play",self.actionStop,0],
                                    ["Play",self.actionInit,0],
                                    ["Text Edit",self.actionUndo,1],
                                    ["Text Edit",self.actionRedo,1],
                                    ["Text Edit",self.actionSearch,1],
                                    ["Text Edit",self.actionComment,1],
                                    ["Text Edit",self.actionUnComment,1],
                                    ["Text Edit",self.actionRunSelection,1],
                                    ["Text Edit",self.actionSave,1]]]
                                    
        QtCore.QObject.connect(self, QtCore.SIGNAL('tabCloseRequested(int)'),self.autoClose)

        self.addDefaultTab()
	    
    def addDefaultTab(self):
        """
        Display a welcom tab if nothing is opened
        """
        welcomePage = WelcomePage(session = self.session)
        self.addTab(welcomePage, "Welcome")
        
    def rmDefaultTab(self):
        """
        Remove the welcome tab
        """
        for i in range(self.count()):
            if self.tabText(i) == "Welcome":
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
        self.rmDefaultTab()
        
        # TODO : permit to add more than one script...
        # existing_tabs = list()
        # for name in self.session.project.scripts:
        #    existing_tabs.append(name)
        # tab_name = check_if_name_is_unique(tab_name, existing_tabs)
        
        if (applet_type == "python") or (applet_type == "py"):
            self.applets.append(PythonApplet(self.session, name=tab_name, script=script))
        elif applet_type == "lpy":
            self.applets.append(LPyApplet(self.session, name=tab_name, script=script))
        elif applet_type in ("wpy","visualea"):
            self.applets.append(VisualeaApplet(self.session, name=tab_name, script=script))
        elif applet_type in ("r","R"):
            self.applets.append(RApplet(self.session, name=tab_name, script=script))
    
        self.addTab(self.applets[-1].widget(), tab_name)
        self.setCurrentWidget(self.applets[-1].widget())
        self.applets[-1].widget().name = tab_name
        
        self.session.connect_actions(self.applets[-1].widget(), self.session.menu)
        QtCore.QObject.connect(self, QtCore.SIGNAL('currentChanged(int)'),self.focusChange)
        
    def focusChange(self):
        if self.currentWidget():
            self.currentWidget().applet.focus_change()
        
    def closeTab(self):
        """
        Close current tab
        """
        if self.session.current_is_script():
            fname = self.tabText(self.currentIndex())
            del self.session.project[fname]
            self.session.project_widget._tree_view_change()
        
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
        try:
            self.currentWidget().applet.run_selected_part()
            logger.debug("Run selected part " + self.currentWidget().applet.name)
        except:
            logger.debug("Can't run selected part " + self.currentWidget().applet.name)
        
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
        
    def reinit(self):
        self.currentWidget().applet.reinit()
        logger.debug("Reinit " + self.currentWidget().applet.name)

    def undo(self):
        try:
            self.currentWidget().undo()
        except:
            pass
        logger.debug("Undo " + self.currentWidget().applet.name)
        
    def redo(self):
        try:
            self.currentWidget().redo()
        except:
            pass
        logger.debug("Redo " + self.currentWidget().applet.name)
        
    def search(self):
        self.currentWidget().search()
        logger.debug("Search " + self.currentWidget().applet.name)
        
    def comment(self):
        self.currentWidget().comment()
        logger.debug("comment " + self.currentWidget().applet.name)

    def uncomment(self):
        self.currentWidget().uncomment()
        logger.debug("uncomment " + self.currentWidget().applet.name)
        
class WelcomePage(QtGui.QWidget):
    """
    Welcome page in the applet container.
    Permit to open an existing project,
    or to create a new one,
    or to work on scripts outside projects.
    """
    def __init__(self, session, parent=None):
        super(WelcomePage, self).__init__()
        
        self.session = session
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
        
        #layout.addWidget(messageBegin,0,0,1,1)
        #layout.addWidget(messageNew,1,0)
        #layout.addWidget(newBtn,2,0)
        #layout.addWidget(newSvnBtn,3,0)
        #layout.addWidget(newGitBtn,4,0)
        #layout.addWidget(newScriptBtn,5,0)
        
        #layout.addWidget(messageOpen,1,1)        
        #layout.addWidget(openBtn,2,1)
        #layout.addWidget(openSvnBtn,3,1)
        #layout.addWidget(openGitBtn,4,1)
        #layout.addWidget(openScriptBtn,5,1)
        
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
        self.session.project_widget.new()
        logger.debug("New Project from welcome page")
        
    def newSvn(self):
        self.session.project_widget.newSvn()    
        
    def newGit(self):
        self.session.project_widget.newGit()   
        
    def newScript(self):
        self.session._is_proj = False
        self.session._is_script = True
        self.session.project_widget.newPython()
        logger.debug("New Script from welcome page")
          
    def open(self):
        self.session._is_proj = True
        self.session._is_script = False
        self.session.project_widget.open()
        logger.debug("Open Project from welcome page")
        
    def openSvn(self):
        self.session.project_widget.openSvn()
        
    def openGit(self):
        self.session.project_widget.openGit()

    def openScript(self):
        self.session._is_proj = False
        self.session._is_script = True
        self.session.project_widget.openPython()
        logger.debug("Open Script from welcome page")
        
    def restoreSession(self):
        settings = QtCore.QSettings("OpenAlea", "OpenAleaLaboratory")
        proj = settings.value("session")
        if proj is None:
            pass
        elif proj.is_project():
            self.session._is_proj = True
            self.session._is_script = False
            name = path(proj.path).abspath()/proj.name
            self.session.project_widget.open(name)
        elif proj.is_script():
            self.session._is_proj = False
            self.session._is_script = True
            self.session._project = proj
            
            self.session.project_widget._project_changed()
            #self.session.project_widget.importFile(filename=fname, extension="*.py")

