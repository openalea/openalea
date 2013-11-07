# -*- python -*-
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2013 INRIA - CIRAD - INRA
#
#       File author(s): Julien Coste <julien.coste@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
__revision__ = "$Id: $"

from openalea.vpltk.qt import QtGui, QtCore
#from openalea.vpltk import plugin
from openalea.lpy.gui.materialeditor import MaterialEditor
#from openalea.lpy.gui.objectpanel import LpyObjectPanelDock
from openalea.lpy.gui.objectpanel import ObjectPanelManager, TriggerParamFunc, ObjectListDisplay



class LPyPanelWidget(QtGui.QWidget):
    def __init__(self,parent,name,panelmanager = None):       
        super(LPyPanelWidget, self).__init__(parent)  
        self.panelmanager = panelmanager
        self.setObjectName(name.replace(' ','_'))
        self.setName(name)
        self.verticalLayout = QtGui.QVBoxLayout(parent)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(name+"verticalLayout")              

        self.objectpanel = QtGui.QScrollArea(parent)
        self.view = ObjectListDisplay(self,panelmanager)
        self.view.dock = self # ?
        
        self.objectpanel.setWidget(self.view)
        self.objectpanel.setWidgetResizable(True)
        self.objectpanel.setObjectName(name+"panelarea")

        self.verticalLayout.addWidget(self.objectpanel)
        self.objectNameEdit = QtGui.QLineEdit(self)
        self.objectNameEdit.setObjectName(name+"NameEdit")
        self.verticalLayout.addWidget(self.objectNameEdit)        
        self.objectNameEdit.hide()
        self.setLayout(self.verticalLayout)
        
        QtCore.QObject.connect(self.view,QtCore.SIGNAL('valueChanged(int)'),self.__updateStatus)
        QtCore.QObject.connect(self.view,QtCore.SIGNAL('AutomaticUpdate()'),self.__transmit_autoupdate)
        QtCore.QObject.connect(self.view,QtCore.SIGNAL('selectionChanged(int)'),self.endNameEditing)
        QtCore.QObject.connect(self.view,QtCore.SIGNAL('renameRequest(int)'),self.displayName)
        QtCore.QObject.connect(self.objectNameEdit,QtCore.SIGNAL('editingFinished()'),self.updateName)
        self.dockNameEdition = False
        self.nameEditorAutoHide = True
        self.setAcceptDrops(True)   

    def dragEnterEvent(self,event):
        event.acceptProposedAction()

    def dropEvent(self,event):
        if event.mimeData().hasUrls() :
            self.fileDropEvent(str(event.mimeData().urls()[0].toLocalFile()))

    def fileDropEvent(self,fname):
        for manager in self.view.managers.itervalues():
            if manager.canImportData(fname):
                objects = manager.importData(fname)
                self.view.appendObjects([(manager,i) for i in objects])    
                self.showMessage('import '+str(len(objects))+" object(s) from '"+fname+"'.",5000)
                return

    def endNameEditing(self,id):
        if id != -1 and self.objectNameEdit.isVisible():
            self.displayName(-1)
    
    def displayName(self,id):
        if id == -1:
            self.objectNameEdit.clear()
            if self.nameEditorAutoHide : 
                self.objectNameEdit.hide()
        else:
            if self.nameEditorAutoHide : 
                self.objectNameEdit.show()
            self.objectNameEdit.setText(self.view.getSelectedObjectName())
            self.objectNameEdit.setFocus()

    def updateName(self):
        if not self.dockNameEdition :
            if self.view.hasSelection():
                self.view.setSelectedObjectName(str(self.objectNameEdit.text()))
                self.view.updateGL()
                if self.nameEditorAutoHide : 
                    self.objectNameEdit.hide()
        else :
            self.setName(self.objectNameEdit.text())
            if self.nameEditorAutoHide : 
                self.objectNameEdit.hide()            
            self.dockNameEdition = False
        
    def setObjects(self,objects):
        self.view.setObjects(objects)

    def appendObjects(self,objects):
        self.view.appendObjects(objects)

    def getObjects(self):
        return self.view.objects

    def getObjectsCopy(self):
        return self.view.getObjectsCopy()

    def setStatusBar(self,st):
        self.objectpanel.statusBar = st
        self.view.statusBar = st

    def showMessage(self,msg,timeout):
        if hasattr(self,'statusBar'):
            self.statusBar.showMessage(msg,timeout)
        else:
            print(msg)    
            
    def __updateStatus(self,i=None):
        if not i is None and i >= 0 and self.view.objects[i][0].managePrimitive():
            self.emit(QtCore.SIGNAL('valueChanged(bool)'),True)
        else:
            self.emit(QtCore.SIGNAL('valueChanged(bool)'),False)

    def __transmit_autoupdate(self):
        self.emit(QtCore.SIGNAL('AutomaticUpdate()'))
        
    def setName(self,name):
        self.name = name
        self.setWindowTitle(name)
        
    def rename(self):
        self.dockNameEdition = True
        if self.nameEditorAutoHide : 
            self.objectNameEdit.show()
        self.objectNameEdit.setText(self.name)
        self.objectNameEdit.setFocus()
    
    def getInfo(self):
        visibility = True
        if not self.isVisible() :
            if self.parent().isVisible() :
                visibility = False
            else:
                visibility = getattr(self,'previousVisibility',True)
        return {'name':str(self.name),'active':bool(self.view.isActive()),'visible':visibility }
        
    def setInfo(self,info):
        self.setName(info['name'])
        if info.has_key('active'):
            self.view.setActive(info['active'])        
        if info.has_key('visible'):
            self.previousVisibility = info['visible']
            self.setVisible(info['visible'])     

# Add a dict interface
class ControlPanelManager(ObjectPanelManager):
    def __init__(self, session):
        # Create unused menu to fit with original ObjectPanaleManager from lpy
        parent = QtCore.QObject()
        parent.vparameterView = QtGui.QMenu()
        super(ControlPanelManager, self).__init__(parent)
        self.session = session

    '''
    ##################################
    # Block save state in an xml file
    # TODO : do the same thing in a more beautiful way
    def restoreState(self, obj=None):
        controls = self.session.project().controls
        print controls
            
    def saveState(self, obj=None):
        self.session.project().controls = self.get_controls()
    ##################################

    def clear(self):
        """
        Del all controls
        """
        
        # Doesn't work...
        for panel in self.getObjectPanels():
            for manager,obj in panel.getObjects():
                del(manager, obj)
    
    def get_controls_and_managers(self):
        """
        :return: two Dict. Controls and Managers associated to controls.
        """
        c = self.get_controls()
        m = self.get_managers()
        return c, m

    def get_managers(self):
        """
        :return: dict of Managers (manager_name, manager) 
        """
        managers = dict()
        
        # Get panels
        panels = self.get_panel()
        
        for panel in panels:
            for manager,obj in panel.getObjects():
                managers[obj.getName()] = manager
            
        return managers   

    def get_controls(self):
        """
        :return: dict of Controls (control_name, control) 
        """
        controls = dict()
        
        # Get panels
        panels = self.get_panel()
        
        for panel in panels:
            for manager,obj in panel.getObjects():
                controls[obj.getName()] = obj
            
        return controls

    def get_panel(self):
        return self.getObjectPanels()'''
    
    def completeMenu(self,menu,panel):
        panelmenu = QtGui.QMenu("Panel",menu)
        menu.addSeparator()
        menu.addMenu(panelmenu)
        subpanelmenu = QtGui.QMenu("Theme",menu)
        panelmenu.addSeparator()
        panelmenu.addMenu(subpanelmenu)
        for themename,value in ObjectListDisplay.THEMES.iteritems():
            panelAction = QtGui.QAction(themename,subpanelmenu)
            
            QtCore.QObject.connect(panelAction,QtCore.SIGNAL('triggered(bool)'),TriggerParamFunc(panel.view.applyTheme,value))
            subpanelmenu.addAction(panelAction)
            
        return panelmenu


class ControlPanel(QtGui.QTabWidget):
    """
    Widget to display controls of the current project.
    Permit to create new control and to delete.
    Double-clic permit to edit control
    """
    def __init__(self, session):
        super(ControlPanel, self).__init__() 
        
        # Color Map
        self.colormap_editor = MaterialEditor(self)
        self.addTab(self.colormap_editor, "Color Map")
        
        # Geometry
        self.control_panel_manager = ControlPanelManager(session)
        self.geometry_editor = LPyPanelWidget(parent=None,name="Control Panel", panelmanager=self.control_panel_manager)
        self.geometry_editor.view.setTheme(self.geometry_editor.view.WHITE_THEME)
        # objects = self.geometry_editor.getObjects()
        # for object in objects:
            # object[1].name, object
        
        #o = self.geometry_editor.getObjectsCopy()
        #self.geometry_editor.setObjects(o)
        
        #from copy import copy
        #objects = self.geometry_editor.getObjects()
        #objects = copy(objects)
        #self.geometry_editor.setObjects(objects)
        

        # Print Warning in PlantGL/src/plantg/gui/curve2deditor.py l.227
        """
        Edit curve
        Ok
        Edit Function
        Apply
        Ok --> error
        
        Traceback (most recent call last):
            
        File "/home/julien/dev/vplants_trunk/lpy/src/openalea/lpy/gui/objectpanel.py", line 64, in __transmit_valueChanged__
            self.panel.retrieveObject(self)
            
        File "/home/julien/dev/vplants_trunk/lpy/src/openalea/lpy/gui/objectpanel.py", line 397, in retrieveObject
            object,objectid = managerDialog.getEditedObject()
            
        TypeError: 'NoneType' object is not iterable
        """
        self.addTab(self.geometry_editor, "Geometry")
        
        # Scalars
        self.scalars_editor = QtGui.QWidget()
        self.addTab(self.scalars_editor, "Scalars")   
        
'''
        # connected to current_project.control
        # and connect display_thumbnail
        
        # TODO self.controls = current_project.control
        self.discover_controls()
    
    def discover_controls(self):
        """
        Use a plugin system to discover all controls type available.
        
        :return: a dict name/controlManager
        """
        self.managers = plugin.discover("oalab.control")
    
    def new_control(self):
        """
        Find types available.
        User choose a type.
        Create a new control and add it to the current project.
        """
        # Discover control managers
        self.discover_controls()

        # User choose a type in self.managers
        # TODO
##        for p in self.managers: print p
        #Here always Int
        
        # Create a new control
        entry_point = self.managers['IntControl']
        Control = plugin.Plugin(entry_point)
        new_control = Control().load()
        
        # Add it into the current project.
        # TODO
##        print new_control.value
        
    def rename(self):
        """
        Rename current control in current project.
        """
        # Get Current
        control = self.current()
        
        # Ask new name to the user
        # TODO
        name = ""
        
        #Rename
        control.rename(name)
        
    def delete(self):
        """
        Delete current control.
        Delete from current project.
        """    
        # Get Current
        control = self.current()
        
        #Delete from current project
        #TODO
        
    def edit(self):
        """
        Edit current control
        - Call control.edit()
        
        Thumbnail widget become an editor widget
        """    
        # Get Current
        control = self.current()
        
        #Edit
        control.edit()
        
    def display_thumbnails(self):
        """
        Display thumbnails of all controls.
        - List controls
        - Call control.thumbnail() on each one
        """
        pass
        
    def current():
        """
        :return: current control
        """
        pass


'''
