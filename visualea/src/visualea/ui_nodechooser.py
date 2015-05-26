# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nodechooser.ui'
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

class Ui_NodeChooser(object):
    def setupUi(self, NodeChooser):
        NodeChooser.setObjectName(_fromUtf8("NodeChooser"))
        NodeChooser.resize(417, 156)
        self.vboxlayout = QtGui.QVBoxLayout(NodeChooser)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.comboBox = QtGui.QComboBox(NodeChooser)
        self.comboBox.setEditable(True)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.vboxlayout.addWidget(self.comboBox)
        self.buttonBox = QtGui.QDialogButtonBox(NodeChooser)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(NodeChooser)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), NodeChooser.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), NodeChooser.reject)
        QtCore.QMetaObject.connectSlotsByName(NodeChooser)

    def retranslateUi(self, NodeChooser):
        NodeChooser.setWindowTitle(_translate("NodeChooser", "Choose a node", None))

