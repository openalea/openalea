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
from openalea.core.algo.dataflow_evaluation import EvaluationException

def busy_cursor(f):
    """ Decorator to display a busy pointer """

    def wrapped(*args):
        try:
            QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.BusyCursor))
            ret = f(*args)
            
        finally:
            QtGui.QApplication.restoreOverrideCursor ()

        return ret
        
    return wrapped


def exception_display(f):
    """ Decorator to display exception if raised """

    def wrapped(*args):
        try:
            ret = f(*args)            

        except EvaluationException, e:
            self = args[0]
            if not isinstance(self,QtGui.QWidget):
                self = None            
            QtGui.QMessageBox.critical(self,'Exception raised !',e.exception.__class__.__name__+': '+ str(e.exception))
            raise e.exception
        
        except Exception, e:
            self = args[0]
            if not isinstance(self,QtGui.QWidget):
                self = None
            QtGui.QMessageBox.critical(None,'Exception raised !',e.__class__.__name__+': '+ str(e))

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

