# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'listedit.ui'
#
# Created: Tue Oct  2 13:56:54 2007
#      by: PyQt4 UI code generator 4.2
#
# WARNING! All changes made in this file will be lost!

from openalea.vpltk.qt import qt

class Ui_ListEdit(object):
    def setupUi(self, ListEdit):
        ListEdit.setObjectName("ListEdit")
        ListEdit.resize(qt.QtCore.QSize(qt.QtCore.QRect(0,0,400,300).size()).expandedTo(ListEdit.minimumSizeHint()))

        self.vboxlayout = qt.QtGui.QVBoxLayout(ListEdit)
        self.vboxlayout.setObjectName("vboxlayout")

        self.listWidget = qt.QtGui.QListWidget(ListEdit)
        self.listWidget.setObjectName("listWidget")
        self.vboxlayout.addWidget(self.listWidget)

        self.buttonBox = qt.QtGui.QDialogButtonBox(ListEdit)
        self.buttonBox.setOrientation(qt.QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(qt.QtGui.QDialogButtonBox.Cancel|qt.QtGui.QDialogButtonBox.NoButton|qt.QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(ListEdit)
        qt.QtCore.QObject.connect(self.buttonBox,qt.QtCore.SIGNAL("accepted()"),ListEdit.accept)
        qt.QtCore.QObject.connect(self.buttonBox,qt.QtCore.SIGNAL("rejected()"),ListEdit.reject)
        qt.QtCore.QMetaObject.connectSlotsByName(ListEdit)

    def retranslateUi(self, ListEdit):
        ListEdit.setWindowTitle(qt.QtGui.QApplication.translate("ListEdit", "Dialog", None, qt.QtGui.QApplication.UnicodeUTF8))

