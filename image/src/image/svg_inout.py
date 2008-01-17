# -*- python -*-
# -*- coding: latin-1 -*-
#
#       svg : image package
#
#       Copyright or © or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
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

from openalea.svgdraw import open_svg,SVGImage,SVGSphere,SVGGroup,SVGLayer,SVGScene,Color3

def loadsc (filename) :
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

def svg_image (image, filename, svgid) :
    svgim=SVGImage(None,svgid)
    svgim.set_filename(filename)
    svgim.set_image(image)
    if image is not None :
        w,h=image.size
        svgim.scale2D( (w,h,0) )
    return svgim

def svg_point (x, y, radius=2, color=None, svgid=None) :
    svgelm=SVGSphere(None,svgid)
    svgelm.scale2D( (radius,radius,radius) )
    svgelm.translate2D( (x,y,0) )
    svgelm.fill=color
    return svgelm

def svg_group (svg_elms, svgid) :
    svggr=SVGGroup(None,svgid)
    for elm in svg_elms :
        svggr.append(elm)
    return svggr

def svg_layer (svg_elms, name, svgid) :
    svglay=SVGLayer(None,svgid)
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

def elements (svggr) :
    return list(svggr.elements())

def positions (svg_pts) :
    coords={}
    for pt in svg_pts :
        x,y,z=pt.center()
        coords[pt.svgid()]=(x,y)
    return coords
