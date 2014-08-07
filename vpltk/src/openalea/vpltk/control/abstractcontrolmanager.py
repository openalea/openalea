def get_managers():
    managers = dict()
    
    from openalea.vpltk.control.pythonmanager import IntManager
##    from openalea.lpy.gui.plugins.curve2dmanager import Curve2DManager 
##    from openalea.lpy.gui.plugins.functionmanager import FunctionManager
##    from openalea.lpy.gui.plugins.nurbspatchmanager import NurbsPatchManager
    
    managers[IntManager.typename] = IntManager
##    managers[Curve2DManager().typename] = Curve2DManager
##    managers[FunctionManager().typename] = FunctionManager
##    managers[NurbsPatchManager().typename] = NurbsPatchManager
    return managers


def get_manager(type):
    managers = get_managers()
    try:
        return managers[type]
    except KeyError:
        return None
    
##class AbstractControl(object):
##    def __init__(self):
##        self.type = None
##        self.name = None
##        self.object = None
##        
##    def createDefault(self):    
##        self.type = "int"
##        self.name = "my_int"
##        self.object = 42
##        
##    def thumbnail(self):
##        pass
##        
##    def editor(self):
##        pass
##        
##    def dblClick(self):
##        pass
##        
##    def reprProtocol(self):
##        pass
        
    
class AbstractControlManager(object):
    """
    'typename' is the type of control that is manage by this control manager.
    It can be a python type (ex: 'int') or something else (ex: 'Curve2D').
    """
    typename = None
    
    def __init__(self, name=None, object=None):
        """
        :param name: of the control
        :param object: value of the control
        """
        self.name = name
        self.object = object
        
    def thumbnail(self):
        """
        Permit to display a thumbnail of the control.
        
        :return: widget to display
        """
        raise NotImplementedError('thumbnail')
        
    def editor(self):
        """
        Permit to edit the control.
        
        Launch edition (inside the thumbnail or in a new widget)
        """
        raise NotImplementedError('editor')
        
    def dblClick(self):
        """
        Connect double click with edition.
        """
        pass
        
    def repr(self):
        """
        :return: string representation of the control to write it on the disk
        """
        return str(self.object)
        


    
    
    
    
    
    
    
    
    
    
    
##    """ Manage a type of data. Make it possible to name it, display it as thumbnail and edit it"""
##    def __init__(self, typename = None):
##        """We need the name of the object managed by the editor to link the manager with the right Editor"""
##        QtCore.QObject.__init__(self)
##        self.typename =  typename
##        
##    def setName(self,obj,name):
##        obj.name=name
##
##    def getName(self,obj):
##        return obj.name
##
##    def displayThumbnail(self,obj,id,mode,objectthumbwidth):
##        """ display of an object in the Lpy main window Panel, 
##            :param obj: the object to display
##            :param id: id of the object in the list
##            :param mode: define if object has mode, 
##            :param thumbwidth: width of the thumbnail representing the object in the panel
##            :param objectthumbwidth: width for the representation of the object in the panel
##            Should be reimplemented
##        """
##        raise NotImplementedError('displayThumbnail')
##            
##    def reset(self,obj):
##        return self.createDefaultObject()
##        
##    def getEditor(self,parent_widget):
##        """ ask for creation of editor. Should be reimplemented """
##        raise NotImplementedError('getEditor')
##
##    def fillEditorMenu(self,menubar,editor):
##        """ Function call to fill the menu of the editor """
##        pass
##        
##    def setObjectToEditor(self,editor,obj):
##        """ ask for edition of obj with editor. Should be reimplemented """
##        raise NotImplementedError('setObjectToEditor')
##
##    def retrieveObjectFromEditor(self,editor):
##        """ ask for current value of object being edited """
##        raise NotImplementedError('startObjectEdition')
##    
##    def defaultObjectTypes(self):
##        """ ask for type of object managed by this manager. Several are possible. None means that typename should be used. """
##        return None
##        
##    def createDefaultObject(self, objtype = None):
##        """ 
##        create a default object of the type handled by the manager.
##        requires instanciate a new item in the panel.
##        Should be reimplemented
##        """
##        raise NotImplementedError('createDefaultObject')
##        
##    def initWriting(self,indentation):
##        return ''
##        
##    def writeObject(self,obj,indentation):
##        """
##        :return: representation of object to write
##        """
##        raise NotImplementedError('writeObject')
##    
##    def writeObjectToLsysContext(self,obj):
##        return obj.name
##    
##    def canImportData(self,fname):
##        return False
##    
##    def importData(self,fname):
##        raise NotImplementedError('importData')
##    
##    def completeContextMenu(self,menu,obj,widget):
##        pass
##    
##    def managePrimitive(self):
##        return False
##    
##    def getTheme(self):
##        """ get the color theme currenlty used """
##        return {}
##    
##    def setTheme(self,theme):
##        """ get the color theme acccording to the theme dict """
##        pass
##    
##    
##    
##    


