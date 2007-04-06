# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newgraph.ui'
#
# Created: Fri Apr  6 11:45:11 2007
#      by: PyQt4 UI code generator 4.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt4 import QtCore, QtGui

class Ui_NewGraphDialog(object):
    def setupUi(self, NewGraphDialog):
        NewGraphDialog.setObjectName("NewGraphDialog")
        NewGraphDialog.resize(QtCore.QSize(QtCore.QRect(0,0,424,260).size()).expandedTo(NewGraphDialog.minimumSizeHint()))

        self.gridlayout = QtGui.QGridLayout(NewGraphDialog)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.packageBox = QtGui.QComboBox(NewGraphDialog)
        self.packageBox.setObjectName("packageBox")
        self.gridlayout.addWidget(self.packageBox,0,1,1,1)

        self.label = QtGui.QLabel(NewGraphDialog)
        self.label.setObjectName("label")
        self.gridlayout.addWidget(self.label,0,0,1,1)

        self.label_2 = QtGui.QLabel(NewGraphDialog)
        self.label_2.setObjectName("label_2")
        self.gridlayout.addWidget(self.label_2,1,0,1,1)

        self.label_5 = QtGui.QLabel(NewGraphDialog)
        self.label_5.setObjectName("label_5")
        self.gridlayout.addWidget(self.label_5,2,2,1,1)

        self.inBox = QtGui.QSpinBox(NewGraphDialog)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.inBox.sizePolicy().hasHeightForWidth())
        self.inBox.setSizePolicy(sizePolicy)
        self.inBox.setObjectName("inBox")
        self.gridlayout.addWidget(self.inBox,2,3,1,1)

        self.outBox = QtGui.QSpinBox(NewGraphDialog)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(0),QtGui.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.outBox.sizePolicy().hasHeightForWidth())
        self.outBox.setSizePolicy(sizePolicy)
        self.outBox.setObjectName("outBox")
        self.gridlayout.addWidget(self.outBox,3,3,1,1)

        self.label_6 = QtGui.QLabel(NewGraphDialog)
        self.label_6.setObjectName("label_6")
        self.gridlayout.addWidget(self.label_6,3,2,1,1)

        self.nameEdit = QtGui.QLineEdit(NewGraphDialog)
        self.nameEdit.setObjectName("nameEdit")
        self.gridlayout.addWidget(self.nameEdit,1,1,1,1)

        self.categoryEdit = QtGui.QComboBox(NewGraphDialog)
        self.categoryEdit.setEditable(True)
        self.categoryEdit.setObjectName("categoryEdit")
        self.gridlayout.addWidget(self.categoryEdit,2,1,1,1)

        self.descriptionEdit = QtGui.QLineEdit(NewGraphDialog)
        self.descriptionEdit.setObjectName("descriptionEdit")
        self.gridlayout.addWidget(self.descriptionEdit,3,1,1,1)

        self.label_3 = QtGui.QLabel(NewGraphDialog)
        self.label_3.setObjectName("label_3")
        self.gridlayout.addWidget(self.label_3,2,0,1,1)

        self.label_4 = QtGui.QLabel(NewGraphDialog)
        self.label_4.setObjectName("label_4")
        self.gridlayout.addWidget(self.label_4,3,0,1,1)

        self.buttonBox = QtGui.QDialogButtonBox(NewGraphDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.NoButton|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridlayout.addWidget(self.buttonBox,4,0,1,4)

        self.retranslateUi(NewGraphDialog)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("accepted()"),NewGraphDialog.accept)
        QtCore.QObject.connect(self.buttonBox,QtCore.SIGNAL("rejected()"),NewGraphDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(NewGraphDialog)
        NewGraphDialog.setTabOrder(self.nameEdit,self.descriptionEdit)
        NewGraphDialog.setTabOrder(self.descriptionEdit,self.inBox)
        NewGraphDialog.setTabOrder(self.inBox,self.outBox)
        NewGraphDialog.setTabOrder(self.outBox,self.buttonBox)

    def retranslateUi(self, NewGraphDialog):
        self.label.setText(QtGui.QApplication.translate("NewGraphDialog", "Package", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("NewGraphDialog", "Name", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("NewGraphDialog", "Nb Inputs", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("NewGraphDialog", "Nb Outputs", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("NewGraphDialog", "Category", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("NewGraphDialog", "Description", None, QtGui.QApplication.UnicodeUTF8))

