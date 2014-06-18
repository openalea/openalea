
from openalea.vpltk.qt import QtCore
from openalea.oalab.gui.control.widget import AbstractInterfaceWidgetControl
from openalea.visualea.gui_catalog import IFloatWidget, IDateTimeWidget


class FloatWidget(IFloatWidget, AbstractInterfaceWidgetControl):

    def __init__(self):
        AbstractInterfaceWidgetControl.__init__(self, IFloatWidget, 'IFloat')

    def valueChanged(self, newval):
        self.on_value_changed(newval)

    @classmethod
    def get_label(cls, node, parameter_str):
        return ""

    def notify(self, sender, event):
        self._notify(sender, event)

    def setValue(self, value):
        self.spin.setValue(value)

    def value(self, interface=None):
        return self.spin.value()

class DateTimeWidget(IDateTimeWidget, AbstractInterfaceWidgetControl):

    def __init__(self):
        AbstractInterfaceWidgetControl.__init__(self, IDateTimeWidget, 'IDateTime')

    def valueChanged(self, newval):
        self.on_value_changed(newval)

    @classmethod
    def get_label(cls, node, parameter_str):
        return ""

    def notify(self, sender, event):
        self._notify(sender, event)

    def setValue(self, value):
        if value is None:
            value = QtCore.QDateTime.currentDateTime()
        self.subwidget.setDateTime(value)

    def value(self, interface=None):
        return self.subwidget.dateTime().toPyDateTime()

