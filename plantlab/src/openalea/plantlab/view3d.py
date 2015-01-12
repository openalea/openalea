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
from openalea.plantgl.all import Scene, Sphere, Discretizer, GLRenderer, BoundingBox
from openalea.core.observer import AbstractListener
from openalea.oalab.gui import resources_rc
from openalea.oalab.world.world import WorldObject
from PyQGLViewer import QGLViewer, Vec, Quaternion
import sys

from openalea.oalab.service.geometry import to_shape3d
from openalea.oalab.session.session import Session


class view3D(QGLViewer):

    """
    This class is used to create and manipulate a 3 dimensions scene.
    This scene is based on QGLViewer.
    For the moment, we have only one view of this scene.
    """

    def __init__(self, parent=None, scene=None, statefilename='.temp_scene.xml', shareWidget=None):
        QGLViewer.__init__(self, parent, shareWidget)
        self.set_bg_white()
        # set the scene
        if scene == None:
            scene = self.defaultScene()
        self.scene = scene
        # set some parameters
        self.setAxisIsDrawn(False)  # show axis
        self.setGridIsDrawn(True)  # show grid

        orientation = Quaternion(0.475117, 0.472505, 0.524479, 0.525286)
        position = Vec(2.91287, -0.0109797, 0.659613)
        self.camera().setPosition(position)
        self.camera().setOrientation(orientation)

        self.camera().setSceneRadius(1)  # Size of vectors x,y,z
        # connection
        self.connect(self, QtCore.SIGNAL("drawNeeded()"), self.draw)
        self.orientation_initiale = self.camera().orientation()
        self.position_initiale = self.camera().position()
        # Block "*.xml" save
        self.setStateFileName("")
        # Disable Quit in clicking on 'Escape'
        # Set "show_axis" instead of "kill_application"
        self.setShortcut(0, QtCore.Qt.Key_Escape)

    def set_bg_white(self):
        color_white = QtGui.QColor(255, 255, 255)
        self.setBackgroundColor(color_white)

    def set_bg_black(self):
        color_black = QtGui.QColor(0, 0, 0)
        self.setBackgroundColor(color_black)

    # Method for lpy.registerPlotter to "animate"
    def plot(self, scene):
        scenedict = {"new": scene}
        self.setScene(scenedict)
        self.updateGL()

    # Method for lpy.registerPlotter to "animate"
    def selection(self):
        return super(view3D, self).selection

    # Method for lpy.registerPlotter to "animate"
    def waitSelection(self, txt):
        return super(view3D, self).waitSelection(txt)

    # Method for lpy.registerPlotter to "animate"
    def save(self, fname, format):
        super(view3D, self).frameGL.saveImage(fname, format)

    def setScene(self, scenes):
        """
        Set the scene
        (erase old scene if necessary)

        :param scene: dict with every sub-scenes to add
        """
        self.scene.clear()
        for s in scenes:
            world_obj = scenes[s]
            if isinstance(world_obj, WorldObject):
                if world_obj.in_scene:
                    obj = to_shape3d(world_obj)
                else:
                    obj = None
            else:
                obj = to_shape3d(world_obj)

            if obj:
                self.scene += to_shape3d(obj)
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

            x = max(abs(xmin), abs(xmax))
            y = max(abs(ymin), abs(ymax))
            z = max(abs(zmin), abs(zmax))

            radius = max(x, y, z)
            self.camera().setSceneRadius(radius * 1.1)
            self.show_entire_scene()
        except:
            pass


class Viewer(AbstractListener, view3D):

    """
    Widget of 3D Viewer to show the scene.
    """

    def __init__(self, parent=None):
        #         super(Viewer, self).__init__()
        AbstractListener.__init__(self)
        view3D.__init__(self, parent=parent)

        self.setAccessibleName("3DViewer")
        self.setMinimumSize(100, 100)

        self.autofocus = True
        self._fps = False
        self.axis = False
        self.grid = True

        actionResetZoom = QtGui.QAction(QtGui.QIcon(":/images/resources/resetzoom.png"), "Home", self)
        self.actionAutoFocus = QtGui.QAction(QtGui.QIcon(":/images/resources/resetzoom.png"), "Auto Focus", self)
        self.actionAutoFocus.setCheckable(True)
        self.actionAutoFocus.setChecked(self.autofocus)
        self.actionAutoFocus.changed.connect(self._on_autofocus_changed)
        actionZoomOut = QtGui.QAction(QtGui.QIcon(":/images/resources/zoomout.png"), "Zoom Out", self)
        actionZoomIn = QtGui.QAction(QtGui.QIcon(":/images/resources/zoomin.png"), "Zoom In", self)
        actionShowAxis = QtGui.QAction(QtGui.QIcon(":/images/resources/axis.png"), "Show Axis", self)
        actionShowGrid = QtGui.QAction(QtGui.QIcon(":/images/resources/grid.png"), "Show Grid", self)
        actionRadius = QtGui.QAction(QtGui.QIcon(":/images/resources/growth2.png"), "Focus", self)
        actionShowFps = QtGui.QAction(QtGui.QIcon(":/images/resources/fps.png"), "Show FPS", self)

        actionBlack = QtGui.QAction(QtGui.QIcon(""), "Bg Black", self)
        actionWhite = QtGui.QAction(QtGui.QIcon(""), "Bg White", self)

        actionShowAxis.setShortcut(
            QtGui.QApplication.translate("MainWindow", "Ctrl+A", None, QtGui.QApplication.UnicodeUTF8))
        actionShowGrid.setShortcut(
            QtGui.QApplication.translate("MainWindow", "Ctrl+I", None, QtGui.QApplication.UnicodeUTF8))
        actionRadius.setShortcut(
            QtGui.QApplication.translate("MainWindow", "Ctrl+M", None, QtGui.QApplication.UnicodeUTF8))
        actionResetZoom.setShortcut(
            QtGui.QApplication.translate("MainWindow", "Ctrl+0", None, QtGui.QApplication.UnicodeUTF8))
        actionZoomOut.setShortcut(
            QtGui.QApplication.translate("MainWindow", "Ctrl+-", None, QtGui.QApplication.UnicodeUTF8))
        actionZoomIn.setShortcut(
            QtGui.QApplication.translate("MainWindow", "Ctrl++", None, QtGui.QApplication.UnicodeUTF8))

        QtCore.QObject.connect(actionResetZoom, QtCore.SIGNAL('triggered(bool)'), self.resetzoom)
        QtCore.QObject.connect(actionZoomOut, QtCore.SIGNAL('triggered(bool)'), self.zoomout)
        QtCore.QObject.connect(actionZoomIn, QtCore.SIGNAL('triggered(bool)'), self.zoomin)

        QtCore.QObject.connect(actionShowAxis, QtCore.SIGNAL('triggered(bool)'), self.show_hide_axis)
        QtCore.QObject.connect(actionShowGrid, QtCore.SIGNAL('triggered(bool)'), self.show_hide_grid)
        QtCore.QObject.connect(actionRadius, QtCore.SIGNAL('triggered(bool)'), self.update_radius)

        QtCore.QObject.connect(actionShowFps, QtCore.SIGNAL('triggered(bool)'), self.show_fps)

        QtCore.QObject.connect(actionBlack, QtCore.SIGNAL('triggered(bool)'), self.set_bg_black)
        QtCore.QObject.connect(actionWhite, QtCore.SIGNAL('triggered(bool)'), self.set_bg_white)

        session = Session()
        session.world.register_listener(self)

        self._actions = [["Viewer", "Zoom", actionResetZoom, 0],
                         ["Viewer", "Zoom", actionZoomOut, 0],
                         ["Viewer", "Zoom", actionZoomIn, 0],
                         ["Viewer", "Zoom", self.actionAutoFocus, 0],
                         ["Viewer", "Camera", actionShowAxis, 0],
                         ["Viewer", "Camera", actionShowGrid, 0],
                         ["Viewer", "Camera", actionRadius, 0],
                         ["Viewer", "Camera", actionBlack, 0],
                         ["Viewer", "Camera", actionWhite, 0],
                         #["Viewer", "Informations", actionShowFps, 1]
                         ]

    def initialize(self):
        from openalea.lpy import registerPlotter
        registerPlotter(self)

    def notify(self, sender, event=None):
        signal, data = event
        if signal in ('WorldChanged', 'world_sync'):
            self.setScene(data)
            self.updateGL()

    def actions(self):
        return self._actions

    def toolbar_actions(self):
        return self.actions()

    def menus(self):
        menu = QtGui.QMenu('View', self)
        actions = [action[2] for action in self.actions()]
        menu.addActions(actions)
        return [menu]

    def resetzoom(self):
        self.camera().setOrientation(self.orientation_initiale)
        self.camera().setPosition(self.position_initiale)
        self.updateGL()

    def zoomout(self):
        cam = self.camera()
        new_position = (cam.position() - cam.sceneCenter()) * 2
        cam.setPosition(new_position)
        self.updateGL()

    def zoomin(self):
        cam = self.camera()
        new_position = (cam.position() - cam.sceneCenter()) / 2
        cam.setPosition(new_position)
        self.updateGL()

    def show_fps(self):
        self._fps = not self._fps
        self.setFPSIsDisplayed(self._fps)

    def mainMenu(self):
        """
        :return: Name of menu tab to automatically set current when current widget
        begin current.
        """
        return "Viewer"

    def show_hide_axis(self):
        if self.axis:
            self.setAxisIsDrawn(False)  # hide axis
            self.axis = False
        else:
            self.setAxisIsDrawn(True)  # show axis
            self.axis = True

    def show_hide_grid(self):
        if self.grid:
            self.setGridIsDrawn(False)  # hide grid
            self.grid = False
        else:
            self.setGridIsDrawn(True)  # show grid
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

    def _on_autofocus_changed(self):
        self.autofocus = self.actionAutoFocus.isChecked()


def main():
    app = QtGui.QApplication(sys.argv)
    view = view3D()
    view.addToScene(Sphere())
    view.start()
    app.exec_()


if (__name__ == "__main__"):
    main()
