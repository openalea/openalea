from openalea.oalab.plugins.applets import PluginApplet


class TextualModelGUI(PluginApplet):
    name = 'Textual'
    mimetype_model = '*'
    mimetype_data = '*'

    def __call__(self):
        from openalea.oalab.gui.paradigm.textual import TextualModelController
        return TextualModelController
