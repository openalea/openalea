""" import qt.py from IPython to set QString and QVariant

The goal is to have the same version of QString and QVariant in all OpenAlea
"""
import os

def load_qt():
    from PyQt4 import QtCore, QtGui, QtSvg
	try:
		# Try to set api of QString at 2 to have the same thing if user have IPython or not
		import sip
		sip.setapi("QString",2)
	except:
		pass
    return QtCore, QtGui, QtSvg

try: 
    from IPython.external.qt import QtCore, QtGui, QtSvg, QT_API
except ImportError:
    QT_API = 'pyqt'
    QtCore, QtGui, QtSvg = load_qt()
except:
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
    QT_API = 'pyqt'
    QtCore, QtGui, QtSvg = load_qt()
    
os.environ['QT_API'] = QT_API
    


