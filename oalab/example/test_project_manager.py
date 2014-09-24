

from openalea.vpltk.qt import QtGui
from openalea.oalab.service.applet import get_applet
from openalea.oalab.gui.mainwindow import MainWindow
from openalea.oalab.session.session import  Session
from openalea.vpltk.plugin import iter_plugins

if __name__ == '__main__':
    instance = QtGui.QApplication.instance()
    if instance is None :
        app = QtGui.QApplication([])
    else :
        app = instance

    session = Session()
    mainwin = MainWindow(session)
    for plugin in iter_plugins('oalab.applet'):
        if plugin.name in ('ProjectManager', 'EditorManager'):
            mainwin.add_plugin(plugin())

    pm = session.project_manager
    pm.cproject = pm.default()
    pmw = get_applet(identifier='ProjectManager', class_args=dict(mainwindow=mainwin))
    pcw = get_applet(identifier='EditorManager', class_args=dict(mainwindow=mainwin))

    session.interpreter.locals['pmw'] = pmw
    session.interpreter.locals['pcw'] = pcw

    mainwin.show()
    mainwin.raise_()

    if instance is None :
        app.exec_()

"""
from openalea.core.control.manager import ControlManager
from openalea.core.control import Control
a = Control('length', 'IInt', value=4)
b = Control('curve', 'ICurve2D')
c = Control('colors', 'IColorList')
cm  = ControlManager()
for control in (a, b, c):
    cm.add_control(control)
"""
