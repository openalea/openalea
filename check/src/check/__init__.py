# Version: $Id$
#
#

# Commentary:
#
#

# Change Log:
#
#

# Code:

__license__ = "Cecill-C"
__revision__ = "$Id$"

def global_module(module):
    import __builtin__
    __builtin__.__dict__[module.__name__] = module

#
# __init__.py ends here
