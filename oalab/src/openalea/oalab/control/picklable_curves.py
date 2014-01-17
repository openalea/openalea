from openalea.plantgl.all import NurbsCurve2D, BezierCurve2D, Polyline2D, NurbsPatch

class RedNurbs2D(NurbsCurve2D):
    def __init__(self, ctrlPoint, typename=""):
        super(RedNurbs2D, self).__init__(ctrlPoint)
        self.typename = typename
        
    def __reduce__(self):
        return (RedNurbs2D, (self.ctrlPointList, self.typename,))
        
class RedBezierNurbs2D(BezierCurve2D):
    def __init__(self, ctrlPoint, typename=""):
        super(RedBezierNurbs2D, self).__init__(ctrlPoint)
        self.typename = typename
        
    def __reduce__(self):
        return (RedBezierNurbs2D, (self.ctrlPointList, self.typename,))
        
class RedPolyline2D(Polyline2D):
    def __init__(self, ctrlPoint, typename=""):
        super(RedPolyline2D, self).__init__(ctrlPoint)
        self.typename = typename
        
    def __reduce__(self):
        return (RedPolyline2D, (self.pointList, self.typename,))       
        
class RedNurbsPatch(NurbsPatch):
    def __init__(self, ctrlPoint, typename=""):
        super(RedNurbsPatch, self).__init__(ctrlPoint)
        self.typename = typename
        
    def __reduce__(self):
        return (RedNurbsPatch, (self.ctrlPointMatrix, self.typename,))  


"""
def curve():
    return NurbsCurve2D([(-0.5,0,1),(-0.198198,0.40991,1),(0.198198,-0.220721,1),(0.5,0,1)])

c = curve() # No Picklable

cu = RedNurbs2D(c.ctrlPointList) # Picklable
"""
