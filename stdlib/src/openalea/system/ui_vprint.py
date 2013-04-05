# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'resources/visualprint.ui'
#
# Created: Tue Nov 18 17:08:28 2008
#      by: PyQt4 UI code generator 4.4.2
#
# WARNING! All changes made in this file will be lost!
"""tobe done"""

__revision__ = "$Id$"
__license__ = "Cecill-C"

from openalea.vpltk.qt import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(288,170)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.captionText = QtGui.QLabel(Dialog)
        self.captionText.setObjectName("captionText")
        self.gridLayout.addWidget(self.captionText,0,0,1,1)
        self.valueDisplay = QtGui.QTextEdit(Dialog)
        self.valueDisplay.setReadOnly(True)
        self.valueDisplay.setTabStopWidth(20)
        self.valueDisplay.setObjectName("valueDisplay")
        self.gridLayout.addWidget(self.valueDisplay,1,0,1,2)
        spacerItem = QtGui.QSpacerItem(330,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem,2,0,1,1)
        self.okButton = QtGui.QPushButton(Dialog)
        self.okButton.setObjectName("okButton")
        self.gridLayout.addWidget(self.okButton,2,1,1,1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.okButton,QtCore.SIGNAL("clicked()"),Dialog.accept)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Value Display", None, QtGui.QApplication.UnicodeUTF8))
        self.captionText.setText(QtGui.QApplication.translate("Dialog", "Value is", None, QtGui.QApplication.UnicodeUTF8))
        self.okButton.setText(QtGui.QApplication.translate("Dialog", "Ok", None, QtGui.QApplication.UnicodeUTF8))

