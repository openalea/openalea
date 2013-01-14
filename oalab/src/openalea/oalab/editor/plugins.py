class WrapperOALab(object):
    def __init__(self):
        pass

class EditorOALab(WrapperOALab):
    def __init__(self):
        pass
        
class WorkFlowEditorOALab(EditorOALab):
    def __init__(self):
        pass
        
class TextEditorOALab(EditorOALab):
    def __init__(self):
        super(TextEditorOALab, self).__init__()
        self.setup()
    
    def setup(self):
        # Setup the editor
        pass
        
    def set_actions(self):
        # Create qt actions
        pass
        
    def set_buttons(self, a, b):
        # Create qt btns and connect actions
        pass    

    def set_menu(self, a, b):
        # Create qt menu and connect actions
        pass    
    
    def set_language(self, language='py'):
        # Set the language of the editor
        # 'language' can be 'py', 'lpy' or 'wf'
        # (script python, script l-system, workflow)
        pass
        
    def get_language(self):
        # Return the language of the editor
        # 'language' can be 'py', 'lpy' or 'wf'
        # (script python, script l-system, workflow)
        pass    
        
    def set_text(self, text=''):
        # Set the text 'text' in the editor
        pass
        
    def get_text(self, start='sof', end='eof'):
        # Return text which is contained in the editor between 'start' and 'end'
        pass
        
    
        