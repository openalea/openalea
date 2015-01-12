class LPyModelGUI(object):
    name = 'LSystem'
    mimetype_data = "text/vnd-lpy"
    mimetype_model = "text/vnd-lpy"

    def __call__(self):
        from openalea.plantlab.paradigm import LPyModelController
        return LPyModelController
