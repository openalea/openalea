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

from Qt import QtCore, QtGui, QtWidgets

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

def to_qvariant(pyobj=None):
    return QtCore.QVariant(pyobj)

def from_qvariant(qobj=None, convfunc=None):
    assert callable(convfunc)
    if convfunc in (unicode, str):
        return convfunc(qobj.toString())
    elif convfunc is bool:
        return qobj.toBool()
    elif convfunc is int:
        return qobj.toInt()[0]
    elif convfunc is float:
        return qobj.toDouble()[0]
    else:
        return convfunc(qobj)

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
