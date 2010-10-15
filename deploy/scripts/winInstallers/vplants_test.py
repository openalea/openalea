import sys

try:
    from openalea.plantgl.all import *
    sys.exit(0)
except Exception, e:
    sys.exit(1)
