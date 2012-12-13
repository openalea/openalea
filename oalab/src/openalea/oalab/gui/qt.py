#---------------------------------------------
# qt class
# 
# Usefull to use the same version of Qt
# (PyQt, Pyside...)
#---------------------------------------------

# Set Api
import sip
sip.setapi("QString", 2)
sip.setapi("QVariant", 2)
sip.setapi("QDate", 2)
sip.setapi("QDateTime", 2)
sip.setapi("QTextStream", 2)
sip.setapi("QTime", 2)
sip.setapi("QUrl", 2)

# Import PyQt
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.Qt import *