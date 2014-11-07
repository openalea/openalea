
import copy
from openalea.core.control.manager import ControlManager
from openalea.core.project.manager import ProjectManager
from openalea.core.service.model import to_model

cm = ControlManager()
pm = ProjectManager()


def get_model(name):
    data = pm.cproject.get_model(name)
    if data:
        model = to_model(data)
        if model:
            return copy.copy(model)


def namespace():
    # Move to runner class (model manager or ParadigmEditor)

    namespace = {}
    namespace.update(cm.namespace())
    namespace.update(pm.cproject.ns)
    namespace['Model'] = get_model

    return namespace
