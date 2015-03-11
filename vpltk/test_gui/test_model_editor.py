

from openalea.vpltk.qt import QtGui
import random
from openalea.oalab.gui.container import ParadigmContainer
from openalea.core.service.data import DataFactory
from openalea.core.path import path as Path
from openalea.core.path import tempdir

if __name__ == '__main__':
    tmp = tempdir()

    instance = QtGui.QApplication.instance()
    if instance is None:
        app = QtGui.QApplication([])
    else:
        app = instance

    pmw = ParadigmContainer(None, None)

    def test():
        model1 = DataFactory('data/model.py')
        pmw.open_data(model1)

    from openalea.oalab.shell import get_shell_class
    from openalea.core.service.ipython import interpreter as interpreter_

    # Set interpreter
    interpreter = interpreter_()
    interpreter.user_ns['interp'] = interpreter
    interpreter.user_ns.update(locals())
    interpreter.user_ns['pmw'] = pmw
    interpreter.user_ns['data'] = DataFactory

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

    if instance is None:
        app.exec_()

    tmp.rmtree()
