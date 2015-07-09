

import sys
from pyqode.core.api import ColorScheme
from pyqode.python.backend import server
from pyqode.core import api
from pyqode.core import modes
from pyqode.core import panels
from pyqode.python import modes as pymodes
from pyqode.python import panels as pypanels
from pyqode.python.folding import PythonFoldDetector
from pyqode.python.widgets import PyCodeEditBase


class PyCodeEditor(PyCodeEditBase):

    """
    Extends PyCodeEditBase with a set of hardcoded modes and panels specifics
    to a python code editor widget.
    """
    DARK_STYLE = 0
    LIGHT_STYLE = 1

    mimetypes = ['text/x-python']

    def __init__(self, parent=None, server_script=server.__file__,
                 interpreter=sys.executable, args=None,
                 create_default_actions=True, color_scheme='default'):
        super(PyCodeEditor, self).__init__(
            parent=parent, create_default_actions=create_default_actions)
        self.backend.start(server_script, interpreter, args)
        self.setLineWrapMode(self.NoWrap)
        self.setWindowTitle("pyQode for LPy")

        # panels
        self.panels.append(panels.FoldingPanel())
        self.panels.append(panels.LineNumberPanel())
        self.panels.append(panels.CheckerPanel())
        self.panels.append(panels.GlobalCheckerPanel(),
                           panels.GlobalCheckerPanel.Position.RIGHT)
        self._panel_search = panels.SearchAndReplacePanel()
        self.panels.append(self._panel_search, panels.SearchAndReplacePanel.Position.BOTTOM)
        self.panels.append(panels.EncodingPanel(), api.Panel.Position.TOP)
        self.add_separator()
        self.panels.append(pypanels.QuickDocPanel(), api.Panel.Position.BOTTOM)

        # modes

        # generic
        self.modes.append(modes.CaretLineHighlighterMode())
        self.modes.append(modes.FileWatcherMode())
        self.modes.append(modes.RightMarginMode())
        self.modes.append(modes.ZoomMode())
        self.modes.append(modes.SymbolMatcherMode())
        self.modes.append(modes.CodeCompletionMode())
        self.modes.append(modes.OccurrencesHighlighterMode())
        self.modes.append(modes.SmartBackSpaceMode())
        self.modes.append(modes.ExtendedSelectionMode())

        # python specifics
        self.modes.append(pymodes.PyAutoIndentMode())
        self.modes.append(pymodes.PyAutoCompleteMode())
        # self.modes.append(pymodes.FrostedCheckerMode())
        self.modes.append(pymodes.PEP8CheckerMode())
        self.modes.append(pymodes.CalltipsMode())
        self.modes.append(pymodes.PyIndenterMode())
        self.modes.append(pymodes.GoToAssignmentsMode())
        self.modes.append(pymodes.CommentsMode())

        self.modes.append(pymodes.PythonSH(
            self.document(), color_scheme=ColorScheme(color_scheme)))
        self.syntax_highlighter.fold_detector = PythonFoldDetector()

    def clone(self):
        clone = self.__class__(
            parent=self.parent(), server_script=self.backend.server_script,
            interpreter=self.backend.interpreter, args=self.backend.args,
            color_scheme=self.syntax_highlighter.color_scheme.name)
        return clone

    def setPlainText(self, txt, mimetype='text/x-python', encoding='utf-8'):
        """
        Extends QCodeEdit.setPlainText to allow user to setPlainText without
        mimetype (since the python syntax highlighter does not use it).
        """
        api.CodeEdit.setPlainText(self, txt, mimetype, encoding)

    def __repr__(self):
        return 'LPyCodeEdit(path=%r)' % self.file.path

    def actions(self):
        """
        :return: list of actions to set in the menu.
        """
        return None

    def mainMenu(self):
        return "Project"

    def set_text(self, txt):
        self.setPlainText(txt)

    set_script = set_text

    def get_text(self, start='sof', end='eof'):
        """
        Return a part of the text.

        :param start: is the begining of what you want to get
        :param end: is the end of what you want to get
        :return: text which is contained in the editor between 'start' and 'end'
        """
        txt = self.toPlainText()
        if txt is None:
            txt = ""
        return unicode(txt).replace(u'\u2029', u'\n')  # replace paragraph separators by new lines

    def get_selected_text(self):
        cursor = self.textCursor()
        txt = cursor.selectedText()
        return unicode(txt).replace(u'\u2029', u'\n')  # replace paragraph separators by new lines

    def get_code(self, start='sof', end='eof'):
        return self.get_text(start=start, end=end)

    def replace_tab(self):
        raise NotImplementedError

    def goto(self):
        raise NotImplementedError

    def search(self):
        self._panel_search.enabled = not self._panel_search.enabled
        self._panel_search.setVisible(self._panel_search.enabled)
