import sys

try:
    import pkg_resources, openalea
    #maybe the version should be configured by makeWinInstaller
    pkg_resources.require("openalea.core")[0].version == "0.9" 
    sys.exit(0)
except Exception, e:
    sys.exit(1)
