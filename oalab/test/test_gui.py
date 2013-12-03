from openalea.oalab.gui.session import Session
from openalea.oalab.gui.menu import PanedMenu
from openalea.oalab.gui.mainwindow import MainWindow
from openalea.oalab.applets.container import AppletContainer
from openalea.oalab.editor.text_editor import TextEditor

from openalea.vpltk.qt import QtGui, QtCore
import sys

app = QtGui.QApplication(sys.argv)
session = Session()

def test_session_and_mainwindow():
    mw = MainWindow(session)
    session.store.showhide()
    session.store.showhide()
    assert session.project == None
    assert session.store.mainMenu() == "Package Store" 

def test_applet_container():
    container = AppletContainer(session)
    assert type(container.applets) == type(list())
    assert container.count() == 1
    container.rmDefaultTab()
    assert container.count() == 0

def test_text_edit():
    editor = TextEditor(session)
    assert editor is not None
"""
def test_applet_container_opentab():
    container = AppletContainer(session)
    assert type(container.applets) == type(list())
    assert container.count() == 1
    container.rmDefaultTab()
    assert container.count() == 0

    container.openTab(applet_type="py", tab_name="plop.py", script="print('hello world')")
    container.openTab(applet_type="lpy", tab_name="plop.lpy", script="")
    container.openTab(applet_type="r", tab_name="plop.r", script="")
    container.openTab(applet_type="wpy", tab_name="plop.wpy", script="")
    a = container.count() #4
    container.closeTab()
    a += container.count() #7
    if type(session.help.actions()) == type(list()):
        a += 1 #8
    if session.help.mainMenu() == "Help":
        a += 1 #9
    assert a == 9
    
    container.reset()
    assert container.count() == 0"""

def test_create_paned_menu():
    menu = PanedMenu()
    obj = QtCore.QObject()
    myaction = QtGui.QAction("Plop", obj)
    menu.addBtn(pane_name="Test Pane", group_name="Test Group", btn_name="Test Button", btn_icon=QtGui.QIcon(""), btn_type=0)
    menu.addBtnByAction(pane_name="Test Pane 2", group_name="Test Group 2", action=myaction, btn_type=1)
    menu.addSpecialTab(label="specialtab", widget=QtGui.QWidget())
    assert len(menu.tab_name) == 3
    