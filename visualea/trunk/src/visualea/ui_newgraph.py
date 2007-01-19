# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newgraph.ui'
#
# Created: Thu Jan 18 14:59:37 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_NewGraphDialog(object):
    def setupUi(self, NewGraphDialog):
        NewGraphDialog.setObjectName("NewGraphDialog")
        NewGraphDialog.resize(QtCore.QSize(QtCore.QRect(0,0,372,229).size()).expandedTo(NewGraphDialog.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(NewGraphDialog)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label_4 = QtGui.QLabel(NewGraphDialog)
        self.label_4.setObjectName("label_4")
        self.vboxlayout.addWidget(self.label_4)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.label = QtGui.QLabel(NewGraphDialog)
        self.label.setObjectName("label")
        self.hboxlayout.addWidget(self.label)

        self.nameEdit = QtGui.QLineEdit(NewGraphDialog)
        self.nameEdit.setObjectName("nameEdit")
        self.hboxlayout.addWidget(self.nameEdit)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.inBox = QtGui.QSpinBox(NewGraphDialog)
        self.inBox.setObjectName("inBox")
        self.hboxlayout1.addWidget(self.inBox)

        self.label_2 = QtGui.QLabel(NewGraphDialog)
        self.label_2.setObjectName("label_2")
        self.hboxlayout1.addWidget(self.label_2)
        self.vboxlayout.addLayout(self.hboxlayout1)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setMargin(0)
        self.hboxlayout2.setSpacing(6)
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.outBox = QtGui.QSpinBox(NewGraphDialog)
        self.outBox.setObjectName("outBox")
        self.hboxlayout2.addWidget(self.outBox)

        self.label_3 = QtGui.QLabel(NewGraphDialog)
        self.label_3.setObjectName("label_3")
        self.hboxlayout2.addWidget(self.label_3)
        self.vboxlayout.addLayout(self.hboxlayout2)

        self.buttonBox = QtGui.QDialogButtonBox(NewGraphDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(NewGraphDialog)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),NewGraphDialog.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),NewGraphDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewGraphDialog)

    def retranslateUi(self, NewGraphDialog):
        NewGraphDialog.setWindowTitle(QtGui.QApplication.translate("NewGraphDialog", "New Network", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("NewGraphDialog", "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
        "p, li { white-space: pre-wrap; }\n"
        "</style></head><body style=\" font-family:\'Sans Serif\'; font-size:9pt; font-weight:400; font-style:normal; text-decoration:none;\">\n"
        "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:13pt; font-weight:600;\">New Network</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("NewGraphDialog", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("NewGraphDialog", "Inputs", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("NewGraphDialog", "Outputs", None, QtGui.QApplication.UnicodeUTF8))

