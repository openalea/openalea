# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newgraph.ui'
#
# Created: Wed Jun 27 16:59:22 2007
#      by: PyQt4 UI code generator 4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_NewGraphDialog(object):
    def setupUi(self, NewGraphDialog):
        NewGraphDialog.setObjectName("NewGraphDialog")
        NewGraphDialog.resize(QtCore.QSize(QtCore.QRect(0,0,424,326).size()).expandedTo(NewGraphDialog.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(NewGraphDialog)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.buttonBox = QtGui.QDialogButtonBox(NewGraphDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox,5,0,1,4)

        self.nameEdit = QtGui.QLineEdit(NewGraphDialog)
        self.nameEdit.setObjectName("nameEdit")
        self.gridlayout.addWidget(self.nameEdit,1,1,1,1)

        self.label_2 = QtGui.QLabel(NewGraphDialog)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,1,0,1,1)

        self.descriptionEdit = QtGui.QLineEdit(NewGraphDialog)
        self.descriptionEdit.setObjectName("descriptionEdit")
        self.gridlayout.addWidget(self.descriptionEdit,3,1,1,1)

        self.label_3 = QtGui.QLabel(NewGraphDialog)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3,2,0,1,1)

        self.label = QtGui.QLabel(NewGraphDialog)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,0,0,1,1)

        self.packageBox = QtGui.QComboBox(NewGraphDialog)
        self.packageBox.setObjectName("packageBox")
        self.gridlayout.addWidget(self.packageBox,0,1,1,1)

        self.categoryEdit = QtGui.QComboBox(NewGraphDialog)
        self.categoryEdit.setEditable(True)
        self.categoryEdit.setObjectName("categoryEdit")
        self.gridlayout.addWidget(self.categoryEdit,2,1,1,1)

        self.label_4 = QtGui.QLabel(NewGraphDialog)
        self.label_4.setObjectName("label_4")
        self.gridlayout.addWidget(self.label_4,3,0,1,1)

        self.ioButton = QtGui.QPushButton(NewGraphDialog)
        self.ioButton.setObjectName("ioButton")
        self.gridlayout.addWidget(self.ioButton,4,1,1,1)

        self.retranslateUi(NewGraphDialog)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),NewGraphDialog.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),NewGraphDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewGraphDialog)
        NewGraphDialog.setTabOrder(self.packageBox,self.nameEdit)
        NewGraphDialog.setTabOrder(self.nameEdit,self.categoryEdit)
        NewGraphDialog.setTabOrder(self.categoryEdit,self.descriptionEdit)
        NewGraphDialog.setTabOrder(self.descriptionEdit,self.buttonBox)

    def retranslateUi(self, NewGraphDialog):
        self.label_2.setText(QtGui.QApplication.translate("NewGraphDialog", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("NewGraphDialog", "Category", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("NewGraphDialog", "Package", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("NewGraphDialog", "Description", None, QtGui.QApplication.UnicodeUTF8))
        self.ioButton.setText(QtGui.QApplication.translate("NewGraphDialog", "Inputs / Outputs", None, QtGui.QApplication.UnicodeUTF8))

