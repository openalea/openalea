""" import qt.py from IPython to set QString and QVariant

The goal is to have the same version of QString and QVariant in all OpenAlea
"""

def load_qt():
    from PyQt4 import QtCore, QtGui, QtSvg
    return QtCore, QtGui, QtSvg



try: 
    from IPython.external.qt import *
except ImportError:
    QtCore, QtGui, QtSvg = load_qt()    
    


