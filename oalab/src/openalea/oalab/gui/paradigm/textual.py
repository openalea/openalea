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

from openalea.oalab.editor.text_editor import RichTextEditor as Editor
from openalea.oalab.editor.highlight import GenericHighlighter



class TextualModelController(object):
    default_name = "file"
    default_file_name = "file"
    pattern = ""
    extension = ""
    icon = ""

    def __init__(self, name="", code="", model=None, filepath=None, editor_container=None, parent=None):
        self.filepath = filepath
        self.model = model
        self.name = name
        self.parent = parent
        self.editor_container = editor_container
        self._widget = None

    def instanciate_widget(self):
        """
        Instanciate the widget managing the current model

        :return: the instanciated widget
        """
        self._widget = Editor(parent=self.parent)
        wid = self._widget
        GenericHighlighter(wid.editor, filename=self.filepath)
        wid.applet = self

        wid.set_text(self.model.code)
        wid.replace_tab()
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

    def widget(self):
        """
        :return: the edition widget
        """
        return self._widget
