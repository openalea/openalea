# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newgraph.ui'
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

class Ui_NewGraphDialog(object):
    def setupUi(self, NewGraphDialog):
        NewGraphDialog.setObjectName(_fromUtf8("NewGraphDialog"))
        NewGraphDialog.resize(424, 326)
        NewGraphDialog.setWindowTitle(_fromUtf8(""))
        self.gridlayout = QtGui.QGridLayout(NewGraphDialog)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.buttonBox = QtGui.QDialogButtonBox(NewGraphDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 5, 0, 1, 4)
        self.nameEdit = QtGui.QLineEdit(NewGraphDialog)
        self.nameEdit.setObjectName(_fromUtf8("nameEdit"))
        self.gridlayout.addWidget(self.nameEdit, 1, 1, 1, 1)
        self.label_2 = QtGui.QLabel(NewGraphDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridlayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.descriptionEdit = QtGui.QLineEdit(NewGraphDialog)
        self.descriptionEdit.setObjectName(_fromUtf8("descriptionEdit"))
        self.gridlayout.addWidget(self.descriptionEdit, 3, 1, 1, 1)
        self.label_3 = QtGui.QLabel(NewGraphDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridlayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label = QtGui.QLabel(NewGraphDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridlayout.addWidget(self.label, 0, 0, 1, 1)
        self.packageBox = QtGui.QComboBox(NewGraphDialog)
        self.packageBox.setObjectName(_fromUtf8("packageBox"))
        self.gridlayout.addWidget(self.packageBox, 0, 1, 1, 1)
        self.categoryEdit = QtGui.QComboBox(NewGraphDialog)
        self.categoryEdit.setEditable(True)
        self.categoryEdit.setObjectName(_fromUtf8("categoryEdit"))
        self.gridlayout.addWidget(self.categoryEdit, 2, 1, 1, 1)
        self.label_4 = QtGui.QLabel(NewGraphDialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridlayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.ioButton = QtGui.QPushButton(NewGraphDialog)
        self.ioButton.setObjectName(_fromUtf8("ioButton"))
        self.gridlayout.addWidget(self.ioButton, 4, 1, 1, 1)

        self.retranslateUi(NewGraphDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), NewGraphDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), NewGraphDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewGraphDialog)
        NewGraphDialog.setTabOrder(self.packageBox, self.nameEdit)
        NewGraphDialog.setTabOrder(self.nameEdit, self.categoryEdit)
        NewGraphDialog.setTabOrder(self.categoryEdit, self.descriptionEdit)
        NewGraphDialog.setTabOrder(self.descriptionEdit, self.ioButton)
        NewGraphDialog.setTabOrder(self.ioButton, self.buttonBox)

    def retranslateUi(self, NewGraphDialog):
        self.label_2.setText(_translate("NewGraphDialog", "Name", None))
        self.label_3.setText(_translate("NewGraphDialog", "Category", None))
        self.label.setText(_translate("NewGraphDialog", "Package", None))
        self.label_4.setText(_translate("NewGraphDialog", "Description", None))
        self.ioButton.setText(_translate("NewGraphDialog", "Inputs / Outputs", None))

