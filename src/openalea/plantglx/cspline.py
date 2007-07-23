###############################################################################
#
# License CECILL
# Author: C. Pradal
# Copyright: CIRAD
#
###############################################################################

"""
Class Cardinal Spline.
A cradinal spline is a spline passing through a set of points.
"""

import os, math
import openalea.plantgl.all as pgl

__metaclass__ = type

class CSpline:
    """
    A CSpline interpolate a set of points.
    """
    def __init__(self, points):
        """
        Create a CSpline from a set of 2d or 3d points.
        """
        self.points = points
        if len(points) != 0:
            self.dim = len(points[0])
        else:
            self.dim = 3
        self.nurbs= None
        self.dist = None
        self.der = None

    def __len__(self):
        return len(self.points)

    def distances(self):
        """
        Compute the distance between the input points.
        """
        n = len(self)
        self.dist = []
        for i in range(n-1):
            p, q = self.points[i],self.points[i+1]
            self.dist.append(pgl.norm(q-p))

    def derivatives(self):
        """
        Compute the derivatives based on the knots and the distance.
        At Pi, the derivative is:
            D_i = P_(i-1)P_i / ||.|| + P_iP_(i+1) / ||.||
        """
        if not self.dist:
            self.distances()

        n = len(self.points)
        d0 = (self.points[1]-self.points[0])/ (2.*self.dist[0])
        dn = (self.points[-1]-self.points[-2])/ (2.*self.dist[-1])
        self.der = [d0]
        
        for i in xrange(1,n-1):
            p, q, r = self.points[i-1], self.points[i], self.points[i+1]
            dx1, dx2 = 2*self.dist[i-1], 2*self.dist[i]
            
            di = (q-p)/dx1+(r-q)/dx2
            self.der.append(di)

        self.der.append(dn)


    def bezier_cp(self):
        """
        Compute bezier control points from the input points.
        """
        n = len(self)
        self.ctrl_pts = []
        for i in xrange(n-1):
            p, q = self.points[i:i+2] 
            dp, dq = self.der[i:i+2]
            self.ctrl_pts.append(p)
            self.ctrl_pts.append(p+dp)
            self.ctrl_pts.append(q-dq)
        # last point
        self.ctrl_pts.append(self.points[-1])


    def bezier_kv(self, linear=False):
        """
        Compute a nurbs knot vector from Bezier control points.
        bezier_kv(linear=False) -> knot_vector

        :param: linear indicate if the parametrization is linear or 
        pseudo curvilinear abscisse.
        """
        degree = 3
        nb_pts = len(self.ctrl_pts )
        nb_arc = len(self)-1
        assert nb_arc == (nb_pts-1) / degree

        nb_knots = degree + nb_pts
        p = 0.
        param = [p]
        if linear:
            param = range(nb_arc)
        else:
            dist = self.dist
            assert len(dist) == nb_arc
            for d in dist:
                p += d
                param.append( p )
    
        self.kv= [ param[ 0 ] ]
        for p in param:
            for j in range( degree ):
                self.kv.append( p )
        self.kv.append( param[ -1 ] )

    def curve(self):
        """
        Return the equivalent PlantGL nurbs curve which interpol the points.
        """
        if not self.nurbs:
            self.distances()
            self.derivatives()
            self.bezier_cp()
            self.bezier_kv()
 
        pts = self.points
        kv = pgl.RealArray(self.kv)

        if self.dim == 3:
            ctrl_pts = pgl.Point4Array(self.ctrl_pts,1)
            self.nurbs = pgl.NurbsCurve( ctrl_pts, kv, 3, 60)
        elif self.dim == 2:
            ctrl_pts = pgl.Point3Array(self.ctrl_pts,1)
            self.nurbs = pgl.NurbsCurve2D( ctrl_pts, kv, 3, 60)
        else:
            raise "Unable to build a spline curve from points of dimension %d"% (self.dim,)

        return self.nurbs
            
