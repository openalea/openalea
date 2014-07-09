from openalea.oalab.plugins.applets import PluginApplet

class VisualeaModelGUI(PluginApplet):
    name = 'Workflow'

    def __call__(self):
        from openalea.oalab.gui.paradigm.visualea import VisualeaModelController
        return VisualeaModelController
