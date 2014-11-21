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

    def instantiate_widget(self):
        """
        Instanciate the widget managing the current model

        :return: the instanciated widget
        """
        self._widget = Editor(parent=self.parent)
        wid = self._widget

        try:
            lexer = guess_lexer_for_filename(self.filepath, "")
        except ClassNotFound:
            lexer = None
        Highlighter(wid.editor, lexer=lexer)

        wid.applet = self

        # Add method to widget to display help
        def _diplay_help(widget):
            doc = widget.applet.model.get_documentation()
            display_help(doc)
        wid.display_help = types.MethodType(_diplay_help, wid)

        self.read()
        return self.widget()

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
