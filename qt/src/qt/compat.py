# -*- coding: utf-8 -*-

# -*- python -*-
#
#       Copyright © 2011 Pierre Raybaut
#       Copyright © 2012-2013 pyLot - andheo
#       Copyright © 2015 INRIA - CIRAD - INRA
#
#       File author(s): Pierre Raybaut
#
#       File contributor(s): Guillaume Baty
#
#       Licensed under the terms of the MIT License
#       (see spyderlib/__init__.py for details)
#       Spyderlib WebSite : https://github.com/spyder-ide/spyder
#
###############################################################################

import os
import sys

import Qt
PYQT4 = (Qt.__binding__ == 'PyQt4')

from Qt import QtCore, QtGui, QtWidgets

import collections

try:
    from openalea.core.path import path as Path
except ImportError:
    FilePath = DirPath = Path = str
else:
    FilePath = DirPath = Path


_tab_position = {
    0: QtWidgets.QTabWidget.North,
    1: QtWidgets.QTabWidget.South,
    2: QtWidgets.QTabWidget.West,
    3: QtWidgets.QTabWidget.East,
}

def arrange_path(path, path_class=Path):
    """
    Return a Path, FilePath or DirPath dependings on path nature.
    Path is used for special path like device "files" or path not
    existing on disk.  If path is empty, returns None.

    If path do not exists on disk or is not file nor directory
    (like /dev/xyz on linux),it return a path_class.
    """

    if not path:
        return None

    path = Path(unicode(path))

    if path.isfile():
        return FilePath(path)
    elif path.isdir():
        return DirPath(path)
    else:
        return path_class(path)


if PYQT4:
    import sip
    try:
        PYQT_API_1 = sip.getapi('QVariant') == 1  # PyQt API #1
    except AttributeError:
        # PyQt <v4.6
        PYQT_API_1 = True

    def to_qvariant(pyobj=None):
        """Convert Python object to QVariant
        This is a transitional function from PyQt API #1 (QVariant exist)
        to PyQt API #2 and Pyside (QVariant does not exist)"""
        if PYQT_API_1:
            # PyQt API #1
            from QtCore import QVariant
            return QVariant(pyobj)
        else:
            # PyQt API #2
            return pyobj

    def from_qvariant(qobj=None, convfunc=None):
        """Convert QVariant object to Python object
        This is a transitional function from PyQt API #1 (QVariant exist)
        to PyQt API #2 and Pyside (QVariant does not exist)"""
        if PYQT_API_1:
            # PyQt API #1
            assert isinstance(convfunc, collections.Callable)
            if convfunc in TEXT_TYPES or convfunc is to_text_string:
                return convfunc(qobj.toString())
            elif convfunc is bool:
                return qobj.toBool()
            elif convfunc is int:
                return qobj.toInt()[0]
            elif convfunc is float:
                return qobj.toDouble()[0]
            else:
                return convfunc(qobj)
        else:
            # PyQt API #2
            return qobj
else:
    def to_qvariant(obj=None):  # analysis:ignore
        """Convert Python object to QVariant
        This is a transitional function from PyQt API#1 (QVariant exist)
        to PyQt API#2 and Pyside (QVariant does not exist)"""
        return obj

    def from_qvariant(qobj=None, pytype=None):  # analysis:ignore
        """Convert QVariant object to Python object
        This is a transitional function from PyQt API #1 (QVariant exist)
        to PyQt API #2 and Pyside (QVariant does not exist)"""
        return qobj


def getexistingdirectory(parent=None, caption='', basedir='', options=None):
    if options is None:
        options = QFileDialog.ShowDirsOnly

    if sys.platform == "win32":
        _temp1, _temp2 = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = None, None
    try:
        result = QtWidgets.QFileDialog.getExistingDirectory(parent, caption, basedir, options)
    finally:
        if sys.platform == "win32":
            sys.stdout, sys.stderr = _temp1, _temp2
    if not isinstance(result, basestring):
        result = arrange_path(result, path_class=Path)

    return result

def _qfiledialog_wrapper(attr, parent=None, caption=u'', basedir=u'', filters=u'', selectedfilter=u'', options=None, path_class=Path):

    if options is None:
        options = QtWidgets.QFileDialog.Options(0)

    tuple_returned = True
    try:
        func = getattr(QtWidgets.QFileDialog, attr + 'AndFilter')
    except AttributeError:
        func = getattr(QtWidgets.QFileDialog, attr)
        selectedfilter = unicode("")
        tuple_returned = False

    if sys.platform == "win32":
        _temp1, _temp2 = sys.stdout, sys.stderr
        sys.stdout, sys.stderr = None, None
    try:
        result = func(parent, caption, basedir, filters)
    finally:
        if sys.platform == "win32":
            sys.stdout, sys.stderr = _temp1, _temp2

    if tuple_returned:
        output, selectedfilter = result
    else:
        output = arrange_path(result, path_class=path_class)

    selectedfilter = unicode(selectedfilter)

    if isinstance(output, unicode):
        output = unicode(output)
    elif output is None:
        pass
    else:
        output = [unicode(fname) for fname in output]

    if isinstance(output, unicode):
        output = arrange_path(output, path_class=path_class)
    elif isinstance(output, list):
        output = [arrange_path(fname, path_class=path_class) for fname in output]
    else:
        output = None

    return output, selectedfilter

def getopenfilename(parent=None, caption=u'', basedir=u'', filters=u'', selectedfilter=u'', options=None):
    return _qfiledialog_wrapper('getOpenFileName', parent=parent,
                                caption=caption, basedir=basedir,
                                filters=filters, selectedfilter=selectedfilter,
                                options=options, path_class=FilePath)


def getopenfilenames(parent=None, caption=u'', basedir=u'', filters=u'', selectedfilter=u'', options=None):
    return _qfiledialog_wrapper('getOpenFileNames', parent=parent,
                                caption=caption, basedir=basedir,
                                filters=filters, selectedfilter=selectedfilter,
                                options=options, path_class=FilePath)


def getsavefilename(parent=None, caption=u'', basedir=u'', filters=u'', selectedfilter=u'', options=None):
    return _qfiledialog_wrapper('getSaveFileName', parent=parent,
                                caption=caption, basedir=basedir,
                                filters=filters, selectedfilter=selectedfilter,
                                options=options, path_class=FilePath)

def tabposition_qt(value):
    if isinstance(value, int):
        return _tab_position[value]
    else:
        return value

def tabposition_int(value):
    if isinstance(value, int):
        return value
    else:
        for idx, pos in _tab_position.items():
            if pos == value:
                return idx

def orientation_qt(value):
    if value == 1:
        return QtCore.Qt.Horizontal
    elif value == 2:
        return QtCore.Qt.Vertical
    else:
        return value

def orientation_int(value):
    if isinstance(value, int):
        return value
    else:
        if value == QtCore.Qt.Horizontal:
            return 1
        elif value == QtCore.Qt.Vertical:
            return 2
        else:
            return 0
