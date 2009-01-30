# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tofactory.ui'
#
# Created: Wed Oct 22 16:38:33 2008
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!


__license__ = "Cecill-C"
__revision__ = " $Id$"

from PyQt4 import QtCore, QtGui

class Ui_FactorySelector(object):
    def setupUi(self, FactorySelector):
        FactorySelector.setObjectName("FactorySelector")
        FactorySelector.resize(371, 143)
        icon = QtGui.QIcon()
        icon.addFile(":/icons/diagram.png")
        FactorySelector.setWindowIcon(icon)
        self.vboxlayout = QtGui.QVBoxLayout(FactorySelector)
        self.vboxlayout.setObjectName("vboxlayout")
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setMargin(0)
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
        self.label_2 = QtGui.QLabel(FactorySelector)
        self.label_2.setObjectName("label_2")
        self.vboxlayout.addWidget(self.label_2)
        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")
        self.label_3 = QtGui.QLabel(FactorySelector)
        self.label_3.setObjectName("label_3")
        self.hboxlayout1.addWidget(self.label_3)
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
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), FactorySelector.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), FactorySelector.reject)
        QtCore.QMetaObject.connectSlotsByName(FactorySelector)
        FactorySelector.setTabOrder(self.comboBox, self.newFactoryButton)
        FactorySelector.setTabOrder(self.newFactoryButton, self.buttonBox)

    def retranslateUi(self, FactorySelector):
        FactorySelector.setWindowTitle(QtGui.QApplication.translate("FactorySelector", "Selector", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("FactorySelector", "Select a Composite Node :", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("FactorySelector", "Or", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("FactorySelector", "Create a new Composite Node", None, QtGui.QApplication.UnicodeUTF8))
        self.newFactoryButton.setText(QtGui.QApplication.translate("FactorySelector", "New", None, QtGui.QApplication.UnicodeUTF8))

import images_rc
