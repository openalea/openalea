
from openalea.core.util import warn_deprecated
warn_deprecated(__name__, 'openalea.oalab.shell', date=(2014, 9, 25))
warn_deprecated(__name__, 'openalea.core.interpreter', date=(2014, 9, 25))
from openalea.oalab.shell import get_shell_class
from openalea.core.interpreter import get_interpreter_class
