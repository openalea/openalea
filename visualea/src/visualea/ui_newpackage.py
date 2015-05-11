# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newpackage.ui'
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

class Ui_NewPackageDialog(object):
    def setupUi(self, NewPackageDialog):
        NewPackageDialog.setObjectName(_fromUtf8("NewPackageDialog"))
        NewPackageDialog.resize(479, 435)
        self.vboxlayout = QtGui.QVBoxLayout(NewPackageDialog)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.gridlayout = QtGui.QGridLayout()
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.authorsEdit = QtGui.QLineEdit(NewPackageDialog)
        self.authorsEdit.setObjectName(_fromUtf8("authorsEdit"))
        self.gridlayout.addWidget(self.authorsEdit, 4, 1, 1, 1)
        self.label_2 = QtGui.QLabel(NewPackageDialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridlayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.pathButton = QtGui.QPushButton(NewPackageDialog)
        self.pathButton.setObjectName(_fromUtf8("pathButton"))
        self.gridlayout.addWidget(self.pathButton, 7, 2, 1, 1)
        self.label = QtGui.QLabel(NewPackageDialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridlayout.addWidget(self.label, 0, 0, 1, 1)
        self.versionEdit = QtGui.QLineEdit(NewPackageDialog)
        self.versionEdit.setObjectName(_fromUtf8("versionEdit"))
        self.gridlayout.addWidget(self.versionEdit, 2, 1, 1, 1)
        self.label_7 = QtGui.QLabel(NewPackageDialog)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridlayout.addWidget(self.label_7, 6, 0, 1, 1)
        self.label_8 = QtGui.QLabel(NewPackageDialog)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridlayout.addWidget(self.label_8, 7, 0, 1, 1)
        self.pathEdit = QtGui.QLineEdit(NewPackageDialog)
        self.pathEdit.setObjectName(_fromUtf8("pathEdit"))
        self.gridlayout.addWidget(self.pathEdit, 7, 1, 1, 1)
        self.label_6 = QtGui.QLabel(NewPackageDialog)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridlayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.descriptionEdit = QtGui.QLineEdit(NewPackageDialog)
        self.descriptionEdit.setObjectName(_fromUtf8("descriptionEdit"))
        self.gridlayout.addWidget(self.descriptionEdit, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(NewPackageDialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridlayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.institutesEdit = QtGui.QLineEdit(NewPackageDialog)
        self.institutesEdit.setObjectName(_fromUtf8("institutesEdit"))
        self.gridlayout.addWidget(self.institutesEdit, 5, 1, 1, 1)
        self.urlEdit = QtGui.QLineEdit(NewPackageDialog)
        self.urlEdit.setObjectName(_fromUtf8("urlEdit"))
        self.gridlayout.addWidget(self.urlEdit, 6, 1, 1, 1)
        self.label_4 = QtGui.QLabel(NewPackageDialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridlayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.nameEdit = QtGui.QLineEdit(NewPackageDialog)
        self.nameEdit.setObjectName(_fromUtf8("nameEdit"))
        self.gridlayout.addWidget(self.nameEdit, 0, 1, 1, 1)
        self.label_5 = QtGui.QLabel(NewPackageDialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridlayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.licenseEdit = QtGui.QLineEdit(NewPackageDialog)
        self.licenseEdit.setObjectName(_fromUtf8("licenseEdit"))
        self.gridlayout.addWidget(self.licenseEdit, 3, 1, 1, 1)
        self.vboxlayout.addLayout(self.gridlayout)
        self.buttonBox = QtGui.QDialogButtonBox(NewPackageDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(NewPackageDialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), NewPackageDialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), NewPackageDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewPackageDialog)
        NewPackageDialog.setTabOrder(self.nameEdit, self.descriptionEdit)
        NewPackageDialog.setTabOrder(self.descriptionEdit, self.versionEdit)
        NewPackageDialog.setTabOrder(self.versionEdit, self.licenseEdit)
        NewPackageDialog.setTabOrder(self.licenseEdit, self.authorsEdit)
        NewPackageDialog.setTabOrder(self.authorsEdit, self.institutesEdit)
        NewPackageDialog.setTabOrder(self.institutesEdit, self.urlEdit)
        NewPackageDialog.setTabOrder(self.urlEdit, self.pathEdit)
        NewPackageDialog.setTabOrder(self.pathEdit, self.pathButton)
        NewPackageDialog.setTabOrder(self.pathButton, self.buttonBox)

    def retranslateUi(self, NewPackageDialog):
        NewPackageDialog.setWindowTitle(_translate("NewPackageDialog", "Package", None))
        self.label_2.setText(_translate("NewPackageDialog", "Description", None))
        self.pathButton.setText(_translate("NewPackageDialog", "...", None))
        self.label.setText(_translate("NewPackageDialog", "Name", None))
        self.label_7.setText(_translate("NewPackageDialog", "URL", None))
        self.label_8.setText(_translate("NewPackageDialog", "Path", None))
        self.label_6.setText(_translate("NewPackageDialog", "Institutes", None))
        self.label_3.setText(_translate("NewPackageDialog", "Version", None))
        self.label_4.setText(_translate("NewPackageDialog", "License", None))
        self.label_5.setText(_translate("NewPackageDialog", "Authors", None))

