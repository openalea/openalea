# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tableedit.ui'
#
# Created: Mon May 11 14:54:41 2015
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_TableEditor(object):
    def setupUi(self, TableEditor):
        TableEditor.setObjectName(_fromUtf8("TableEditor"))
        TableEditor.resize(261, 300)
        self.vboxlayout = QtGui.QVBoxLayout(TableEditor)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.tableWidget = QtGui.QTableWidget(TableEditor)
        self.tableWidget.setObjectName(_fromUtf8("tableWidget"))
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.vboxlayout.addWidget(self.tableWidget)
        self.buttonBox = QtGui.QDialogButtonBox(TableEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(TableEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), TableEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), TableEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(TableEditor)

    def retranslateUi(self, TableEditor):
        TableEditor.setWindowTitle(_translate("TableEditor", "Internals", None))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("TableEditor", "Key", None))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("TableEditor", "Value", None))

