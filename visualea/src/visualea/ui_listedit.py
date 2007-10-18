# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'listedit.ui'
#
# Created: Tue Oct  2 13:56:54 2007
#      by: PyQt4 UI code generator 4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_ListEdit(object):
    def setupUi(self, ListEdit):
        ListEdit.setObjectName("ListEdit")
        ListEdit.resize(QtCore.QSize(QtCore.QRect(0,0,400,300).size()).expandedTo(ListEdit.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(ListEdit)
        self.vboxlayout.setObjectName("vboxlayout")

        self.listWidget = QtGui.QListWidget(ListEdit)
        self.listWidget.setObjectName("listWidget")
        self.vboxlayout.addWidget(self.listWidget)

        self.buttonBox = QtGui.QDialogButtonBox(ListEdit)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(ListEdit)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),ListEdit.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),ListEdit.reject)
        QtCore.QMetaObject.connectSlotsByName(ListEdit)

    def retranslateUi(self, ListEdit):
        ListEdit.setWindowTitle(QtGui.QApplication.translate("ListEdit", "Dialog", None, QtGui.QApplication.UnicodeUTF8))

