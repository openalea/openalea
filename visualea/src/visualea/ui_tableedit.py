# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tableedit.ui'
#
# Created: Wed Oct 22 16:38:34 2008
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_TableEditor(object):
    def setupUi(self, TableEditor):
        TableEditor.setObjectName("TableEditor")
        TableEditor.resize(261, 300)
        self.vboxlayout = QtGui.QVBoxLayout(TableEditor)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")
        self.tableWidget = QtGui.QTableWidget(TableEditor)
        self.tableWidget.setObjectName("tableWidget")
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
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(TableEditor)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), TableEditor.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), TableEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(TableEditor)

    def retranslateUi(self, TableEditor):
        TableEditor.setWindowTitle(QtGui.QApplication.translate("TableEditor", "Internals", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("TableEditor", "Key", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("TableEditor", "Value", None, QtGui.QApplication.UnicodeUTF8))

