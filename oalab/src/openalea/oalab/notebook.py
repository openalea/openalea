from openalea.core.service.project import *
from openalea.core.service.run import *
from openalea.core.service.control import *
from openalea.core.service.ipython import interpreter


def init():
    ip = interpreter()
    discover_projects()
    ip.user_ns.update(locals())
    ip.user_ns.update(globals())
