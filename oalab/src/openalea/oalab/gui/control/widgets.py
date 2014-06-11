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

class IControlWidget(object):
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


class AbstractControlWidget(AbstractListener):
    def __init__(self):
        AbstractListener.__init__(self)
        self._control_in = None
        self._control_out = None
        self.value_changed_signal = None

    def set(self, control, autoread=True, autoapply=True):
        self.autoread(control, autoread)
        self.autoapply(control, autoapply)

    def autoread(self, control, auto=True):
        if auto is True:
            self._control_in = control
            self._control_in.register_listener(self)
            self.read(control)
        else:
            if self._control_in is not None:
                self._control_in.unregister_listener(self)
                self._control_in = None
            # unregister listener

    def autoapply(self, control, auto=True):
        if auto is True:
            self._control_out = control
            signal = self.value_changed_signal
            if signal:
                if hasattr(signal, 'connect') and hasattr(signal, 'disconnect'):
                    signal.connect(self.on_value_changed)
                elif isinstance(signal, basestring):
                    self.connect(self, QtCore.SIGNAL(signal), self.on_value_changed)
                else:
                    raise NotImplementedError, 'Signal %s support is not implemented' % signal
        else:
            self._control_out = None
            signal = self.value_changed_signal
            if signal:
                if hasattr(signal, 'connect') and hasattr(signal, 'disconnect'):
                    signal = signal.signal
                elif isinstance(signal, basestring):
                    pass
                else:
                    raise NotImplementedError, 'Signal %s support is not implemented' % signal
                self.disconnect(self, QtCore.SIGNAL(signal), self.on_value_changed)

    def on_value_changed(self, *args, **kwargs):
        if self._control_out:
            self.apply(self._control_out)

    def apply(self, control):
        control.value = self.value()

    def read(self, control):
        self.reset(control.value)

    def notify(self, sender, event):
        signal, value = event
        if signal == 'value_changed':
            self.read(sender)

    def reset(self, value=None, *kargs):
        raise NotImplementedError

    def setValue(self, value):
        raise NotImplementedError

    def value(self):
        raise NotImplementedError


class BoolCheckBox(QtGui.QCheckBox, AbstractControlWidget):

    def __init__(self):
        QtGui.QCheckBox.__init__(self)
        AbstractControlWidget.__init__(self)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.setAutoFillBackground(True)
        self.value_changed_signal = self.stateChanged

    def reset(self, value=0, *kargs):
        self.setChecked(value)

    def setValue(self, value):
        return self.setChecked(value)

    def value(self):
        return self.isChecked()

class AbstractIntWidget(AbstractControlWidget):
    def __init__(self):
        AbstractControlWidget.__init__(self)

    def reset(self, value=1, minimum=None, maximum=None, **kwargs):
        self.setValue(value)
        if maximum is not None:
            self.setMinimum(minimum)
        if minimum is not None:
            self.setMaximum(maximum)

    def read(self, control):
        mini = control.interface.min
        maxi = control.interface.max
        self.reset(control.value, minimum=mini, maximum=maxi)

    def apply(self, control):
        AbstractControlWidget.apply(self, control)
        control.interface.min = self.minimum()
        control.interface.max = self.maximum()


class IntSpinBox(QtGui.QSpinBox, AbstractIntWidget):
    """
    For documentation, see :class:`~openalea.oalab.interfaces.all.IQtControl`
    """

    def __init__(self):
        QtGui.QSpinBox.__init__(self)
        AbstractIntWidget.__init__(self)
        self.value_changed_signal = self.valueChanged

class IntSimpleSlider(QtGui.QSlider, AbstractIntWidget):
    """
    For documentation, see :class:`~openalea.oalab.interfaces.all.IQtControl`
    """

    def __init__(self):
        QtGui.QSlider.__init__(self)
        AbstractIntWidget.__init__(self)
        self.value_changed_signal = self.valueChanged

class IntSlider(QtGui.QWidget, AbstractIntWidget):
    """
    For documentation, see :class:`~openalea.oalab.interfaces.all.IQtControl`
    """
    valueChanged = QtCore.Signal(int)

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


        self.slider.valueChanged.connect(self.spinbox.setValue)
        self.spinbox.valueChanged.connect(self.slider.setValue)
        self.slider.valueChanged.connect(self.valueChanged)

        layout = QtGui.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(self.spinbox)
        layout.addWidget(self.slider)

        self.value_changed_signal = self.valueChanged

    def reset(self, value=1, minimum=None, maximum=None, **kwargs):
        self.setValue(value)

        if minimum is not None:
            self.slider.setMinimum(minimum)
            self.spinbox.setMinimum(minimum)

        if maximum is not None:
            self.slider.setMaximum(maximum)
            self.spinbox.setMaximum(maximum)

    def apply(self, control):
        AbstractControlWidget.apply(self, control)
        control.interface.min = self.slider.minimum()
        control.interface.max = self.slider.maximum()

    def value(self):
        return self.spinbox.value()

    def setValue(self, value):
        self.slider.setValue(value)
        self.spinbox.setValue(value)

class IntDial(QtGui.QDial, AbstractIntWidget):
    """
    For documentation, see :class:`~openalea.oalab.interfaces.all.IQtControl`
    """

    def __init__(self):
        QtGui.QDial.__init__(self)
        AbstractIntWidget.__init__(self)
        self.value_changed_signal = self.valueChanged


################################################################################
# PlantGL and LPY widgets                                                      #
################################################################################


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


# Will move to openalea.lpy module
from openalea.plantgl.gui.materialeditor import MaterialEditor
from openalea.plantgl.all import PglTurtle

class ColorListWidget(MaterialEditor, AbstractControlWidget):

    def __init__(self):
        AbstractControlWidget.__init__(self)
        MaterialEditor.__init__(self, parent=None)

        # Signal used by "autoapply" method
        self.value_changed_signal = 'valueChanged()'

    def reset(self, value=[], **kwargs):
        self.setValue(value)

    def value(self):
        material_list = self.getTurtle().getColorList()
        return to_color(material_list)

    def setValue(self, value):
        turtle = PglTurtle()
        turtle.clearColorList()
        for color in to_material(value):
            turtle.appendMaterial(color)
        self.setTurtle(turtle)

    @classmethod
    def paint(self, control, shape=None):
        if shape == 'hline':
            return PainterColorList()


from openalea.plantgl.gui.curve2deditor import Curve2DEditor
class Curve2DWidget(Curve2DEditor, AbstractControlWidget):
    def __init__(self):
        AbstractControlWidget.__init__(self)
        Curve2DEditor.__init__(self, parent=None)

    def reset(self, value=None, **kwargs):
        if value is None:
            value = self.newDefaultCurve()
        self.setValue(value)

    def value(self):
        return self.curveshape.geometry

    def setValue(self, value):
        self.setCurve(value)

    @classmethod
    def paint(self, control, shape=None):
        if shape == 'hline':
            return PainterInterfaceObject()


'''
    @classmethod
    def _paint(cls, control, painter, rectangle, option=None):
        x = rectangle.bottomLeft().x()
        y = rectangle.topRight().y()
        w = rectangle.width()
        h = rectangle.height()
        if h > 50 and w > 50 :
            painter.fillRect(x, y, w, h, QtGui.QColor(255, 0, 255))
'''

from openalea.oalab.service.interface import alias
from openalea.oalab.control.control import Control

class AbstractPainter(object):

    def __call__(self, data, painter, rectangle, option=None):
        if isinstance(data, Control):
            self.paint_control(data, painter, rectangle, option)
        else:
            self.paint_data(data, painter, rectangle, option)

    def paint_control(self, control, painter, rectangle, option=None):
        self.paint_data(control.value, painter, rectangle, option)

    def paint_data(self, data, painter, rectangle, option=None):
        raise NotImplementedError


class PainterColorList(AbstractPainter):

    def paint_data(self, data, painter, rectangle, option=None):
        painter.save()
        r = rectangle
        x = r.bottomLeft().x()
        y = r.topRight().y()
        ncolor = len(data)
        if ncolor:
            lx = r.width() / ncolor
            for name, color in data:
                painter.fillRect(x, y, lx, r.height(), QtGui.QColor(*color))
                x += lx
        painter.restore()


class PainterInterfaceObject(AbstractPainter):

    def paint_control(self, control, painter, rectangle, option=None):
        self.paint_data(alias(control.interface), painter, rectangle, option)

    def paint_data(self, data, painter, rectangle, option=None):
        painter.save()

        pen = QtGui.QPen()
        if option and option.state & QtGui.QStyle.State_Selected:
            painter.fillRect(option.rect, option.palette.highlight())
            pen.setColor(option.palette.highlightedText().color())
        else:
            pen.setColor(QtCore.Qt.blue)
        painter.setPen(pen)

        painter.setRenderHint(painter.Antialiasing, True)

        text_option = QtGui.QTextOption()
        text_option.setAlignment(QtCore.Qt.AlignHCenter)
        painter.drawText(QtCore.QRectF(rectangle), data, text_option)
        painter.restore()

