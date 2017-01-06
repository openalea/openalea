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

import os

cdir = os.path.dirname(__file__)
pdir = os.path.join(cdir, "../../qt")
pdir = os.path.abspath(pdir)

__path__ = [pdir] + __path__[:]

from openalea.qt.__init__ import *

#
# __init__.py ends here
