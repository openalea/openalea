# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ioconfig.ui'
#
# Created: Wed Oct 22 16:38:34 2008
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from openalea.vpltk.qt import qt

class Ui_IOConfig(object):
    def setupUi(self, IOConfig):
        IOConfig.setObjectName("IOConfig")
        IOConfig.resize(444, 441)
        self.vboxlayout = qt.QtGui.QVBoxLayout(IOConfig)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setContentsMargins(9, 9, 9, 9)
        self.vboxlayout.setObjectName("vboxlayout")
        self.label = qt.QtGui.QLabel(IOConfig)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)
        self.inTable = qt.QtGui.QTableView(IOConfig)
        self.inTable.setObjectName("inTable")
        self.vboxlayout.addWidget(self.inTable)
        self.hboxlayout = qt.QtGui.QHBoxLayout()
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setContentsMargins(0, 0, 0, 0)
        self.hboxlayout.setObjectName("hboxlayout")
        self.addInput = qt.QtGui.QPushButton(IOConfig)
        self.addInput.setObjectName("addInput")
        self.hboxlayout.addWidget(self.addInput)
        self.delInput = qt.QtGui.QPushButton(IOConfig)
        self.delInput.setObjectName("delInput")
        self.hboxlayout.addWidget(self.delInput)
        self.vboxlayout.addLayout(self.hboxlayout)
        self.label_2 = qt.QtGui.QLabel(IOConfig)
        self.label_2.setObjectName("label_2")
        self.vboxlayout.addWidget(self.label_2)
        self.outTable = qt.QtGui.QTableView(IOConfig)
        self.outTable.setObjectName("outTable")
        self.vboxlayout.addWidget(self.outTable)
        self.hboxlayout1 = qt.QtGui.QHBoxLayout()
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setContentsMargins(0, 0, 0, 0)
        self.hboxlayout1.setObjectName("hboxlayout1")
        self.addOutput = qt.QtGui.QPushButton(IOConfig)
        self.addOutput.setObjectName("addOutput")
        self.hboxlayout1.addWidget(self.addOutput)
        self.delOutput = qt.QtGui.QPushButton(IOConfig)
        self.delOutput.setObjectName("delOutput")
        self.hboxlayout1.addWidget(self.delOutput)
        self.vboxlayout.addLayout(self.hboxlayout1)
        self.buttonBox = qt.QtGui.QDialogButtonBox(IOConfig)
        self.buttonBox.setOrientation(qt.QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(qt.QtGui.QDialogButtonBox.Cancel|qt.QtGui.QDialogButtonBox.NoButton|qt.QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(IOConfig)
        qt.QtCore.QObject.connect(self.buttonBox, qt.QtCore.SIGNAL("accepted()"), IOConfig.accept)
        qt.QtCore.QObject.connect(self.buttonBox, qt.QtCore.SIGNAL("rejected()"), IOConfig.reject)
        qt.QtCore.QMetaObject.connectSlotsByName(IOConfig)
        IOConfig.setTabOrder(self.inTable, self.addInput)
        IOConfig.setTabOrder(self.addInput, self.delInput)
        IOConfig.setTabOrder(self.delInput, self.outTable)
        IOConfig.setTabOrder(self.outTable, self.addOutput)
        IOConfig.setTabOrder(self.addOutput, self.delOutput)
        IOConfig.setTabOrder(self.delOutput, self.buttonBox)

    def retranslateUi(self, IOConfig):
        IOConfig.setWindowTitle(qt.QtGui.QApplication.translate("IOConfig", "I/O Configuration", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.label.setText(qt.QtGui.QApplication.translate("IOConfig", "Inputs", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.addInput.setText(qt.QtGui.QApplication.translate("IOConfig", "+", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.delInput.setText(qt.QtGui.QApplication.translate("IOConfig", "-", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(qt.QtGui.QApplication.translate("IOConfig", "Outputs", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.addOutput.setText(qt.QtGui.QApplication.translate("IOConfig", "+", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.delOutput.setText(qt.QtGui.QApplication.translate("IOConfig", "-", None, qt.QtGui.QApplication.UnicodeUTF8))

