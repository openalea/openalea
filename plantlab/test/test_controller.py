

from openalea.core.compositenode import CompositeNodeFactory, CompositeNode
from openalea.core.pkgmanager import PackageManager
from openalea.core.project.manager import ProjectManager
from openalea.core.project import Project

from openalea.core.service.control import new_control
from openalea.core.service.model import ModelFactory

from openalea.oalab.service.paradigm import paradigm_controller


from openalea.core.service.ipython import interpreter
interp = interpreter()
interp.locals['interp'] = interp


pm = PackageManager()

project_manager = ProjectManager()
project = Project('unittest')
project_manager.cproject = project
if not project.started:
    project.start()
interp.locals['project_manager'] = project_manager
interp.locals['project'] = project


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


def test_visualea_io():
    factory = composite_node()
    model = ModelFactory(mimetype='text/x-visualea', name='test_workflow_io')
    model.set_code(factory)
    controller = paradigm_controller(model)
    new_control('a', 'IInt', 1)
    new_control('b', 'IInt', 2)
    interp.user_ns['c'] = 3
    assert controller.run() == [1, 2, 3, 0]
    assert controller.run(10) == [10, 2, 3, 0]
    assert controller.run(d=5) == [1, 2, 3, 5]
