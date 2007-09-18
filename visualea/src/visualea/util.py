# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2006 - 2007 INRIA - CIRAD - INRA  
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#                       Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the CeCILL v2 License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL_V2-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

__doc__="""
Utilities
"""

__license__= "CeCILL v2"
__revision__=" $Id: mainwindow.py 616 2007-06-29 17:20:52Z dufourko $ "


from PyQt4 import QtGui, QtCore

def busy_pointer(f):
    """ Decorator to display a busy pointer """

    def wrapped(*args):
        QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.BusyCursor))
        f(*args)
        QtGui.QApplication.restoreOverrideCursor ()
        
    return wrapped

