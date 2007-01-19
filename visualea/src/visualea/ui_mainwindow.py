# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Thu Jan 18 14:59:37 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,847,593).size()).expandedTo(MainWindow.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.hboxlayout = QtGui.QHBoxLayout(self.centralwidget)
        self.hboxlayout.setMargin(9)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.splitter_2 = QtGui.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")

        self.tabPackager = QtGui.QTabWidget(self.splitter_2)
        self.tabPackager.setObjectName("tabPackager")

        self.packageview = QtGui.QWidget()

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(3),QtGui.QSizePolicy.Policy(5))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.packageview.sizePolicy().hasHeightForWidth())
        self.packageview.setSizePolicy(sizePolicy)
        self.packageview.setObjectName("packageview")

        self.vboxlayout = QtGui.QVBoxLayout(self.packageview)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")
        self.tabPackager.addTab(self.packageview,"")

        self.categoryview = QtGui.QWidget()
        self.categoryview.setObjectName("categoryview")

        self.vboxlayout1 = QtGui.QVBoxLayout(self.categoryview)
        self.vboxlayout1.setMargin(9)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")
        self.tabPackager.addTab(self.categoryview,"")

        self.splitter = QtGui.QSplitter(self.splitter_2)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(10)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")

        self.tabWorkspace = QtGui.QTabWidget(self.splitter)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(4)
        sizePolicy.setVerticalStretch(3)
        sizePolicy.setHeightForWidth(self.tabWorkspace.sizePolicy().hasHeightForWidth())
        self.tabWorkspace.setSizePolicy(sizePolicy)
        self.tabWorkspace.setObjectName("tabWorkspace")

        self.workspace1 = QtGui.QWidget()
        self.workspace1.setObjectName("workspace1")

        self.vboxlayout2 = QtGui.QVBoxLayout(self.workspace1)
        self.vboxlayout2.setMargin(9)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setObjectName("vboxlayout2")
        self.tabWorkspace.addTab(self.workspace1,"")
        self.hboxlayout.addWidget(self.splitter_2)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,847,25))
        self.menubar.setObjectName("menubar")

        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")

        self.menu_Package = QtGui.QMenu(self.menubar)
        self.menu_Package.setObjectName("menu_Package")

        self.menu_Wralea_2 = QtGui.QMenu(self.menu_Package)
        self.menu_Wralea_2.setObjectName("menu_Wralea_2")

        self.menu_Workspace = QtGui.QMenu(self.menubar)
        self.menu_Workspace.setObjectName("menu_Workspace")

        self.menu_Help = QtGui.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")

        self.menu_Python = QtGui.QMenu(self.menubar)
        self.menu_Python.setObjectName("menu_Python")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.action_About = QtGui.QAction(MainWindow)
        self.action_About.setObjectName("action_About")

        self.action_Help = QtGui.QAction(MainWindow)
        self.action_Help.setObjectName("action_Help")

        self.action_New_Project = QtGui.QAction(MainWindow)
        self.action_New_Project.setObjectName("action_New_Project")

        self.action_Open_Project = QtGui.QAction(MainWindow)
        self.action_Open_Project.setObjectName("action_Open_Project")

        self.action_Save_Project = QtGui.QAction(MainWindow)
        self.action_Save_Project.setObjectName("action_Save_Project")

        self.actionSave_as = QtGui.QAction(MainWindow)
        self.actionSave_as.setObjectName("actionSave_as")

        self.action_Quit = QtGui.QAction(MainWindow)
        self.action_Quit.setObjectName("action_Quit")

        self.action_Find = QtGui.QAction(MainWindow)
        self.action_Find.setObjectName("action_Find")

        self.action_New_Package = QtGui.QAction(MainWindow)
        self.action_New_Package.setObjectName("action_New_Package")

        self.action_Remove_Package = QtGui.QAction(MainWindow)
        self.action_Remove_Package.setObjectName("action_Remove_Package")

        self.actionSystem_Search = QtGui.QAction(MainWindow)
        self.actionSystem_Search.setObjectName("actionSystem_Search")

        self.action_Add_File = QtGui.QAction(MainWindow)
        self.action_Add_File.setObjectName("action_Add_File")

        self.action_Auto_Search = QtGui.QAction(MainWindow)
        self.action_Auto_Search.setObjectName("action_Auto_Search")

        self.action_Close_current_workspace = QtGui.QAction(MainWindow)
        self.action_Close_current_workspace.setObjectName("action_Close_current_workspace")

        self.action_Run = QtGui.QAction(MainWindow)
        self.action_Run.setObjectName("action_Run")

        self.action_New_Network = QtGui.QAction(MainWindow)
        self.action_New_Network.setObjectName("action_New_Network")

        self.actionOpenAlea_Web = QtGui.QAction(MainWindow)
        self.actionOpenAlea_Web.setObjectName("actionOpenAlea_Web")

        self.actionExport_as_Application = QtGui.QAction(MainWindow)
        self.actionExport_as_Application.setObjectName("actionExport_as_Application")

        self.actionSearch_Path = QtGui.QAction(MainWindow)
        self.actionSearch_Path.setObjectName("actionSearch_Path")

        self.action_Execute_script = QtGui.QAction(MainWindow)
        self.action_Execute_script.setObjectName("action_Execute_script")
        self.menu_File.addAction(self.action_New_Project)
        self.menu_File.addAction(self.action_Open_Project)
        self.menu_File.addAction(self.action_Save_Project)
        self.menu_File.addAction(self.actionSave_as)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_Quit)
        self.menu_Wralea_2.addAction(self.action_Add_File)
        self.menu_Wralea_2.addAction(self.action_Auto_Search)
        self.menu_Wralea_2.addAction(self.actionSearch_Path)
        self.menu_Package.addAction(self.menu_Wralea_2.menuAction())
        self.menu_Package.addSeparator()
        self.menu_Package.addAction(self.action_New_Network)
        self.menu_Workspace.addAction(self.action_Close_current_workspace)
        self.menu_Workspace.addSeparator()
        self.menu_Workspace.addAction(self.action_Run)
        self.menu_Workspace.addSeparator()
        self.menu_Workspace.addAction(self.actionExport_as_Application)
        self.menu_Help.addAction(self.action_Help)
        self.menu_Help.addSeparator()
        self.menu_Help.addAction(self.action_About)
        self.menu_Help.addAction(self.actionOpenAlea_Web)
        self.menu_Python.addAction(self.action_Execute_script)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Package.menuAction())
        self.menubar.addAction(self.menu_Workspace.menuAction())
        self.menubar.addAction(self.menu_Python.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(MainWindow)
        self.tabPackager.setCurrentIndex(0)
        self.tabWorkspace.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "VisuAlea", None, QtGui.QApplication.UnicodeUTF8))
        self.tabPackager.setTabText(self.tabPackager.indexOf(self.packageview), QtGui.QApplication.translate("MainWindow", "Package", None, QtGui.QApplication.UnicodeUTF8))
        self.tabPackager.setTabText(self.tabPackager.indexOf(self.categoryview), QtGui.QApplication.translate("MainWindow", "Category", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWorkspace.setTabText(self.tabWorkspace.indexOf(self.workspace1), QtGui.QApplication.translate("MainWindow", "Root", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_File.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Package.setTitle(QtGui.QApplication.translate("MainWindow", "&Package", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Wralea_2.setTitle(QtGui.QApplication.translate("MainWindow", "&Import", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Workspace.setTitle(QtGui.QApplication.translate("MainWindow", "&Workspace", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Help.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Python.setTitle(QtGui.QApplication.translate("MainWindow", "P&ython", None, QtGui.QApplication.UnicodeUTF8))
        self.action_About.setText(QtGui.QApplication.translate("MainWindow", "&About", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Help.setText(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Help.setShortcut(QtGui.QApplication.translate("MainWindow", "F1", None, QtGui.QApplication.UnicodeUTF8))
        self.action_New_Project.setText(QtGui.QApplication.translate("MainWindow", "&New Project", None, QtGui.QApplication.UnicodeUTF8))
        self.action_New_Project.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open_Project.setText(QtGui.QApplication.translate("MainWindow", "&Open Project", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Open_Project.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+O", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Save_Project.setText(QtGui.QApplication.translate("MainWindow", "&Save Project", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Save_Project.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_as.setText(QtGui.QApplication.translate("MainWindow", "Save Project &as", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setText(QtGui.QApplication.translate("MainWindow", "&Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Quit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Find.setText(QtGui.QApplication.translate("MainWindow", "&Find", None, QtGui.QApplication.UnicodeUTF8))
        self.action_New_Package.setText(QtGui.QApplication.translate("MainWindow", "&Create Package", None, QtGui.QApplication.UnicodeUTF8))
        self.action_New_Package.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+N", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Remove_Package.setText(QtGui.QApplication.translate("MainWindow", "&Remove Package", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSystem_Search.setText(QtGui.QApplication.translate("MainWindow", "System &Search", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Add_File.setText(QtGui.QApplication.translate("MainWindow", "&Add File", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Auto_Search.setText(QtGui.QApplication.translate("MainWindow", "Auto &Search", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Close_current_workspace.setText(QtGui.QApplication.translate("MainWindow", "&Close workspace", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Run.setText(QtGui.QApplication.translate("MainWindow", "&Run ", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Run.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+R", None, QtGui.QApplication.UnicodeUTF8))
        self.action_New_Network.setText(QtGui.QApplication.translate("MainWindow", "&New Network", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpenAlea_Web.setText(QtGui.QApplication.translate("MainWindow", "OpenAlea Web", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExport_as_Application.setText(QtGui.QApplication.translate("MainWindow", "Export as Application", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSearch_Path.setText(QtGui.QApplication.translate("MainWindow", "Search &Path", None, QtGui.QApplication.UnicodeUTF8))
        self.action_Execute_script.setText(QtGui.QApplication.translate("MainWindow", "&Execute script", None, QtGui.QApplication.UnicodeUTF8))

