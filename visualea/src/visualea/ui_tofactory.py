# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tofactory.ui'
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

class Ui_FactorySelector(object):
    def setupUi(self, FactorySelector):
        FactorySelector.setObjectName(_fromUtf8("FactorySelector"))
        FactorySelector.resize(371, 143)
        icon = QtGui.QIcon()
        icon.addFile(_fromUtf8(":/icons/diagram.png"))
        FactorySelector.setWindowIcon(icon)
        self.vboxlayout = QtGui.QVBoxLayout(FactorySelector)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.label = QtGui.QLabel(FactorySelector)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.hboxlayout.addWidget(self.label)
        self.comboBox = QtGui.QComboBox(FactorySelector)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.hboxlayout.addWidget(self.comboBox)
        self.vboxlayout.addLayout(self.hboxlayout)
        self.label_2 = QtGui.QLabel(FactorySelector)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.vboxlayout.addWidget(self.label_2)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName(_fromUtf8("hboxlayout1"))
        self.label_3 = QtGui.QLabel(FactorySelector)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.hboxlayout1.addWidget(self.label_3)
        self.newFactoryButton = QtGui.QPushButton(FactorySelector)
        self.newFactoryButton.setObjectName(_fromUtf8("newFactoryButton"))
        self.hboxlayout1.addWidget(self.newFactoryButton)
        self.vboxlayout.addLayout(self.hboxlayout1)
        self.buttonBox = QtGui.QDialogButtonBox(FactorySelector)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(FactorySelector)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), FactorySelector.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), FactorySelector.reject)
        QtCore.QMetaObject.connectSlotsByName(FactorySelector)
        FactorySelector.setTabOrder(self.comboBox, self.newFactoryButton)
        FactorySelector.setTabOrder(self.newFactoryButton, self.buttonBox)

    def retranslateUi(self, FactorySelector):
        FactorySelector.setWindowTitle(_translate("FactorySelector", "Selector", None))
        self.label.setText(_translate("FactorySelector", "Select a Composite Node :", None))
        self.label_2.setText(_translate("FactorySelector", "Or", None))
        self.label_3.setText(_translate("FactorySelector", "Create a new Composite Node", None))
        self.newFactoryButton.setText(_translate("FactorySelector", "New", None))

import images_rc
