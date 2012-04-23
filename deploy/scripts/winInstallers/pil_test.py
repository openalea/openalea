import sys

try:
    from PIL import Image
    sys.exit(0)
except Exception, e:
    sys.exit(1)
