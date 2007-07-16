# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Sat Jul 14 17:30:05 2007
#      by: PyQt4 UI code generator 4.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,779,662).size()).expandedTo(MainWindow.minimumSizeHint()))
        MainWindow.setWindowIcon(QtGui.QIcon(":/icons/openalea_icon.png"))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.vboxlayout = QtGui.QVBoxLayout(self.centralwidget)
        self.vboxlayout.setMargin(9)
        self.vboxlayout.setSpacing(6)
        self.vboxlayout.setObjectName("vboxlayout")

        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.vboxlayout.addWidget(self.label)

        self.packageList = QtGui.QListWidget(self.centralwidget)
        self.packageList.setObjectName("packageList")
        self.vboxlayout.addWidget(self.packageList)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.proceedButton = QtGui.QPushButton(self.centralwidget)
        self.proceedButton.setObjectName("proceedButton")
        self.hboxlayout.addWidget(self.proceedButton)

        self.refreshButton = QtGui.QPushButton(self.centralwidget)
        self.refreshButton.setObjectName("refreshButton")
        self.hboxlayout.addWidget(self.refreshButton)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setObjectName("label_3")
        self.vboxlayout.addWidget(self.label_3)

        self.listWidget = QtGui.QListWidget(self.centralwidget)
        self.listWidget.setObjectName("listWidget")
        self.vboxlayout.addWidget(self.listWidget)

        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName("label_2")
        self.vboxlayout.addWidget(self.label_2)

        self.locationList = QtGui.QListWidget(self.centralwidget)

        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Policy(7),QtGui.QSizePolicy.Policy(7))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.locationList.sizePolicy().hasHeightForWidth())
        self.locationList.setSizePolicy(sizePolicy)
        self.locationList.setObjectName("locationList")
        self.vboxlayout.addWidget(self.locationList)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.addLocButton = QtGui.QPushButton(self.centralwidget)
        self.addLocButton.setObjectName("addLocButton")
        self.hboxlayout1.addWidget(self.addLocButton)

        self.removeLocButton = QtGui.QPushButton(self.centralwidget)
        self.removeLocButton.setObjectName("removeLocButton")
        self.hboxlayout1.addWidget(self.removeLocButton)
        self.vboxlayout.addLayout(self.hboxlayout1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,779,25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.packageList,self.proceedButton)
        MainWindow.setTabOrder(self.proceedButton,self.refreshButton)
        MainWindow.setTabOrder(self.refreshButton,self.listWidget)
        MainWindow.setTabOrder(self.listWidget,self.locationList)
        MainWindow.setTabOrder(self.locationList,self.addLocButton)
        MainWindow.setTabOrder(self.addLocButton,self.removeLocButton)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "OpenAlea Installer", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Packages", None, QtGui.QApplication.UnicodeUTF8))
        self.proceedButton.setText(QtGui.QApplication.translate("MainWindow", "Proceed", None, QtGui.QApplication.UnicodeUTF8))
        self.refreshButton.setText(QtGui.QApplication.translate("MainWindow", "Refresh", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Log", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "Locations", None, QtGui.QApplication.UnicodeUTF8))
        self.addLocButton.setText(QtGui.QApplication.translate("MainWindow", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.removeLocButton.setText(QtGui.QApplication.translate("MainWindow", "Remove", None, QtGui.QApplication.UnicodeUTF8))

import images_rc
