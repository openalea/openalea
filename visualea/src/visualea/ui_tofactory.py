# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'tofactory.ui'
#
# Created: Wed Oct 22 16:38:33 2008
#      by: PyQt4 UI code generator 4.4.3
#
# WARNING! All changes made in this file will be lost!


__license__ = "Cecill-C"
__revision__ = " $Id$"

from openalea.vpltk.qt import qt

class Ui_FactorySelector(object):
    def setupUi(self, FactorySelector):
        FactorySelector.setObjectName("FactorySelector")
        FactorySelector.resize(371, 143)
        icon = qt.QtGui.QIcon()
        icon.addFile(":/icons/diagram.png")
        FactorySelector.setWindowIcon(icon)
        self.vboxlayout = qt.QtGui.QVBoxLayout(FactorySelector)
        self.vboxlayout.setObjectName("vboxlayout")
        self.hboxlayout = qt.QtGui.QHBoxLayout()
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setContentsMargins(0, 0, 0, 0)
        self.hboxlayout.setObjectName("hboxlayout")
        self.label = qt.QtGui.QLabel(FactorySelector)
        self.label.setLayoutDirection(qt.QtCore.Qt.LeftToRight)
        self.label.setScaledContents(True)
        self.label.setAlignment(qt.QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.hboxlayout.addWidget(self.label)
        self.comboBox = qt.QtGui.QComboBox(FactorySelector)
        self.comboBox.setObjectName("comboBox")
        self.hboxlayout.addWidget(self.comboBox)
        self.vboxlayout.addLayout(self.hboxlayout)
        self.label_2 = qt.QtGui.QLabel(FactorySelector)
        self.label_2.setObjectName("label_2")
        self.vboxlayout.addWidget(self.label_2)
        self.hboxlayout1 = qt.QtGui.QHBoxLayout()
        self.hboxlayout1.setObjectName("hboxlayout1")
        self.label_3 = qt.QtGui.QLabel(FactorySelector)
        self.label_3.setObjectName("label_3")
        self.hboxlayout1.addWidget(self.label_3)
        self.newFactoryButton = qt.QtGui.QPushButton(FactorySelector)
        self.newFactoryButton.setObjectName("newFactoryButton")
        self.hboxlayout1.addWidget(self.newFactoryButton)
        self.vboxlayout.addLayout(self.hboxlayout1)
        self.buttonBox = qt.QtGui.QDialogButtonBox(FactorySelector)
        self.buttonBox.setOrientation(qt.QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(qt.QtGui.QDialogButtonBox.Cancel|qt.QtGui.QDialogButtonBox.NoButton|qt.QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.vboxlayout.addWidget(self.buttonBox)

        self.retranslateUi(FactorySelector)
        qt.QtCore.QObject.connect(self.buttonBox, qt.QtCore.SIGNAL("accepted()"), FactorySelector.accept)
        qt.QtCore.QObject.connect(self.buttonBox, qt.QtCore.SIGNAL("rejected()"), FactorySelector.reject)
        qt.QtCore.QMetaObject.connectSlotsByName(FactorySelector)
        FactorySelector.setTabOrder(self.comboBox, self.newFactoryButton)
        FactorySelector.setTabOrder(self.newFactoryButton, self.buttonBox)

    def retranslateUi(self, FactorySelector):
        FactorySelector.setWindowTitle(qt.QtGui.QApplication.translate("FactorySelector", "Selector", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.label.setText(qt.QtGui.QApplication.translate("FactorySelector", "Select a Composite Node :", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(qt.QtGui.QApplication.translate("FactorySelector", "Or", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(qt.QtGui.QApplication.translate("FactorySelector", "Create a new Composite Node", None, qt.QtGui.QApplication.UnicodeUTF8))
        self.newFactoryButton.setText(qt.QtGui.QApplication.translate("FactorySelector", "New", None, qt.QtGui.QApplication.UnicodeUTF8))

import images_rc
