"""
Provides widget classes and functions.

.. warning:: All PyQt4/PySide gui classes are exposed but when you use
    PyQt5, those classes are not available. Therefore, you should treat/use
    this package as if it was ``PyQt5.QtPrintSupport`` module.
"""
import os
from openalea.vpltk.qt import QT_API
from openalea.vpltk.qt import PYQT5_API
from openalea.vpltk.qt import PYQT4_API
from openalea.vpltk.qt import PYSIDE_API

if os.environ[QT_API] in PYQT5_API:
    from PyQt5.QtPrintSupport import *
elif os.environ[QT_API] in PYQT4_API:
    from PyQt4.QtGui import *
elif os.environ[QT_API] in PYSIDE_API:
    from PySide.QtGui import *
