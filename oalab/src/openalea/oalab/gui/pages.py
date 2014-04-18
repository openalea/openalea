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

from openalea.core import logger
from openalea.vpltk.qt import QtCore, QtGui
from openalea.vpltk.qt.compat import from_qvariant

class WelcomePage(QtGui.QWidget):
    """
    Welcome page in the applet container.
    Permit to open an existing project,
    or to create a new one,
    or to work on src outside projects.
    """
    def __init__(self, session, controller, parent=None):
        super(WelcomePage, self).__init__(parent=parent)
        
        self.session = session
        self.controller = controller
        layout = QtGui.QGridLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)
        
        max_size = QtCore.QSize(200,60)
        min_size = QtCore.QSize(200,60)      
        
        newBtn = QtGui.QPushButton(QtGui.QIcon(":/images/resources/openalealogo.png"),"New Project")
        newBtn.setMaximumSize(max_size)  
        newBtn.setMinimumSize(min_size)         
        
        openBtn = QtGui.QPushButton(QtGui.QIcon(":/images/resources/openalealogo.png"),"Open Project")
        openBtn.setMaximumSize(max_size)    
        openBtn.setMinimumSize(min_size)
        
        QtCore.QObject.connect(newBtn, QtCore.SIGNAL("clicked()"),self.new)
        QtCore.QObject.connect(openBtn, QtCore.SIGNAL("clicked()"),self.open)
        
        layout.addWidget(newBtn,0,0)
        layout.addWidget(openBtn,1,0)
        
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
        self.controller.project_manager.new()
        logger.debug("New Project from welcome page")

    def newScript(self):
        pass
        #self.controller.applet_container.addCreateFileTab()
          
    def open(self):
        self.session._is_proj = True
        self.controller.project_manager.open()
        logger.debug("Open Project from welcome page")
        
    def restoreSession(self):
        settings = QtCore.QSettings("OpenAlea", "OpenAleaLaboratory")
        proj = from_qvariant(settings.value("session"))
        if proj is None:
            logger.debug("Can't restore previous session. May be it is empty")
        elif proj.is_project():
            self.session._is_proj = True
            name = path(proj.path).abspath()/proj.name
            self.controller.project_manager.open(name)
            logger.debug("Restore previous session. (project)")

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


class CreateFilePage(QtGui.QWidget):
    """
    Welcome page in the applet container.
    Permit to open an existing project,
    or to create a new one,
    or to work on src outside projects.
    """
    def __init__(self, session, controller, parent=None):
        super(CreateFilePage, self).__init__(parent=parent)
        
        self.session = session
        self.controller = controller
        layout = QtGui.QGridLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)
        
        max_size = QtCore.QSize(100,80)
        min_size = QtCore.QSize(100,80)
              
        text = QtGui.QLabel("Select type of file to create:")
        layout.addWidget(text,0,0,1,-1)
        
        i, j = 1, 0
        for action in self.controller.project_manager.paradigms_actions:
            newAction = QtGui.QToolButton()
            newAction.setDefaultAction(action)
            newAction.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
            newAction.setMinimumSize(min_size)
            layout.addWidget(newAction,i,j)
            if j == 0:
                j = 1
            else:
                j = 0
                i += 1
    
        text2 = QtGui.QLabel("You can add a file from your computer:")  
        layout.addWidget(text2,10,0,1,-1)
        
        # editFile = QtGui.QToolButton()
        # editFile.setDefaultAction(self.controller.project_manager.actionEditFile)
        # editFile.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        # editFile.setMinimumSize(min_size)
        # layout.addWidget(editFile,11,0,1,-1)
        
        importFile = QtGui.QToolButton()
        importFile.setDefaultAction(self.controller.project_manager.actionImportFile)
        importFile.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        importFile.setMinimumSize(min_size)         
        layout.addWidget(importFile,11,0,1,-1)
        
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
