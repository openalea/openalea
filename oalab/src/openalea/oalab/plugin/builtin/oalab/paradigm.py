from openalea.core.plugin import PluginDef


class AbstractParadigmPlugin(object):
    implement = 'IParadigmApplet'


@PluginDef
class PythonModelGUI(AbstractParadigmPlugin):
    name = 'Python'
    mimetype_model = 'text/x-python'
    mimetype_data = 'text/x-python'

    def __call__(self):
        from openalea.oalab.paradigm.python import PythonModelController
        return PythonModelController


@PluginDef
class VisualeaModelGUI(AbstractParadigmPlugin):
    name = 'Workflow'
    mimetype_model = "text/x-visualea"
    mimetype_data = "text/x-visualea"

    def __call__(self):
        from openalea.oalab.paradigm.visualea import VisualeaModelController
        return VisualeaModelController


@PluginDef
class TextualModelGUI(AbstractParadigmPlugin):
    name = 'Textual'
    mimetype_model = '*'
    mimetype_data = '*'

    def __call__(self):
        from openalea.oalab.paradigm.textual import TextualModelController
        return TextualModelController


@PluginDef
class RModelGUI(AbstractParadigmPlugin):
    name = 'R'
    mimetype_model = 'text/x-r'
    mimetype_data = 'text/x-r'

    def __call__(self):
        from openalea.oalab.paradigm.r import RModelController
        return RModelController
