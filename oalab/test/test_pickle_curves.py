from openalea.plantgl.all import BezierCurve2D, NurbsCurve2D, Polyline2D, NurbsPatch
from openalea.oalab.control.picklable_curves import RedNurbs2D, RedBezierNurbs2D, RedPolyline2D, RedNurbsPatch
from openalea.lpy.gui.objectmanagers import get_managers
from pickle import loads, dumps

def curve():
    return NurbsCurve2D([(-0.5,0,1),(-0.198198,0.40991,1),(0.198198,-0.220721,1),(0.5,0,1)])

def test_pickle_crv2D():
    crv = curve()
    ctrl_pts = crv.ctrlPointList
    # Dump
    new_ctrl_pts = dumps(ctrl_pts)
    # Load
    new_curve = NurbsCurve2D(loads(new_ctrl_pts))
    # Check
    assert repr(new_curve) == repr(crv)

def test_pickle_newcrv2D():
    crv = RedNurbs2D([(-0.5,0,1),(-0.198198,0.40991,1),(0.198198,-0.220721,1),(0.5,0,1)], "Curve2D")
    saved_curve = dumps(crv)
    loaded_curve = loads(saved_curve)
    # Check
    assert repr(crv) == repr(loaded_curve), "%s != %s"%(repr(crv), repr(loaded_curve))
    assert crv.typename == loaded_curve.typename
    assert loaded_curve.typename == "Curve2D"
    
def test_pickle_newbezier():
    pointlist = [(-0.5,0,1),(-0.198198,0.40991,1),(0.198198,-0.220721,1),(0.5,0,1)]
    crv = RedBezierNurbs2D(pointlist)
    saved_curve = dumps(crv)
    loaded_curve = loads(saved_curve)
    # Check
    assert repr(crv) == repr(loaded_curve), "%s != %s"%(repr(crv), repr(loaded_curve))
    
def test_pickle_newpolyline():
    pointlist = [(-0.5,0),(-0.198198,0.40991),(0.198198,-0.220721),(0.5,0)]
    crv = RedPolyline2D(pointlist)
    saved_curve = dumps(crv)
    loaded_curve = loads(saved_curve)
    # Check
    assert repr(crv) == repr(loaded_curve), "%s != %s"%(repr(crv), repr(loaded_curve))
    
def test_pickle_newnurbspatch():
    crv = RedNurbsPatch(([[(0,-0.5,0,1),(0,-0.166667,0,1),(0,0.166667,0,1),(1.50456e-16,0.00720354,0.739195,1)],[(0,-0.5,0.333333,1),(0,-0.166667,0.333333,1),(0,0.166667,0.333333,1),(0,0.5,0.333333,1)],[(0,-0.5,0.666667,1),(0,-0.166667,0.666667,1),(0,0.166667,0.666667,1),(0,0.5,0.666667,1)],[(0,-0.5,1,1),(0,-0.166667,1,1),(0,0.166667,1,1),(0,0.5,1,1)]]))
    saved_curve = dumps(crv)
    loaded_curve = loads(saved_curve)
    # Check
    assert repr(crv.ctrlPointMatrix) == repr(loaded_curve.ctrlPointMatrix), "%s != %s"%(repr(crv.ctrlPointMatrix), repr(loaded_curve.ctrlPointMatrix))

def test_pickle_newcrv2Dbis():
    crv = PickableNurbsCurve2D([(-0.5,0,1),(-0.198198,0.40991,1),(0.198198,-0.220721,1),(0.5,0,1)])
    saved_curve = dumps(crv)
    loaded_curve = loads(saved_curve)
    # Check
    assert repr(crv) == repr(loaded_curve), "%s != %s"%(repr(crv), repr(loaded_curve))
    
def test_pickle_typename():
    crv = PickableNurbsCurve2D_bis([(-0.5,0,1),(-0.198198,0.40991,1),(0.198198,-0.220721,1),(0.5,0,1)])
    crv.typename = "Curve2D"
    saved_curve = dumps(crv)
    loaded_curve = loads(saved_curve)
    assert loaded_curve.typename == "Curve2D"
    
class PickableNurbsCurve2D_bis(NurbsCurve2D):
    def __init__(self, ctrlPointList, typename=""):
        super(PickableNurbsCurve2D_bis, self).__init__(ctrlPointList)
        self.typename = typename
        
    def __reduce__(self):
        return (PickableNurbsCurve2D_bis, (self.ctrlPointList, self.typename,))

        
class PickableNurbsCurve2D(object):
    def __init__(self, *args, **kwds):
        self.crv = NurbsCurve2D(*args, **kwds)
        self.ctrl_pts = self.crv.ctrlPointList
    
    def __getstate__(self):
        d = self.__dict__.copy()
        del d["crv"]
        return d
        
    def __setstate__(self,dict):
        ctrl_pts = dict["ctrl_pts"]
        self.__dict__.update(dict)
        self.crv = NurbsCurve2D(ctrl_pts)
        
    def __repr__(self):
        return repr(self.crv)

if( __name__ == "__main__"):
    test_pickle_crv2D()
    test_pickle_newcrv2D()
    
    test_pickle_newcrv2Dbis()
    test_pickle_newbezier()
    test_pickle_newpolyline()
    test_pickle_newnurbspatch()
    
    test_pickle_typename()
    
