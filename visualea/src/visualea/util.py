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
import sys
import traceback as tb


def busy_cursor(f):
    """ Decorator to display a busy pointer """

    def wrapped(*args):
        try:
            QtGui.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.BusyCursor))
            ret = f(*args)
            QtGui.QApplication.restoreOverrideCursor ()
            return ret
        except:
            QtGui.QApplication.restoreOverrideCursor ()
            raise
        
    return wrapped


def processText(txt):
    txt = txt.replace('File','<B>File</B>')
    txt = txt.replace(', in',', <B>in</B>')
    txt = txt.replace(', line',', <B>line</B>')
    return txt

use_error_box = True
errorbox = None

def exception_display(f):
    """ Decorator to display exception if raised """
    
    def wrapped(*args):
        global use_error_box
        global errorbox
        try:
            return f(*args)            
        except EvaluationException, e:
            self = args[0]
            if not isinstance(self, QtGui.QWidget):
                self = None
            txt = e.exception.__class__.__name__+': '+ str(e.exception)
            
            if not use_error_box:
                QtGui.QMessageBox.critical(None,'Exception raised !',txt)
            else:
                if errorbox is None:
                    errorbox = QtGui.QErrorMessage(self)
                    errorbox.setModal(False)
                errorbox.setWindowTitle(txt)
                errorbox.showMessage(processText('<BR>'.join(e.exc_info)))
                errorbox.exec_()
            raise e.exception
        
        except Exception, e:
            self = args[0]
            if not isinstance(self,QtGui.QWidget):
                self = None
            txt = e.__class__.__name__+': '+ str(e)
            if not use_error_box:
                QtGui.QMessageBox.critical(None,'Exception raised !',txt)
            else:
                if errorbox is None:
                    errorbox = QtGui.QErrorMessage(self)
                    errorbox.setModal(False)
                errorbox.setWindowTitle(txt)
                errorbox.showMessage(processText('<BR>'.join(tb.format_tb(sys.exc_info()[2]))))
                errorbox.exec_()
            raise e.exception

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

