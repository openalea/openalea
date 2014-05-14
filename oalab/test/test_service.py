from openalea.plantgl.all import Viewer, PointSet, Color4Array, Color4
import numpy

from openalea.oalab.service.geometry import to_shape3d, register_shape3d

class MyObject(object):
    def __init__(self, n):
        self.points = numpy.random.randn(n, 3) * 100
        self.colors = zip(numpy.random.randint(0, 255, n).tolist(),
                          numpy.random.randint(0, 255, n).tolist(),
                          numpy.random.randint(0, 255, n).tolist())

def myobjectIn3d(obj):
    return PointSet(obj.points, colorList=Color4Array(map(Color4, obj.colors)))

register_shape3d(MyObject, myobjectIn3d)

if __name__ == '__main__':

    from openalea.vpltk.qt import QtGui
    instance = QtGui.QApplication.instance()
    if instance is None :
        app = QtGui.QApplication([])
    else :
        app = instance

    t = MyObject(100)
    Viewer.display(to_shape3d(t))

    if instance is None :
        app.exec_()

