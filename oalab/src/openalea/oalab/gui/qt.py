"""
qt class.
import Qt and set the api to version 2

Usefull to use the same version of Qt
(PyQt, Pyside...)
"""

try:
    # Set Api
    import sip
    sip.setapi("QString", 2)
    sip.setapi("QVariant", 2)
    sip.setapi("QDate", 2)
    sip.setapi("QDateTime", 2)
    sip.setapi("QTextStream", 2)
    sip.setapi("QTime", 2)
    sip.setapi("QUrl", 2)
except:
    print "Warning in openalea.oalab.gui.qt :"
    print "\tThe API of Qt is yet to the old version!"
    print "\tOALab need the api v2 to work."
    print "\tApplication will not totally work."

# Import PyQt
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.Qt import *