
from openalea.core.service.project import active_project


def get_model(name, *args, **kwds):
    project = active_project()
    if project:
        return project.get_runnable_model(name)

model = get_model
