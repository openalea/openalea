import sys

try:
    import pkg_resources
    #maybe the version should be configured by makeWinInstaller
    pkg_resources.require("gnuplot")[0].version == "4.2.2-1" 
    sys.exit(0)
except Exception, e:
    sys.exit(1)
