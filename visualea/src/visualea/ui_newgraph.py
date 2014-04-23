# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newgraph.ui'
#
# Created: Wed Oct 22 16:38:32 2008
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!

from openalea.vpltk.qt import qt

class Ui_NewGraphDialog(object):
    def setupUi(self, NewGraphDialog):
        NewGraphDialog.setObjectName("NewGraphDialog")
        NewGraphDialog.resize(424, 326)
        self.gridlayout = qt.QtGui.QGridLayout(NewGraphDialog)
        self.gridlayout.setContentsMargins(9, 9, 9, 9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")
        self.buttonBox = qt.QtGui.QDialogButtonBox(NewGraphDialog)
        self.buttonBox.setOrientation(qt.QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(qt.QtGui.QDialogButtonBox.Cancel|qt.QtGui.QDialogButtonBox.NoButton|qt.QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox, 5, 0, 1, 4)
        self.nameEdit = qt.QtGui.QLineEdit(NewGraphDialog)
        self.nameEdit.setObjectName("nameEdit")
        self.gridlayout.addWidget(self.nameEdit, 1, 1, 1, 1)
        self.label_2 = qt.QtGui.QLabel(NewGraphDialog)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.descriptionEdit = qt.QtGui.QLineEdit(NewGraphDialog)
        self.descriptionEdit.setObjectName("descriptionEdit")
        self.gridlayout.addWidget(self.descriptionEdit, 3, 1, 1, 1)
        self.label_3 = qt.QtGui.QLabel(NewGraphDialog)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label = qt.QtGui.QLabel(NewGraphDialog)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label, 0, 0, 1, 1)
        self.packageBox = qt.QtGui.QComboBox(NewGraphDialog)
        self.packageBox.setObjectName("packageBox")
        self.gridlayout.addWidget(self.packageBox, 0, 1, 1, 1)
        self.categoryEdit = qt.QtGui.QComboBox(NewGraphDialog)
        self.categoryEdit.setEditable(True)
        self.categoryEdit.setObjectName("categoryEdit")
        self.gridlayout.addWidget(self.categoryEdit, 2, 1, 1, 1)
        self.label_4 = qt.QtGui.QLabel(NewGraphDialog)
        self.label_4.setObjectName("label_4")
        self.gridlayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.ioButton = qt.QtGui.QPushButton(NewGraphDialog)
        self.ioButton.setObjectName("ioButton")
        self.gridlayout.addWidget(self.ioButton, 4, 1, 1, 1)

        self.retranslateUi(NewGraphDialog)
        qt.QtCore.QObject.connect(self.buttonBox, qt.QtCore.SIGNAL("accepted()"), NewGraphDialog.accept)
        qt.QtCore.QObject.connect(self.buttonBox, qt.QtCore.SIGNAL("rejected()"), NewGraphDialog.reject)
        qt.QtCore.QMetaObject.connectSlotsByName(NewGraphDialog)
        NewGraphDialog.setTabOrder(self.packageBox, self.nameEdit)
        NewGraphDialog.setTabOrder(self.nameEdit, self.categoryEdit)
        NewGraphDialog.setTabOrder(self.categoryEdit, self.descriptionEdit)
        NewGraphDialog.setTabOrder(self.descriptionEdit, self.ioButton)
        NewGraphDialog.setTabOrder(self.ioButton, self.buttonBox)

    def retranslateUi(self, NewGraphDialog):
        self.label_2.setText(qt.QtGui.QApplication.translate("NewGraphDialog", "Name", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(qt.QtGui.QApplication.translate("NewGraphDialog", "Category", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.label.setText(qt.QtGui.QApplication.translate("NewGraphDialog", "Package", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(qt.QtGui.QApplication.translate("NewGraphDialog", "Description", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.ioButton.setText(qt.QtGui.QApplication.translate("NewGraphDialog", "Inputs / Outputs", None, qt.QtGui.QApplication.UnicodeUTF8))

