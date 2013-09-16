from openalea.vpltk.qt import QtCore, QtGui
from collections import OrderedDict
from openalea.core.singleton import Singleton
import warnings

class SceneWidget(QtGui.QTableWidget):
    """
    Display a QTreeView with object of the scene.
    Permit to hide/show a sub-scene
    """
    def __init__(self, session):
        super(SceneWidget, self).__init__(0,2)
        
        self.session = session
        self._actions = None
        
        self.scene = VPLScene()
        
        QtCore.QObject.connect(self.scene.signaler, QtCore.SIGNAL('SceneChanged'),session.viewer.setScene)
        QtCore.QObject.connect(self.scene.signaler, QtCore.SIGNAL('SceneChanged'),session.viewer.updateGL)
        QtCore.QObject.connect(self.scene.signaler, QtCore.SIGNAL('SceneChanged'),self._update)
        
        sc = self.getScene()
        self._update(sc)

        
    def _update(self, scene):
        self._reset()
        row = 0
        for h in scene:
            itemName = QtGui.QTableWidgetItem(str(h))
            itemObj = QtGui.QTableWidgetItem(str(scene[h]))
            if self.rowCount()<=row:
                self.insertRow(row)
            self.setItem(row,0,itemName)
            self.setItem(row,1,itemObj)
            row += 1
        
    def _reset(self):
        while self.rowCount() > 0:
            self.removeRow( 0 )
        self.clear()
        headerName1 = QtGui.QTableWidgetItem("name")
        headerName2 = QtGui.QTableWidgetItem("value")
        self.setHorizontalHeaderItem(0,headerName1)
        self.setHorizontalHeaderItem(1,headerName2)
        
    def getScene(self):
        return self.scene.getScene() 
    
    def hide(self, obj):
        """
        hide the sub-scene 'obj' in the viewer
        """
        # TODO : to implement
        # print "Hide ", obj
        pass
        
    def show(self, obj):
        """
        hide the sub-scene 'obj' in the viewer
        """
        # TODO : to implement
        # print "Show ", obj 
        pass
        
    def actions(self):
        return self._actions

    def mainMenu(self):
        """
        :return: Name of menu tab to automatically set current when current widget
        begin current.
        """
        return "3D View"  


class VPLScene(OrderedDict):
    """
    Scene for OALab. Singleton.
    
    This class inherit from ordered dict. 
    But when the dict is modified, self.signaler emit a qt signal (arg=self).
    This is really usefull to realize automatic updates of viewer!
    """
    
    __metaclass__ = Singleton
    
    def __init__(self, *args, **kwds):
        super(VPLScene, self).__init__(*args, **kwds)
        self._block = False
        self.signaler = QtCore.QObject()
        self.actionChanged = QtGui.QAction(self.signaler)
        self._valueChanged()
        
    def add(self, name="unnamed object", obj="None"):
        """
        Add a new object in the scene.
        
        :param name: name of the object to add in the scene
        :param obj: object to add
        """
        name = self._check_if_name_is_unique(name)
        self[name] = obj
        
    def block(self):
        """
        Block sent of signals.
        Useful to add many objects in the scene without refresh the viewer
        """
        self._block = True   
         
    def release(self):
        """
        Release signals sending and update scene.
        """
        self._block = False
        self.update()
                
    def getScene(self):
        """ 
        :return: the scene (ordered dict)
        """
        return self
    
    def rename(self, oldname, newname):
        """
        Try to rename object named 'oldname' in 'newname'.
        
        :param oldname: str of the name of scene component to access
        :param newname: str of the name to set
        """
        obj = None
        try:
            obj = self[oldname]
        except:
            warnings.warn("scene[%s] doesn't exist." %oldname)
        
        if obj is not None:
            self.add(name=newname1, obj=obj)
            del self[oldname]
        
    def reset(self):
        """
        clear the scene
        """
        self.clear()

    def _check_if_name_is_unique(self, name):
        """
        Check if an sub_scene with the name 'name' is alreadey register
        in the VPLScene.
        
        If it is the case, the name is changed ("_1" is append).
        This is realize until the name becomes unique.
        
        :param name: name to check unicity
        
        TODO : remove this method if we want unicity of name, 
        like in a classical dict
        """
        while name in self:
            try:
                end = name.split("_")[-1]
                l = len(end)
                end = int(end)
                end += 1
                name = name[0:-l] + str(end)
            except:    
                name += "_1"
        return name  
    
    def __setitem__(self, key, value):
        super(VPLScene, self).__setitem__(key, value)
        self._valueChanged()
        
    def update(self):
        super(VPLScene, self).update()
        self._valueChanged()    
        
    def __delitem__(self, key):
        super(VPLScene, self).__delitem__(key)
        self._valueChanged()
        
    def popitem(self, last=True):
        super(VPLScene, self).popitem(last)
        self._valueChanged()
        
    def clear(self):    
        super(VPLScene, self).clear()
        self._valueChanged()
        
    def __reversed__(self):
        super(VPLScene, self).__reversed__()
        self._valueChanged()
        
    def __reduce__(self):
        super(VPLScene, self).__reduce__()
        self._valueChanged()
        
    def _valueChanged(self):
        """  
        Emit Qt Signal when the dict change
        """
        if not self._block:
            self.signaler.emit(QtCore.SIGNAL('SceneChanged'), self)   

Scene = VPLScene
