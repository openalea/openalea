# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tofactory.ui'
#
# Created: Mon Apr 23 18:35:38 2007
#      by: PyQt4 UI code generator 4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,367,154).size()).expandedTo(Dialog.minimumSizeHint()))

        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20,20,56,17))
        self.label.setObjectName("label")

        self.comboBox = QtGui.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(90,10,211,26))
        self.comboBox.setObjectName("comboBox")

        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(-40,100,341,32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.newFactoryButton = QtGui.QPushButton(Dialog)
        self.newFactoryButton.setGeometry(QtCore.QRect(220,50,80,27))
        self.newFactoryButton.setObjectName("newFactoryButton")

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),Dialog.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.comboBox,self.newFactoryButton)
        Dialog.setTabOrder(self.newFactoryButton,self.buttonBox)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Save as Model", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dialog", "Graph", None, QtGui.QApplication.UnicodeUTF8))
        self.newFactoryButton.setText(QtGui.QApplication.translate("Dialog", "New Graph", None, QtGui.QApplication.UnicodeUTF8))

