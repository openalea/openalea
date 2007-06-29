# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tofactory.ui'
#
# Created: Fri Jun 29 10:54:04 2007
#      by: PyQt4 UI code generator 4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_FactorySelector(object):
    def setupUi(self, FactorySelector):
        FactorySelector.setObjectName("FactorySelector")
        FactorySelector.resize(QtCore.QSize(QtCore.QRect(0,0,208,219).size()).expandedTo(FactorySelector.minimumSizeHint()))
        FactorySelector.setWindowIcon(QtGui.QIcon(":/icons/diagram.png"))

        self.vboxlayout = QtGui.QVBoxLayout(FactorySelector)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.label = QtGui.QLabel(FactorySelector)
        self.label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label.setScaledContents(True)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.hboxlayout.addWidget(self.label)

        self.comboBox = QtGui.QComboBox(FactorySelector)
        self.comboBox.setObjectName("comboBox")
        self.hboxlayout.addWidget(self.comboBox)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.newFactoryButton = QtGui.QPushButton(FactorySelector)
        self.newFactoryButton.setObjectName("newFactoryButton")
        self.hboxlayout1.addWidget(self.newFactoryButton)
        self.vboxlayout.addLayout(self.hboxlayout1)

        self.buttonBox = QtGui.QDialogButtonBox(FactorySelector)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(FactorySelector)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),FactorySelector.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),FactorySelector.reject)
        QtCore.QMetaObject.connectSlotsByName(FactorySelector)
        FactorySelector.setTabOrder(self.comboBox,self.newFactoryButton)
        FactorySelector.setTabOrder(self.newFactoryButton,self.buttonBox)

    def retranslateUi(self, FactorySelector):
        FactorySelector.setWindowTitle(QtGui.QApplication.translate("FactorySelector", "Selector", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("FactorySelector", "Composite Node :", None, QtGui.QApplication.UnicodeUTF8))
        self.newFactoryButton.setText(QtGui.QApplication.translate("FactorySelector", "New Composite Node", None, QtGui.QApplication.UnicodeUTF8))

import images_rc
