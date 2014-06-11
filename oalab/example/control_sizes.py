# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'control_sizes.ui'
#
# Created: Thu Jun  5 14:49:13 2014
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(647, 356)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.line = QtGui.QFrame(Form)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.gridLayout.addWidget(self.line, 1, 2, 2, 1)
        self.hline = QtGui.QWidget(Form)
        self.hline.setMinimumSize(QtCore.QSize(200, 30))
        self.hline.setMaximumSize(QtCore.QSize(16777215, 30))
        self.hline.setStyleSheet(_fromUtf8("background-color: rgb(170, 255, 184);"))
        self.hline.setObjectName(_fromUtf8("hline"))
        self.l_hline = QtGui.QHBoxLayout(self.hline)
        self.l_hline.setMargin(0)
        self.l_hline.setObjectName(_fromUtf8("l_hline"))
        self.gridLayout.addWidget(self.hline, 1, 1, 1, 1)
        self.large = QtGui.QWidget(Form)
        self.large.setMinimumSize(QtCore.QSize(200, 200))
        self.large.setMaximumSize(QtCore.QSize(300, 300))
        self.large.setObjectName(_fromUtf8("large"))
        self.l_large = QtGui.QHBoxLayout(self.large)
        self.l_large.setMargin(0)
        self.l_large.setObjectName(_fromUtf8("l_large"))
        self.gridLayout.addWidget(self.large, 2, 1, 1, 1)
        self.vline = QtGui.QWidget(Form)
        self.vline.setMinimumSize(QtCore.QSize(30, 200))
        self.vline.setMaximumSize(QtCore.QSize(30, 16777215))
        self.vline.setStyleSheet(_fromUtf8("background-color: rgb(255, 226, 212);"))
        self.vline.setObjectName(_fromUtf8("vline"))
        self.l_vline = QtGui.QHBoxLayout(self.vline)
        self.l_vline.setMargin(0)
        self.l_vline.setObjectName(_fromUtf8("l_vline"))
        self.gridLayout.addWidget(self.vline, 1, 0, 2, 1)
        self.small = QtGui.QWidget(Form)
        self.small.setMinimumSize(QtCore.QSize(50, 50))
        self.small.setMaximumSize(QtCore.QSize(50, 50))
        self.small.setStyleSheet(_fromUtf8("background-color: rgb(170, 160, 255);"))
        self.small.setObjectName(_fromUtf8("small"))
        self.l_small = QtGui.QHBoxLayout(self.small)
        self.l_small.setMargin(0)
        self.l_small.setObjectName(_fromUtf8("l_small"))
        self.gridLayout.addWidget(self.small, 3, 1, 1, 1)
        self.responsive = QtGui.QWidget(Form)
        self.responsive.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);"))
        self.responsive.setObjectName(_fromUtf8("responsive"))
        self.l_responsive = QtGui.QHBoxLayout(self.responsive)
        self.l_responsive.setMargin(0)
        self.l_responsive.setObjectName(_fromUtf8("l_responsive"))
        self.gridLayout.addWidget(self.responsive, 1, 3, 4, 1)
        self.l_title = QtGui.QLabel(Form)
        self.l_title.setObjectName(_fromUtf8("l_title"))
        self.gridLayout.addWidget(self.l_title, 0, 0, 1, 4)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))
        self.l_title.setText(_translate("Form", "Title", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

