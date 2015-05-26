""" import qt.py from IPython to set QString and QVariant

The goal is to have the same version of QString and QVariant in all OpenAlea
"""

try:
    from openalea.vpltk.qt import QtCore
except ImportError:
    pass

try:
    from openalea.vpltk.qt import QtGui
except ImportError:
    pass

try:
    from openalea.vpltk.qt import QtOpenGL
except ImportError:
    pass

try:
    from openalea.vpltk.qt import QtTest
except ImportError:
    pass

try:
    from openalea.vpltk.qt import QtSql
except ImportError:
    pass

try:
    from openalea.vpltk.qt import QtWebKit
except ImportError:
    pass

try:
    from openalea.vpltk.qt import QtSvg
except ImportError:
    pass

try:
    from openalea.vpltk.qt import phonon
except ImportError:
    pass
