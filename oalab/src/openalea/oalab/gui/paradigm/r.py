# -*- python -*-
#
#       R Manager applet
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
from openalea.oalab.model.r import RModel
from openalea.oalab.service.help import help


class RModelController(object):
    default_name = RModel.default_name
    default_file_name = RModel.default_file_name
    pattern = RModel.pattern
    extension = RModel.extension
    icon = RModel.icon

    def __init__(self, name="script.R", code="", model=None, filepath=None, interpreter=None, editor_container=None, parent=None):
        self.name = name
        self.filepath = filepath
        if model:
            self.model = model
        else:
            self.model = RModel(name=name, code=code)
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
        doc = self.model.get_documentation()
        help(doc)

    def run_selected_part(self):
        code = self.widget().get_selected_text()
        if len(code) == 0:
            code = self.widget().get_text()
        return self.model.run_code(code)

    def run(self):
        code = self.widget().get_text()
        self.model.code = code
        return self.model()

    def step(self):
        code = self.widget().get_text()
        self.model.code = code
        return self.model.step()

    def stop(self):
        return self.model.stop()

    def animate(self):
        code = self.widget().get_text()
        self.model.code = code
        return self.model.animate()

    def reinit(self):
        code = self.widget().get_text()
        self.model.code = code
        return self.model.init()

    def widget(self):
        """
        :return: the edition widget
        """
        return self._widget

    def save(self, name=None):
        code = self.widget().get_text()
        if name:
            self.model.filepath = name
        self.model.code = code
        self.widget().save(name=self.model.filepath)