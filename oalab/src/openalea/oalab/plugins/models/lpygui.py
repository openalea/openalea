from openalea.oalab.plugins.applets import PluginApplet

class LPyModelGUI(PluginApplet):
    name = 'LSystem'

    def __call__(self):
        from openalea.oalab.gui.paradigm.lpy import LPyModelController
        return LPyModelController
