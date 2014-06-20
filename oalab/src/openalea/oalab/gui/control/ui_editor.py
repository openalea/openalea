# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/openalea/oalab/gui/control/editor.ui'
#
# Created: Fri Jun 20 11:42:26 2014
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

class Ui_ControlEditor(object):
    def setupUi(self, ControlEditor):
        ControlEditor.setObjectName(_fromUtf8("ControlEditor"))
        ControlEditor.resize(476, 311)
        self._layout = QtGui.QVBoxLayout(ControlEditor)
        self._layout.setObjectName(_fromUtf8("_layout"))
        self.label_4 = QtGui.QLabel(ControlEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self._layout.addWidget(self.label_4)
        self.widget_control = QtGui.QWidget(ControlEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_control.sizePolicy().hasHeightForWidth())
        self.widget_control.setSizePolicy(sizePolicy)
        self.widget_control.setObjectName(_fromUtf8("widget_control"))
        self._layout_control = QtGui.QFormLayout(self.widget_control)
        self._layout_control.setFieldGrowthPolicy(QtGui.QFormLayout.ExpandingFieldsGrow)
        self._layout_control.setRowWrapPolicy(QtGui.QFormLayout.DontWrapRows)
        self._layout_control.setContentsMargins(1, 0, 0, 15)
        self._layout_control.setObjectName(_fromUtf8("_layout_control"))
        self.label = QtGui.QLabel(self.widget_control)
        self.label.setMinimumSize(QtCore.QSize(60, 0))
        self.label.setObjectName(_fromUtf8("label"))
        self._layout_control.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.e_name = QtGui.QLineEdit(self.widget_control)
        self.e_name.setObjectName(_fromUtf8("e_name"))
        self._layout_control.setWidget(0, QtGui.QFormLayout.FieldRole, self.e_name)
        self.l_type = QtGui.QLabel(self.widget_control)
        self.l_type.setMinimumSize(QtCore.QSize(60, 0))
        self.l_type.setObjectName(_fromUtf8("l_type"))
        self._layout_control.setWidget(1, QtGui.QFormLayout.LabelRole, self.l_type)
        self.cb_interface = QtGui.QComboBox(self.widget_control)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_interface.sizePolicy().hasHeightForWidth())
        self.cb_interface.setSizePolicy(sizePolicy)
        self.cb_interface.setObjectName(_fromUtf8("cb_interface"))
        self._layout_control.setWidget(1, QtGui.QFormLayout.FieldRole, self.cb_interface)
        self.label_3 = QtGui.QLabel(self.widget_control)
        self.label_3.setMinimumSize(QtCore.QSize(60, 0))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self._layout_control.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.cb_widget = QtGui.QComboBox(self.widget_control)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_widget.sizePolicy().hasHeightForWidth())
        self.cb_widget.setSizePolicy(sizePolicy)
        self.cb_widget.setObjectName(_fromUtf8("cb_widget"))
        self._layout_control.setWidget(2, QtGui.QFormLayout.FieldRole, self.cb_widget)
        self._layout.addWidget(self.widget_control)
        self.label_5 = QtGui.QLabel(ControlEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self._layout.addWidget(self.label_5)
        self.groupBox = QtGui.QGroupBox(ControlEditor)
        self.groupBox.setAlignment(QtCore.Qt.AlignCenter)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget_preview = QtGui.QLabel(self.groupBox)
        self.widget_preview.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_preview.sizePolicy().hasHeightForWidth())
        self.widget_preview.setSizePolicy(sizePolicy)
        self.widget_preview.setStyleSheet(_fromUtf8("color: rgb(168, 193, 255);"))
        self.widget_preview.setFrameShape(QtGui.QFrame.Box)
        self.widget_preview.setFrameShadow(QtGui.QFrame.Plain)
        self.widget_preview.setLineWidth(1)
        self.widget_preview.setAlignment(QtCore.Qt.AlignCenter)
        self.widget_preview.setObjectName(_fromUtf8("widget_preview"))
        self.verticalLayout.addWidget(self.widget_preview)
        self._layout.addWidget(self.groupBox)
        self._l_constraints = QtGui.QLabel(ControlEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self._l_constraints.sizePolicy().hasHeightForWidth())
        self._l_constraints.setSizePolicy(sizePolicy)
        self._l_constraints.setObjectName(_fromUtf8("_l_constraints"))
        self._layout.addWidget(self._l_constraints)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self._layout.addItem(spacerItem)

        self.retranslateUi(ControlEditor)
        QtCore.QMetaObject.connectSlotsByName(ControlEditor)

    def retranslateUi(self, ControlEditor):
        ControlEditor.setWindowTitle(_translate("ControlEditor", "Form", None))
        self.label_4.setText(_translate("ControlEditor", "<html><head/><body><p><span style=\" font-weight:600;\">Control</span></p></body></html>", None))
        self.label.setText(_translate("ControlEditor", "Name", None))
        self.l_type.setText(_translate("ControlEditor", "Type", None))
        self.label_3.setText(_translate("ControlEditor", "Widget", None))
        self.label_5.setText(_translate("ControlEditor", "<html><head/><body><p><span style=\" font-weight:600;\">Preview</span></p></body></html>", None))
        self.widget_preview.setText(_translate("ControlEditor", "Preview", None))
        self._l_constraints.setText(_translate("ControlEditor", "<html><head/><body><p><span style=\" font-weight:600;\">Constraints</span></p></body></html>", None))

