# -*- python -*-
#
#       Python Manager applet
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


from openalea.oalab.editor.highlight import Highlighter
from openalea.oalab.editor.text_editor import RichTextEditor as Editor
from openalea.oalab.gui.paradigm.controller import ParadigmController
from openalea.oalab.service.help import display_help
from pygments.lexers import guess_lexer_for_filename
from pygments.util import ClassNotFound
import types


class TextualModelController(ParadigmController):
    default_name = "file"
    default_file_name = "file"
    pattern = ""
    extension = ""
    icon = ""

    def _default_editor(self):
        from openalea.oalab.editor.plaintext_editor import PlainTextEditor as Editor
        editor = Editor(parent=self.parent)
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

    def runnable(self):
        return False

    def execute(self):
        """
        Execute only selected text.
        """
        return None

    def run(self, *args, **kwargs):
        return None

    def step(self, *args, **kwargs):
        return None

    def stop(self, *args, **kwargs):
        return None

    def animate(self, *args, **kwargs):
        return None

    def init(self, *args, **kwargs):
        return None
