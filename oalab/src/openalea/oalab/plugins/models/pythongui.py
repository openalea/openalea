from openalea.oalab.plugins.applets import PluginApplet


class PythonModelGUI(PluginApplet):
    name = 'Python'
    mimetype_model = 'text/x-python'
    mimetype_data = 'text/x-python'

    def __call__(self):
        from openalea.oalab.gui.paradigm.python import PythonModelController
        return PythonModelController
