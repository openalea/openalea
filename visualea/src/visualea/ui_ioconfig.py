# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ioconfig.ui'
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

class Ui_IOConfig(object):
    def setupUi(self, IOConfig):
        IOConfig.setObjectName(_fromUtf8("IOConfig"))
        IOConfig.resize(444, 441)
        self.vboxlayout = QtGui.QVBoxLayout(IOConfig)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.label = QtGui.QLabel(IOConfig)
        self.label.setObjectName(_fromUtf8("label"))
        self.vboxlayout.addWidget(self.label)
        self.inTable = QtGui.QTableView(IOConfig)
        self.inTable.setObjectName(_fromUtf8("inTable"))
        self.vboxlayout.addWidget(self.inTable)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.addInput = QtGui.QPushButton(IOConfig)
        self.addInput.setObjectName(_fromUtf8("addInput"))
        self.hboxlayout.addWidget(self.addInput)
        self.delInput = QtGui.QPushButton(IOConfig)
        self.delInput.setObjectName(_fromUtf8("delInput"))
        self.hboxlayout.addWidget(self.delInput)
        self.vboxlayout.addLayout(self.hboxlayout)
        self.label_2 = QtGui.QLabel(IOConfig)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.vboxlayout.addWidget(self.label_2)
        self.outTable = QtGui.QTableView(IOConfig)
        self.outTable.setObjectName(_fromUtf8("outTable"))
        self.vboxlayout.addWidget(self.outTable)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setObjectName(_fromUtf8("hboxlayout1"))
        self.addOutput = QtGui.QPushButton(IOConfig)
        self.addOutput.setObjectName(_fromUtf8("addOutput"))
        self.hboxlayout1.addWidget(self.addOutput)
        self.delOutput = QtGui.QPushButton(IOConfig)
        self.delOutput.setObjectName(_fromUtf8("delOutput"))
        self.hboxlayout1.addWidget(self.delOutput)
        self.vboxlayout.addLayout(self.hboxlayout1)
        self.buttonBox = QtGui.QDialogButtonBox(IOConfig)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(IOConfig)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), IOConfig.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), IOConfig.reject)
        QtCore.QMetaObject.connectSlotsByName(IOConfig)
        IOConfig.setTabOrder(self.inTable, self.addInput)
        IOConfig.setTabOrder(self.addInput, self.delInput)
        IOConfig.setTabOrder(self.delInput, self.outTable)
        IOConfig.setTabOrder(self.outTable, self.addOutput)
        IOConfig.setTabOrder(self.addOutput, self.delOutput)
        IOConfig.setTabOrder(self.delOutput, self.buttonBox)

    def retranslateUi(self, IOConfig):
        IOConfig.setWindowTitle(_translate("IOConfig", "I/O Configuration", None))
        self.label.setText(_translate("IOConfig", "Inputs", None))
        self.addInput.setText(_translate("IOConfig", "+", None))
        self.delInput.setText(_translate("IOConfig", "-", None))
        self.label_2.setText(_translate("IOConfig", "Outputs", None))
        self.addOutput.setText(_translate("IOConfig", "+", None))
        self.delOutput.setText(_translate("IOConfig", "-", None))

