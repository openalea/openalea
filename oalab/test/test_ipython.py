from openalea.vpltk.check.ipython import has_ipython, has_ipython_config
from openalea.vpltk.shell.shell import get_interpreter_class, get_shell_class
from openalea.vpltk.qt import QtGui, QtCore
import sys

def test_has_qt():
    from openalea.vpltk.qt import QtGui, QtCore
    assert QtCore.QObject()

def test_has_ipython():
    assert has_ipython()
    
def test_has_ipython_config():
	assert has_ipython_config()
    
def test_get_interpreter():  
    interpreter_class = get_interpreter_class()
    shell_class = get_shell_class()
    
    assert bool(interpreter_class) and bool(shell_class)
    
    

