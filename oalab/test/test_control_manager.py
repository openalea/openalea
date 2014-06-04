

from openalea.vpltk.qt import QtGui
from openalea.oalab.control.control import Control
from openalea.oalab.control.manager import ControlManager
from openalea.oalab.gui.control.manager import ControlManagerWidget

if __name__ == '__main__':
    instance = QtGui.QApplication.instance()
    if instance is None :
        app = QtGui.QApplication([])
    else :
        app = instance

    cm = ControlManager()

    w = ControlManagerWidget()

    from openalea.oalab.service.interface import get_interface
    b_interface = get_interface('IInt')(min=15, max=100)

    a = Control('a', 'IInt', widget='IntSpinBox')
    b = Control('b', b_interface, widget='IntSlider')
    c = Control('c', 'IColorList')
    d = Control('d', 'ICurve2D')
    autre = Control('autre', 'IInt', widget='IntSpinBox')


    cm.add_control(a)
    cm.add_control(b)
    cm.add_control(c)
    cm.add_control(d)

    cm.add_control(autre, 'test')


    w.showTag('test')

#     w = edit_qt(c3)
#     w.show()
#     w.raise_()

#     from openalea.oalab.editor.text_editor import TextEditor
#     from openalea.oalab.editor.highlight import Highlighter
#     text = TextEditor()
#     Highlighter(text)
#     text.show()
#     text.raise_()

#     w = Dialog()
#     w.show()



    from openalea.vpltk.shell.ipythoninterpreter import Interpreter
    from openalea.vpltk.shell.ipythonshell import ShellWidget
    # Set interpreter
    interpreter = Interpreter()
    interpreter.locals['interp'] = interpreter
    interpreter.locals.update(locals())
    # Set Shell Widget

    widget = QtGui.QWidget()
    layout = QtGui.QHBoxLayout(widget)

    shellwdgt = ShellWidget(interpreter)

    layout.addWidget(w)
    layout.addWidget(shellwdgt)

    layout.setSpacing(0)
    layout.setContentsMargins(0, 0, 0, 0)
    widget.show()
    widget.raise_()

    if instance is None :
        app.exec_()


    print cm.namespace()
#     print cm.namespace('test')

"""
from openalea.oalab.control.manager import ControlManager
from openalea.oalab.control.control import Control
a = Control('length', 'IInt', value=4)
b = Control('curve', 'ICurve2D')
c = Control('colors', 'IColorList')
cm  = ControlManager()
for control in (a, b, c):
    cm.add_control(control)

Goal: create user friendly application to study meristems
    - model morphogenesis using different paradigms: LPy, Visual programming, Python or R scripts, Java ...
    - easy to extend with new algorithm
    - visualize 4D data : meshes and 3D images over time
    - share data with others
    -> all in a user friendly graphical user interface base on OpenAleaLab

OpenAleaLab:
   - Modular platform
   - Easy to specialize (extension)
   - Support multiple design paradigms and models
   - Assemble many sub-models, make them interoperable.
   - Explicit architecture and key concepts (Project, Controls, Simulator, ...)

   - First development step, currently in progress

Extend OpenAleaLab:
    Idée: intégrer tous les travaux des partenaires/de l'équipe (Léo, Grégoire, ...)

Edit 4D Data
    - Visualize data like meshes, points of interest or 3D images
    - Interact (select cells, ...)
    - First exploration with simple vtk viewer

Share data:
    - support database/clouds widely used by biologist
    - first exploration with Omero DB

"""
