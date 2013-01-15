from openalea.oalab.plugins import TextEditorOALab


class MyWorkflowEditor(TextEditorOALab):
    __plugin_name__ = 'Editeur_de_workflow_1'
    __categorie__ = 'WorkflowEditor'

    
    def __init__(self, parent=None):
        pass