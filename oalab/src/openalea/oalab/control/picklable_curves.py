from openalea.plantgl.all import *

class RedNurbs2D(NurbsCurve2D):
    def __reduce__(self):
        return (RedNurbs2D, (self.ctrlPointList,))
        
class RedBezierNurbs2D(BezierCurve2D):
    def __reduce__(self):
        return (RedBezierNurbs2D, (self.ctrlPointList,))
        
class RedPolyline2D(Polyline2D):
    def __reduce__(self):
        return (RedPolyline2D, (self.pointList,))
        
class RedNurbsPatch(NurbsPatch):
    def __reduce__(self):
        return (RedNurbsPatch, (self.ctrlPointMatrix,))


"""
def curve():
    return NurbsCurve2D([(-0.5,0,1),(-0.198198,0.40991,1),(0.198198,-0.220721,1),(0.5,0,1)])

c = curve() # No Picklable

cu = RedNurbs2D(c.ctrlPointList) # Picklable
"""
