

from openalea.vpltk.qt import QtGui
import random
from openalea.oalab.project.projectwidget2 import ProjectManagerWidget
from openalea.vpltk.project.manager2 import ProjectManager
from openalea.oalab.session.session import  Session
from openalea.core.path import tempdir


def new_tmp_project(projectdir):
    pm = ProjectManager()
    project = pm.create('tmpproject', projectdir=projectdir)
    pm.cproject = project
    return project

def add_lot_of_data(project, category='model', n=10):
    for i in range(n):
        project.add(category, filename='%s_%05d.ext' % (category, i))

def load_all_projects():
    projects = list(pm.search())
    random.shuffle(projects)
    for proj in projects:
        print 'load', proj
        pm.cproject = proj

if __name__ == '__main__':
    tmp = tempdir()

    instance = QtGui.QApplication.instance()
    if instance is None :
        app = QtGui.QApplication([])
    else :
        app = instance


    session = Session()
    pm = ProjectManager()
    pm.discover()
    pmw = ProjectManagerWidget()
    pmw.initialize()
#     pm.load('mtg')

    from openalea.vpltk.shell.shell import get_shell_class, get_interpreter_class

    # Set interpreter
    interpreter = get_interpreter_class()()
    interpreter.locals['interp'] = interpreter
    interpreter.locals.update(locals())
    interpreter.locals['pmw'] = pmw
    interpreter.locals['pm'] = pm
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

