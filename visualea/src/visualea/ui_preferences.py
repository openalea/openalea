# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'preferences.ui'
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

class Ui_Preferences(object):
    def setupUi(self, Preferences):
        Preferences.setObjectName(_fromUtf8("Preferences"))
        Preferences.resize(596, 369)
        self.gridlayout = QtGui.QGridLayout(Preferences)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.buttonBox = QtGui.QDialogButtonBox(Preferences)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridlayout.addWidget(self.buttonBox, 1, 0, 1, 1)
        self.tabWidget = QtGui.QTabWidget(Preferences)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab = QtGui.QWidget()
        self.tab.setObjectName(_fromUtf8("tab"))
        self.gridlayout1 = QtGui.QGridLayout(self.tab)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName(_fromUtf8("gridlayout1"))
        self.label_2 = QtGui.QLabel(self.tab)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridlayout1.addWidget(self.label_2, 0, 0, 1, 1)
        self.pathList = QtGui.QListWidget(self.tab)
        self.pathList.setObjectName(_fromUtf8("pathList"))
        self.gridlayout1.addWidget(self.pathList, 0, 1, 3, 1)
        self.addButton = QtGui.QPushButton(self.tab)
        self.addButton.setObjectName(_fromUtf8("addButton"))
        self.gridlayout1.addWidget(self.addButton, 1, 0, 1, 1)
        self.removeButton = QtGui.QPushButton(self.tab)
        self.removeButton.setObjectName(_fromUtf8("removeButton"))
        self.gridlayout1.addWidget(self.removeButton, 2, 0, 1, 1)
        self.tabWidget.addTab(self.tab, _fromUtf8(""))
        self.tab_2 = QtGui.QWidget()
        self.tab_2.setObjectName(_fromUtf8("tab_2"))
        self.vboxlayout = QtGui.QVBoxLayout(self.tab_2)
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.externalBool = QtGui.QCheckBox(self.tab_2)
        self.externalBool.setObjectName(_fromUtf8("externalBool"))
        self.vboxlayout.addWidget(self.externalBool)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.label_4 = QtGui.QLabel(self.tab_2)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.hboxlayout.addWidget(self.label_4)
        self.commandStr = QtGui.QLineEdit(self.tab_2)
        self.commandStr.setObjectName(_fromUtf8("commandStr"))
        self.hboxlayout.addWidget(self.commandStr)
        self.commandPath = QtGui.QPushButton(self.tab_2)
        self.commandPath.setObjectName(_fromUtf8("commandPath"))
        self.hboxlayout.addWidget(self.commandPath)
        self.vboxlayout.addLayout(self.hboxlayout)
        self.tabWidget.addTab(self.tab_2, _fromUtf8(""))
        self.tab_3 = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_3.sizePolicy().hasHeightForWidth())
        self.tab_3.setSizePolicy(sizePolicy)
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.gridlayout2 = QtGui.QGridLayout(self.tab_3)
        self.gridlayout2.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName(_fromUtf8("gridlayout2"))
        self.label = QtGui.QLabel(self.tab_3)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridlayout2.addWidget(self.label, 0, 0, 1, 1)
        self.dbclickBox = QtGui.QComboBox(self.tab_3)
        self.dbclickBox.setObjectName(_fromUtf8("dbclickBox"))
        self.dbclickBox.addItem(_fromUtf8(""))
        self.dbclickBox.addItem(_fromUtf8(""))
        self.dbclickBox.addItem(_fromUtf8(""))
        self.gridlayout2.addWidget(self.dbclickBox, 0, 1, 1, 1)
        self.comboBox = QtGui.QComboBox(self.tab_3)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.comboBox.addItem(_fromUtf8(""))
        self.gridlayout2.addWidget(self.comboBox, 1, 1, 1, 1)
        self.label_edge_style = QtGui.QLabel(self.tab_3)
        self.label_edge_style.setObjectName(_fromUtf8("label_edge_style"))
        self.gridlayout2.addWidget(self.label_edge_style, 1, 0, 1, 1)
        self.evalCue = QtGui.QCheckBox(self.tab_3)
        self.evalCue.setObjectName(_fromUtf8("evalCue"))
        self.gridlayout2.addWidget(self.evalCue, 2, 0, 1, 2)
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.gridlayout.addWidget(self.tabWidget, 0, 0, 1, 1)

        self.retranslateUi(Preferences)
        self.tabWidget.setCurrentIndex(2)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Preferences.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Preferences.reject)
        QtCore.QMetaObject.connectSlotsByName(Preferences)

    def retranslateUi(self, Preferences):
        Preferences.setWindowTitle(_translate("Preferences", "Preferences", None))
        self.label_2.setText(_translate("Preferences", "Search Path", None))
        self.addButton.setText(_translate("Preferences", "Add", None))
        self.removeButton.setText(_translate("Preferences", "Remove", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("Preferences", "Package Manager", None))
        self.externalBool.setText(_translate("Preferences", "Use External editor", None))
        self.label_4.setText(_translate("Preferences", "Command", None))
        self.commandPath.setText(_translate("Preferences", "...", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Preferences", "Editor", None))
        self.label.setText(_translate("Preferences", "Double click on item", None))
        self.dbclickBox.setItemText(0, _translate("Preferences", "Run + Open (Default)", None))
        self.dbclickBox.setItemText(1, _translate("Preferences", "Run", None))
        self.dbclickBox.setItemText(2, _translate("Preferences", "Open", None))
        self.comboBox.setItemText(0, _translate("Preferences", "Spline (Default)", None))
        self.comboBox.setItemText(1, _translate("Preferences", "Polyline", None))
        self.comboBox.setItemText(2, _translate("Preferences", "Line", None))
        self.label_edge_style.setText(_translate("Preferences", "Edge Style", None))
        self.evalCue.setText(_translate("Preferences", "Show evaluation cue (side effect: slows down evaluation)", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Preferences", "UI", None))

