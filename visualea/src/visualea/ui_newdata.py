# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newdata.ui'
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

class Ui_NewDataDialog(object):
    def setupUi(self, NewDataDialog):
        NewDataDialog.setObjectName(_fromUtf8("NewDataDialog"))
        NewDataDialog.resize(444, 169)
        self.gridlayout = QtGui.QGridLayout(NewDataDialog)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.label = QtGui.QLabel(NewDataDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridlayout.addWidget(self.label, 0, 0, 1, 1)
        self.packageBox = QtGui.QComboBox(NewDataDialog)
        self.packageBox.setObjectName(_fromUtf8("packageBox"))
        self.gridlayout.addWidget(self.packageBox, 0, 1, 1, 2)
        self.label_2 = QtGui.QLabel(NewDataDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridlayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.nameEdit = QtGui.QLineEdit(NewDataDialog)
        self.nameEdit.setObjectName(_fromUtf8("nameEdit"))
        self.gridlayout.addWidget(self.nameEdit, 1, 1, 1, 1)
        self.browseButton = QtGui.QPushButton(NewDataDialog)
        self.browseButton.setObjectName(_fromUtf8("browseButton"))
        self.gridlayout.addWidget(self.browseButton, 1, 2, 1, 1)
        self.label_4 = QtGui.QLabel(NewDataDialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridlayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.descriptionEdit = QtGui.QLineEdit(NewDataDialog)
        self.descriptionEdit.setObjectName(_fromUtf8("descriptionEdit"))
        self.gridlayout.addWidget(self.descriptionEdit, 2, 1, 1, 2)
        self.buttonBox = QtGui.QDialogButtonBox(NewDataDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 3, 0, 1, 3)

        self.retranslateUi(NewDataDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), NewDataDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), NewDataDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewDataDialog)
        NewDataDialog.setTabOrder(self.packageBox, self.nameEdit)
        NewDataDialog.setTabOrder(self.nameEdit, self.descriptionEdit)
        NewDataDialog.setTabOrder(self.descriptionEdit, self.buttonBox)

    def retranslateUi(self, NewDataDialog):
        NewDataDialog.setWindowTitle(_translate("NewDataDialog", "Import data", None))
        self.label.setText(_translate("NewDataDialog", "Package", None))
        self.label_2.setText(_translate("NewDataDialog", "File", None))
        self.browseButton.setText(_translate("NewDataDialog", "...", None))
        self.label_4.setText(_translate("NewDataDialog", "Description", None))

