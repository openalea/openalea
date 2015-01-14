# -*- python -*-
#
#       LPy manager applet.
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


from openalea.oalab.gui.paradigm.python import PythonModelController
from openalea.plantlab.lpy_data import LPyFile
from openalea.oalab.session.session import Session
from openalea.oalab.service.help import display_help


class LPyModelController(PythonModelController):
    default_name = LPyFile.default_name
    default_file_name = LPyFile.default_file_name
    pattern = LPyFile.pattern
    extension = LPyFile.extension
    icon = LPyFile.icon
    mimetype_data = LPyFile.mimetype
    mimetype_model = 'text/vnd-lpy'

    def __init__(self, **kwds):
        PythonModelController.__init__(self, **kwds)
        self.session = Session()

    def _default_editor(self):
        from openalea.oalab.editor.text_editor import RichTextEditor as Editor
        from openalea.oalab.editor.highlight import Highlighter
        editor = Editor(parent=self.parent)
        Highlighter(editor.editor)
        return editor

    def focus_change(self):
        """
        Set doc string in Help widget when focus changed
        """
        doc = self.model.get_documentation()
        display_help(doc)

    def runnable(self):
        return self._model.__class__.__name__ == 'LPyModel'

    def update_world(self):
        # TODO: remove this hard link!
        # Update world ?
        world = self.session.world
        world[self.model.scene_name] = self.model.axialtree

    def namespace(self, **kwargs):
        ns = PythonModelController.namespace(self, **kwargs)
        # Extract one colorlist to set as THE colormap.
        # In case of ambiguity, select the one whose the name contains lpy.
        # Else select a random one.

        def select_colormap():
            # @GBY must move to plantgl or lpy
            from openalea.core.control.manager import ControlManager
            from openalea.plantlab.tools import to_material
            controls = ControlManager().namespace(interface='IColorList')
            for v in controls.values():
                return to_material(v)

        materials = select_colormap()
        if materials:
            for i, mat in enumerate(materials):
                self.model.lsystem.context().turtle.setMaterial(i, mat)
        ns['colormap'] = materials
        return ns

    def run(self, *args, **kwargs):
        ret = PythonModelController.run(self, *args, **kwargs)
        self.update_world()
        return ret

    def step(self, i=None, *args, **kwargs):
        self.apply()
        ret = self.model.step(i=i, *args, **kwargs)
        self.update_world()
        return ret

    def stop(self, *args, **kwargs):
        ret = PythonModelController.stop(self, *args, **kwargs)
        self.update_world()
        return ret

    def animate(self, *args, **kwargs):
        ret = PythonModelController.animate(self, *args, **kwargs)
        self.update_world()
        return ret

    def init(self, *args, **kwargs):
        ret = PythonModelController.init(self, *args, **kwargs)
        self.update_world()
        return ret

    def widget(self):
        """
        :return: the edition widget
        """
        return self._widget
