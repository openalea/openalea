
from openalea.core.util import warn_deprecated
warn_deprecated(__name__, 'openalea.core.interpreter', date=(2014, 9, 25))
from openalea.core.interpreter.ipython import Interpreter, showtraceback
from openalea.core.interpreter import adapt_interpreter
adapt_interpreter(Interpreter)
