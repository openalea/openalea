"""
Provides Qt UI tools
"""
import os
from openalea.vpltk.qt import QT_API
from openalea.vpltk.qt import PYQT5_API
from openalea.vpltk.qt import PYQT4_API
from openalea.vpltk.qt import PYSIDE_API

try:
    _QT_API = os.environ.get(QT_API)
    if _QT_API in PYQT5_API:
        from PyQt5.uic import compileUi
        compile_args = dict(execute=False, indent=4)
    elif _QT_API in PYQT4_API:
        from PyQt4.uic import compileUi
        compile_args = dict(execute=False, indent=4)
    elif _QT_API in PYSIDE_API:
        from pysideuic import compileUi
        compile_args = dict(execute=False, indent=4, from_imports=False)
    elif _QT_API is None:
        # default
        from PyQt4.uic import compileUi
        compile_args = dict(execute=False, indent=4)
    else :
        raise NotImplementedError
except ImportError, e:
    message = 'You must install %s-tools' % os.environ['QT_API']
    e.args = (message,)
    raise e
