
from openalea.core.plugin import iter_plugins
from openalea.core.model import Model
from openalea.core.data import Data

MIME_MODEL_CONTROLLER = {}
MIME_DATA_CONTROLLER = {}


def _fill_registery(registery, mimetypes):
    if mimetypes in (None, unicode):
        return
    elif isinstance(mimetypes, basestring):
        registery.setdefault(mimetypes, []).append(plugin)
    elif isinstance(mimetypes, (list, tuple, set)):
        for mimetype in mimetypes:
            registery.setdefault(mimetype, []).append(plugin)


for plugin in iter_plugins('oalab.paradigm_applet'):
    _fill_registery(MIME_MODEL_CONTROLLER, plugin.mimetype_model)
for plugin in iter_plugins('oalab.paradigm_applet'):
    _fill_registery(MIME_DATA_CONTROLLER, plugin.mimetype_data)


def paradigm_controller_class(mimetype):
    if mimetype in MIME_DATA_CONTROLLER:
        return MIME_DATA_CONTROLLER[mimetype][0]()()
    elif mimetype in MIME_MODEL_CONTROLLER:
        return MIME_MODEL_CONTROLLER[mimetype][0]()()
    else:
        return None


def paradigm_controller(obj):
    klass = paradigm_controller_class(obj.mimetype)
    if klass is None:
        return
    if isinstance(obj, Data):
        return klass(data=obj)
    elif isinstance(obj, Model):
        return klass(model=obj)
