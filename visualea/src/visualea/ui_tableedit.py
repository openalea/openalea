# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tableedit.ui'
#
# Created: Mon Sep 17 12:18:24 2007
#      by: PyQt4 UI code generator 4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_TableEditor(object):
    def setupUi(self, TableEditor):
        TableEditor.setObjectName("TableEditor")
        TableEditor.resize(QtCore.QSize(QtCore.QRect(0,0,261,300).size()).expandedTo(TableEditor.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(TableEditor)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.tableWidget = QtGui.QTableWidget(TableEditor)
        self.tableWidget.setObjectName("tableWidget")
        self.vboxlayout.addWidget(self.tableWidget)

        self.buttonBox = QtGui.QDialogButtonBox(TableEditor)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(TableEditor)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),TableEditor.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),TableEditor.reject)
        QtCore.QMetaObject.connectSlotsByName(TableEditor)

    def retranslateUi(self, TableEditor):
        TableEditor.setWindowTitle(QtGui.QApplication.translate("TableEditor", "Internals", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)

        headerItem = QtGui.QTableWidgetItem()
        headerItem.setText(QtGui.QApplication.translate("TableEditor", "Key", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(0,headerItem)

        headerItem1 = QtGui.QTableWidgetItem()
        headerItem1.setText(QtGui.QApplication.translate("TableEditor", "Value", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.setHorizontalHeaderItem(1,headerItem1)

