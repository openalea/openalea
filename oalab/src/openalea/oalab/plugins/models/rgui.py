from openalea.oalab.plugins.applets import PluginApplet


class RModelGUI(PluginApplet):
    name = 'R'
    mimetype_model = 'text/x-r'
    mimetype_data = 'text/x-r'

    def __call__(self):
        from openalea.oalab.gui.paradigm.r import RModelController
        return RModelController
