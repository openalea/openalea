# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newdata.ui'
#
# Created: Wed Apr  2 00:35:40 2008
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from openalea.vpltk.qt import qt

class Ui_NewDataDialog(object):
    def setupUi(self, NewDataDialog):
        NewDataDialog.setObjectName("NewDataDialog")
        NewDataDialog.resize(qt.QtCore.QSize(qt.QtCore.QRect(0,0,444,169).size()).expandedTo(NewDataDialog.minimumSizeHint()))

        self.gridlayout = qt.QtGui.QGridLayout(NewDataDialog)
        self.gridlayout.setObjectName("gridlayout")

        self.label = qt.QtGui.QLabel(NewDataDialog)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,0,0,1,1)

        self.packageBox = qt.QtGui.QComboBox(NewDataDialog)
        self.packageBox.setObjectName("packageBox")
        self.gridlayout.addWidget(self.packageBox,0,1,1,2)

        self.label_2 = qt.QtGui.QLabel(NewDataDialog)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,1,0,1,1)

        self.nameEdit = qt.QtGui.QLineEdit(NewDataDialog)
        self.nameEdit.setObjectName("nameEdit")
        self.gridlayout.addWidget(self.nameEdit,1,1,1,1)

        self.browseButton = qt.QtGui.QPushButton(NewDataDialog)
        self.browseButton.setObjectName("browseButton")
        self.gridlayout.addWidget(self.browseButton,1,2,1,1)

        self.label_4 = qt.QtGui.QLabel(NewDataDialog)
        self.label_4.setObjectName("label_4")
        self.gridlayout.addWidget(self.label_4,2,0,1,1)

        self.descriptionEdit = qt.QtGui.QLineEdit(NewDataDialog)
        self.descriptionEdit.setObjectName("descriptionEdit")
        self.gridlayout.addWidget(self.descriptionEdit,2,1,1,2)

        self.buttonBox = qt.QtGui.QDialogButtonBox(NewDataDialog)
        self.buttonBox.setOrientation(qt.QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(qt.QtGui.QDialogButtonBox.Cancel|qt.QtGui.QDialogButtonBox.NoButton|qt.QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox,3,0,1,3)

        self.retranslateUi(NewDataDialog)
        qt.QtCore.QObject.connect(self.buttonBox,qt.QtCore.SIGNAL("accepted()"),NewDataDialog.accept)
        qt.QtCore.QObject.connect(self.buttonBox,qt.QtCore.SIGNAL("rejected()"),NewDataDialog.reject)
        qt.QtCore.QMetaObject.connectSlotsByName(NewDataDialog)
        NewDataDialog.setTabOrder(self.packageBox,self.nameEdit)
        NewDataDialog.setTabOrder(self.nameEdit,self.descriptionEdit)
        NewDataDialog.setTabOrder(self.descriptionEdit,self.buttonBox)

    def retranslateUi(self, NewDataDialog):
        NewDataDialog.setWindowTitle(qt.QtGui.QApplication.translate("NewDataDialog", "Import data", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.label.setText(qt.QtGui.QApplication.translate("NewDataDialog", "Package", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(qt.QtGui.QApplication.translate("NewDataDialog", "File", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.browseButton.setText(qt.QtGui.QApplication.translate("NewDataDialog", "...", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(qt.QtGui.QApplication.translate("NewDataDialog", "Description", None, qt.QtGui.QApplication.UnicodeUTF8))

