from openalea.oalab.plugins.applets import PluginApplet

class RModelGUI(PluginApplet):
    name = 'R'

    def __call__(self):
        from openalea.oalab.gui.paradigm.r import RModelController
        return RModelController
