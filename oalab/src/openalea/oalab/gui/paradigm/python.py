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
from openalea.oalab.editor.highlight import Highlighter
from openalea.oalab.model.python import PythonModel


class PythonModelController(object):
    default_name = PythonModel.default_name
    default_file_name = PythonModel.default_file_name
    pattern = PythonModel.pattern
    extension = PythonModel.extension
    icon = PythonModel.icon

    def __init__(self, name="", code="", model=None, filepath=None, interpreter=None, editor_container=None, parent=None):
        self.name = name
        self.filepath = filepath
        if model:
            self.model = model
        else:
            self.model = PythonModel(name=name, code=code)
        self.parent = parent
        self.editor_container = editor_container
        self._widget = None

    def instanciate_widget(self):
        self._widget = Editor(editor_container=self.editor_container, parent=self.parent)
        Highlighter(self._widget.editor)
        self.widget().applet = self

        self.widget().set_text(self.model.code)
        return self.widget()

    def focus_change(self):
        """
        Set doc string in Help widget when focus changed
        """
        txt = """
<H1><IMG SRC=%s
 ALT="icon"
 HEIGHT=25
 WIDTH=25
 TITLE="Python logo">Python</H1>

more informations: http://www.python.org/
"""%str(self.icon)
        return txt

    def run_selected_part(self, *args, **kwargs):
        code = self.widget().get_selected_text()
        if len(code) == 0:
            code = self.widget().get_text()
        return self.model.run_code(code, *args, **kwargs)

    def run(self, *args, **kwargs):
        code = self.widget().get_text()
        self.model.code = code
        return self.model(*args, **kwargs)

    def step(self, *args, **kwargs):
        code = self.widget().get_text()
        self.model.code = code
        return self.model.step(*args, **kwargs)

    def stop(self, *args, **kwargs):
        return self.model.stop(*args, **kwargs)

    def animate(self, *args, **kwargs):
        code = self.widget().get_text()
        self.model.code = code
        return self.model.animate(*args, **kwargs)

    def reinit(self, *args, **kwargs):
        code = self.widget().get_text()
        self.model.code = code
        return self.model.init(*args, **kwargs)

    def widget(self):
        """
        :return: the edition widget
        """
        return self._widget
