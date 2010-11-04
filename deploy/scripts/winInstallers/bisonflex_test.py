import sys

try:
    import pkg_resources
    #maybe the version should be configured by makeWinInstaller
    pkg_resources.require("bisonflex")[0].version == "2.4.1-2.5.35" 
    sys.exit(0)
except Exception, e:
    sys.exit(1)
