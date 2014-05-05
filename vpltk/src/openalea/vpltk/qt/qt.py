""" import qt.py from IPython to set QString and QVariant

The goal is to have the same version of QString and QVariant in all OpenAlea
"""
import os
# print "qt"
try: 
    from IPython.external.qt import QtCore, QtGui, QtSvg, QT_API
except ImportError:
    # Use local IPython qt loader
    from qt_loaders import (load_qt, QT_API_PYSIDE, QT_API_PYQT, QT_API_PYQT_DEFAULT)
    
    QT_API = os.environ.get('QT_API', None)
    if QT_API not in [QT_API_PYSIDE, QT_API_PYQT, None]:
        raise RuntimeError("Invalid Qt API %r, valid values are: %r, %r" %
                           (QT_API, QT_API_PYSIDE, QT_API_PYQT))
    if QT_API is None:
        api_opts = [QT_API_PYSIDE, QT_API_PYQT]
    else:
        api_opts = [QT_API]
    
    try:
        QtCore, QtGui, QtSvg, QT_API = load_qt(api_opts)    
    except ImportError, e :
        import warnings
        message = """
    
===============================================================================
You are trying to import openalea.vpltk.qt.
This import will set api of Qt to version 2 (cf sip).

But api is yet set to 1!

So, if you want to use IPython inside OpenAlea applications (ie. LPy, 
Visualea...), you have to import openalea.vpltk.qt before other applications 
using Qt (ex: matplotlib with backend qtAgg).

Else, you can continue: api 1 will be used.
===============================================================================

"""
        warnings.warn(message)
        QT_API = QT_API_PYQT_DEFAULT
        QtCore, QtGui, QtSvg, QT_API = load_qt([QT_API])
    
os.environ['QT_API'] = QT_API
    


