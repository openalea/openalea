# -*- python -*-
# -*- coding: latin-1 -*-
#
#       svg : image package
#
#       Copyright 2006 - 2008 INRIA - CIRAD - INRA  
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

"""#This module provide basics function to handle 2D images"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

from openalea.svgdraw import open_svg,SVGImage,SVGSphere\
                            ,SVGPath,SVGGroup,SVGLayer,SVGScene\
                            ,Color3

def loadsc (filename) :
    """todo"""
    f=open_svg(filename,'r')
    sc=f.read()
    f.close()
    return sc

def writesc (sc, filename) :
    f=open_svg(filename,'w')
    f.write(sc)
    f.close()

def get_elm (svggr, svgid) :
    return svggr.get_id(svgid)

def svg_image (svgid, image, filename=None) :
    svgim=SVGImage(None,svgid)
    if filename is None :
        svgim.set_filename(svgid)
    else :
        svgim.set_filename(filename)
    svgim.set_image(image)
    if image is not None :
        w,h=image.size
        svgim.scale2D( (w,h,0) )
    return svgim

def svg_point (svgid, x, y, radius=2, color=None) :
    svgelm=SVGSphere(None,svgid)
    svgelm.scale2D( (radius,radius,radius) )
    svgelm.translate2D( (x,y,0) )
    if color is None :
        svgelm.fill=color
    else :
        svgelm.fill=Color3(*color)
    return svgelm

def svg_polyline (svgid, pts, color=None, stroke_width=1.) :
    svgelm=SVGPath(None,svgid)
    svgelm.append("M",[pts[0]])
    for pt in pts[1:] :
        svgelm.append("L",[pt])
    if color is None :
        svgelm.stroke=color
    else :
        svgelm.stroke=Color3(*color)
    svgelm.stroke_width=stroke_width
    return svgelm

def svg_group (svgid, svg_elms) :
    svggr=SVGGroup(None,svgid)
    for elm in svg_elms :
        svggr.append(elm)
    return svggr

def svg_layer (svgid, svg_elms, name=None) :
    svglay=SVGLayer(None,svgid)
    if name is None :
        svglay.set_name(svgid)
    else :
        svglay.set_name(name)
    for elm in svg_elms :
        svglay.append(elm)
    return svglay

def svg_scene (width,height,layers) :
    svgsc=SVGScene()
    svgsc.set_size(width,height)
    for lay in layers :
        svgsc.append(lay)
    return svgsc

def svg_elements (svggr) :
    return list(svggr.elements())

def svg_positions (svg_pts) :
    coords={}
    for pt in svg_pts :
        x,y,z=pt.center()
        coords[pt.svgid()]=(x,y)
    return coords

__all__=["loadsc","writesc",
         "get_elm",
         "svg_image","svg_point","svg_polyline",
         "svg_group","svg_layer",
         "svg_scene",
         "svg_elements",
         "svg_positions"]
