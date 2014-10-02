

from openalea.core.util import warn_deprecated
warn_deprecated(__name__ + '.new', 'oalab.core.service.control.new_control', (2014, 9, 25))

from openalea.core.service.control import new_control

new = new_control
