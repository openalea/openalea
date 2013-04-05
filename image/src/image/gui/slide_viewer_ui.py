# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/vmanalysis/visu/slide_viewer.ui'
#
# Created: Tue Jun  8 10:15:01 2010
#      by: PyQt4 UI code generator 4.6
#
# WARNING! All changes made in this file will be lost!

from openalea.vpltk.qt import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(576, 522)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMinimumSize(QtCore.QSize(100, 150))
        self.im_view = QtGui.QWidget(MainWindow)
        self.im_view.setMinimumSize(QtCore.QSize(50, 50))
        self.im_view.setObjectName("im_view")
        self.horizontalLayout = QtGui.QHBoxLayout(self.im_view)
        self.horizontalLayout.setObjectName("horizontalLayout")
        MainWindow.setCentralWidget(self.im_view)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolbar = QtGui.QToolBar(MainWindow)
        self.toolbar.setObjectName("toolbar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolbar)
        self.action_close = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/image/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_close.setIcon(icon)
        self.action_close.setObjectName("action_close")
        self.action_snapshot = QtGui.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/image/snapshot.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_snapshot.setIcon(icon1)
        self.action_snapshot.setObjectName("action_snapshot")
        self.action_rotate_left = QtGui.QAction(MainWindow)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/image/rotate_left.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_rotate_left.setIcon(icon2)
        self.action_rotate_left.setObjectName("action_rotate_left")
        self.action_rotate_right = QtGui.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/image/rotate_right.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_rotate_right.setIcon(icon3)
        self.action_rotate_right.setObjectName("action_rotate_right")
        self.toolbar.addAction(self.action_close)
        self.toolbar.addAction(self.action_snapshot)
        self.toolbar.addAction(self.action_rotate_left)
        self.toolbar.addAction(self.action_rotate_right)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.toolbar.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar", None, QtGui.QApplication.UnicodeUTF8))
        self.action_close.setText(QtGui.QApplication.translate("MainWindow", "close", None, QtGui.QApplication.UnicodeUTF8))
        self.action_close.setToolTip(QtGui.QApplication.translate("MainWindow", "close window", None, QtGui.QApplication.UnicodeUTF8))
        self.action_close.setShortcut(QtGui.QApplication.translate("MainWindow", "Esc", None, QtGui.QApplication.UnicodeUTF8))
        self.action_snapshot.setText(QtGui.QApplication.translate("MainWindow", "snapshot", None, QtGui.QApplication.UnicodeUTF8))
        self.action_snapshot.setToolTip(QtGui.QApplication.translate("MainWindow", "take snapshot", None, QtGui.QApplication.UnicodeUTF8))
        self.action_rotate_left.setText(QtGui.QApplication.translate("MainWindow", "rotate left", None, QtGui.QApplication.UnicodeUTF8))
        self.action_rotate_left.setToolTip(QtGui.QApplication.translate("MainWindow", "rotate left", None, QtGui.QApplication.UnicodeUTF8))
        self.action_rotate_right.setText(QtGui.QApplication.translate("MainWindow", "rotate right", None, QtGui.QApplication.UnicodeUTF8))
        self.action_rotate_right.setToolTip(QtGui.QApplication.translate("MainWindow", "rotate right", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc
