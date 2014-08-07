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
from openalea.core import logger

class SearchWidget(QtGui.QWidget):
    def __init__(self, parent=None, session=None):
        super(SearchWidget, self).__init__(parent)
        self.hiden = True
        
        self.setMinimumSize(100,100)
        self.setWindowTitle("Search")

        self.actionSearch = QtGui.QAction("Search Next", self)
        self.actionBackSearch = QtGui.QAction("Search Previous", self)
        self.actionReplace = QtGui.QAction("Replace All", self)
        self.lineEdit = QtGui.QLineEdit()
        self.lineEditReplace = QtGui.QLineEdit()
        self.textSearch = QtGui.QLabel("Search :")
        self.textReplaceBy = QtGui.QLabel("Replace by :")
        
        self.btnNext = QtGui.QToolButton()
        self.btnPrev = QtGui.QToolButton()
        self.btnReplace = QtGui.QToolButton()
        self.btnReplace.setMinimumSize(100,40)
        self.btnNext.setMinimumSize(100,40)
        self.btnPrev.setMinimumSize(100,40)
        self.btnReplace.setDefaultAction(self.actionReplace)
        self.btnPrev.setDefaultAction(self.actionBackSearch)
        self.btnNext.setDefaultAction(self.actionSearch)
        
        self.caseBtn = QtGui.QCheckBox("Match Case")
        self.wholeBtn = QtGui.QCheckBox("Whole Word (Disabled if case sensitive)")

        QtCore.QObject.connect(self.actionBackSearch, QtCore.SIGNAL('triggered(bool)'),self.searchBack)
        QtCore.QObject.connect(self.actionSearch, QtCore.SIGNAL('triggered(bool)'),self.search)
        QtCore.QObject.connect(self.actionReplace, QtCore.SIGNAL('triggered(bool)'),self.replaceall)
        QtCore.QObject.connect(self.lineEdit, QtCore.SIGNAL('returnPressed()'),self.search)

        layout = QtGui.QGridLayout()
        layout.setAlignment(QtCore.Qt.AlignLeft)
        
        layout.addWidget(self.textSearch,0,0)
        layout.addWidget(self.lineEdit,0,1,1,2)
        layout.addWidget(self.textReplaceBy,1,0)
        layout.addWidget(self.lineEditReplace,1,1,1,2)
        
        layout.addWidget(self.caseBtn,2,0)
        layout.addWidget(self.wholeBtn,2,1)
        
        layout.addWidget(self.btnReplace,3,0)
        layout.addWidget(self.btnPrev,3,1)
        layout.addWidget(self.btnNext,3,2)
        
        self.setLayout(layout)

    def search(self):
        options = None

        if self.caseBtn.isChecked():
            options = QtGui.QTextDocument.FindCaseSensitively
     
        if self.wholeBtn.isChecked():
            if options is None:
                options = QtGui.QTextDocument.FindWholeWords
            else:
                options = options or QtGui.QTextDocument.FindWholeWords
        
        to_search_txt = self.lineEdit.text()
        
        if hasattr(self.parent.editor, "find"):
            logger.debug("Search text: " + to_search_txt)
            if options is not None:
                self.parent.editor.find(to_search_txt, options)
            else:
                self.parent.editor.find(to_search_txt)
        else:
            logger.debug("Can't Search text " + to_search_txt)

    def searchBack(self):
        options = QtGui.QTextDocument.FindBackward

        if self.caseBtn.isChecked():
            options = options or QtGui.QTextDocument.FindCaseSensitively
     
        if self.wholeBtn.isChecked():
            options = options or QtGui.QTextDocument.FindWholeWords
        
        to_search_txt = self.lineEdit.text()
        
        if hasattr(self.parent.editor, "find"):
            logger.debug("Search text: " + to_search_txt)
            self.parent.editor.find(to_search_txt, options)
        else:
            logger.debug("Can't Search text " + to_search_txt)


     
    def replaceall(self):
        # Replace all occurences without interaction

        # Here I am just getting the replacement data
        # from my UI so it will be different for you
        old = self.lineEdit.text()
        new = self.lineEditReplace.text()

        # Beginning of undo block
        cursor = self.parent.editor.textCursor()
        cursor.beginEditBlock()

        # Use flags for case match
        flags = QtGui.QTextDocument.FindFlags()
        if self.caseBtn.isChecked():
            flags = flags | QtGui.QTextDocument.FindCaseSensitively
        if self.wholeBtn.isChecked():
            flags = flags | QtGui.QTextDocument.FindWholeWords

        # Replace all we can
        while True:
            # self.editor is the QPlainTextEdit
            r = self.parent.editor.find(old,flags)
            if r:
                qc = self.parent.editor.textCursor()
                if qc.hasSelection():
                    qc.insertText(new)
            else:
                break

        # Mark end of undo block
        cursor.endEditBlock()
