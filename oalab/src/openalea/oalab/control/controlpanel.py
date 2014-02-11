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
from openalea.lpy.gui.scalareditor import ScalarEditor



class LPyPanelWidget(QtGui.QWidget):
    def __init__(self,parent,name,panelmanager = None):       
        super(LPyPanelWidget, self).__init__(None)  
        self.panelmanager = panelmanager
        self.setObjectName(name.replace(' ','_'))
        self.setName(name)
        self.verticalLayout = QtGui.QVBoxLayout(parent)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
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

    def clear(self):
        self.setObjects([])

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

    def endNameEditing(self, ident):
        if ident != -1 and self.objectNameEdit.isVisible():
            self.displayName(-1)
    
    def displayName(self, ident):
        if ident == -1:
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
        if not i is None and i >= 0:
            if int(i) < int(len(self.view.objects)):
                if self.view.objects[i][0].managePrimitive():
                    self.emit(QtCore.SIGNAL('valueChanged(bool)'),True)
                else:
                    self.emit(QtCore.SIGNAL('valueChanged(bool)'),False)
            else:
                self.emit(QtCore.SIGNAL('valueChanged(bool)'),False)
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
    def __init__(self, session, controller, parent=None):
        # Create unused menu to fit with original ObjectPanaleManager from lpy
        parent = QtCore.QObject()
        parent.vparameterView = QtGui.QMenu()
        super(ControlPanelManager, self).__init__(parent)
        self.session = session
    
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
    def __init__(self, session, controller, parent=None):
        super(ControlPanel, self).__init__() 
        
        # Color Map
        self.colormap_editor = MaterialEditor(self)
        self.addTab(self.colormap_editor, "Color Map")
        
        # Geometry
        self.control_panel_manager = ControlPanelManager(session, controller, parent=parent)
        self.geometry_editor = LPyPanelWidget(parent=None,name="Control Panel", panelmanager=self.control_panel_manager)
        self.geometry_editor.view.setTheme(self.geometry_editor.view.WHITE_THEME)
        # Print Warning in PlantGL/src/plantg/gui/curve2deditor.py l.227

        self.addTab(self.geometry_editor, "Geometry")
        
        # Scalars
        self.scalars_editor = ScalarEditor(self)
        # scalars = self.scalars_editor.getScalars()
        # for scalar in scalars:
        # cPickle.dump(scalar)
        
        #cPcikle.load(scalar)
        # self.scalars_editor.setScalars([scalar,,,])

        self.addTab(self.scalars_editor, "Scalars")   
