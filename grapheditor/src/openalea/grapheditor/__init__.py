
# Redirect path
import os

cdir = os.path.dirname(__file__)
pdir = os.path.join(cdir, "../../grapheditor")
pdir = os.path.abspath(pdir)

__path__ = [pdir] + __path__[:]

from openalea.grapheditor.__init__ import *
