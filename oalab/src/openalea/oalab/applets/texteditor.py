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

# Try to refactor LPy editor
from openalea.lpy.gui.lpycodeeditor import LpyCodeEditor as _LpyCodeEditor, Margin      
from openalea.lpy.gui.lpystudio import LPyWindow

from openalea.core.path import path
from openalea.core import settings

ErrorMarker,BreakPointMarker,CodePointMarker = range(3)

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class TextEditor(_LpyCodeEditor):
    def __init__(self, session, parent=None):
        super(TextEditor, self).__init__(parent)
        self.parent = parent
        
        self.session = session

        self.actionSave = QtGui.QAction(QtGui.QIcon(":/images/resources/save.png"),"Save", self)
        self.actionFind = QtGui.QAction(QtGui.QIcon(":/lpy_images/resources/lpy/editfind.png"),"Find", self)
        self.actionReplace = QtGui.QAction(QtGui.QIcon(":/lpy_images/resources/lpy/editfind.png"),"Replace", self)
        self.actionGoto = QtGui.QAction(QtGui.QIcon(":/lpy_images/resources/lpy/next.png"),"Go to line", self)
        self.actionUndo = QtGui.QAction(QtGui.QIcon(":/lpy_images/resources/lpy/editundo.png"),"Undo", self)
        self.actionRedo = QtGui.QAction(QtGui.QIcon(":/lpy_images/resources/lpy/editredo.png"),"Redo", self)
        self.actionCheck = QtGui.QAction(QtGui.QIcon(":/lpy_images/resources/lpy/warningsErrors.png"),"Check Source", self)
        self.actionDebug = QtGui.QAction(QtGui.QIcon(":/lpy_images/resources/lpy/play-green.png"),"Debug", self)
        self.actionProfle = QtGui.QAction(QtGui.QIcon(":/lpy_images/resources/lpy/play-yellow.png"),"Profile", self)
        self.actionClose = QtGui.QAction(QtGui.QIcon(":/images/resources/closeButton.png"),"Close", self)
        
        self.actionSave.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        
        QtCore.QObject.connect(self.actionSave, QtCore.SIGNAL('triggered(bool)'),self.session.applet_container.save)
        QtCore.QObject.connect(self.actionFind, QtCore.SIGNAL('triggered(bool)'),self.find)
        QtCore.QObject.connect(self.actionReplace, QtCore.SIGNAL('triggered(bool)'),self.replace)
        QtCore.QObject.connect(self.actionGoto, QtCore.SIGNAL('triggered(bool)'),self.goto)
        QtCore.QObject.connect(self.actionUndo, QtCore.SIGNAL('triggered(bool)'),self.undo)
        QtCore.QObject.connect(self.actionRedo, QtCore.SIGNAL('triggered(bool)'),self.redo)
        QtCore.QObject.connect(self.actionCheck, QtCore.SIGNAL('triggered(bool)'),self.check)
        QtCore.QObject.connect(self.actionDebug, QtCore.SIGNAL('triggered(bool)'),self.debug)
        QtCore.QObject.connect(self.actionProfle, QtCore.SIGNAL('triggered(bool)'),self.profile)
        QtCore.QObject.connect(self.actionClose, QtCore.SIGNAL('triggered(bool)'),self.close)
        

        self._actions = ["Simulation",[
                                    #["Text Edit",self.actionSave,0],
                                    ["Text Edit",self.actionFind,1],
                                    ["Text Edit",self.actionReplace,1],
                                    ["Text Edit",self.actionGoto,1],
                                    ["Text Edit",self.actionUndo,1],
                                    ["Text Edit",self.actionRedo,1],
                                    ["Text Edit",self.actionCheck,1],
                                    ["Text Edit",self.actionDebug,1],
                                    ["Text Edit",self.actionProfle,1],
                                    ["Text Edit",self.actionClose,1]]]

        self.init()

    def init(self):
        self.statusBar = self.session.statusBar
        self.positionLabel = QtGui.QLabel(self.statusBar)
        self.statusBar.addPermanentWidget(self.positionLabel)
        QtCore.QObject.connect(self, QtCore.SIGNAL('cursorPositionChanged()'),self.printCursorPosition)
        self.defaultEditionFont = self.currentFont()
        self.defaultPointSize = self.currentFont().pointSize()
        self.setViewportMargins(50,0,0,0)
        self.sidebar = Margin(self,self)
        self.sidebar.setGeometry(0,0,50,100)
        self.sidebar.defineMarker(ErrorMarker,QtGui.QPixmap(':/images/icons/warningsErrors16.png'))
        self.sidebar.defineMarker(BreakPointMarker,QtGui.QPixmap(':/images/icons/BreakPoint.png'))
        self.sidebar.defineMarker(CodePointMarker,QtGui.QPixmap(':/images/icons/greenarrow16.png'))
        self.sidebar.show() 
        QtCore.QObject.connect(self.sidebar, QtCore.SIGNAL('lineClicked(int)'),self.checkLine)

    def saveState(self,obj):
        pass

    def focusInEvent ( self, event ):
        return QtGui.QTextEdit.focusInEvent ( self, event )

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
    
    def set_text(self, txt):
        """
        Set text in the editor
        
        :param text: text you want to set 
        """
        cursor = self.textCursor()
        cursor.insertText(txt)
        
    set_script = set_text
        
    def get_text(self, start='sof', end='eof'):
        """
        Return a part of the text.
        
        :param start: is the begining of what you want to get
        :param end: is the end of what you want to get
        :return: text which is contained in the editor between 'start' and 'end'
        """
        return self.toPlainText()
        # TODO get text NOT FULL TEXT
        
    def get_full_text(self):
        """
        :return: the full text in the editor
        """
        return self.toPlainText()

    def save(self, name=None):
        """
        Save current file.
        
        :param name: name of the file to save.
        If not name, self.name is used.
        If self.name is not setted and name is not give in parameter,
        a File Dialog is opened.
        """
        if name:
            self.name = name
            
        if not self.name:
            temp_path = path(settings.get_project_dir())
            self.name = QtGui.QFileDialog.getSaveFileName(self, 'Select name to save the file', 
                temp_path)

        # print "save text", name
        txt = self.get_full_text()
        project = self.session.project
        
        if self.session.current_is_project():
            project.scripts[self.name] = txt
            project._save_scripts()
            
        elif self.session.current_is_script():
            # Save a script outside a project
            fname = project.fname
            f = open(fname, "w")
            code = project.value
            code_enc = code.encode("utf8","ignore") 
            f.write(code_enc)
            f.close()
        
    def debug(self):
        pass
    
    def profile(self):
        pass
    
    def close(self):
        pass
        
    def check(self):
        pass
        
    def checkLine(self,line):
##        self.editor.statusBar().showMessage("Line "+str(line)+" clicked",2000)
        if self.sidebar.hasMarkerAt(line):
            if self.hasError and self.errorLine == line:
                self.clearErrorHightlight()
            elif self.sidebar.hasMarkerTypeAt(line,BreakPointMarker):
                self.sidebar.removeMarkerTypeAt(line,BreakPointMarker)
            else:
                self.sidebar.appendMarkerAt(line,BreakPointMarker)
        else:
            self.sidebar.setMarkerAt(line,BreakPointMarker)        
    
    def find(self):
        pass
        
    def replace(self):
        pass
        
    def undo(self):
        cursor = self.textCursor()
        super(TextEditor, self).undo() 
        self.setTextCursor(cursor)
        # TODO: manage update of sidebar

    def redo(self):
        cursor = self.textCursor()
        super(TextEditor, self).redo() 
        self.setTextCursor(cursor)
        # TODO: manage update of sidebar

    def goto(self):
        # print "goto"
        pass

