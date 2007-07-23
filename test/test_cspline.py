import sys
sys.path.insert(0,r'D:\pradal\devlp\alea\openalea\branches\plantglx\src\openalea')

import random

from plantglx.cspline import CSpline
import openalea.plantgl.all as pgl
vec2 = pgl.Vector2
vec3 = pgl.Vector3

def test_points2d():
    pts2d = map(vec2, zip(xrange(10),xrange(10)))
    spline = CSpline(pts2d)
    crv = spline.curve()

def test_points3d():
    pts3d = map(vec3, zip(xrange(10),xrange(10),xrange(10)))
    spline = CSpline(pts3d)
    crv = spline.curve()

def random_pts(n,interval=(-10,10)):
    def pts(interval=interval):
        return vec3( random.randint(*interval),
                     random.randint(*interval),
                     random.randint(*interval) )
    return [pts() for i in range(n) ]

def spline_crv(pts):
    spline = CSpline(pts)
    return spline.curve()
    
