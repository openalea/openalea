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

from Qt import QtCore, QtGui, QtWidgets

from openalea.core import logger

class SearchWidget(QtWidgets.QWidget):

    def __init__(self, parent=None, session=None):
        super(SearchWidget, self).__init__(parent)

        self._editor = parent
        self.hiden = True

        self.setMinimumSize(100, 100)
        self.setWindowTitle("Search")

        self.actionSearch = QtWidgets.QAction("Search Next", self)
        self.actionBackSearch = QtWidgets.QAction("Search Previous", self)
        self.actionReplace = QtWidgets.QAction("Replace All", self)
        self.lineEdit = QtWidgets.QLineEdit()
        self.lineEditReplace = QtWidgets.QLineEdit()
        self.textSearch = QtWidgets.QLabel("Search :")
        self.textReplaceBy = QtWidgets.QLabel("Replace by :")

        self.btnNext = QtWidgets.QToolButton()
        self.btnPrev = QtWidgets.QToolButton()
        self.btnReplace = QtWidgets.QToolButton()
        self.btnReplace.setMinimumSize(100, 40)
        self.btnNext.setMinimumSize(100, 40)
        self.btnPrev.setMinimumSize(100, 40)
        self.btnReplace.setDefaultAction(self.actionReplace)
        self.btnPrev.setDefaultAction(self.actionBackSearch)
        self.btnNext.setDefaultAction(self.actionSearch)

        self.caseBtn = QtWidgets.QCheckBox("Match Case")
        self.wholeBtn = QtWidgets.QCheckBox("Whole Word (Disabled if case sensitive)")

        self.actionBackSearch.triggered[bool].connect(self.searchBack)
        self.actionSearch.triggered[bool].connect(self.search)
        self.actionReplace.triggered[bool].connect(self.replaceall)
        self.lineEdit.returnPressed.connect(self.search)

        layout = QtWidgets.QGridLayout()
        layout.setAlignment(QtCore.Qt.AlignLeft)

        layout.addWidget(self.textSearch, 0, 0)
        layout.addWidget(self.lineEdit, 0, 1, 1, 2)
        layout.addWidget(self.textReplaceBy, 1, 0)
        layout.addWidget(self.lineEditReplace, 1, 1, 1, 2)

        layout.addWidget(self.caseBtn, 2, 0)
        layout.addWidget(self.wholeBtn, 2, 1)

        layout.addWidget(self.btnReplace, 3, 0)
        layout.addWidget(self.btnPrev, 3, 1)
        layout.addWidget(self.btnNext, 3, 2)

        self.setLayout(layout)

    def set_editor(self, editor):
        self._editor = editor

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

        if hasattr(self._editor, "find"):
            logger.debug("Search text: " + to_search_txt)
            if options is not None:
                self._editor.find(to_search_txt, options)
            else:
                self._editor.find(to_search_txt)
        else:
            logger.debug("Can't Search text " + to_search_txt)

    def searchBack(self):
        options = QtGui.QTextDocument.FindBackward

        if self.caseBtn.isChecked():
            options = options or QtGui.QTextDocument.FindCaseSensitively

        if self.wholeBtn.isChecked():
            options = options or QtGui.QTextDocument.FindWholeWords

        to_search_txt = self.lineEdit.text()

        if hasattr(self._editor, "find"):
            logger.debug("Search text: " + to_search_txt)
            self._editor.find(to_search_txt, options)
        else:
            logger.debug("Can't Search text " + to_search_txt)

    def replaceall(self):
        # Replace all occurences without interaction

        # Here I am just getting the replacement data
        # from my UI so it will be different for you
        old = self.lineEdit.text()
        new = self.lineEditReplace.text()

        # Beginning of undo block
        cursor = self._editor.textCursor()
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
            r = self._editor.find(old, flags)
            if r:
                qc = self._editor.textCursor()
                if qc.hasSelection():
                    qc.insertText(new)
            else:
                break

        # Mark end of undo block
        cursor.endEditBlock()
