# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_container.ui'
#
# Created: Wed Jun 11 09:07:37 2014
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from Qt import QtCore, QtGui, QtWidgets

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class Ui_WidgetContainer(object):
    def setupUi(self, WidgetContainer):
        WidgetContainer.setObjectName(_fromUtf8("WidgetContainer"))
        WidgetContainer.resize(517, 370)
        self.gridlayout = QtWidgets.QGridLayout(WidgetContainer)
        self.gridlayout.setMargin(0)
        self.gridlayout.setSpacing(0)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.widget = QtWidgets.QWidget(WidgetContainer)
        self.widget.setObjectName(_fromUtf8("widget"))
        self.layout = QtWidgets.QVBoxLayout(self.widget)
        self.layout.setSpacing(0)
        self.layout.setMargin(0)
        self.layout.setObjectName(_fromUtf8("layout"))
        self.gridlayout.addWidget(self.widget, 1, 1, 1, 1)
        self.bottom_right = QtWidgets.QLabel(WidgetContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bottom_right.sizePolicy().hasHeightForWidth())
        self.bottom_right.setSizePolicy(sizePolicy)
        self.bottom_right.setMinimumSize(QtCore.QSize(20, 20))
        self.bottom_right.setMaximumSize(QtCore.QSize(20, 20))
        self.bottom_right.setObjectName(_fromUtf8("bottom_right"))
        self.gridlayout.addWidget(self.bottom_right, 2, 2, 1, 1)
        self.top_right = QtWidgets.QLabel(WidgetContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.top_right.sizePolicy().hasHeightForWidth())
        self.top_right.setSizePolicy(sizePolicy)
        self.top_right.setMinimumSize(QtCore.QSize(20, 20))
        self.top_right.setMaximumSize(QtCore.QSize(20, 20))
        self.top_right.setObjectName(_fromUtf8("top_right"))
        self.gridlayout.addWidget(self.top_right, 0, 2, 1, 1)
        self.top_left = QtWidgets.QLabel(WidgetContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.top_left.sizePolicy().hasHeightForWidth())
        self.top_left.setSizePolicy(sizePolicy)
        self.top_left.setObjectName(_fromUtf8("top_left"))
        self.gridlayout.addWidget(self.top_left, 0, 0, 1, 1)
        self.bottom_left = QtWidgets.QLabel(WidgetContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bottom_left.sizePolicy().hasHeightForWidth())
        self.bottom_left.setSizePolicy(sizePolicy)
        self.bottom_left.setObjectName(_fromUtf8("bottom_left"))
        self.gridlayout.addWidget(self.bottom_left, 2, 0, 1, 1)
        self.l_title = QtWidgets.QLabel(WidgetContainer)
        self.l_title.setStyleSheet(_fromUtf8("background-color: rgba(255, 255, 255, 0);"))
        self.l_title.setAlignment(QtCore.Qt.AlignCenter)
        self.l_title.setObjectName(_fromUtf8("l_title"))
        self.gridlayout.addWidget(self.l_title, 0, 1, 1, 1)
        self.line = QtWidgets.QFrame(WidgetContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line.sizePolicy().hasHeightForWidth())
        self.line.setSizePolicy(sizePolicy)
        self.line.setMinimumSize(QtCore.QSize(20, 0))
        self.line.setMaximumSize(QtCore.QSize(20, 16777215))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridlayout.addWidget(self.line, 1, 0, 1, 1)
        self.line_2 = QtWidgets.QFrame(WidgetContainer)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_2.sizePolicy().hasHeightForWidth())
        self.line_2.setSizePolicy(sizePolicy)
        self.line_2.setMinimumSize(QtCore.QSize(20, 0))
        self.line_2.setMaximumSize(QtCore.QSize(20, 16777215))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.gridlayout.addWidget(self.line_2, 1, 2, 1, 1)
        self.widget_2 = QtWidgets.QWidget(WidgetContainer)
        self.widget_2.setObjectName(_fromUtf8("widget_2"))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget_2)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pb_grab = QtWidgets.QPushButton(self.widget_2)
        self.pb_grab.setCheckable(True)
        self.pb_grab.setChecked(False)
        self.pb_grab.setFlat(False)
        self.pb_grab.setObjectName(_fromUtf8("pb_grab"))
        self.horizontalLayout.addWidget(self.pb_grab)
        self.pb_resize = QtWidgets.QPushButton(self.widget_2)
        self.pb_resize.setCheckable(True)
        self.pb_resize.setChecked(False)
        self.pb_resize.setFlat(False)
        self.pb_resize.setObjectName(_fromUtf8("pb_resize"))
        self.horizontalLayout.addWidget(self.pb_resize)
        self.gridlayout.addWidget(self.widget_2, 2, 1, 1, 1)

        self.retranslateUi(WidgetContainer)
        QtCore.QMetaObject.connectSlotsByName(WidgetContainer)

    def retranslateUi(self, WidgetContainer):
        WidgetContainer.setWindowTitle(_translate("WidgetContainer", "Form", None))
        self.bottom_right.setText(_translate("WidgetContainer", "┘", None))
        self.top_right.setText(_translate("WidgetContainer", "┐", None))
        self.top_left.setText(_translate("WidgetContainer", "┌", None))
        self.bottom_left.setText(_translate("WidgetContainer", "└", None))
        self.l_title.setText(_translate("WidgetContainer", "title", None))
        self.pb_grab.setText(_translate("WidgetContainer", "G", None))
        self.pb_resize.setText(_translate("WidgetContainer", "S", None))
