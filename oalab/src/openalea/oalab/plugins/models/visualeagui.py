
class VisualeaModelGUI(object):
    name = 'Workflow'
    mimetype_model = "text/x-visualea"
    mimetype_data = "text/x-visualea"

    def __call__(self):
        from openalea.oalab.gui.paradigm.visualea import VisualeaModelController
        return VisualeaModelController
