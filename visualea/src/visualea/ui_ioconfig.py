# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ioconfig.ui'
#
# Created: Fri Jun 29 10:54:05 2007
#      by: PyQt4 UI code generator 4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_IOConfig(object):
    def setupUi(self, IOConfig):
        IOConfig.setObjectName("IOConfig")
        IOConfig.resize(QtCore.QSize(QtCore.QRect(0,0,291,528).size()).expandedTo(IOConfig.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(IOConfig)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label = QtGui.QLabel(IOConfig)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        self.inTable = QtGui.QTableWidget(IOConfig)
        self.inTable.setObjectName("inTable")
        self.vboxlayout.addWidget(self.inTable)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.addInput = QtGui.QPushButton(IOConfig)
        self.addInput.setObjectName("addInput")
        self.hboxlayout.addWidget(self.addInput)

        self.delInput = QtGui.QPushButton(IOConfig)
        self.delInput.setObjectName("delInput")
        self.hboxlayout.addWidget(self.delInput)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.label_2 = QtGui.QLabel(IOConfig)
        self.label_2.setObjectName("label_2")
        self.vboxlayout.addWidget(self.label_2)

        self.outTable = QtGui.QTableWidget(IOConfig)
        self.outTable.setObjectName("outTable")
        self.vboxlayout.addWidget(self.outTable)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.addOutput = QtGui.QPushButton(IOConfig)
        self.addOutput.setObjectName("addOutput")
        self.hboxlayout1.addWidget(self.addOutput)

        self.delOutput = QtGui.QPushButton(IOConfig)
        self.delOutput.setObjectName("delOutput")
        self.hboxlayout1.addWidget(self.delOutput)
        self.vboxlayout.addLayout(self.hboxlayout1)

        self.buttonBox = QtGui.QDialogButtonBox(IOConfig)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(IOConfig)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),IOConfig.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),IOConfig.reject)
        QtCore.QMetaObject.connectSlotsByName(IOConfig)

    def retranslateUi(self, IOConfig):
        IOConfig.setWindowTitle(QtGui.QApplication.translate("IOConfig", "I/O Configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("IOConfig", "Inputs", None, QtGui.QApplication.UnicodeUTF8))
        self.inTable.clear()
        self.inTable.setColumnCount(2)
        self.inTable.setRowCount(0)

        headerItem = QtGui.QTableWidgetItem()
        headerItem.setText(QtGui.QApplication.translate("IOConfig", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.inTable.setHorizontalHeaderItem(0,headerItem)

        headerItem1 = QtGui.QTableWidgetItem()
        headerItem1.setText(QtGui.QApplication.translate("IOConfig", "Interface", None, QtGui.QApplication.UnicodeUTF8))
        self.inTable.setHorizontalHeaderItem(1,headerItem1)
        self.addInput.setText(QtGui.QApplication.translate("IOConfig", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.delInput.setText(QtGui.QApplication.translate("IOConfig", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("IOConfig", "Outputs", None, QtGui.QApplication.UnicodeUTF8))
        self.outTable.clear()
        self.outTable.setColumnCount(2)
        self.outTable.setRowCount(0)

        headerItem2 = QtGui.QTableWidgetItem()
        headerItem2.setText(QtGui.QApplication.translate("IOConfig", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.outTable.setHorizontalHeaderItem(0,headerItem2)

        headerItem3 = QtGui.QTableWidgetItem()
        headerItem3.setText(QtGui.QApplication.translate("IOConfig", "Interface", None, QtGui.QApplication.UnicodeUTF8))
        self.outTable.setHorizontalHeaderItem(1,headerItem3)
        self.addOutput.setText(QtGui.QApplication.translate("IOConfig", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.delOutput.setText(QtGui.QApplication.translate("IOConfig", "-", None, QtGui.QApplication.UnicodeUTF8))

