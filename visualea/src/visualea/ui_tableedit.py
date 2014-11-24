# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tableedit.ui'
#
# Created: Wed Oct 22 16:38:34 2008
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from openalea.vpltk.qt import qt

class Ui_TableEditor(object):
    def setupUi(self, TableEditor):
        TableEditor.setObjectName("TableEditor")
        TableEditor.resize(261, 300)
        self.vboxlayout = qt.QtGui.QVBoxLayout(TableEditor)
        self.vboxlayout.setContentsMargins(9, 9, 9, 9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")
        self.tableWidget = qt.QtGui.QTableWidget(TableEditor)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(2)
        self.tableWidget.setRowCount(0)
        item = qt.QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = qt.QtGui.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.vboxlayout.addWidget(self.tableWidget)
        self.buttonBox = qt.QtGui.QDialogButtonBox(TableEditor)
        self.buttonBox.setOrientation(qt.QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(qt.QtGui.QDialogButtonBox.Cancel|qt.QtGui.QDialogButtonBox.NoButton|qt.QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(TableEditor)
        qt.QtCore.QObject.connect(self.buttonBox, qt.QtCore.SIGNAL("accepted()"), TableEditor.accept)
        qt.QtCore.QObject.connect(self.buttonBox, qt.QtCore.SIGNAL("rejected()"), TableEditor.reject)
        qt.QtCore.QMetaObject.connectSlotsByName(TableEditor)

    def retranslateUi(self, TableEditor):
        TableEditor.setWindowTitle(qt.QtGui.QApplication.translate("TableEditor", "Internals", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(0).setText(qt.QtGui.QApplication.translate("TableEditor", "Key", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.horizontalHeaderItem(1).setText(qt.QtGui.QApplication.translate("TableEditor", "Value", None, qt.QtGui.QApplication.UnicodeUTF8))

