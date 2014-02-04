# -*- python -*-
#
#       3D scene viewer for OALab Scene
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
__revision__ = ""

from openalea.vpltk.qt import QtGui, QtCore
from openalea.plantgl.all import *
from PyQGLViewer import *
import sys

class view3D(QGLViewer):
    """
    This class is used to create and manipulate a 3 dimensions scene.
    This scene is based on QGLViewer.
    For the moment, we have only one view of this scene.
    """
    
    def __init__(self,parent=None,scene=None,statefilename='.temp_scene.xml',shareWidget=None):
        QGLViewer.__init__(self,parent,shareWidget)
        # set the scene
        if scene == None:        
            scene = self.defaultScene()
        self.scene = scene
        # set some parameters
        self.setAxisIsDrawn(False) # show axis
        self.setGridIsDrawn(True) # show grid
        position = Vec(0.0,-1.0,0.1)
        self.camera().setPosition(position) # set camera
        self.camera().lookAt(self.sceneCenter())
        self.camera().setSceneRadius(1)#Size of vectors x,y,z
        self.camera().showEntireScene()
        # connection
        self.connect(self,QtCore.SIGNAL("drawNeeded()"),self.draw)
        self.orientation_initiale = self.camera().orientation()
        self.position_initiale = self.camera().position()
        # Block "*.xml" save
        self.setStateFileName("") 
        # Disable Quit in clicking on 'Escape'
        # Set "show_axis" instead of "kill_application"
        self.setShortcut(0,QtCore.Qt.Key_Escape)

    # Method for lpy.registerPlotter to "animate"
    def plot(self,scene):
        scenedict = {"new":scene}
        self.setScene(scenedict)
        self.updateGL()        

    # Method for lpy.registerPlotter to "animate"        
    def selection(self):
        return super(view3D, self).selection

    # Method for lpy.registerPlotter to "animate"    
    def waitSelection(self,txt):
        return super(view3D, self).waitSelection(txt)

    # Method for lpy.registerPlotter to "animate"    
    def save(self,fname,format):
        super(view3D, self).frameGL.saveImage(fname,format)

    def setScene(self, scenes):
        """
        Set the scene
        (erase old scene if necessary)
        
        :param scene: dict with every sub-scenes to add
        """
        self.scene.clear()
        for s in scenes:
            self.scene += scenes[s]
        self.draw()


    def getScene(self):
        """
        :return: the scene (orderedDict)
        """
        return self.scene
        
    def addToScene(self, obj):
        """
        Add a new object in existing scene
        
        :param obj: object to add in the scene
        """
        scene = self.getScene()
        scene += obj
        self.setScene(scene)
    
    def draw(self):
        """
        Draw the scene
        """
        d = Discretizer()
        gl = GLRenderer(d)       
        self.scene.apply(gl)

    def start(self):
        self.show()
        
    def defaultScene(self):
        """
        Create a default scene.
        Here she is empty.
        
        :return: the scene
        """    
        scene = Scene()
        return scene
        
    def update_radius(self):
        """
        Set the scene radius to 110% of the max size in the scene
        """
        try:
            bBox = BoundingBox(self.scene)
            xmax = bBox.getXMax()
            ymax = bBox.getYMax()
            zmax = bBox.getZMax()
            
            xmin = bBox.getXMin()
            ymin = bBox.getYMin()
            zmin = bBox.getZMin()
            
            x = max(abs(xmin),abs(xmax))
            y = max(abs(ymin),abs(ymax))
            z = max(abs(zmin),abs(zmax))
            
            radius = max(x,y,z)
            self.camera().setSceneRadius(radius*1.1)
            self.show_entire_scene()
        except:
            pass


class Viewer(view3D):
    """
    Widget of 3D Viewer to show the scene.
    """
    def __init__(self, session):
        super(Viewer, self).__init__() 
        
        self.setAccessibleName("3DViewer")
        
        self.autofocus = True
        self._fps = False
        self.axis = False
        self.grid = True
        
        actionResetZoom = QtGui.QAction(QtGui.QIcon(":/lpy_images/resources/lpy/resetzoom.png"),"Reset Zoom", self)
        actionZoomOut = QtGui.QAction(QtGui.QIcon(":/lpy_images/resources/lpy/zoomout.png"),"Zoom Out", self)
        actionZoomIn = QtGui.QAction(QtGui.QIcon(":/lpy_images/resources/lpy/zoomin.png"),"Zoom In", self)
        actionShowAxis = QtGui.QAction(QtGui.QIcon(":/images/resources/axis.png"),"Show Axis", self)
        actionShowGrid = QtGui.QAction(QtGui.QIcon(":/images/resources/grid.png"),"Show Grid", self)
        actionRadius = QtGui.QAction(QtGui.QIcon(":/images/resources/growth2.png"),"Focus", self)
        actionShowFps = QtGui.QAction(QtGui.QIcon(":/images/resources/fps.png"),"Show FPS", self)
        
        actionShowAxis.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+A", None, QtGui.QApplication.UnicodeUTF8))
        actionShowGrid.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+G", None, QtGui.QApplication.UnicodeUTF8))
        actionRadius.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+F", None, QtGui.QApplication.UnicodeUTF8))
        
        QtCore.QObject.connect(actionResetZoom, QtCore.SIGNAL('triggered(bool)'),self.resetzoom)
        QtCore.QObject.connect(actionZoomOut, QtCore.SIGNAL('triggered(bool)'),self.zoomout)
        QtCore.QObject.connect(actionZoomIn, QtCore.SIGNAL('triggered(bool)'),self.zoomin)
        
        QtCore.QObject.connect(actionShowAxis, QtCore.SIGNAL('triggered(bool)'),self.show_hide_axis)
        QtCore.QObject.connect(actionShowGrid, QtCore.SIGNAL('triggered(bool)'),self.show_hide_grid)
        QtCore.QObject.connect(actionRadius, QtCore.SIGNAL('triggered(bool)'),self.update_radius)
        
        QtCore.QObject.connect(actionShowFps, QtCore.SIGNAL('triggered(bool)'),self.show_fps)
        
        QtCore.QObject.connect(session.scene.signaler, QtCore.SIGNAL('SceneChanged'),self.setScene)
        QtCore.QObject.connect(session.scene.signaler, QtCore.SIGNAL('SceneChanged'),self.updateGL)        
        
        self._actions = [["3D Viewer","Zoom",actionResetZoom,0],
                        ["3D Viewer","Zoom",actionZoomOut,0],
                        ["3D Viewer","Zoom",actionZoomIn,0],
                        ["3D Viewer","Camera",actionShowAxis,1],
                        ["3D Viewer","Camera",actionShowGrid,1],
                        ["3D Viewer","Camera",actionRadius,1],
                        ["3D Viewer","Informations",actionShowFps,1]]

    def actions(self):
        return self._actions
    
    def resetzoom(self):
        self.camera().setOrientation(self.orientation_initiale)
        self.camera().setPosition(self.position_initiale)
        self.updateGL() 
        
    def zoomout(self):
        cam = self.camera()
        new_position = (cam.position()-cam.sceneCenter())*2
        cam.setPosition(new_position)
        self.updateGL() 
        
    def zoomin(self):
        cam = self.camera()
        new_position = (cam.position()-cam.sceneCenter())/2
        cam.setPosition(new_position)
        self.updateGL() 
        
        #coef = qMax(fabsf((camera->frame()->coordinatesOf(camera->revolveAroundPoint())).z), 0.2f*camera->sceneRadius())
        #trans(0.0, 0.0, -coef * (event->y() - prevPos_.y()) / camera->screenHeight())
        #translate(inverseTransformOf(trans))
        
    def show_fps(self):
        self._fps = not self._fps
        self.setFPSIsDisplayed(self._fps)

    def mainMenu(self):
        """
        :return: Name of menu tab to automatically set current when current widget
        begin current.
        """
        return "3D Viewer"  

    def show_hide_axis(self):
        if self.axis:
            self.setAxisIsDrawn(False) # hide axis
            self.axis = False
        else:
            self.setAxisIsDrawn(True) # show axis
            self.axis = True
        
    def show_hide_grid(self):
        if self.grid:
            self.setGridIsDrawn(False) # hide grid
            self.grid = False
        else:
            self.setGridIsDrawn(True) # show grid 
            self.grid = True

    def show_entire_scene(self):
        self.camera().showEntireScene()
        self.updateGL()  
        
    def setScene(self, scenes):
        """
        Set the scene
        (erase old scene if necessary)
        
        Class overloaded to use an autofocus if you add a first object in the scene
        
        :param scene: dict with every sub-scenes to add
        """
        super(Viewer, self).setScene(scenes)
        if self.autofocus:
            self.update_radius()    
            self.autofocus = False
        
def main():
        app = QApplication(sys.argv)
        view = view3D()
        view.addToScene(Sphere())
        view.start() 
        app.exec_()
        
        
if( __name__ == "__main__"):
    main()
                
