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
from openalea.vpltk.datamodel.python import PythonModel
from openalea.oalab.service.help import display_help
from openalea.oalab.control.manager import control_dict
import types


class PythonModelController(object):
    default_name = PythonModel.default_name
    default_file_name = PythonModel.default_file_name
    pattern = PythonModel.pattern
    extension = PythonModel.extension
    icon = PythonModel.icon

    def __init__(self, name="", code="", model=None, filepath=None, editor_container=None, parent=None):
        self.filepath = filepath
        if model is not None:
            self.model = model
        else:
            self.model = PythonModel(name=name, code=code, filepath=filepath)
        self.name = self.model.filename
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
        Highlighter(wid.editor)
        wid.applet = self

        # Add method to widget to display help
        def _diplay_help(widget):
            doc = widget.applet.model.get_documentation()
            display_help(doc)
        wid.display_help = types.MethodType(_diplay_help, wid)

        wid.set_text(self.model.code)
        wid.replace_tab()
        return self.widget()

    def execute(self):
        """
        Execute only selected text.
        """
        code = self.widget().get_selected_text()
        return self.model.execute(code)

    def run(self, *args, **kwargs):
        controls = control_dict()
        self.model.ns.update(controls)
        code = self.widget().get_text()
        self.model.code = code
        return self.model(*args, **kwargs)

    def step(self, *args, **kwargs):
        controls = control_dict()
        self.model.ns.update(controls)
        code = self.widget().get_text()
        self.model.code = code
        return self.model.step(*args, **kwargs)

    def stop(self, *args, **kwargs):
        return self.model.stop(*args, **kwargs)

    def animate(self, *args, **kwargs):
        controls = control_dict()
        self.model.ns.update(controls)
        code = self.widget().get_text()
        self.model.code = code
        return self.model.animate(*args, **kwargs)

    def init(self, *args, **kwargs):
        controls = control_dict()
        self.model.ns.update(controls)
        code = self.widget().get_text()
        self.model.code = code
        return self.model.init(*args, **kwargs)

    def widget(self):
        """
        :return: the edition widget
        """
        return self._widget
