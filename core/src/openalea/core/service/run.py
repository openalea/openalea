
from openalea.core.service.project import active_project
from openalea.core.service.control import control_namespace


def namespace(model, **kwargs):
    ns = {}
    # Project namespace if available
    if hasattr(model, 'package'):
        if hasattr(model.package, 'ns'):
            ns.update(model.package.ns)
        if hasattr(model.package, 'namespace'):
            ns.update(model.package.namespace())

    # Control namespace
    ns.update(control_namespace())

    # User namespace
    ns.update(kwargs)
    return ns


def get_model(name, *args, **kwds):
    project = active_project()
    if project:
        return project.get_runnable_model(name)

model = get_model
