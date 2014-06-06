
import weakref
from openalea.vpltk.qt import QtGui, QtCore

from openalea.oalab.service import interface
from openalea.oalab.service.control import discover_qt_controls, qt_editors
from openalea.oalab.control.control import Control


# class ControlDataEditor(QtGui.):
#     def __init__(self):
#         QtGui.QGroupBox._
#
# class ControlConstraintEditor():
#     pass
#
# class ControlWidgetPreview():
#     def set(self, widgetname):
#         pass


class ControlEditorDialog(QtGui.QDialog):
    def __init__(self, name='default'):
        QtGui.QDialog.__init__(self)

        self._interfaces = []
        self._constraints = None

        self.e_name = QtGui.QLineEdit(name)
        self.cb_interface = QtGui.QComboBox()
        self.cb_widget = QtGui.QComboBox()

        self._layout = QtGui.QVBoxLayout(self)

        self.widget_control = QtGui.QWidget()
        self.widget_control.setContentsMargins(0, 0, 0, 0)

        self.widget_preview = QtGui.QLabel("No preview")
        self.widget_preview.setContentsMargins(0, 0, 0, 0)

        self._layout_control = QtGui.QFormLayout(self.widget_control)
        self._layout_control.addRow(QtGui.QLabel(u'Name'), self.e_name)
        self._layout_control.addRow(QtGui.QLabel(u'Type'), self.cb_interface)
        self._layout_control.addRow(QtGui.QLabel(u'Widget'), self.cb_widget)

        self._l_constraints = QtGui.QLabel("Constraints")

        self._layout.addWidget(QtGui.QLabel("Control"))
        self._layout.addWidget(self.widget_control)
        self._layout.addWidget(QtGui.QLabel("Preview"))
        self._layout.addWidget(self.widget_preview)
        self._layout.addWidget(self._l_constraints)
        self._layout.addStretch()


        controls = discover_qt_controls()
        for iname, widgets in controls.items() :
            alias = interface.alias(iname)
            self._interfaces.append(iname)
            self.cb_interface.addItem(alias)

        self.cb_interface.currentIndexChanged.connect(self.refresh)
        self.cb_widget.currentIndexChanged.connect(self.on_widget_changed)

        self.refresh()

    def on_widget_changed(self):
        widget_name = self.cb_widget.currentText()
        interface_name = self._interfaces[self.cb_interface.currentIndex()]
        qt_controls = discover_qt_controls()[interface_name]
        widget = None

        for plugin in qt_controls :
            if widget_name == plugin.name:
                widget = plugin.load()
                if hasattr(plugin, 'icon_path'):
                    self.widget_preview.setPixmap(QtGui.QPixmap(plugin.icon_path))
                else:
                    self.widget_preview.setText("No preview")
                break

        if self._constraints:
            widget_constraints = self._constraints()
            self._layout.removeWidget(widget_constraints)
            widget_constraints.close()
            self._constraints = None
            self._l_constraints.hide()

        if widget and hasattr(widget, 'edit_constraints'):
            widget_constraints = widget.edit_constraints()
            widget_constraints.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            self._layout.addWidget(widget_constraints)
            self._l_constraints.show()

            self._constraints = weakref.ref(widget_constraints)

    def refresh(self):
        interface_name = self._interfaces[self.cb_interface.currentIndex()]
        editors = qt_editors(interface_name)
        self.cb_widget.clear()
        for widget in editors:
            self.cb_widget.addItem(str(widget.name))

    def control(self):
        return Control(self.e_name.text(), self._interfaces[self.cb_interface.currentIndex()],
                       widget=self.cb_widget.currentText(),
                       constraints=self.constraints())

    def constraints(self):
        if self._constraints:
            return self._constraints().constraints()
        else:
            return {}

