# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'listedit.ui'
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

class Ui_ListEdit(object):
    def setupUi(self, ListEdit):
        ListEdit.setObjectName(_fromUtf8("ListEdit"))
        ListEdit.resize(400, 300)
        self.vboxlayout = QtGui.QVBoxLayout(ListEdit)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.listWidget = QtGui.QListWidget(ListEdit)
        self.listWidget.setObjectName(_fromUtf8("listWidget"))
        self.vboxlayout.addWidget(self.listWidget)
        self.buttonBox = QtGui.QDialogButtonBox(ListEdit)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(ListEdit)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), ListEdit.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), ListEdit.reject)
        QtCore.QMetaObject.connectSlotsByName(ListEdit)

    def retranslateUi(self, ListEdit):
        ListEdit.setWindowTitle(_translate("ListEdit", "Dialog", None))

