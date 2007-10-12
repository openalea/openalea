from openalea.plantgl.all import *

from cspline import cspline, CSpline

def loft( nurbs_curves, distances ):
    
    assert len(nurbs_curves) == len(distances)
    nb_crv = len(nurbs_curves)
    crv0 = nurbs_curves[0]
    ku = crv0.knotList

    pts = map(lambda x:x.ctrlPointList,nurbs_curves)
    for i, z in enumerate(distances):
        for pt in pts[i]:
            pt.z = z
    
    raws =zip(*pts) 
    
    raws_curves = map(lambda x:cspline(x,is_linear=True),raws)
    #for curve in raws_curves:
    #    curve.setKnotListToDefault()
        
    spline = CSpline(raws[0])
    crv = spline.curve(is_linear=True)
    kv = RealArray(spline.kv)

    nb_crv = len(raws_curves)
    nb_pts = len(crv.ctrlPointList)
    ctrlPoint_mat= Point4Matrix(nb_crv, nb_pts)
    for i in range(nb_crv):
        cpts = raws_curves[i].ctrlPointList
        for j in range(nb_pts):
            ctrlPoint_mat.__setitem__(i,j,cpts[j])
    
    scene= Scene()
    surface = NurbsPatch(ctrlPoint_mat, ku, kv, crv0.degree, crv.degree, crv0.getStride(), crv.getStride())
    #surface.setVKnotListToDefault()
    return surface
    
