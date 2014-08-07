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
from openalea.vpltk.qt import QtGui, QtCore
from openalea.oalab.editor.highlight import Highlighter
import resources_rc # do not remove this import else icon are not drawn


class HistoryWidget(QtGui.QTextBrowser):
    """
    Widget which permit to display history
    """
    def __init__(self, parent=None):
        super(HistoryWidget, self).__init__(parent=parent)
        Highlighter(self)
        self.setAccessibleName("HistoryWidget")
        self.setText("")
        self.setLineWrapMode(QtGui.QTextEdit.NoWrap)

        clear_action = QtGui.QAction(QtGui.QIcon(":/images/resources/editraise.png"), "Clear History", self)
        QtCore.QObject.connect(clear_action, QtCore.SIGNAL('triggered(bool)'), self.clear)
        self._actions = [["Edit", "History", clear_action, 0]]

    def clear(self):
        """
        Remove existing history
        """
        self.setText("")

    def actions(self):
        return self._actions

    def append(self, txt):
        """
        Append a new line *txt* into existing history

        :param txt: text to add in history
        """
        previous_txt = self.toPlainText()
        if previous_txt:
            # Check if previous line is not the same as the new one
            if previous_txt.splitlines()[-1] != txt:
                txt = previous_txt + """
""" + txt
            else:
                txt = previous_txt
        self.setText(txt)


def main():
    from openalea.vpltk.qt import QtCore, QtGui
    from openalea.vpltk.shell.ipythoninterpreter import Interpreter
    from openalea.vpltk.shell.ipythonshell import ShellWidget
    import sys

    app = QtGui.QApplication(sys.argv)

    history = HistoryWidget()
    # Set interpreter
    interpreter = Interpreter()

    interpreter.locals['interp'] = interpreter
    interpreter.locals['hist'] = history
    # Set Shell Widget
    shellwdgt = ShellWidget(interpreter)

    mainWindow = QtGui.QMainWindow()

    dock_widget = QtGui.QDockWidget("shell", mainWindow)
    dock_widget.setWidget(shellwdgt)

    mainWindow.setCentralWidget(history)
    mainWindow.addDockWidget(QtCore.Qt.BottomDockWidgetArea, dock_widget)
    mainWindow.show()

    app.exec_()


if( __name__ == "__main__"):
    main()