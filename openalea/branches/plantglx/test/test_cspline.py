import random

from plantglx.cspline import CSpline
import openalea.plantgl.all as pgl
vec2 = pgl.Vector2
vec3 = pgl.Vector3

def spline_curve(pts,is_closed=False):
    spline = CSpline(pts,is_closed)
    return spline.curve()
    
def circle_pts(n, radius= 10):
    import math
    theta = 2*math.pi/n 
    pts = [vec3(math.cos(i*theta),math.sin(i*theta),random.random())*0.1*radius for i in range(n)]
    return pts

def random_pts(n,interval=(-10,10)):
    def pts(interval=interval):
        return vec3( random.randint(*interval),
                     random.randint(*interval),
                     random.randint(*interval) )
    return [pts() for i in range(n) ]

def test_points2d():
    pts2d = map(vec2, zip(xrange(10),xrange(10)))
    crv = spline_curve(pts2d)

def test_points3d():
    pts3d = map(vec3, zip(xrange(10),xrange(10),xrange(10)))
    crv = spline_curve(pts3d)

def test_random():
    pts = random_pts(10)
    crv = spline_curve(pts)

def test_closedrandom():
    pts = random_pts(10)
    crv = spline_curve(pts, is_closed=True)

def test_bigrandom():
    pts = random_pts(100)
    crv = spline_curve(pts) 

def test_circle():
    pts = circle_pts(10)
    crv = spline_curve(pts)

