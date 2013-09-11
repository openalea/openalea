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
from openalea.vpltk.project.project import Script
from openalea.oalab.applets.lpy import LPyApplet
from openalea.oalab.applets.python import PythonApplet
from openalea.oalab.applets.r import RApplet
from openalea.oalab.applets.visualea import VisualeaApplet

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
        
        #self.actionSave.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
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
        
        self._actions = ["Simulation",[["Play",self.actionRun,0],
                                    ["Play",self.actionAnimate,0],
                                    ["Play",self.actionStep,0],
                                    ["Play",self.actionStop,0],
                                    ["Play",self.actionInit,0]]]
                                    
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
        if applet_type in  ("wpy","visualea"):
            self.newTab(applet_type, tab_name, script=script)
        else:
            self.newTab(applet_type, tab_name)
            self.applets[-1].widget().set_script(script)
            
    def newTab(self, applet_type, tab_name="", script=None):
        """
        Open a tab with the widget 'applet_type'
        """
        self.rmDefaultTab()
        
        if (applet_type == "python") or (applet_type == "py"):
            self.applets.append(PythonApplet(self.session, name=tab_name))
        elif applet_type == "lpy":
            self.applets.append(LPyApplet(self.session, name=tab_name))
        elif applet_type in ("wpy","visualea"):
            self.applets.append(VisualeaApplet(self.session, name=tab_name,repr_model=script))
        elif applet_type in ("r","R"):
            self.applets.append(RApplet(self.session, name=tab_name))
    
        self.addTab(self.applets[-1].widget(), tab_name)
        self.setCurrentWidget(self.applets[-1].widget())
        self.applets[-1].widget().name = tab_name
        
        self.session.connect_actions(self.applets[-1].widget(), self.session.menu)
        
    def closeTab(self):
        """
        Close current tab
        """
        self.removeTab(self.currentIndex())
        
    def autoClose(self, n_tab):
        self.setCurrentIndex(n_tab)
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
        self.currentWidget().save(name=name)
    
    def save_all(self):
        """
        Save all opened scripts
        """
        n = self.count()
        for i in range(n) :
            wid = self.widget(i)
            name = wid.applet.name
            wid.save(name=name)
        
    def run(self):
        self.currentWidget().applet.run()
        
    def animate(self):
        self.currentWidget().applet.animate()
        
    def step(self):
        self.currentWidget().applet.step()
        
    def stop(self):
        self.currentWidget().applet.stop()
        
    def reinit(self):
        self.currentWidget().applet.reinit()


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
        
        messageBegin = QtGui.QLabel("Would you like")
        messageNew = QtGui.QLabel("* to create a new:")
        messageOpen =QtGui.QLabel("* to open an existing:")        
        
        newBtn = QtGui.QPushButton(QtGui.QIcon(":/images/resources/openalealogo.png"),"New Project")
        newBtn.setMaximumSize(max_size)  
        newBtn.setMinimumSize(min_size)         
        newSvnBtn = QtGui.QPushButton(QtGui.QIcon(":/images/resources/svn.png"),"Versionned Project (SVN)")
        newSvnBtn.setMaximumSize(max_size)  
        newSvnBtn.setMinimumSize(min_size)  
        newGitBtn = QtGui.QPushButton(QtGui.QIcon(":/images/resources/git.png"),"Versionned Project (Git)")
        newGitBtn.setMaximumSize(max_size)  
        newGitBtn.setMinimumSize(min_size)  
        newScriptBtn = QtGui.QPushButton(QtGui.QIcon(":/images/resources/Python-logo.png"),"Script")
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
        openScriptBtn = QtGui.QPushButton(QtGui.QIcon(":/images/resources/Python-logo.png"),"Script")
        openScriptBtn.setMaximumSize(max_size)  
        openScriptBtn.setMinimumSize(min_size)
                
        QtCore.QObject.connect(newBtn, QtCore.SIGNAL("clicked()"),self.new)
        QtCore.QObject.connect(newSvnBtn, QtCore.SIGNAL("clicked()"),self.newSvn)
        QtCore.QObject.connect(newGitBtn, QtCore.SIGNAL("clicked()"),self.newGit)
        QtCore.QObject.connect(newScriptBtn, QtCore.SIGNAL("clicked()"),self.newScript)
        QtCore.QObject.connect(openBtn, QtCore.SIGNAL("clicked()"),self.open)
        QtCore.QObject.connect(openSvnBtn, QtCore.SIGNAL("clicked()"),self.openSvn)
        QtCore.QObject.connect(openGitBtn, QtCore.SIGNAL("clicked()"),self.openGit)
        QtCore.QObject.connect(openScriptBtn, QtCore.SIGNAL("clicked()"),self.openScript)
            
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
        layout.addWidget(openBtn,0,1)
        
        self.setLayout(layout)

    def new(self):
        self.session.project_widget.new()
        
    def newSvn(self):
        self.session.project_widget.newSvn()    
        
    def newGit(self):
        self.session.project_widget.newGit()   
        
    def newScript(self):
        #self.session.project_widget.newPython()
        script = Script()
        #script.filename = ""
        #script.value = ""
        tab_name = ""
        
        self.session.cprojname = "no-proj_%s" %tab_name
        self.session.projects[self.session.cprojname] = script
        
        self.session.applet_container.newTab(applet_type="python", tab_name=script.filename)
        self.session.project_widget._project_changed()
          
    def open(self):
        self.session.project_widget.open()
        
    def openSvn(self):
        self.session.project_widget.openSvn()
        
    def openGit(self):
        self.session.project_widget.openGit()

    def openScript(self):
        self.session.project_widget.openPython()
        
