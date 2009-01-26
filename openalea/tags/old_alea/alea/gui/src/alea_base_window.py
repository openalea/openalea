# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'alea_base_window.ui'
#
# Created: Wed Mar  8 18:30:06 2006
#      by: PyQt4 UI code generator vsnapshot-20060307
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_BaseWnd(object):
    def setupUi(self, BaseWnd):
        BaseWnd.setObjectName("BaseWnd")
        BaseWnd.resize(QtCore.QSize(QtCore.QRect(0,0,769,663).size()).expandedTo(BaseWnd.minimumSizeHint()))
        
        self.widget = QtGui.QWidget(BaseWnd)
        self.widget.setObjectName("widget")
        
        self.hboxlayout = QtGui.QHBoxLayout(self.widget)
        self.hboxlayout.setMargin(11)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")
        
        self.vsplitter = QtGui.QSplitter(self.widget)
        self.vsplitter.setOrientation(QtCore.Qt.Horizontal)
        self.vsplitter.setObjectName("vsplitter")
        
        self.explore_frame = QtGui.QTabWidget(self.vsplitter)
        self.explore_frame.setObjectName("explore_frame")
        
        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")
        
        self.vboxlayout = QtGui.QVBoxLayout(self.tab)
        self.vboxlayout.setMargin(0)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")
        self.explore_frame.addTab(self.tab, "")
        
        self.tab1 = QtGui.QWidget()
        self.tab1.setObjectName("tab1")
        
        self.vboxlayout1 = QtGui.QVBoxLayout(self.tab1)
        self.vboxlayout1.setMargin(0)
        self.vboxlayout1.setSpacing(6)
        self.vboxlayout1.setObjectName("vboxlayout1")
        self.explore_frame.addTab(self.tab1, "")
        
        self.TabPage = QtGui.QWidget()
        self.TabPage.setObjectName("TabPage")
        
        self.vboxlayout2 = QtGui.QVBoxLayout(self.TabPage)
        self.vboxlayout2.setMargin(0)
        self.vboxlayout2.setSpacing(6)
        self.vboxlayout2.setObjectName("vboxlayout2")
        self.explore_frame.addTab(self.TabPage, "")
        
        self.hsplitter = QtGui.QSplitter(self.vsplitter)
        self.hsplitter.setMinimumSize(QtCore.QSize(99,73))
        self.hsplitter.setOrientation(QtCore.Qt.Vertical)
        self.hsplitter.setObjectName("hsplitter")
        
        self.workspaces = QtGui.QTabWidget(self.hsplitter)
        self.workspaces.setMinimumSize(QtCore.QSize(0,0))
        self.workspaces.setObjectName("workspaces")
        
        self.tab2 = QtGui.QWidget()
        self.tab2.setObjectName("tab2")
        self.workspaces.addTab(self.tab2, "")
        
        self.shell_frame = QtGui.QFrame(self.hsplitter)
        self.shell_frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.shell_frame.setFrameShadow(QtGui.QFrame.Raised)
        self.shell_frame.setObjectName("shell_frame")
        self.hboxlayout.addWidget(self.vsplitter)
        BaseWnd.setCentralWidget(self.widget)
        
        self.MenuBar = QtGui.QMenuBar(BaseWnd)
        self.MenuBar.setGeometry(QtCore.QRect(0,0,769,24))
        self.MenuBar.setObjectName("MenuBar")
        
        self.editMenu = QtGui.QMenu(self.MenuBar)
        self.editMenu.setObjectName("editMenu")
        
        self.helpMenu = QtGui.QMenu(self.MenuBar)
        self.helpMenu.setObjectName("helpMenu")
        
        self.fileMenu = QtGui.QMenu(self.MenuBar)
        self.fileMenu.setObjectName("fileMenu")
        BaseWnd.setMenuBar(self.MenuBar)
        
        self.toolBar = QtGui.QToolBar(BaseWnd)
        self.toolBar.setOrientation(QtCore.Qt.Horizontal)
        self.toolBar.setObjectName("toolBar")
        BaseWnd.addToolBar(self.toolBar)
        
        self.fileNewAction = QtGui.QAction(BaseWnd)
        self.fileNewAction.setIcon(QtGui.QIcon("image0"))
        self.fileNewAction.setObjectName("fileNewAction")
        
        self.fileOpenAction = QtGui.QAction(BaseWnd)
        self.fileOpenAction.setIcon(QtGui.QIcon("image1"))
        self.fileOpenAction.setObjectName("fileOpenAction")
        
        self.fileSaveAction = QtGui.QAction(BaseWnd)
        self.fileSaveAction.setIcon(QtGui.QIcon("image2"))
        self.fileSaveAction.setObjectName("fileSaveAction")
        
        self.fileSaveAsAction = QtGui.QAction(BaseWnd)
        self.fileSaveAsAction.setObjectName("fileSaveAsAction")
        
        self.filePrintAction = QtGui.QAction(BaseWnd)
        self.filePrintAction.setIcon(QtGui.QIcon("image3"))
        self.filePrintAction.setObjectName("filePrintAction")
        
        self.fileExitAction = QtGui.QAction(BaseWnd)
        self.fileExitAction.setIcon(QtGui.QIcon("image4"))
        self.fileExitAction.setObjectName("fileExitAction")
        
        self.editUndoAction = QtGui.QAction(BaseWnd)
        self.editUndoAction.setIcon(QtGui.QIcon("image5"))
        self.editUndoAction.setObjectName("editUndoAction")
        
        self.editRedoAction = QtGui.QAction(BaseWnd)
        self.editRedoAction.setIcon(QtGui.QIcon("image6"))
        self.editRedoAction.setObjectName("editRedoAction")
        
        self.editCutAction = QtGui.QAction(BaseWnd)
        self.editCutAction.setIcon(QtGui.QIcon("image7"))
        self.editCutAction.setObjectName("editCutAction")
        
        self.editCopyAction = QtGui.QAction(BaseWnd)
        self.editCopyAction.setIcon(QtGui.QIcon("image8"))
        self.editCopyAction.setObjectName("editCopyAction")
        
        self.editPasteAction = QtGui.QAction(BaseWnd)
        self.editPasteAction.setIcon(QtGui.QIcon("image9"))
        self.editPasteAction.setObjectName("editPasteAction")
        
        self.editFindAction = QtGui.QAction(BaseWnd)
        self.editFindAction.setIcon(QtGui.QIcon("image10"))
        self.editFindAction.setObjectName("editFindAction")
        
        self.helpContentsAction = QtGui.QAction(BaseWnd)
        self.helpContentsAction.setObjectName("helpContentsAction")
        
        self.helpIndexAction = QtGui.QAction(BaseWnd)
        self.helpIndexAction.setObjectName("helpIndexAction")
        
        self.helpAboutAction = QtGui.QAction(BaseWnd)
        self.helpAboutAction.setObjectName("helpAboutAction")
        
        self.new_itemAction = QtGui.QAction(BaseWnd)
        self.new_itemAction.setObjectName("new_itemAction")
        
        self.fileOpenHistoryAction = QtGui.QAction(BaseWnd)
        self.fileOpenHistoryAction.setObjectName("fileOpenHistoryAction")
        
        self.fileSaveHistoryAction = QtGui.QAction(BaseWnd)
        self.fileSaveHistoryAction.setObjectName("fileSaveHistoryAction")
        self.editMenu.addAction(self.editUndoAction)
        self.editMenu.addAction(self.editRedoAction)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.editCutAction)
        self.editMenu.addAction(self.editCopyAction)
        self.editMenu.addAction(self.editPasteAction)
        self.editMenu.addSeparator()
        self.editMenu.addAction(self.editFindAction)
        self.helpMenu.addAction(self.helpContentsAction)
        self.helpMenu.addAction(self.helpIndexAction)
        self.helpMenu.addSeparator()
        self.helpMenu.addAction(self.helpAboutAction)
        self.fileMenu.addAction(self.fileNewAction)
        self.fileMenu.addAction(self.fileOpenAction)
        self.fileMenu.addAction(self.fileOpenHistoryAction)
        self.fileMenu.addAction(self.fileSaveAction)
        self.fileMenu.addAction(self.fileSaveHistoryAction)
        self.fileMenu.addAction(self.fileSaveAsAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.filePrintAction)
        self.fileMenu.addSeparator()
        self.fileMenu.addAction(self.fileExitAction)
        self.MenuBar.addAction(self.fileMenu.menuAction())
        self.MenuBar.addAction(self.editMenu.menuAction())
        self.MenuBar.addAction(self.helpMenu.menuAction())
        self.toolBar.addSeparator()
        
        self.retranslateUi(BaseWnd)
        QtCore.QMetaObject.connectSlotsByName(BaseWnd)
    
    def tr(self, string):
        return QtGui.QApplication.translate("BaseWnd", string, None, QtGui.QApplication.UnicodeUTF8)
    
    def retranslateUi(self, BaseWnd):
        BaseWnd.setWindowTitle(self.tr("ALEA - Software for Plant Research"))
        self.explore_frame.setTabText(self.explore_frame.indexOf(self.tab), self.tr("Nodes"))
        self.explore_frame.setTabText(self.explore_frame.indexOf(self.tab1), self.tr("Objects"))
        self.explore_frame.setTabText(self.explore_frame.indexOf(self.TabPage), self.tr("Applications"))
        self.workspaces.setTabText(self.workspaces.indexOf(self.tab2), self.tr("Workspace 1"))
        self.editMenu.setTitle(self.tr("&Edit"))
        self.helpMenu.setTitle(self.tr("&Help"))
        self.fileMenu.setTitle(self.tr("&File"))
        self.fileNewAction.setText(self.tr("&New"))
        self.fileNewAction.setIconText(self.tr("New"))
        self.fileNewAction.setShortcut(self.tr("Ctrl+N"))
        self.fileOpenAction.setText(self.tr("&Open..."))
        self.fileOpenAction.setIconText(self.tr("Open"))
        self.fileOpenAction.setShortcut(self.tr("Ctrl+O"))
        self.fileSaveAction.setText(self.tr("&Save"))
        self.fileSaveAction.setIconText(self.tr("Save"))
        self.fileSaveAction.setShortcut(self.tr("Ctrl+S"))
        self.fileSaveAsAction.setText(self.tr("Save &As..."))
        self.fileSaveAsAction.setIconText(self.tr("Save As"))
        self.filePrintAction.setText(self.tr("&Print..."))
        self.filePrintAction.setIconText(self.tr("Print"))
        self.filePrintAction.setShortcut(self.tr("Ctrl+P"))
        self.fileExitAction.setText(self.tr("E&xit"))
        self.fileExitAction.setIconText(self.tr("Exit"))
        self.fileExitAction.setShortcut(self.tr("Ctrl+Q"))
        self.editUndoAction.setText(self.tr("&Undo"))
        self.editUndoAction.setIconText(self.tr("Undo"))
        self.editUndoAction.setShortcut(self.tr("Ctrl+Z"))
        self.editRedoAction.setText(self.tr("&Redo"))
        self.editRedoAction.setIconText(self.tr("Redo"))
        self.editRedoAction.setShortcut(self.tr("Ctrl+Y"))
        self.editCutAction.setText(self.tr("Cu&t"))
        self.editCutAction.setIconText(self.tr("Cut"))
        self.editCutAction.setShortcut(self.tr("Ctrl+X"))
        self.editCopyAction.setText(self.tr("&Copy"))
        self.editCopyAction.setIconText(self.tr("Copy"))
        self.editCopyAction.setShortcut(self.tr("Ctrl+C"))
        self.editPasteAction.setText(self.tr("&Paste"))
        self.editPasteAction.setIconText(self.tr("Paste"))
        self.editPasteAction.setShortcut(self.tr("Ctrl+V"))
        self.editFindAction.setText(self.tr("&Find..."))
        self.editFindAction.setIconText(self.tr("Find"))
        self.editFindAction.setShortcut(self.tr("Ctrl+F"))
        self.helpContentsAction.setText(self.tr("&Contents..."))
        self.helpContentsAction.setIconText(self.tr("Contents"))
        self.helpIndexAction.setText(self.tr("&Index..."))
        self.helpIndexAction.setIconText(self.tr("Index"))
        self.helpAboutAction.setText(self.tr("&About"))
        self.helpAboutAction.setIconText(self.tr("About"))
        self.new_itemAction.setText(self.tr("new item"))
        self.new_itemAction.setIconText(self.tr("new item"))
        self.fileOpenHistoryAction.setText(self.tr("Open &History"))
        self.fileOpenHistoryAction.setIconText(self.tr("Open Python history"))
        self.fileSaveHistoryAction.setText(self.tr("Save H&istory"))
        self.fileSaveHistoryAction.setIconText(self.tr("Save Python history"))
