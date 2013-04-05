# -*- coding: utf-8 -*-
#
# Copyright © 2011 Pierre Raybaut
# Licensed under the terms of the MIT License
# (see spyderlib/__init__.py for details)

"""
spyderlib.qt.compat
-------------------

Transitional module providing compatibility functions intended to help 
migrating from PyQt to PySide.

This module should be fully compatible with:
    * PyQt >=v4.4
    * both PyQt API #1 and API #2
    * PySide
"""

import os
import sys

#===============================================================================
# QVariant conversion utilities
#===============================================================================

PYQT_API_1 = False
if os.environ['QT_API'] == 'pyqt':
    import sip
    try:
        PYQT_API_1 = sip.getapi('QVariant') == 1 # PyQt API #1
    except AttributeError:
        # PyQt <v4.6
        PYQT_API_1 = True
    def to_qvariant(pyobj=None):
        """Convert Python object to QVariant
        This is a transitional function from PyQt API #1 (QVariant exist) 
        to PyQt API #2 and Pyside (QVariant does not exist)"""
        if PYQT_API_1:
            # PyQt API #1
            from PyQt4.QtCore import QVariant
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


