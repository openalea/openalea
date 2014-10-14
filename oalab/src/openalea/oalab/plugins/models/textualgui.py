from openalea.oalab.plugins.applets import PluginApplet

class TextualModelGUI(PluginApplet):
    name = 'Textual'

    def __call__(self):
        from openalea.oalab.gui.paradigm.textual import TextualModelController
        return TextualModelController
