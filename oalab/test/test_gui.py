from openalea.oalab.session.session import Session
from openalea.oalab.gui.menu import PanedMenu
from openalea.oalab.gui.mainwindow import MainWindow
from openalea.oalab.editor.text_editor import TextEditor
from openalea.oalab.gui.allwidgets import AllWidgets
from openalea.vpltk.project.manager import ProjectManager
from openalea.vpltk.qt import QtGui, QtCore
import sys

app = QtGui.QApplication(sys.argv)
session = Session()
controller = AllWidgets(session)
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
    assert container.count() == 4
    container.closeTab()
    assert container.count() == 3
    assert type(session.help.actions()) == type(list())
    assert session.help.mainMenu() == "Help"
    container.reset()
    assert container.count() == 0
"""

"""
def test_session_and_mainwindow():
    project_manager = ProjectManager()
    mw = MainWindow(session, controller, parent=None)
    assert session.project.name == project_manager.default().name
    assert controller.applets['Store'].actions() == None
    assert controller.applets['Store'].mainMenu() == "Package Store"
"""

def test_text_edit():
    editor = TextEditor(session, controller, parent=None)
    assert editor is not None


def test_create_paned_menu():
    menu = PanedMenu()
    obj = QtCore.QObject()
    myaction = QtGui.QAction("Plop", obj)
    menu.addBtn(pane_name="Test Pane", group_name="Test Group", btn_name="Test Button", btn_icon=QtGui.QIcon(""),
                btn_type=0)
    menu.addBtnByAction(pane_name="Test Pane 2", group_name="Test Group 2", action=myaction, btn_type=1)
    menu.addSpecialTab(label="specialtab", widget=QtGui.QWidget())
    assert len(menu.tab_name) == 3
