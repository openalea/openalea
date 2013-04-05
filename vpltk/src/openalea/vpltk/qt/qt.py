""" import qt.py from IPython to set QString and QVariant

The goal is to have the same version of QString and QVariant in all OpenAlea
"""
import os

def load_qt():
    from PyQt4 import QtCore, QtGui, QtSvg
    return QtCore, QtGui, QtSvg

try: 
    from IPython.external.qt import QtCore, QtGui, QtSvg, QT_API
except ImportError:
    QT_API = 'pyqt'
    QtCore, QtGui, QtSvg = load_qt()    
    
os.environ['QT_API'] = QT_API
    


