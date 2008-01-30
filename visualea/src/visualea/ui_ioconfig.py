# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ioconfig.ui'
#
# Created: Wed Jan 30 10:45:37 2008
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_IOConfig(object):
    def setupUi(self, IOConfig):
        IOConfig.setObjectName("IOConfig")
        IOConfig.resize(QtCore.QSize(QtCore.QRect(0,0,444,441).size()).expandedTo(IOConfig.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(IOConfig)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label = QtGui.QLabel(IOConfig)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        self.inTable = QtGui.QTableView(IOConfig)
        self.inTable.setObjectName("inTable")
        self.vboxlayout.addWidget(self.inTable)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(0)
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

        self.outTable = QtGui.QTableView(IOConfig)
        self.outTable.setObjectName("outTable")
        self.vboxlayout.addWidget(self.outTable)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setMargin(0)
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
        IOConfig.setTabOrder(self.inTable,self.addInput)
        IOConfig.setTabOrder(self.addInput,self.delInput)
        IOConfig.setTabOrder(self.delInput,self.outTable)
        IOConfig.setTabOrder(self.outTable,self.addOutput)
        IOConfig.setTabOrder(self.addOutput,self.delOutput)
        IOConfig.setTabOrder(self.delOutput,self.buttonBox)

    def retranslateUi(self, IOConfig):
        IOConfig.setWindowTitle(QtGui.QApplication.translate("IOConfig", "I/O Configuration", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("IOConfig", "Inputs", None, QtGui.QApplication.UnicodeUTF8))
        self.addInput.setText(QtGui.QApplication.translate("IOConfig", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.delInput.setText(QtGui.QApplication.translate("IOConfig", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("IOConfig", "Outputs", None, QtGui.QApplication.UnicodeUTF8))
        self.addOutput.setText(QtGui.QApplication.translate("IOConfig", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.delOutput.setText(QtGui.QApplication.translate("IOConfig", "-", None, QtGui.QApplication.UnicodeUTF8))

