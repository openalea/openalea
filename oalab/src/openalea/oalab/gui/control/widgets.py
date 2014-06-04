# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014 INRIA
#
#       File author(s): Guillaume Baty <guillaume.baty@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################


from openalea.vpltk.qt import QtGui, QtCore
from openalea.core.observer import AbstractListener


class IControlHandler(object):
    """
    """

    def reset(self, value=None, *kargs):
        """
        Reset widget to default values.
        """

    def set(self, control):
        """
        Use control to preset widget.
        Starts to listen to control events and read control's values
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

class IControlWidget(AbstractListener):
    def __init__(self):
        """

        shape: None, line, icon
        """

    @classmethod
    def edit(self, control, shape=None):
        """
        Returns an instance of IControlHandler that modifies control in place.
        Control can be updated continuously or on explicit user action
        (click on apply button for instance)
        """

    @classmethod
    def view(self, control, shape=None):
        """
        Returns an instance of IControlHandler that view control.
        This function never modify control.
        If you finally want to modify it, you can call "apply" explicitly.
        """

    @classmethod
    def paint(self, control, painter, rectangle, option=None):
        """
        Returns a QPixmap that show control.
        This function never modify control.
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

    @classmethod
    def edit(cls, control, shape=None):
        raise NotImplementedError

    @classmethod
    def view(cls, control, shape=None):
        raise NotImplementedError

    @classmethod
    def edit_constraints(cls):
        widget = IntConstraintWidget()
        return widget


    def set(self, control):
        self._control = control
        if self._control:
            self.read(self._control)
            self.initialise(self._control)

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

    def on_value_changed(self, value):
        self._control.value = value

class IntSpinBox(QtGui.QSpinBox, AbstractIntWidget):
    """
    For documentation, see :class:`~openalea.oalab.interfaces.all.IQtControl`
    """

    def __init__(self):
        QtGui.QSpinBox.__init__(self)
        AbstractIntWidget.__init__(self)

    @classmethod
    def edit(cls, control, shape=None):
        if shape in ('line', 'thumbnail'):
            widget = cls()
            widget.valueChanged.connect(widget.on_value_changed)
            return widget

class IntSlider(QtGui.QWidget, AbstractIntWidget):
    """
    For documentation, see :class:`~openalea.oalab.interfaces.all.IQtControl`
    """

    def __init__(self):
        QtGui.QWidget.__init__(self)

        self.slider = QtGui.QSlider(QtCore.Qt.Horizontal)
        self.spinbox = QtGui.QSpinBox()

        # Fill background to avoid to see text or widget behind
        self.setAutoFillBackground(True)

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

    @classmethod
    def edit(cls, control, shape=None):
        if shape in ('line', 'thumbnail'):
            widget = cls()
            widget.slider.valueChanged.connect(widget.on_value_changed)
            widget.spinbox.valueChanged.connect(widget.on_value_changed)
            return widget

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

    @classmethod
    def edit(cls, control, shape=None):
        if shape in ('line', 'thumbnail'):
            widget = cls()
            widget.set(control)
            widget.show()
            return widget

    @classmethod
    def view(cls, control, shape=None):
        widget = cls()
        widget.set(control)
        widget.register(control)
        widget.show()
        return widget

    def apply(self, control):
        control.set_value(self.currentText())

    def read(self, control):
        self.clear()

    def notify(self, sender, event):
        self.read(self._control)


# Will move to openalea.lpy module
from openalea.lpy.gui.materialeditor import MaterialEditor
from openalea.plantgl.all import PglTurtle

def to_color(material_list):
    """
    Material(name='C0', ambient=Color3(65,45,15)) -> ('C0', (65,45,15))
    """
    color_list = []
    for material in material_list:
        a = material.ambient
        color = (material.name, (a.red, a.green, a.blue))
        color_list.append(color)
    return color_list

def to_material(color_list):
    """
    ('C0', (65,45,15)) -> Material(name='C0', ambient=Color3(65,45,15))
    """

    from openalea.plantgl.all import Material, Color3
    material_list = []
    for color in color_list:
        material = Material(color[0], Color3(*color[1][:3]))
        material_list.append(material)
    return material_list

class ColorListWidget(MaterialEditor, AbstractListener):
    def __init__(self):
        AbstractListener.__init__(self)
        MaterialEditor.__init__(self, parent=None)

    def value(self):
        material_list = self.getTurtle().getColorList()
        return to_color(material_list)

    def set(self, control):
        self._control = control
        self.initialise(control)
        self.read(control)

    def read(self, control):
        value = control.value
        turtle = PglTurtle()
        turtle.clearColorList()
        for color in to_material(value):
            turtle.appendMaterial(color)
        self.setTurtle(turtle)

    def apply(self, control):
        control.value = self.value()

    @classmethod
    def edit(cls, control, shape=None):
        if shape == 'large':
            widget = cls()
            return widget

    @classmethod
    def paint(cls, control, painter, rectangle, option=None):
        r = rectangle
        x = r.bottomLeft().x()
        y = r.topRight().y()
        ncolor = len(control.value)
        if ncolor:
            lx = r.width() / ncolor
            for name, color in control.value:
                painter.fillRect(x, y, lx, r.height(), QtGui.QColor(*color))
                x += lx

    def notify(self, sender, event):
        self.read(self._control)

from openalea.plantgl.gui.curve2deditor import Curve2DEditor

class Curve2DWidget(Curve2DEditor, AbstractListener):
    def __init__(self):
        AbstractListener.__init__(self)
        Curve2DEditor.__init__(self, parent=None)

    @classmethod
    def edit(cls, control, shape=None):
        if shape == 'large':
            widget = cls()
            return widget

    @classmethod
    def paint(cls, control, painter, rectangle, option=None):
        x = rectangle.bottomLeft().x()
        y = rectangle.topRight().y()
        w = rectangle.width()
        h = rectangle.height()
        if h > 50 and w > 50 :
            painter.fillRect(x, y, w, h, QtGui.QColor(255, 0, 255))
        else:
            painter.drawText(QtCore.QRectF(rectangle), 'Curve Object')

    def value(self):
        return self.curveshape.geometry

    def set(self, control):
        self._control = control
        self.initialise(control)
        self.read(control)

    def read(self, control):
        self.setCurve(control.value)

    def apply(self, control):
        control.value = self.value()

    def notify(self, sender, event):
        self.read(self._control)
