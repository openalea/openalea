from openalea.plantgl.all import *
import numpy 

sphere = Sphere()

shapes = [Sphere, Box, Cylinder]
scene = Scene([ shape() for shape in shapes])

class Toto(object):
    def __init__(self, geometry, color=(155,10,39)):
        self.geometry = geometry
        self.color = color

    def _repr_3d_(self):
        return Shape(self.geometry, Material(self.color))


# Service
_registry = {}

def adapt(obj):
    import openalea.plantgl.all as pgl
    import collections
    if isinstance(obj, (pgl.Scene, pgl.Shape, pgl.Geometry)):
        return obj
    
    if issubclass(type(obj), collections.Sequence):
        try:
            result = pgl.Scene(obj)
            return result
        except Exception, e:
            pass

    # Case _repr_3d_
    if hasattr(obj, "_repr_3d_"):
        return adapt(obj._repr_3d_())

    for types, function in _registry.iteritems():
        if isinstance(obj, types):
            return adapt(function(obj))

def register_3d(type_or_types, functor):
    _registry[type_or_types] = functor


class MyObject(object):
    def __init__(self, n):
        self.points = numpy.random.randn(n,3)*100
        self.colors = zip(numpy.random.randint(0,255,n).tolist(), 
                          numpy.random.randint(0,255,n).tolist(), 
                          numpy.random.randint(0,255,n).tolist())

def myobjectIn3d(obj):
    return PointSet(obj.points,colorList=Color4Array(map(Color4, obj.colors)))

register_3d(MyObject, myobjectIn3d)

#t= Toto(sphere)
#Viewer.display(adapt(t))

t = MyObject(100)
Viewer.display(adapt(t))
