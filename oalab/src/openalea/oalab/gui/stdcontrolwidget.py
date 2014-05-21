
from openalea.vpltk.qt import QtGui

NO_SYNC = 0
CONTROL_TO_EDITOR = 1
EDITOR_TO_CONTROL = 2
TWO_WAY = CONTROL_TO_EDITOR | EDITOR_TO_CONTROL

from openalea.core.observer import AbstractListener

class QtControl(AbstractListener):
    def __init__(self):
        AbstractListener.__init__(self)
        self._control = None
        self.reset()

    def reset(self):
        self.set(None)
        self.setValue(1)
        self.setMinimum(0)
        self.setMaximum(100)

    def set(self, control):
        """
        Use control to preset widget
        """
        self._control = control
        if self._control:
            self.initialise(self._control)
            self.read(self._control)

    def edit(self, control):
        """
        Modify control in place.
        Control can be updated continuously or on explicit user action
        (click on apply button for instance)
        """
        self.set(control)
        self.show()

    def view(self, control):
        """
        View control. This function never modify control.
        If you finally want to modify it, you can call "apply" explicitly.
        """
        self.set(control)
        self.register(control)
        self.show()

    def apply(self, control):
        control.set_value(self.value())
        control.set_range((self.minimum(), self.maximum()))

    def read(self, control):
        self.setValue(control.value())
        range = control.range()
        self.setMinimum(range[0])
        self.setMaximum(range[1])

    def notify(self, sender, event):
        self.read(self._control)

class IntSpinBox(QtGui.QSpinBox, QtControl):
    def __init__(self):
        QtGui.QSpinBox.__init__(self)
        QtControl.__init__(self)

    def reset(self):
        # self.valueChanged.disconnect()
        QtControl.reset(self)

    def edit(self, control):
        self.valueChanged.connect(control.set_value)
        QtControl.edit(self, control)

class IntSlider(QtGui.QSlider, QtControl):
    def __init__(self):
        QtGui.QSlider.__init__(self)
        QtControl.__init__(self)

    def reset(self):
        # self.valueChanged.disconnect()
        QtControl.reset(self)

    def edit(self, control):
        self.valueChanged.connect(control.set_value)
        QtControl.edit(self, control)

class IntIPython(object):
    def __init__(self):
        self._value = 0
        self._range = (0, 100)

    def set(self, control):
        self._range = control.range()
        self._value = control.value()

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
        print '%s=%d' % (control.name, control.value())

from IPython.html.widgets.widget_int import IntSliderWidget
class IntNotebook(IntSliderWidget):
    def __init__(self):
        IntSliderWidget.__init__(self)

    def edit(self, control):
        self.min = control.range()[0]
        self.max = control.range()[1]
        self.value = control.value()

# Will move to openalea.lpy module
from openalea.lpy.gui.materialeditor import MaterialEditor
from openalea.plantgl.all import PglTurtle
from openalea.oalab.control.control import SYNCHRO_AUTO

class ColorListWidget(MaterialEditor):
    def __init__(self):
        MaterialEditor.__init__(self, parent=None)

    def value(self):
        clist = self.getTurtle().getColorList()
        return clist

    def set(self, control):
        value = control.value()
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
