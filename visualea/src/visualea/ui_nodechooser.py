# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nodechooser.ui'
#
# Created: Fri Feb  1 16:06:26 2008
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_NodeChooser(object):
    def setupUi(self, NodeChooser):
        NodeChooser.setObjectName("NodeChooser")
        NodeChooser.resize(QtCore.QSize(QtCore.QRect(0,0,417,156).size()).expandedTo(NodeChooser.minimumSizeHint()))

        self.vboxlayout = QtGui.QVBoxLayout(NodeChooser)
        self.vboxlayout.setObjectName("vboxlayout")

        self.comboBox = QtGui.QComboBox(NodeChooser)
        self.comboBox.setEditable(True)
        self.comboBox.setObjectName("comboBox")
        self.vboxlayout.addWidget(self.comboBox)

        self.buttonBox = QtGui.QDialogButtonBox(NodeChooser)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(NodeChooser)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),NodeChooser.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),NodeChooser.reject)
        QtCore.QMetaObject.connectSlotsByName(NodeChooser)

    def retranslateUi(self, NodeChooser):
        NodeChooser.setWindowTitle(QtGui.QApplication.translate("NodeChooser", "Choose a node", None, QtGui.QApplication.UnicodeUTF8))

