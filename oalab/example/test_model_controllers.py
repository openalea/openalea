

from openalea.core.compositenode import CompositeNodeFactory, CompositeNode
from openalea.core.interface import IInt
from openalea.core.node import NodeFactory
from openalea.core.package import Package
from openalea.core.path import path as Path
from openalea.core.pkgmanager import PackageManager

from openalea.core.service.control import new_control
from openalea.core.service.data import DataFactory
from openalea.core.service.model import ModelFactory

from openalea.oalab.paradigm.python import PythonModelController
from openalea.oalab.paradigm.visualea import VisualeaModelController
from openalea.core.world.world import World

from openalea.oalab.service.paradigm import paradigm_controller


from openalea.vpltk.qt import QtGui

from openalea.core.service.ipython import interpreter
interp = interpreter()
interp.user_ns['interp'] = interp


pm = PackageManager()
pm.init()


def composite_node():
    inputs = []
    outputs = []
    for io in list('abcd'):
        inputs.append({'name': io, 'desc': 'Input %s' % io.upper(), 'value': 0})
        outputs.append({'name': io, 'desc': 'Input %s' % io.upper()})

    sg = CompositeNode(inputs=inputs, outputs=outputs)

    for i in range(len(inputs)):
        sg.connect(sg.id_in, i, sg.id_out, i)

    sgfactory = CompositeNodeFactory("addition")
    sg.to_factory(sgfactory)

    return sgfactory


def test_load_project():
    from openalea.core.project.manager import ProjectManager
    project_manager = ProjectManager()
    project = project_manager.load('test_project', '.')
    if not project.started:
        project.start()
    interp.user_ns['project_manager'] = project_manager
    interp.user_ns['project'] = project
    return True


def test_create_controllers():
    project = interp.locals['project']
    controllers = []
    for name, data in project.model.items():
        if data.mimetype == 'text/vnd-lpy':
            continue
        controller = paradigm_controller(data)
        varname = name.replace('.', '_')
        interp.locals['controller_%s' % varname] = controller
        interp.locals['item_%s' % varname] = data
        controllers.append(controller)
    return controllers


def test_instantiate_widgets(controllers):
    layout = interp.locals['layout']
    tabwidget = interp.locals.get('tabwidget', QtGui.QTabWidget())
    interp.user_ns['tabwidget'] = tabwidget
    layout.addWidget(tabwidget)
    for controller in controllers:
        widget = controller.instantiate_widget()
        tabwidget.addTab(widget, controller._obj.name)
    return True


def test_run_all(controllers):
    interp.user_ns['world'] = World()
    interp.user_ns['lst'] = [1, 2, 1, 3, 1, 4]
    for i, controller in enumerate(controllers):
        controller.run()
    return True


def test_visualea_io():
    factory = composite_node()
    model = ModelFactory(mimetype='text/x-visualea', name='test_workflow_io')
    model.set_code(factory)
    controller = paradigm_controller(model)
    test_instantiate_widgets([controller])
    new_control('a', 'IInt', 1)
    new_control('b', 'IInt', 2)
    interp.user_ns['c'] = 3
    assert controller.run() == [1, 2, 3, 0]
    assert controller.run(10) == [10, 2, 3, 0]
    assert controller.run(d=5) == [1, 2, 3, 5]
    return True


def test_all():
    success = True
    success = success and test_load_project()
    controllers = test_create_controllers()
    success = success and test_instantiate_widgets(controllers)
    success = success and test_run_all(controllers)
    success = success and test_visualea_io()
    return success


if __name__ == '__main__':
    instance = QtGui.QApplication.instance()
    if instance is None:
        app = QtGui.QApplication([])
    else:
        app = instance

    from openalea.oalab.shell import get_shell_class

    # Set interpreter
    interp.locals.update(locals())

    # Set Shell Widget
    widget = QtGui.QWidget()
    layout = QtGui.QHBoxLayout(widget)

    shellwdgt = get_shell_class()(interp)
    interp.locals['layout'] = layout

#    layout.addWidget(editor)
    layout.addWidget(shellwdgt)

    layout.setSpacing(0)
    layout.setContentsMargins(0, 0, 0, 0)
    widget.show()
    widget.raise_()

    if instance is None:
        app.exec_()
