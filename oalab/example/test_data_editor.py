

from openalea.vpltk.qt import QtGui
from openalea.oalab.gui.container import ParadigmContainer
from openalea.oalab.session.session import Session

if __name__ == '__main__':
    instance = QtGui.QApplication.instance()
    if instance is None:
        app = QtGui.QApplication([])
    else:
        app = instance

    from openalea.core.service.ipython import interpreter
    from openalea.oalab.shell import get_shell_class

    # Set interpreter
    interpreter = interpreter()
    interpreter.user_ns['interp'] = interpreter
    interpreter.user_ns.update(locals())
    # Set Shell Widget

    widget = QtGui.QWidget()
    layout = QtGui.QHBoxLayout(widget)

    shellwdgt = get_shell_class()(interpreter)

    editor = ParadigmContainer(None, None)
    interpreter.user_ns['editor'] = editor
    session = Session()
    session.debug = True
    interpreter.user_ns['session'] = session

    pm = session.project_manager
    pm.discover()
    proj = session.project_manager.load('Koch')
    interpreter.user_ns['pm'] = pm
    interpreter.user_ns['proj'] = proj

    interpreter.user_ns['dlpy'] = proj.model['koch_curve.lpy']
    interpreter.user_ns['dpy'] = proj.model['simulator.py']
    interpreter.user_ns['dwf'] = proj.model['koch_wf.wpy']

    layout.addWidget(editor)
    layout.addWidget(shellwdgt)

    layout.setSpacing(0)
    layout.setContentsMargins(0, 0, 0, 0)
    widget.show()
    widget.raise_()

    if instance is None:
        app.exec_()
