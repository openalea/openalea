from openalea.oalab.service import control

from openalea.core.interface import IBool

minterface = IBool()
mcontrol = control.new(u'FLAKE',minterface,True)

