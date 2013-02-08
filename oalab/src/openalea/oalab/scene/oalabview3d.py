from openalea.oalab.gui import qt
from openalea.plantgl.all import *
# from PyQGLViewer import QGLViewer, Vec
from PyQGLViewer import *


class oalabView3D (QGLViewer):
    def __init__(self,parent=None,scene=None,statefilename='.temp_scene.xml'):
        QGLViewer.__init__(self,parent)
        
        self.setAxisIsDrawn()
        self.setGridIsDrawn()
        
        if scene == None:
            scene = self.defaultScene()
        self.scene = scene
        
        self.setStateFileName(statefilename)
        self.connect(self,qt.SIGNAL("drawNeeded()"),self.draw)
        
        position = Vec(0.0,-1.0,0.1)
        self.camera().setPosition(position)
        self.camera().lookAt(self.sceneCenter())
        self.camera().setSceneRadius(5)

        # self.camera().setType(Camera.ORTHOGRAPHIC)
        self.camera().showEntireScene()

    def setScene(self, scene):
        self.scene = Scene()
        for s in scene:
            self.scene += s
        self.draw()
        
    def getScene(self):
        return self.scene
        
    def addToScene(self, add):
        scene = self.getScene()
        scene += add
        self.setScene(scene)
    
    def draw(self):
        d = Discretizer()
        gl = GLRenderer(d)
        self.scene.apply(gl)
    
    def start(self):
        # self.show()
        pass
        
    def defaultScene(self):
        from math import pi

        def line_prof():
            """ create a list of profiles with polyline """
            return [Polyline2D([(0,0),(1.5,0.1),(0.75,2),(1.1,2.2),(0.55,3),(0.8,3.1),(0,4),(0,4)]),
                    Polyline2D([(0,0),(1.2,0.1),(0.7,2),(1.0,2.3),(0.5,3.1),(0.8,3.1),(0,4),(0,4)]),
                    Polyline2D([(0,0),(1.4,0.1),(0.8,2),(1.1,2.1),(0.6,3),(0.85,3.0),(0,4),(0,4)]),
                    Polyline2D([(0,0),(1.6,0.1),(0.8,2),(1.2,2.2),(0.4,3),(0.7,3.2),(0,4),(0,4)]),
                    Polyline2D([(0,0),(1.5,0.1),(0.75,2),(1.1,2.2),(0.55,3),(0.8,3.1),(0,4),(0,4)])]

        scene = Scene()
        
        # #the angles to associate to profiles
        # angles = [0,pi/2.,pi,3.*pi/2.,2.*pi]
        # col = Material(Color3(0,100,50))
        
        # # a swung interpolating the profiles associated to the angles
        # scene += Shape(Translated(1,1,0,Swung(line_prof(),angles)),col)

        
        return scene
        
        
        
