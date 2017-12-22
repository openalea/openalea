""" This file define a simple use case for the plugin manager
from a user point of view.
"""

from openalea.core.service.plugin import plugin, plugins

for pl in plugins(group='openalea.core'):
    print pl


pl = plugin("openalea.core.plugin.builtin:PythonFile", group='openalea.core')
# TODO: pb, need the group attribute even with a unique id

PythonFile = pl.implementation

pyfile = PythonFile(path="pluggin_user_case.py")

print dir(pyfile)
print pyfile.dtype
print pyfile.mimetype
print pyfile.extension
print pyfile.content


