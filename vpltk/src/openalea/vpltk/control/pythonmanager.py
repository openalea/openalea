from openalea.vpltk.control.abstractcontrolmanager import AbstractControlManager
##from openalea.vpltk.qt import QtGui

class AbstractPythonObjectManager(AbstractControlManager):
    def __init__(self, typename = None):
        AbstractControlManager.__init__(self, typename)

    def initWriting(self,indentation=0):
        return ''
        
    def writeObject(self,obj,indentation=0):
        """
        :return: representation of object to write
        """
        return str(obj)


class IntEditor(object):
    def __init__(self, parent):
        self.obj = None
        
    def setInt(self, obj):
        self.obj = obj
        
    def getInt(self):
        return self.obj  

    
def displayIntThumbnail():
    pass


class IntManager(AbstractPythonObjectManager):
    def __init__(self, typename = "int"):
        AbstractPythonObjectManager.__init__(self, typename)

    def displayThumbnail(self,obj,id,mode,objectthumbwidth):
        """ display of an object in the Lpy main window Panel, 
            :param obj: the object to display
            :param id: id of the object in the list
            :param mode: define if object has mode, 
            :param thumbwidth: width of the thumbnail representing the object in the panel
            :param objectthumbwidth: width for the representation of the object in the panel
            Should be reimplemented
        """
        displayIntThumbnail()
            
    def reset(self,obj):
        return self.createDefaultObject()
        
    def getEditor(self,parent_widget):
        """ ask for creation of editor. Should be reimplemented """
        return IntEditor(parent_widget)

    def fillEditorMenu(self,menubar,editor):
        """ Function call to fill the menu of the editor """
        pass
        
    def setObjectToEditor(self,editor,obj):
        """ ask for edition of obj with editor. Should be reimplemented """
        editor.setInt(obj)

    def retrieveObjectFromEditor(self,editor):
        """ ask for current value of object being edited """
        return editor.getInt()
##    
##    def defaultObjectTypes(self):
##        """ ask for type of object managed by this manager. Several are possible. None means that typename should be used. """
##        return None
##        
    def createDefaultObject(self, objtype = None):
        """ 
        create a default object of the type handled by the manager.
        requires instanciate a new item in the panel.
        Should be reimplemented
        """
        return 1
##        
##    def initWriting(self,indentation=0):
##        return ''
##        
##    def writeObject(self,obj,indentation=0):
##        """
##        :return: representation of object to write
##        """
##        return str(obj)
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
    
    
    
    


