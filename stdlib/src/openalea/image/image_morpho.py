# -*- coding: latin-1 -*-
#
#       basics : image package
#
#       Copyright or © or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Da SILVA David <david.da_silva@cirad.fr>
#						Jerome Chopard <jerome.chopard@sophia.inria.fr>
#						Fernandez Romain <romain.fernandez@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

__doc__="""
This module provide basics function to handle 2D images
"""

__license__= "Cecill-C"
__revision__=" $Id: graph.py 116 2007-02-07 17:44:59Z tyvokka $ "

from math import sin,cos
import numpy
#from openalea.plantgl.math import Vector2
from data_image import DataImage
from raster import create_raster

def surface (raster, dx=1., dy=1.) :
    """
    compute exact surface of a raster
    """
    return len(raster)*dx*dy

def barycenter (raster) :
    xmoy=float(numpy.sum(raster.xlist()))
    ymoy=float(numpy.sum(raster.ylist()))
    return xmoy/len(raster),ymoy/len(raster)

#prcomp
def projection (vec1, vec2) :
    return vec1[0]*vec2[0]+vec1[1]*vec2[1]

def distance (vec1, vec2) :
    proj=projection(vec1,vec2)
    hx=vec1[0]-vec2[0]*proj
    hy=vec1[1]-vec2[1]*proj
    return hx*hx+hy*hy

def pca (raster, nb_axes=3) :
    """
    axe 0 : barycenter
    axe 1 : main ellipse axis
    axe 2 : second ellipse axis
    """
    from scipy.optimize import leastsq
    #barycenter
    xmoy,ymoy=barycenter(raster)
    bary=(xmoy,ymoy)
    #main axis
    pts=[(x-xmoy,y-ymoy) for x,y in raster.points()]
    def reg (alpha) :
        direction=(cos(alpha),sin(alpha))
        return [distance(vec,direction) for vec in pts]
    res=leastsq(reg,0.)
    alpha=float(res[0])
    axis=(cos(alpha),sin(alpha))
    lengths=[projection(v,axis) for v in pts]
    l1,l2=min(lengths),max(lengths)
    gd1=(axis[0]*l1,axis[1]*l1)
    gd2=(axis[0]*l2,axis[1]*l2)
    #second axis
    axis=(-axis[1],axis[0])
    lengths=[projection(v,axis) for v in pts]
    l1,l2=min(lengths),max(lengths)
    pt1=(axis[0]*l1,axis[1]*l1)
    pt2=(axis[0]*l2,axis[1]*l2)
    return bary,gd1,gd2,pt1,pt2

def extract_rasters (data_im) :
    """
    extract rasters from a data image
    """
    raster_points=dict( (col,[]) for col in set(data_im.data().flat) )
    #parcours de l'image
    w,h=data_im.size()
    for i in xrange(w) :
        for j in xrange(h) :
            col=data_im[i,j]
            raster_points[col].append( (i,j) )
    return dict( (col,create_raster(pts)) for col,pts in raster_points.iteritems() )

def connected_spaces (data_im) :
    """
    data_im is a boolean data image 0 or 1
    create a data image where each connected space of 
    ones has a single label
    connection between two diagonal pixel is not considered
    """
    w,h=data_im.size()
    label_im=DataImage(w,h)
    points_list={}
    free_label=1
    for i in xrange(w) :
        for j in xrange(h) :
            if data_im[i,j]>0 :
                new = True
                if i>0 :
                    col=label_im[i-1,j]
                    if col>0 :
                        new=False
                        label_im[i,j]=col
                if j>0 :
                    colj=label_im[i,j-1]
                    if colj>0 :
                        new=False
                        coli=label_im[i,j]
                        label_im[i,j]=colj
                        if coli>0 and coli!=colj :#two different zones must be connected
                            for x,y in points_list[coli] :
                                label_im[x,y]=colj
                            points_list[colj].extend(points_list[coli])
                            del points_list[coli]
                if new :#the point start a new zone
                    label_im[i,j]=free_label
                    points_list[free_label]=[]
                    free_label+=1
                points_list[label_im[i,j]].append( (i,j) )#add point to the list of point in this zone
    rasters=dict( (col,create_raster(pts)) for col,pts in points_list.iteritems() )
    return label_im,rasters

def set_labels (rasters, label_im, point_list) :
    return dict( (label,rasters[label_im[x,y]]) for label,(x,y) in point_list.iteritems() )

def raster_border (raster) :
    """
    return a raster containing only the border
    points of the given raster
    assume the raster is connexe
    """
    pass

__all__ = ["surface","barycenter","pca","extract_rasters","connected_spaces","set_labels"]
