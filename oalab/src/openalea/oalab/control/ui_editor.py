# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/openalea/oalab/gui/control/editor.ui'
#
# Created: Fri Jun 20 15:26:19 2014
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

class Ui_ControlEditor(object):
    def setupUi(self, ControlEditor):
        ControlEditor.setObjectName(_fromUtf8("ControlEditor"))
        ControlEditor.resize(263, 293)
        self._layout = QtWidgets.QVBoxLayout(ControlEditor)
        self._layout.setSpacing(5)
        self._layout.setObjectName(_fromUtf8("_layout"))
        self.l_title = QtWidgets.QLabel(ControlEditor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l_title.sizePolicy().hasHeightForWidth())
        self.l_title.setSizePolicy(sizePolicy)
        self.l_title.setObjectName(_fromUtf8("l_title"))
        self._layout.addWidget(self.l_title)
        self.widget_control = QtWidgets.QWidget(ControlEditor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_control.sizePolicy().hasHeightForWidth())
        self.widget_control.setSizePolicy(sizePolicy)
        self.widget_control.setObjectName(_fromUtf8("widget_control"))
        self._layout_control = QtWidgets.QFormLayout(self.widget_control)
        self._layout_control.setFieldGrowthPolicy(QtWidgets.QFormLayout.ExpandingFieldsGrow)
        self._layout_control.setRowWrapPolicy(QtWidgets.QFormLayout.DontWrapRows)
        self._layout_control.setContentsMargins(1, 0, 0, 15)
        self._layout_control.setSpacing(10)
        self._layout_control.setObjectName(_fromUtf8("_layout_control"))
        self.l_name = QtWidgets.QLabel(self.widget_control)
        self.l_name.setMinimumSize(QtCore.QSize(60, 0))
        self.l_name.setObjectName(_fromUtf8("l_name"))
        self._layout_control.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.l_name)
        self.e_name = QtWidgets.QLineEdit(self.widget_control)
        self.e_name.setObjectName(_fromUtf8("e_name"))
        self._layout_control.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.e_name)
        self.l_type = QtWidgets.QLabel(self.widget_control)
        self.l_type.setMinimumSize(QtCore.QSize(60, 0))
        self.l_type.setObjectName(_fromUtf8("l_type"))
        self._layout_control.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.l_type)
        self.cb_interface = QtWidgets.QComboBox(self.widget_control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_interface.sizePolicy().hasHeightForWidth())
        self.cb_interface.setSizePolicy(sizePolicy)
        self.cb_interface.setObjectName(_fromUtf8("cb_interface"))
        self._layout_control.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.cb_interface)
        self.l_widget = QtWidgets.QLabel(self.widget_control)
        self.l_widget.setMinimumSize(QtCore.QSize(60, 0))
        self.l_widget.setObjectName(_fromUtf8("l_widget"))
        self._layout_control.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.l_widget)
        self.cb_widget = QtWidgets.QComboBox(self.widget_control)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_widget.sizePolicy().hasHeightForWidth())
        self.cb_widget.setSizePolicy(sizePolicy)
        self.cb_widget.setObjectName(_fromUtf8("cb_widget"))
        self._layout_control.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.cb_widget)
        self._layout.addWidget(self.widget_control)
        self.cb_constraints = QtWidgets.QCheckBox(ControlEditor)
        self.cb_constraints.setChecked(True)
        self.cb_constraints.setObjectName(_fromUtf8("cb_constraints"))
        self._layout.addWidget(self.cb_constraints)
        self.widget_constraints = QtWidgets.QWidget(ControlEditor)
        self.widget_constraints.setObjectName(_fromUtf8("widget_constraints"))
        self._layout_constraints = QtWidgets.QVBoxLayout(self.widget_constraints)
        self._layout_constraints.setMargin(0)
        self._layout_constraints.setObjectName(_fromUtf8("_layout_constraints"))
        self._layout.addWidget(self.widget_constraints)
        self.cb_preview = QtWidgets.QCheckBox(ControlEditor)
        self.cb_preview.setChecked(True)
        self.cb_preview.setObjectName(_fromUtf8("cb_preview"))
        self._layout.addWidget(self.cb_preview)
        self.box_preview = QtWidgets.QGroupBox(ControlEditor)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.box_preview.sizePolicy().hasHeightForWidth())
        self.box_preview.setSizePolicy(sizePolicy)
        self.box_preview.setAlignment(QtCore.Qt.AlignCenter)
        self.box_preview.setObjectName(_fromUtf8("box_preview"))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.box_preview)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget_preview = QtWidgets.QLabel(self.box_preview)
        self.widget_preview.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_preview.sizePolicy().hasHeightForWidth())
        self.widget_preview.setSizePolicy(sizePolicy)
        self.widget_preview.setStyleSheet(_fromUtf8("color: rgb(168, 193, 255);"))
        self.widget_preview.setFrameShape(QtWidgets.QFrame.Box)
        self.widget_preview.setFrameShadow(QtWidgets.QFrame.Plain)
        self.widget_preview.setLineWidth(1)
        self.widget_preview.setAlignment(QtCore.Qt.AlignCenter)
        self.widget_preview.setObjectName(_fromUtf8("widget_preview"))
        self.verticalLayout.addWidget(self.widget_preview)
        self._layout.addWidget(self.box_preview)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self._layout.addItem(spacerItem)

        self.retranslateUi(ControlEditor)
        self.cb_preview.toggled[bool].connect(self.box_preview.setVisible)
        self.cb_constraints.toggled[bool].connect(self.widget_constraints.setVisible)
        QtCore.QMetaObject.connectSlotsByName(ControlEditor)

    def retranslateUi(self, ControlEditor):
        ControlEditor.setWindowTitle(_translate("ControlEditor", "Form", None))
        self.l_title.setText(_translate("ControlEditor", "<html><head/><body><p><span style=\" font-weight:600;\">Control</span></p></body></html>", None))
        self.l_name.setText(_translate("ControlEditor", "Name", None))
        self.l_type.setText(_translate("ControlEditor", "Type", None))
        self.l_widget.setText(_translate("ControlEditor", "Widget", None))
        self.cb_constraints.setText(_translate("ControlEditor", "Constraints", None))
        self.cb_preview.setText(_translate("ControlEditor", "Preview", None))
        self.widget_preview.setText(_translate("ControlEditor", "Preview", None))
