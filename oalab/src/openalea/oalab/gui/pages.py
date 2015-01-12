# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2013 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
__revision__ = ""

__all__ = ['CreateFilePage', 'WelcomePage', 'WelcomePage2']

from openalea.core import logger
from openalea.core.path import path
from openalea.vpltk.qt import QtCore, QtGui
from openalea.vpltk.qt.compat import from_qvariant


class IApplet(object):

    def __init__(self):
        self.name = "welcome_page"

    def focus_change(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError

    def animate(self):
        raise NotImplementedError

    def step(self):
        raise NotImplementedError

    def stop(self):
        raise NotImplementedError

    def init(self):
        raise NotImplementedError

# fake methods, like if we have a real applet


class FakeApplet(object):

    """
    Empty implementation of IApplet
    """

    def __init__(self):
        self.name = "welcome_page"

    def focus_change(self):
        pass

    def run(self):
        pass

    def animate(self):
        pass

    def step(self):
        pass

    def stop(self):
        pass

    def init(self):
        pass


class WelcomePage2(QtGui.QWidget):

    """
    Create a widget page that display a list of actions as buttons
    """
    button_size = QtCore.QSize(200, 100)
    icon_size = QtCore.QSize(80, 80)
    stylesheet = "font-size: 12pt;"

    def __init__(self, actions=None, parent=None):
        QtGui.QWidget.__init__(self)
        self._layout = QtGui.QGridLayout(self)
        self._layout.setAlignment(QtCore.Qt.AlignCenter)
        if actions:
            self.set_actions(actions)

    def set_actions(self, actions):
        for i in reversed(range(self._layout.count())):
            widget = self._layout.itemAt(i).widget()
            widget.setParent(None)
            self._layout.removeWidget(widget)

        w = self.size().width()

        nx = w / self.button_size.width()
        if nx == 0:
            nx = 1

        for i, action in enumerate(actions):
            button = QtGui.QToolButton()
            button.setFixedSize(self.button_size)
            # button.setStyleSheet(self.stylesheet)
            button.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)

            qsize = QtCore.QSize(self.icon_size)
            button.setDefaultAction(action)
            button.setIconSize(qsize)

            self._layout.addWidget(button, i / nx, i % nx)


class WelcomePage(QtGui.QWidget):

    """
    Welcome page in the applet container.
    Permit to open an existing project,
    or to create a new one,
    or to work on src outside projects.
    """

    def __init__(self, session, controller, parent=None):
        super(WelcomePage, self).__init__(parent=parent)

        import warnings
        warnings.warn('Please use WelcomePage2 class instead', DeprecationWarning)

        self.session = session
        self.controller = controller
        layout = QtGui.QGridLayout()
        layout.setAlignment(QtCore.Qt.AlignCenter)

        max_size = QtCore.QSize(200, 60)
        min_size = QtCore.QSize(200, 60)

        default_icon = QtGui.QIcon(":/images/resources/openalealogo.png")
        newBtn = QtGui.QPushButton(default_icon, "New Project")
        newBtn.setMaximumSize(max_size)
        newBtn.setMinimumSize(min_size)

        openBtn = QtGui.QPushButton(default_icon, "Open Project")
        openBtn.setMaximumSize(max_size)
        openBtn.setMinimumSize(min_size)

        self.connect(newBtn, QtCore.SIGNAL("clicked()"), self.new)
        self.connect(openBtn, QtCore.SIGNAL("clicked()"), self.open)

        layout.addWidget(newBtn, 0, 0)
        layout.addWidget(openBtn, 1, 0)

        self.setLayout(layout)
        self.applet = FakeApplet()

        logger.debug("Open Welcome Page")

    def new(self):
        self.session._is_proj = True
        self.controller.project_manager.new()
        logger.debug("New Project from welcome page")

    def newScript(self):
        pass
        # self.controller.paradigm_container.addCreateFileTab()

    def open(self):
        self.session._is_proj = True
        self.controller.project_manager.open()
        logger.debug("Open Project from welcome page")

    def restoreSession(self):
        settings = QtCore.QSettings("OpenAlea", "OpenAleaLab")
        proj = from_qvariant(settings.value("session"))
        if proj is None:
            logger.debug("Can't restore previous session. May be it is empty")
        elif proj.is_project():
            self.session._is_proj = True
            name = proj.path.abspath()
            self.controller.project_manager.open(name)
            logger.debug("Restore previous session. (project)")


class CreateFilePage(QtGui.QWidget):

    """
    Welcome page in the applet container.
    Permit to open an existing project,
    or to create a new one,
    or to work on src outside projects.
    """

    def __init__(self, session, controller, parent=None):
        super(CreateFilePage, self).__init__(parent=parent)

        self.session = session
        self.controller = controller
        app_cont = self.controller.paradigm_container
        if app_cont is not None:
            layout = QtGui.QGridLayout()
            layout.setAlignment(QtCore.Qt.AlignCenter)

            max_size = QtCore.QSize(120, 80)
            min_size = QtCore.QSize(120, 80)

            text = QtGui.QLabel("Select type of file to create:")
            layout.addWidget(text, 0, 0, 1, -1)

            i, j = 1, 0
            for action in app_cont.paradigms_actions:
                newAction = QtGui.QToolButton()
                newAction.setDefaultAction(action)
                newAction.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
                newAction.setMinimumSize(min_size)
                layout.addWidget(newAction, i, j)
                if j == 0:
                    j = 1
                else:
                    j = 0
                    i += 1

            text2 = QtGui.QLabel("You can add a file from your computer:")
            layout.addWidget(text2, 10, 0, 1, -1)

            editFile = QtGui.QToolButton()
            editFile.setDefaultAction(app_cont.actionOpenFile)
            editFile.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
            editFile.setMinimumSize(min_size)
            layout.addWidget(editFile, 11, 0, 1, -1)
            self.setLayout(layout)

        # fake methods, like if we have a real applet
        class FakeApplet(object):

            def __init__(self):
                self.name = "create_file_page"

            def focus_change(self):
                pass

            def run(self):
                pass

            def animate(self):
                pass

            def step(self):
                pass

            def stop(self):
                pass

            def init(self):
                pass
        self.applet = FakeApplet()

        logger.debug("Open create_file Page")
