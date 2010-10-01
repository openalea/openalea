import sys

try:
    from PyQt4 import QtCore, QtGui, QtHelp, QtSvg
    sys.exit(0)
except Exception, e:
    sys.exit(1)
