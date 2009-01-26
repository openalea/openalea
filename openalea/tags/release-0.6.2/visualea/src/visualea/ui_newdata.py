# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newdata.ui'
#
# Created: Wed Apr  2 00:35:40 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_NewDataDialog(object):
    def setupUi(self, NewDataDialog):
        NewDataDialog.setObjectName("NewDataDialog")
        NewDataDialog.resize(QtCore.QSize(QtCore.QRect(0,0,444,169).size()).expandedTo(NewDataDialog.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(NewDataDialog)
        self.gridlayout.setObjectName("gridlayout")

        self.label = QtGui.QLabel(NewDataDialog)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,0,0,1,1)

        self.packageBox = QtGui.QComboBox(NewDataDialog)
        self.packageBox.setObjectName("packageBox")
        self.gridlayout.addWidget(self.packageBox,0,1,1,2)

        self.label_2 = QtGui.QLabel(NewDataDialog)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,1,0,1,1)

        self.nameEdit = QtGui.QLineEdit(NewDataDialog)
        self.nameEdit.setObjectName("nameEdit")
        self.gridlayout.addWidget(self.nameEdit,1,1,1,1)

        self.browseButton = QtGui.QPushButton(NewDataDialog)
        self.browseButton.setObjectName("browseButton")
        self.gridlayout.addWidget(self.browseButton,1,2,1,1)

        self.label_4 = QtGui.QLabel(NewDataDialog)
        self.label_4.setObjectName("label_4")
        self.gridlayout.addWidget(self.label_4,2,0,1,1)

        self.descriptionEdit = QtGui.QLineEdit(NewDataDialog)
        self.descriptionEdit.setObjectName("descriptionEdit")
        self.gridlayout.addWidget(self.descriptionEdit,2,1,1,2)

        self.buttonBox = QtGui.QDialogButtonBox(NewDataDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox,3,0,1,3)

        self.retranslateUi(NewDataDialog)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),NewDataDialog.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),NewDataDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewDataDialog)
        NewDataDialog.setTabOrder(self.packageBox,self.nameEdit)
        NewDataDialog.setTabOrder(self.nameEdit,self.descriptionEdit)
        NewDataDialog.setTabOrder(self.descriptionEdit,self.buttonBox)

    def retranslateUi(self, NewDataDialog):
        NewDataDialog.setWindowTitle(QtGui.QApplication.translate("NewDataDialog", "Import data", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("NewDataDialog", "Package", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("NewDataDialog", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.browseButton.setText(QtGui.QApplication.translate("NewDataDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("NewDataDialog", "Description", None, QtGui.QApplication.UnicodeUTF8))

