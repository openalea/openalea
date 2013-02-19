from openalea.oalab.gui import qt
from openalea.plantgl.all import *
from PyQGLViewer import *


class view3D (QGLViewer):
    """ This class is used to create and manipulate a 3 dimensions scene.
    This scene is based on QGLViewer.
    For the moment, we have only one view of this scene."""
    
    def __init__(self,parent=None,scene=None,statefilename='.temp_scene.xml',shareWidget=None):
        QGLViewer.__init__(self,parent,shareWidget)
        # set the scene
        if scene == None:        
            scene = self.defaultScene()
        self.scene = scene
        # temp file
        self.setStateFileName(statefilename)
        # set some parameters
        self.setAxisIsDrawn() # show axis
        self.setGridIsDrawn() # show grid
        position = Vec(0.0,-1.0,0.1)
        self.camera().setPosition(position) # set camera
        self.camera().lookAt(self.sceneCenter())
        self.camera().setSceneRadius(4)#Size of vectors x,y,z
        self.camera().showEntireScene()
        # connection
        self.connect(self,qt.SIGNAL("drawNeeded()"),self.draw)
        
    def setScene(self, scene):
        # Set the scene (erase old scene if necessary)
        self.scene = Scene()
        for s in scene:
            self.scene += scene[s]
        self.draw()
        
    def getScene(self):
        # Return the actual scene
        return self.scene
        
    def addToScene(self, add):
        # Add a new object in existing scene
        scene = self.getScene()
        scene += add
        self.setScene(scene)
    
    def draw(self):
        # Draw the scene
        d = Discretizer()
        gl = GLRenderer(d)       
        self.scene.apply(gl)
    
    def start(self):
        self.show()
        
    def defaultScene(self):
        # Create a default scene.
        # Here she is empty.
        scene = Scene()
        return scene
        
        
def main():
        import sys
        from openalea.oalab.gui import qt
        
        app = qt.QApplication(sys.argv)
        view = view3D()
        view.addToScene(Sphere())
        view.start() 
        app.exec_()
        
        
if( __name__ == "__main__"):
    main()
                