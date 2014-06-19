
from openalea.vpltk.qt import QtCore
from openalea.oalab.gui.control.widget import AbstractInterfaceWidgetControl
from openalea.visualea.gui_catalog import IFloatWidget, IDateTimeWidget
from openalea.core.interface import *

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
        AbstractInterfaceWidgetControl.__init__(self, 'IDateTime')
        IDateTimeWidget.__init__(self, None, None, None, interface=get_class(iname)())

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


class OpenAleaControlWidget(QtGui.QWidget, AbstractQtControlWidget):

    def __init__(self, widget):
        self._widget = monkey_patch_widget(widget)
        QtGui.QWidget.__init__(self._widget)
        AbstractQtControlWidget.__init__(self)

    def reset(self, value=0, *kargs):
        if value is None:
            if self._widget.__interface__:
                value = widget.__interface__.default()

        if value is not None:
            self._widget.set_widget_value(value)

    def setValue(self, value):
        self._widget.set_widget_value(value)

    def value(self, interface=None):
        return self._widget.get_widget_value()

    def set(self, control, autoread=True, autoapply=True):
        AbstractQtControlWidget.set(self,control, autoread, autoapply)
        self._widget.set_control(control)

    def autoapply(self, control, auto=True):
        if auto is True:
            self._control_out = control
        else:
            self._control_out = None

def monkey_patch_widget(widget):

    def set_control(self, control):
        self._control = control

    def set_value(self, newval):
        self._control.value = newval

    def get_value(self):
        return self._control.value

    def get_state(self):
        return ""

    def internal_data(self):
        "return a dict: minimal"
        return dict()

    def get_label(cls, node, parameter_str):
        return  ''

    def unvalidate(self):
        pass

    widget.set_control = set_control
    widget.set_value= set_value
    widget.get_value = get_value
    widget.get_state = get_state
    widget.internal_data = internal_data
    widget.unvalidate = unvalidate
    widget.get_label = classmethod(get_label)

    return widget
