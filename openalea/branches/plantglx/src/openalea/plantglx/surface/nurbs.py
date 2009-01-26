from math import sqrt
from openalea.plantgl.math import Vector3
from openalea.plantgl.scenegraph import Point3Array,RealArray,NurbsCurve2D

def distance (v1, v2) :
	x=v2[0]-v1[0]
	y=v2[1]-v1[1]
	return sqrt(x*x+y*y)

def nurbs (points, knots_values, degree) :
	"""
	create a plantgl nurbs
	"""
	pt_array=Point3Array([Vector3(x,y,1) for x,y in points])
	kv_array=RealArray(knots_values)
	curve=NurbsCurve2D(pt_array,kv_array,degree,60)
	return curve

def bezier_knot_vector (ctrl_pts, degree, uniform=False) :
	"""
	compute a nurbs knot vector from bezier control points
	"""
	nb_pts=len(ctrl_pts)
	nb_arc=(nb_pts-1)/degree
	nb_knots=degree+nb_pts
	p=0.
	param=[p]
	for i in xrange(nb_arc) :
		if uniform :
			p+=1
		else :
			p+=distance(ctrl_pts[degree*(i+1)],ctrl_pts[degree*i])
		param.append(p)
	kv=[param[0]]
	for p in param :
		for j in xrange(degree) :
			kv.append(p)
	kv.append(param[-1])
	return kv

def ctrl_points (data) :
	"""
	extract 2D control points from a list of strings
	"""
	close=False
	nb_arc=0
	points=[]
	for p in data :
		if p.lower()=='m' :
			continue
		elif p.lower() in ['c','l'] :
			nb_arc+=1
		elif p.lower()=='z' :
			close=True
		else :
			pt=p.split(',')
			points.append( (float(pt[0]),float(pt[1])) )
	return points,nb_arc,close

def read_line (line, type, degree) :
	if type=="hull" :
		if 'C' in line or 'c' in line :
			degree=3
		elif 'Q' in line or 'q' in line :
			degree=2
		elif 'L' in line or 'l' in line :
			degree=1
		else :
			raise UserWarning("degree not defined in '%s'" % line)
	data=line.split()
	ctrl_pts,nb_arc,closure=ctrl_points(data)
	if degree==1 :
		closure=False
	if type=="swung" :
		if ctrl_pts[0][1] > ctrl_pts[-1][1] :
			ctrl_pts.reverse()
		x0,y0=ctrl_pts[0]
		x1,y1=ctrl_pts[1]
		pts=[]
		symetry=(x1-x0)<0
		xn,yn=ctrl_pts[-1]
		for x,y in ctrl_pts :
			x=x-x0
			y=yn-y+y0
			if symetry :
				x*=-1
			pts.append( (x,y) )
		ctrl_pts=pts
	else :
		x0,y0=ctrl_pts[0]
		#ctrl_pts=[(x-x0,y-y0) for x,y in ctrl_pts]
	kv=bezier_knot_vector(ctrl_pts,degree,True)
	return nurbs(ctrl_pts,kv,degree)

