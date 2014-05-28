
from openalea.vpltk.qt import QtGui, QtCore
from openalea.core.observer import AbstractListener


class IQtControl(AbstractListener):
    def __init__(self):
        """
        """

    def reset(self, value=None, *kargs):
        """
        Reset widget to default values.
        """

    # Part specific to control
    ##########################

    def set(self, control):
        """
        Use control to preset widget.
        Starts to listen to control events and read control's values
        """

    def edit(self, control):
        """
        Modify control in place.
        Control can be updated continuously or on explicit user action
        (click on apply button for instance)
        """

    def view(self, control):
        """
        View control. This function never modify control.
        If you finally want to modify it, you can call "apply" explicitly.
        """

    def apply(self, control):
        """
        Update control with widget values.
        """

    def read(self, control):
        """
        Update widget with control values
        """

    def notify(self, sender, event):
        """
        Method called when Observed control changes.
        Generally, when control send an event "ValueChanged", we want to
        refresh widget with new value.
        """

class IConstraintWidget(object):
    def constraints(self):
        """
        Returns a dict "constraint name" -> "value"
        """

class IntConstraintWidget(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        layout = QtGui.QFormLayout(self)

        self.e_min = QtGui.QLineEdit('0')
        self.e_max = QtGui.QLineEdit('100')
        text = 'Can be an int (for instance -5) or empty (no limits)'
        self.e_min.setToolTip(text)
        self.e_min.setWhatsThis(text)
        self.e_max.setToolTip(text)
        self.e_max.setWhatsThis(text)

        layout.addRow(QtGui.QLabel('Minimum'), self.e_min)
        layout.addRow(QtGui.QLabel('Maximum'), self.e_max)

    def constraints(self):
        dic = {}
        try:
            dic['min'] = int(self.e_min.text())
        except ValueError:
            pass

        try:
            dic['max'] = int(self.e_max.text())
        except ValueError:
            pass

        return dic

class AbstractIntWidget(AbstractListener):
    def __init__(self):
        AbstractListener.__init__(self)
        self._control = None

    def reset(self, value=1, minimum=None, maximum=None, **kwargs):
        self.setValue(value)
        if maximum is not None:
            self.setMinimum(minimum)
        if minimum is not None:
            self.setMaximum(maximum)

    # Part specific to control
    ##########################

    def set(self, control):
        self._control = control
        if self._control:
            self.initialise(self._control)
            self.read(self._control)

    def edit(self, control):
        self.set(control)
        self.show()

    def view(self, control):
        self.set(control)
        self.register(control)
        self.show()

    def apply(self, control):
        control.value = self.value()
        control.interface.min = self.minimum()
        control.interface.max = self.maximum()

    def read(self, control):
        self._control = control
        mini = control.interface.min
        maxi = control.interface.max
        self.reset(control.value, minimum=mini, maximum=maxi)

    def notify(self, sender, event):
        signal, value = event
        if signal == 'value_changed':
            self.read(sender)

    @staticmethod
    def edit_constraints():
        widget = IntConstraintWidget()
        return widget

    def on_value_changed(self, value):
        self._control.value = value

class IntSpinBox(QtGui.QSpinBox, AbstractIntWidget):
    """
    For documentation, see :class:`~openalea.oalab.interfaces.all.IQtControl`
    """

    def __init__(self):
        QtGui.QSpinBox.__init__(self)
        AbstractIntWidget.__init__(self)

    def edit(self, control):
        self.valueChanged.connect(self.on_value_changed)
        AbstractIntWidget.edit(self, control)

class IntSlider(QtGui.QWidget, AbstractIntWidget):
    """
    For documentation, see :class:`~openalea.oalab.interfaces.all.IQtControl`
    """

    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.spinbox = QtGui.QSpinBox()

        AbstractIntWidget.__init__(self)


        # To be compatible with tree or table views, slider must keep focus
        self.slider.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setMinimumHeight(20)
        self.spinbox.setMinimumHeight(18)
        self.slider.setMinimumHeight(18)

        layout = QtGui.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.spinbox)
        layout.addWidget(self.slider)

    def edit(self, control):
        self.slider.valueChanged.connect(self.on_value_changed)
        self.spinbox.valueChanged.connect(self.on_value_changed)
        AbstractIntWidget.edit(self, control)

    def reset(self, value=1, minimum=None, maximum=None, **kwargs):
        self.setValue(value)

        if minimum is not None:
            self.slider.setMinimum(minimum)
            self.spinbox.setMinimum(minimum)

        if maximum is not None:
            self.slider.setMaximum(maximum)
            self.spinbox.setMaximum(maximum)

    def value(self):
        return self.spinbox.value()

    def setValue(self, value):
        self.slider.setValue(value)
        self.spinbox.setValue(value)

class IntIPython(object):

    def __init__(self):
        self._value = 0
        self._range = (0, 100)

    def set(self, control):
        self._range = control.range()
        self._value = control.value

    def edit(self, control):
        self.set(control)
        val = raw_input('%s=? (range: %s, default: %s) ' % (
            control.name, self._range, self._value))
        if val.strip():
            val = int(val)
        self.apply(control)

    def apply(self, control):
        control.set_value(self._value)

    def view(self, control):
        print '%s=%d' % (control.name, control.value)

from IPython.html.widgets.widget_int import IntSliderWidget
class IntNotebook(IntSliderWidget):
    def __init__(self):
        IntSliderWidget.__init__(self)

    def edit(self, control):
        self.min = control.interface.min
        self.max = control.interface.max
        self.value = control.value

    def apply(self, control):
        control.interface.min = self.min
        control.interface.max = self.max
        control.value = self.value

class StrComboBox(QtGui.QComboBox, AbstractListener):
    """
    For documentation, see :class:`~openalea.oalab.interfaces.all.IQtControl`
    """

    def __init__(self):
        AbstractListener.__init__(self)
        QtGui.QComboBox.__init__(self)
        self._control = None
        self._lst = []
        self.reset()

    def reset(self, value=None, **kwargs):
        self.set(None)
        self.clear()

    def edit(self, control):
        self.set(control)
        self.show()

    def view(self, control):
        self.set(control)
        self.register(control)
        self.show()

    def apply(self, control):
        control.set_value(self.currentText())

    def read(self, control):
        self.clear()

    def notify(self, sender, event):
        self.read(self._control)


# Will move to openalea.lpy module
from openalea.lpy.gui.materialeditor import MaterialEditor
from openalea.plantgl.all import PglTurtle

class ColorListWidget(MaterialEditor):
    def __init__(self):
        MaterialEditor.__init__(self, parent=None)

    def value(self):
        clist = self.getTurtle().getColorList()
        return clist

    def set(self, control):
        value = control.value
        turtle = PglTurtle()
        turtle.clearColorList()
        for material in value:
            turtle.appendMaterial(material)
        self.setTurtle(turtle)

    def edit(self, control):
        self.set(control)
        self.show()

    def closeEvent(self, event):
        pass
