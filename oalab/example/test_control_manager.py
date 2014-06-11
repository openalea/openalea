

from openalea.vpltk.qt import QtGui
from openalea.oalab.control.control import Control
from openalea.oalab.control.manager import ControlManager
from openalea.oalab.gui.control.manager import ControlManagerWidget
from openalea.oalab.gui.control.panel import ControlPanel
from openalea.oalab.service import control as scontrol

if __name__ == '__main__':
    instance = QtGui.QApplication.instance()
    if instance is None :
        app = QtGui.QApplication([])
    else :
        app = instance

    cm = ControlManager()

    cmw = ControlManagerWidget()
    cp = ControlPanel()

    from openalea.oalab.service.interface import interfaces


    for interface in interfaces():
        iname = interface.__name__
        for i, editor in enumerate(scontrol.qt_widget_plugins(iname)):
            name = '%s_%s' % (editor.name, iname)
            c = scontrol.new(name, iname)

    c = scontrol.new('colors', 'IInt')
    cp.add_control(c)


#     from openalea.oalab.editor.text_editor import TextEditor
#     from openalea.oalab.editor.highlight import Highlighter
#     text = TextEditor()
#     Highlighter(text)
#     text.show()
#     text.raise_()


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

    layout.addWidget(cmw)
    layout.addWidget(cp)
    layout.addWidget(shellwdgt)

    layout.setSpacing(0)
    layout.setContentsMargins(0, 0, 0, 0)
    widget.show()
    widget.raise_()

    if instance is None :
        app.exec_()


    print cm.namespace()

"""
from openalea.oalab.control.manager import ControlManager
from openalea.oalab.control.control import Control
a = Control('length', 'IInt', value=4)
b = Control('curve', 'ICurve2D')
c = Control('colors', 'IColorList')
cm  = ControlManager()
for control in (a, b, c):
    cm.add_control(control)
"""
