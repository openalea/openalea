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

    
#===============================================================================
# QVariant conversion utilities
#===============================================================================

PYQT_API_1 = False

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

