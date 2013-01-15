import os

class PluginManager(object):
    def __init__(self):
        self.plugins = []
    
    def set_plugin_path(self, path):
        self.path = path
        
    def get_plugin_path(self):
        return self.path   
    
    def get_all_plugins(self):
        from openalea.core.path import path
        dir = path(self.get_plugin_path()).abspath()

        # import modules
        for file in dir.walkfiles(pattern="*.py"):
            filesplit = os.path.split(file)[1]
            fname = os.path.splitext(filesplit)[0]
            if fname != '__init__':
                module = 'openalea.oalab.plugins_dir.%s' %fname
                plugin = __import__(module, fromlist=['']) 

                self.plugins.append(getattr(plugin, fname))
        
        return self.plugins


class OALabPlugin(object):
    def __init__(self):
        pass
           
    def get_name(self):
        # Get the plugin name
        return __name__
                
    def get_categorie(self):
        # Get the plugin categorie
        return __categorie__
        
        
class VisualizatorOALab(OALabPlugin):
    def __init__(self):
        # self.set_categorie('Visualizator')
        pass
     
        
class WorkFlowEditorOALab(OALabPlugin):
    def __init__(self):
        # self.set_categorie('WorkflowEditor')
        pass
        
        
class TextEditorOALab(OALabPlugin):
    def __init__(self):
        super(TextEditorOALab, self).__init__()
        # self.set_categorie('TextEditor')
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
    
        
    def set_text(self, text=''):
        # Set the text 'text' in the editor
        pass
        
    def get_text(self, start='sof', end='eof'):
        # Return text which is contained in the editor between 'start' and 'end'
        pass
        
    
        