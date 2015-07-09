# -*- python -*-
#
#       Python Manager applet
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2013 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#                       Guillaume Baty <guillaume.baty@inria.fr>
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

from openalea.core.data import PythonFile
from openalea.core.model import PythonModel
import types


from openalea.oalab.paradigm.controller import ParadigmController


class PythonModelController(ParadigmController):
    default_name = PythonFile.default_name
    default_file_name = PythonFile.default_file_name
    pattern = PythonFile.pattern
    extension = PythonFile.extension
    icon = PythonFile.icon
    mimetype_data = PythonFile.mimetype
    mimetype_model = PythonModel.mimetype

    def _default_editor(self):
        try:
            from openalea.oalab.editor.pyeditor import PyCodeEditor as Editor
            editor = Editor(parent=self.parent)
        except ImportError:
            from openalea.oalab.editor.text_editor import RichTextEditor as Editor
            from openalea.oalab.editor.highlight import Highlighter
            editor = Editor(parent=self.parent)
            Highlighter(editor.editor)

        from openalea.oalab.service.drag_and_drop import add_drop_callback

        def drop_text(text, **kwds):
            cursor = kwds.get('cursor')
            cursor.insertText(text)
        add_drop_callback(editor, 'openalea/code.oalab', drop_text)
        add_drop_callback(editor, 'openalea/identifier', drop_text)

        return editor

    def instantiate_widget(self):
        self._widget = self._default_editor()
        from openalea.oalab.service.help import display_help

        # Add method to widget to display help
        def _diplay_help(widget):
            if self.model:
                display_help(self.model.get_documentation())
            else:
                display_help(self._obj.get_documentation())
        self._widget.display_help = types.MethodType(_diplay_help, self._widget)
        self._widget.applet = self

        self.read()
        return self.widget()

    def widget_value(self):
        if self._widget:
            return self._widget.get_text()
        else:
            return None

    def set_widget_value(self, value):
        if self._widget:
            self._widget.set_text(value)

    def execute(self):
        """
        Execute only selected text.
        """
        if self._widget:
            code = self._widget.get_selected_text()
            return self.model.execute(code)
