class PluginManager(object):
    def __init__(self):
        self.plugins = []
        self.categorie = []
        self.sub_categorie = []
        self.language = []
    
    def set_plugin_path(self, path):
        self.path = path
        
    def get_plugin_path(self):
        return self.path   
    
    def get_all_plugins(self):
        for file in self.path:
            plugin = __import__(file)
            self.plugins.append(plugin.get_name())
            self.categorie.append(plugin.get_categorie())
            self.sub_categorie.append(plugin.get_sub_categorie())
            try:
                self.language.append(plugin.get_language())
            except:
                self.language.append('None')
            
        

class OALabPlugin(object):
    def __init__(self):
        pass
        
    def set_name(self, name):
        # Set the plugin name
        self.__name__ = name
        
    def get_name(self):
        # Get the plugin name
        return self.__name__
        
    def set_categorie(self, categorie):
        # Set the plugin categorie
        # Can be 'Editor', 'Visualizator', ...
        self.__categorie__ = categorie
        
    def get_categorie(self):
        # Get the plugin categorie
        return self.__categorie__
        
    def set_sub_categorie(self, sub_catg):
        # Set the plugin subcategorie
        # For an Editor, can be 'Text', 'Workflow', 'PythonObject', ...
        self.__sub_categorie__ = sub_catg
        
    def get_sub_categorie(self):
        # Get the plugin subcategorie
        return self.__sub_categorie__     
        
        
class EditorOALab(OALabPlugin):
    def __init__(self):
        self.set_categorie('Editor')
        
        
class VisualizatorOALab(OALabPlugin):
    def __init__(self):
        self.set_categorie('Visualizator')        
     
        
class WorkFlowEditorOALab(EditorOALab):
    def __init__(self):
        self.set_sub_categorie('Workflow')
        
        
class TextEditorOALab(EditorOALab):
    def __init__(self):
        super(TextEditorOALab, self).__init__()
        self.set_sub_categorie('Text')
        self.setup()
        
    def set_language(self, lang='py'):
        # Set the language of the editor
        # 'language' can be 'py', 'lpy', 'r'
        # (script python, script l-system, R)
        self.__language__ = lang
        
    def get_language(self):
        # Return the language of the editor
        return self.__language__
    
    

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
        
    
        