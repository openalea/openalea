import sys

try:
    import vplants.weberpenn # because there is no import in this package's __init__.py (==fast)
    sys.exit(0)
except Exception, e:
    sys.exit(1)
