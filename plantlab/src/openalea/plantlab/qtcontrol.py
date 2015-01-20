
from openalea.oalab.gui.control.widget import AbstractQtControlWidget
from openalea.oalab.plugins.controls.painters import PainterInterfaceObject
from painters import PainterColorList, PainterMaterialList
from openalea.plantgl.gui.materialeditor import MaterialEditor
from openalea.plantgl.all import PglTurtle, EditableQuantisedFunction
from openalea.plantlab.tools import to_color, to_material


class ColorListWidget(MaterialEditor, AbstractQtControlWidget):

    def __init__(self):
        AbstractQtControlWidget.__init__(self)
        MaterialEditor.__init__(self, parent=None)

        # Signal used by "autoapply" method
        self.value_changed_signal = 'valueChanged()'

    def reset(self, value=[], **kwargs):
        self.setValue(value)

    def value(self):
        return to_color(self.getAppearanceList())

    def setValue(self, value):
        self.setAppearanceList(to_material(value))
        # turtle = PglTurtle()
        # turtle.clearColorList()
        # for color in to_material(value):
        #     turtle.appendMaterial(color)
        # self.setTurtle(turtle)

    @classmethod
    def paint(self, control, shape=None):
        if shape == 'hline':
            return PainterColorList()


class MaterialListWidget(MaterialEditor, AbstractQtControlWidget):

    def __init__(self):
        AbstractQtControlWidget.__init__(self)
        MaterialEditor.__init__(self, parent=None)

        # Signal used by "autoapply" method
        self.value_changed_signal = 'valueChanged()'

    def reset(self, value=[], **kwargs):
        self.setValue(value)

    def value(self):
        return self.getAppearanceList()

    def setValue(self, value):
        self.setAppearanceList(value)

    @classmethod
    def paint(self, control, shape=None):
        if shape == 'hline':
            return PainterMaterialList()


from openalea.plantgl.gui.curve2deditor import Curve2DEditor, FuncConstraint


class Curve2DWidget(Curve2DEditor, AbstractQtControlWidget):

    def __init__(self):
        AbstractQtControlWidget.__init__(self)
        Curve2DEditor.__init__(self, parent=None)
        self.value_changed_signal = 'valueChanged()'

    def reset(self, value=None, **kwargs):
        if value is None:
            value = self.newDefaultCurve()
        self.setValue(value)

    def value(self):
        return self.getCurve()

    def setValue(self, value):
        self.setCurve(value)
        self.updateGL()

    @classmethod
    def paint(self, control, shape=None):
        if shape == 'hline':
            return PainterInterfaceObject()


class QuantisedFunctionWidget(Curve2DEditor, AbstractQtControlWidget):

    def __init__(self):
        AbstractQtControlWidget.__init__(self)
        Curve2DEditor.__init__(self, parent=None, constraints=FuncConstraint())
        self.value_changed_signal = 'valueChanged()'

    def reset(self, value=None, **kwargs):
        if value is None:
            value = EditableQuantisedFunction(self.newDefaultCurve())
        self.setValue(value)

    def value(self):
        return EditableQuantisedFunction(self.getCurve())

    def setValue(self, value):
        self.setCurve(value.curve)

    @classmethod
    def paint(self, control, shape=None):
        if shape == 'hline':
            return PainterInterfaceObject()


from openalea.plantgl.gui.nurbspatcheditor import NurbsPatchEditor


class NurbsPatchWidget(NurbsPatchEditor, AbstractQtControlWidget):

    def __init__(self):
        AbstractQtControlWidget.__init__(self)
        NurbsPatchEditor.__init__(self, parent=None)
        self.value_changed_signal = 'valueChanged()'

    def reset(self, value=None, **kwargs):
        if value is None:
            value = self.newDefaultNurbsPatch()()
        self.setValue(value)

    def value(self):
        return self.getNurbsPatch()

    def setValue(self, value):
        self.setNurbsPatch(value)
        self.updateGL()

    @classmethod
    def paint(self, control, shape=None):
        if shape == 'hline':
            return PainterInterfaceObject()
