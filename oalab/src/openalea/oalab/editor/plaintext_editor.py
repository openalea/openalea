

from openalea.vpltk.qt import QtGui
from openalea.oalab.editor.text_editor import RichTextEditor

class PlainTextEdit(QtGui.QPlainTextEdit):
    def setText(self, txt):
        self.setPlainText(txt)

    def set_text(self, txt):
        """
        Set text in the editor

        :param text: text you want to set
        """
        self.setPlainText(txt)

    def get_selected_text(self):
        cursor = self.textCursor()
        txt = cursor.selectedText()
        return unicode(txt).replace(u'\u2029', u'\n') # replace paragraph separators by new lines

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
        return unicode(txt).replace(u'\u2029', u'\n') # replace paragraph separators by new lines


class PlainTextEditor(RichTextEditor):
    def _default_editor(self, *args, **kwargs):
        return PlainTextEdit(*args, **kwargs)


