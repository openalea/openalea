from qt_loaders import loaded_api as _loaded_api
from qt_loaders import QT_API_PYQT, QT_API_PYQTv1, QT_API_PYSIDE

_qt_api = _loaded_api()
if _qt_api in [QT_API_PYQT, QT_API_PYQTv1]:
	from PyQt4.QtCore import *
elif _qt_api == QT_API_PYSIDE:
	from PySide.QtCore import *
else: # None loaded
	raise ImportError()

del QT_API_PYQT, QT_API_PYQTv1, QT_API_PYSIDE