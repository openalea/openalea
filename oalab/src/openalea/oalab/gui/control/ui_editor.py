# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/openalea/oalab/gui/control/editor.ui'
#
# Created: Fri Jun 20 15:26:19 2014
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
        ControlEditor.resize(263, 293)
        self._layout = QtGui.QVBoxLayout(ControlEditor)
        self._layout.setSpacing(5)
        self._layout.setObjectName(_fromUtf8("_layout"))
        self.l_title = QtGui.QLabel(ControlEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.l_title.sizePolicy().hasHeightForWidth())
        self.l_title.setSizePolicy(sizePolicy)
        self.l_title.setObjectName(_fromUtf8("l_title"))
        self._layout.addWidget(self.l_title)
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
        self._layout_control.setSpacing(10)
        self._layout_control.setObjectName(_fromUtf8("_layout_control"))
        self.l_name = QtGui.QLabel(self.widget_control)
        self.l_name.setMinimumSize(QtCore.QSize(60, 0))
        self.l_name.setObjectName(_fromUtf8("l_name"))
        self._layout_control.setWidget(0, QtGui.QFormLayout.LabelRole, self.l_name)
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
        self.l_widget = QtGui.QLabel(self.widget_control)
        self.l_widget.setMinimumSize(QtCore.QSize(60, 0))
        self.l_widget.setObjectName(_fromUtf8("l_widget"))
        self._layout_control.setWidget(2, QtGui.QFormLayout.LabelRole, self.l_widget)
        self.cb_widget = QtGui.QComboBox(self.widget_control)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.MinimumExpanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cb_widget.sizePolicy().hasHeightForWidth())
        self.cb_widget.setSizePolicy(sizePolicy)
        self.cb_widget.setObjectName(_fromUtf8("cb_widget"))
        self._layout_control.setWidget(2, QtGui.QFormLayout.FieldRole, self.cb_widget)
        self._layout.addWidget(self.widget_control)
        self.cb_constraints = QtGui.QCheckBox(ControlEditor)
        self.cb_constraints.setChecked(True)
        self.cb_constraints.setObjectName(_fromUtf8("cb_constraints"))
        self._layout.addWidget(self.cb_constraints)
        self.widget_constraints = QtGui.QWidget(ControlEditor)
        self.widget_constraints.setObjectName(_fromUtf8("widget_constraints"))
        self._layout_constraints = QtGui.QVBoxLayout(self.widget_constraints)
        self._layout_constraints.setMargin(0)
        self._layout_constraints.setObjectName(_fromUtf8("_layout_constraints"))
        self._layout.addWidget(self.widget_constraints)
        self.cb_preview = QtGui.QCheckBox(ControlEditor)
        self.cb_preview.setChecked(True)
        self.cb_preview.setObjectName(_fromUtf8("cb_preview"))
        self._layout.addWidget(self.cb_preview)
        self.box_preview = QtGui.QGroupBox(ControlEditor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.box_preview.sizePolicy().hasHeightForWidth())
        self.box_preview.setSizePolicy(sizePolicy)
        self.box_preview.setAlignment(QtCore.Qt.AlignCenter)
        self.box_preview.setObjectName(_fromUtf8("box_preview"))
        self.verticalLayout = QtGui.QVBoxLayout(self.box_preview)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.widget_preview = QtGui.QLabel(self.box_preview)
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
        self._layout.addWidget(self.box_preview)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self._layout.addItem(spacerItem)

        self.retranslateUi(ControlEditor)
        QtCore.QObject.connect(self.cb_preview, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.box_preview.setVisible)
        QtCore.QObject.connect(self.cb_constraints, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.widget_constraints.setVisible)
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

