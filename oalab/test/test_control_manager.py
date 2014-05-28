

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
    w.show()
    w.raise_()

    c1 = Control('a', 'IInt', widget='IntSpinBox')
    c2 = Control('b', 'IInt', widget='IntSlider')
#     c3 = Control('b', 'IInt', widget='IntSpinBox2')
    c2.interface.min = 15
    c2.interface.max = 100

    cm.add_control(c1)
    cm.add_control(c2)
#     cm.add_control(c3)

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

    if instance is None :
        app.exec_()


    print cm.namespace()

