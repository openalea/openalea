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

from openalea.oalab.editor.text_editor import RichTextEditor as Editor
from openalea.oalab.editor.highlight import Highlighter
from openalea.plantlab.lpy_lexer import LPyLexer
from openalea.plantlab.picklable_curves import geometry_2_piklable_geometry
from openalea.lpy import Lsystem
from openalea.lpy.__lpy_kernel__ import LpyParsing
from openalea.lpy.gui.objectmanagers import get_managers
from openalea.lpy.gui.scalar import ProduceScalar
from openalea.plantlab.lpy import LPyModel
from openalea.oalab.service.help import display_help
import types

def import_lpy_file(script):
    """
    Extract from an "old style" LPy file script part (str) and associated control (dict).
    Permit compatibility between LPy and OALab.

    :param: script to filter (str)
    :return: lpy script (str) without end begining with "###### INITIALISATION ######"
    and a dict which contain the control (dict)
    """
    control = dict()

    if script is None: script = ""
    beginTag = LpyParsing.InitialisationBeginTag
    if not beginTag in script:
        return str(script), control
    else:
        txts = str(script).split(beginTag)
        new_script = txts[0]
        context_to_translate = txts[1]
        context = Lsystem().context()
        context.initialiseFrom(beginTag + context_to_translate)

        managers = get_managers()
        visualparameters = []
        scalars = []
        functions = []
        curves = []
        geoms = []

        lpy_code_version = 1.0
        if context.has_key('__lpy_code_version__'):
            lpy_code_version = context['__lpy_code_version__']
        if context.has_key('__scalars__'):
            scalars_ = context['__scalars__']
            scalars = [ ProduceScalar(v) for v in scalars_ ]
        if context.has_key('__functions__') and lpy_code_version <= 1.0 :
            functions = context['__functions__']
            for n, c in functions: c.name = n
            functions = [ c for n, c in functions ]
            funcmanager = managers['Function']
            geoms += [(funcmanager, func) for func in functions]
        if context.has_key('__curves__') and lpy_code_version <= 1.0 :
            curves = context['__curves__']
            for n, c in curves: c.name = n
            curves = [ c for n, c in curves ]
            curvemanager = managers['Curve2D']
            geoms += [ (curvemanager, curve) for curve in curves ]
        if context.has_key('__parameterset__'):
            for panelinfo, objects in context['__parameterset__']:
                for typename, obj in objects:
                    visualparameters.append((managers[typename], obj))

        control["color map"] = context.turtle.getColorList()
        for scalar in scalars:
            control[unicode(scalar.name)] = scalar
        for (manager, geom) in geoms:
            if geom != list():
                new_obj, new_name = geometry_2_piklable_geometry(manager, geom)
                control[new_name] = new_obj
        for (manager, geom) in visualparameters:
            if geom != list():
                new_obj, new_name = geometry_2_piklable_geometry(manager, geom)
                control[new_name] = new_obj

        return new_script, control


class LPyModelController(object):
    default_name = LPyModel.default_name
    default_file_name = LPyModel.default_file_name
    pattern = LPyModel.pattern
    extension = LPyModel.extension
    icon = LPyModel.icon

    def __init__(self, name="", code="", model=None, filepath=None, editor_container=None, parent=None):
        self.filepath = filepath
        if model:
            self.model = model
        else:
            self.model = LPyModel(name=name, code=code)
        self.name = self.model.filename
        self.parent = parent
        self.editor_container = editor_container
        self._widget = None

        from openalea.core.service.ipython import interpreter
        interp = interpreter()
        if interp:
            interp.locals['lsystem'] = self.model.lsystem

    def instanciate_widget(self):
        # todo register viewer
        self._widget = Editor(parent=self.parent)
        wid = self._widget
        Highlighter(wid.editor, lexer=LPyLexer())
        wid.applet = self

        # Add method to widget to display help
        def _diplay_help(widget):
            doc = widget.applet.model.get_documentation()
            display_help(doc)
        wid.display_help = types.MethodType(_diplay_help, wid)

        wid.set_text(self.model.read())
        wid.replace_tab()
        return wid

    def focus_change(self):
        """
        Set doc string in Help widget when focus changed
        """
        doc = self.model.get_documentation()
        display_help(doc)

    def execute(self):
        """
        Run selected code like a PYTHON code (not LPy code).
        If nothing selected, run like LPy (not Python).
        """
        code = self.widget().get_selected_text()
        return self.model.execute(code)

    def run(self, *args, **kwargs):
        # Extract one colorlist to set as THE colormap.
        # In case of ambiguity, select the one whose the name contains lpy.
        # Else select a random one.
        def select_colormap():
            # @GBY must move to plantgl or lpy
            from openalea.core.control.manager import ControlManager
            from openalea.plantgl.oaplugins.controls import to_material
            controls = ControlManager().namespace(interface='IColorList')
            for v in controls.values():
                return to_material(v)

        materials = select_colormap()
        if materials:
            for i, mat in enumerate(materials):
                self.model.lsystem.context().turtle.setMaterial(i, mat)

        code = self.widget().get_text()
        self.model.content = code

        # todo: put result in the world ?
        ret = self.model(*args, **kwargs)
        # TODO: remove this hard link!
        world = self.editor_container.session.world
        world[self.model.scene_name] = self.model.axialtree

        return ret

    def step(self, i=None, *args, **kwargs):
        code = self.widget().get_text()
        if code != self.model.read():
            self.model.content = code

        # todo: put result in the world ?
        ret = self.model.step(i=i, *args, **kwargs)
        # TODO: remove this hard link!
        world = self.editor_container.session.world
        world[self.model.scene_name] = self.model.axialtree

        return ret

    def stop(self, *args, **kwargs):
        # todo: put result in the world ?
        ret = self.model.stop(*args, **kwargs)
        # TODO: remove this hard link!
        world = self.editor_container.session.world
        world[self.model.scene_name] = self.model.axialtree

        return ret

    def animate(self, *args, **kwargs):
        code = self.widget().get_text()
        self.model.content = code

        # todo: put result in the world ?
        ret = self.model.animate(*args, **kwargs)
        # TODO: remove this hard link!
        world = self.editor_container.session.world
        world[self.model.scene_name] = self.model.axialtree

        return ret

    def init(self, *args, **kwargs):
        code = self.widget().get_text()
        self.model.content = code

        # todo: put result in the world ?
        ret = self.model.init(*args, **kwargs)
        # TODO: remove this hard link!
        world = self.editor_container.session.world
        world[self.model.scene_name] = self.model.axialtree

        return ret

    def widget(self):
        """
        :return: the edition widget
        """
        return self._widget
