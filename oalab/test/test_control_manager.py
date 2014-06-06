

from openalea.vpltk.qt import QtGui
from openalea.oalab.control.control import Control
from openalea.oalab.control.manager import ControlManager
from openalea.oalab.gui.control.manager import ControlManagerWidget, ControlPanel
from openalea.oalab.service.control import edit_qt

if __name__ == '__main__':
    instance = QtGui.QApplication.instance()
    if instance is None :
        app = QtGui.QApplication([])
    else :
        app = instance

    cm = ControlManager()

    w = ControlManagerWidget()
#     cp = ControlPanel()

    from openalea.oalab.service.interface import get_interface
    b_interface = get_interface('IInt')(min=15, max=100)

    from openalea.oalab.service.control import qt_editors
    from openalea.oalab.service.interface import interfaces

    editors = QtGui.QWidget()
    layout2 = QtGui.QVBoxLayout(editors)

    cs = []
    for interface in interfaces():
        iname = interface.__name__
        for i, editor in enumerate(qt_editors(iname)):
            c = Control('%d_%s_%s' % (i, editor.name, iname), iname, widget=editor.name)
            cs.append(c)
            cm.add_control(c)
            layout2.addWidget(edit_qt(c))


#     w.showTag('test')

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
    layout.addWidget(editors)
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
"""
