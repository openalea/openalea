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
__revision__=" $Id$ "


from PyQt4 import QtGui, QtCore

def busy_pointer(f):
    """ Decorator to display a busy pointer """

    def wrapped(*args):

        try:
            QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.BusyCursor))
            ret = f(*args)
            
        finally:
            QtGui.QApplication.restoreOverrideCursor ()

        return ret
        
    return wrapped


def open_dialog(parent, widget, title, delete_on_close=True):
    """
    Open a widget in a dialog box
    Return dialog instance
    """

    # Open dialog
    dialog = QtGui.QDialog(parent)
    if(delete_on_close):
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
    widget.setParent(dialog)
    
    vboxlayout = QtGui.QVBoxLayout(dialog)
    vboxlayout.setMargin(3)
    vboxlayout.setSpacing(5)
    vboxlayout.addWidget(widget)

    dialog.setWindowTitle(title)
    dialog.show()

    return dialog

