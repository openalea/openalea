# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'nodechooser.ui'
#
# Created: Fri Feb  1 16:06:26 2008
#      by: PyQt4 UI code generator 4.3.1
#
# WARNING! All changes made in this file will be lost!

from openalea.vpltk.qt import qt

class Ui_NodeChooser(object):
    def setupUi(self, NodeChooser):
        NodeChooser.setObjectName("NodeChooser")
        NodeChooser.resize(qt.QtCore.QSize(qt.QtCore.QRect(0,0,417,156).size()).expandedTo(NodeChooser.minimumSizeHint()))

        self.vboxlayout = qt.QtGui.QVBoxLayout(NodeChooser)
        self.vboxlayout.setObjectName("vboxlayout")

        self.comboBox = qt.QtGui.QComboBox(NodeChooser)
        self.comboBox.setEditable(True)
        self.comboBox.setObjectName("comboBox")
        self.vboxlayout.addWidget(self.comboBox)

        self.buttonBox = qt.QtGui.QDialogButtonBox(NodeChooser)
        self.buttonBox.setOrientation(qt.QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(qt.QtGui.QDialogButtonBox.Cancel|qt.QtGui.QDialogButtonBox.NoButton|qt.QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(NodeChooser)
        qt.QtCore.QObject.connect(self.buttonBox,qt.QtCore.SIGNAL("accepted()"),NodeChooser.accept)
        qt.QtCore.QObject.connect(self.buttonBox,qt.QtCore.SIGNAL("rejected()"),NodeChooser.reject)
        qt.QtCore.QMetaObject.connectSlotsByName(NodeChooser)

    def retranslateUi(self, NodeChooser):
        NodeChooser.setWindowTitle(qt.QtGui.QApplication.translate("NodeChooser", "Choose a node", None, qt.QtGui.QApplication.UnicodeUTF8))

