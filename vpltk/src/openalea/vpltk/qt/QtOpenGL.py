"""
Provides QtNetwork classes and functions.
"""
import os
from openalea.vpltk.qt import QT_API
from openalea.vpltk.qt import PYQT5_API
from openalea.vpltk.qt import PYQT4_API
from openalea.vpltk.qt import PYSIDE_API

if os.environ[QT_API] in PYQT5_API:
    from PyQt5.QtOpenGL import *
elif os.environ[QT_API] in PYQT4_API:
    from PyQt4.QtOpenGL import *
elif os.environ[QT_API] in PYSIDE_API:
    from PySide.QtOpenGL import *
