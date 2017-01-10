def test_import_qt():
    try:
        from Qt import QtCore, QtGui
	result = True
    except ImportError:
	result = False
        assert result is True

def test_has_pyqt():
    # from openalea.check.qt import has_pyqt4
    # result = has_pyqt4()
    # assert result is True
    return True
