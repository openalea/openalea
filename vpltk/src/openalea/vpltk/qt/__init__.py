# -*- coding: utf-8 -*-
#
# Copyright © 2011 Spyder
# Contributor: Pierre Raybaut
# Website: http://github.com/spyder-ide/spyder
#
# Copyright © 2012-2013 pyLot - andheo
# Contributor: Guillaume Baty
#
# Copyright © 2014 INRIA - CIRAD - INRA
# Contributor: Frédéric Boudon
# http://github.com/openalea/openalea
#
# Copyright © 2015 PyQode
# Contributor: Colin Duquesnoy
# Website: http://github.com/pyqode/pyqode.qt
#
# -------------------------------------------
# Licensed under the terms of the MIT License
# -------------------------------------------


import os
import sys
import logging

__version__ = '2.6.0.dev0'
__version_info__ = None
is_pyqt46 = False

PyQt_license_warning = "PyQt4 used: your application or derivative works must be released under GPL or CeCILL license !"

#: Qt API environment variable name
QT_API = 'QT_API'
#: names of the expected PyQt5 api
PYQT5_API = ['pyqt5']
#: names of the expected PyQt4 api
PYQT4_API = [
    'pyqt',  # name used in IPython.qt
    'pyqt4'  # pyqode.qt original name
]
#: names of the expected PySide api
PYSIDE_API = ['pyside']


# If IPython is installed, use its order to avoid multiple python-qt loads
try:
    from IPython.external.qt import api_opts
except ImportError:
    QT_API_ORDER = ['pyside', 'pyqt', 'pyqt5']
else:
    QT_API_ORDER = api_opts
_api_version = int(os.environ.setdefault('QT_API_VERSION', '0'))


def setup_apiv2():
    """
    Setup apiv2 when using PyQt4 and Python2.
    """
    # setup PyQt api to version 2
    if sys.version_info[0] == 2:
        import sip
        if _api_version:
            default = _api_version
            apis = [
                ("QDate", default),
                ("QDateTime", default),
                ("QString", default),
                ("QTextStream", default),
                ("QTime", default),
                ("QUrl", default),
                ("QVariant", default),
                ("QFileDialog", default),
            ]
            for name, version in apis:
                try:
                    sip.setapi(name, version)
                except ValueError:
                    logging.getLogger(__name__).critical("failed to set up sip api to version 2 for PyQt4")
                    raise ImportError('PyQt4')
        from PyQt4.QtCore import PYQT_VERSION_STR as __version__


def load_pyside():
    logging.getLogger(__name__).debug('trying PySide')
    import PySide
    os.environ[QT_API] = PYSIDE_API[0]
    logging.getLogger(__name__).debug('imported PySide')


def load_pyqt4():
    global is_pyqt46, __version_info__
    logging.getLogger(__name__).debug('trying PyQt4')
    import PyQt4
    os.environ[QT_API] = PYQT4_API[0]
    setup_apiv2()
    logging.getLogger(__name__).debug('imported PyQt4')
    __version_info__ = tuple(__version__.split('.') + ['final', 1])
    is_pyqt46 = __version__.startswith('4.6')
    print PyQt_license_warning


def load_pyqt5():
    logging.getLogger(__name__).debug('trying PyQt5')
    import PyQt5
    os.environ[QT_API] = PYQT5_API[0]
    logging.getLogger(__name__).debug('imported PyQt5')
    print PyQt_license_warning


QT_API_LOADER = {}
for API in PYSIDE_API:
    QT_API_LOADER[API] = load_pyside
for API in PYQT4_API:
    QT_API_LOADER[API] = load_pyqt4
for API in PYQT5_API:
    QT_API_LOADER[API] = load_pyqt5


class PythonQtError(Exception):

    """
    Error raise if no bindings could be selected
    """
    pass


def autodetect():
    """
    Auto-detects and use the first available QT_API by importing them in order defined in QT_API_ORDER
    """
    logging.getLogger(__name__).debug('auto-detecting QT_API')
    for API in QT_API_ORDER:
        try:
            QT_API_LOADER[API]()
        except ImportError:
            continue
        else:
            break


if QT_API in os.environ:
    # check if the selected QT_API is available
    try:
        if os.environ[QT_API].lower() in PYQT5_API:
            load_pyqt5()
        elif os.environ[QT_API].lower() in PYQT4_API:
            load_pyqt4()
        elif os.environ[QT_API].lower() in PYSIDE_API:
            load_pyside()
    except ImportError:
        logging.getLogger(__name__).warning(
            'failed to import the selected QT_API: %s',
            os.environ[QT_API])
        # use the auto-detected API if possible
        autodetect()
else:
    # user did not select a qt api, let's perform auto-detection
    autodetect()
