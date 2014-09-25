

from openalea.vpltk.qt import QtGui
import random
from openalea.oalab.gui.container import ParadigmContainer
from openalea.oalab.service.data import data
from openalea.core.path import path as Path
from openalea.core.path import tempdir

if __name__ == '__main__':
    tmp = tempdir()

    instance = QtGui.QApplication.instance()
    if instance is None :
        app = QtGui.QApplication([])
    else :
        app = instance


    pmw = ParadigmContainer(None, None)
    def test():
        model1 = data('data/model.py')
        pmw.open_data(model1)

    from openalea.oalab.shell import get_shell_class
    from openalea.core.interpreter import get_interpreter_class

    # Set interpreter
    interpreter = get_interpreter_class()()
    interpreter.locals['interp'] = interpreter
    interpreter.locals.update(locals())
    interpreter.locals['pmw'] = pmw
    interpreter.locals['data'] = data

    # Set Shell Widget
    widget = QtGui.QWidget()
    layout = QtGui.QHBoxLayout(widget)

    shellwdgt = get_shell_class()(interpreter)

    layout.addWidget(pmw)
    layout.addWidget(shellwdgt)

    layout.setSpacing(0)
    layout.setContentsMargins(0, 0, 0, 0)

    widget.show()
    widget.raise_()

    if instance is None :
        app.exec_()

    tmp.rmtree()

