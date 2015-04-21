"""
Provides Qt UI tools
"""
import os
from openalea.vpltk.qt import QT_API
from openalea.vpltk.qt import PYQT5_API
from openalea.vpltk.qt import PYQT4_API
from openalea.vpltk.qt import PYSIDE_API

try:
    if os.environ[QT_API] in PYQT5_API:
        from PyQt5.QtNetwork import *
    elif os.environ[QT_API] in PYQT4_API:
        from PyQt4.uic import compileUi
        compile_args = dict(execute=False, indent=4)
    elif os.environ[QT_API] in PYSIDE_API:
        from pysideuic import compileUi
        compile_args = dict(execute=False, indent=4, from_imports=False)
except ImportError, e:
    message = 'You must install %s-tools' % os.environ['QT_API']
    e.args = (message,)
    raise e
