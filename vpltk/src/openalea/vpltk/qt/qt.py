""" import qt.py from IPython to set QString and QVariant

The goal is to have the same version of QString and QVariant in all OpenAlea
"""
try:
    from IPython.external.qt import *
except ImportError:
    from PyQt4 import QtCore, QtGui
    