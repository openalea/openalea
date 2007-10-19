#!/usr/bin/env python
"""Visualisation of phyllotaxis processes.

Mainly based on mathplotlib.

:todo:
    Nothing.

:bug:
    None known.
    
:organization:
    INRIA

"""
# Module documentation variables:
__authors__="""Szymon Stoma    
"""
__contact__=""
__license__="Cecill-C"
__date__="<Timestamp>"
__version__="0.1"
__docformat__= "restructuredtext en"
__revision__="$Id$"

import openalea.plotools.plotable2 as ptb
#import visual
import math
import openalea.plantgl.all as pgl

def generate_VisualSequence_prim_id2abs_time( prim_id2time={}, legend="Primordium to absolute creation time", linestyle=":", marker="o", color="r" ):
    """Generates VisualSequence object from primordium id and its creation time containing the absolute time between primordia creation.
    
    Primordium id should have < defined.
    
    :parameters:
        prim_id2time : `{int->float}`
            Contains primordium id to creation time mapping. 
        legend : `string`
            legend of a line
        linestyle : `string`
            One of - : -. -
        marker : `string`
            One of + , o . s v x > <,
        color : `string`
                A matplotlib color arg
    :rtype: `ptb.VisualSequence`
    :return: The object containing data to plot prim_id to time. 
    """
    xy=prim_id2time.items()
    xy.sort()
    prim_id=[i[0] for i in xy]
    time=[i[1] for i in xy]  
    return ptb.VisualSequence( x=prim_id, y=time, legend=legend, linestyle=linestyle, marker=marker, color=color )


def generate_VisualSequence_prim_id2rel_time( prim_id2time={}, legend="Primordium to relative creation time", linestyle=":", marker="o", color="r" ):
    """Generates VisualSequence object from primordium id and its creation time containing the relative time between primordia creation.
    
    Primordium id should have < defined.
    
    :parameters:
        prim_id2time : `{int->float}`
            Contains primordium id to creation time mapping. 
        legend : `string`
            legend of a line
        linestyle : `string`
            One of - : -. -
        marker : `string`
            One of + , o . s v x > <,
        color : `string`
                A matplotlib color arg
    :rtype: `VisualSequence`
    :return: The object containing data to plot prim_id to time. 
    """
    xy=prim_id2time.items()
    xy.sort()
    prim_id=[i[0] for i in xy]
    time=[0]+[xy[ i+1 ][1] - xy[i][1] for i in range( len(xy)-1 )]  
    return ptb.VisualSequence( x=prim_id, y=time, legend=legend, linestyle=linestyle, marker=marker, color=color )
    
def generate_VisualSequence_prim_id2div_angle( prim_id2prim_pos, legend="Primordium to divergence angle", linestyle=":", marker="o", color="g" ):       
    """Generates VisualSequence object from primordium id and its creation position reflecting prim and .
    
    Primordium id should have < defined.
    
    :parameters:
        prim_id2prim_pos : `{int->vector}`
            Contains primordium id to creation time mapping. 
        legend : `string`
            legend of a line
        linestyle : `string`
            One of - : -. -
        marker : `string`
            One of + , o . s v x > <,
        color : `string`
                A matplotlib color arg
    :rtype: `VisualSequence`
    :return: The object containing data to plot prim_id to time. 
    """
    xy=prim_id2prim_pos.items()
    xy.sort()
    prim_id=[i[0] for i in xy]
    sta_div_ang=[0]+[standarize_angle( get_angle_between_primordias( xy[ i][1], xy[ i-1][1]) ) for i in range( len(xy)-1 )]  
    return ptb.VisualSequence( x=prim_id, y=sta_div_ang, legend=legend, linestyle=linestyle, marker=marker, color=color )


def generate_VisualSequence_prim_id2abs_angle( prim_id2prim_pos, legend="Primordium to absolute angle", linestyle=":", marker="x", color="r" ):       
    """Generates VisualSequence object from primordium id and its creation position reflecting prim and .
    
    Primordium id should have < defined.
    
    :parameters:
        prim_id2prim_pos : `{int->vector}`
            Contains primordium id to creation time mapping. 
        legend : `string`
            legend of a line
        linestyle : `string`
            One of - : -. -
        marker : `string`
            One of + , o . s v x > <,
        color : `string`
                A matplotlib color arg
    :rtype: `VisualSequence`
    :return: The object containing data to plot prim_id to time. 
    """
    xy=prim_id2prim_pos.items()
    xy.sort()
    prim_id=[i[0] for i in xy]
    #sta_div_ang=[get_angle_between_primordias( visual.vector(), xy[ i-1][1])  for i in range( len(xy) )]
    sta_div_ang=[get_angle_between_primordias( pgl.Vector3(1,0,0), xy[ i-1][1])  for i in range( len(xy) )]  
    return ptb.VisualSequence( x=prim_id, y=sta_div_ang, legend=legend, linestyle=linestyle, marker=marker, color=color )

     
def get_angle_between_primordias( yi, yj):
    """Return the angle between primordias.
    """
    #if yi.__class__ == visual.vector:
    #    d = yi.diff_angle(yj)
    #    if visual.mag( visual.rotate( yi, axis=(0,0,1), angle=d )- yj ) < 0.001:
    #        return d*360/(2*math.pi)
    #    else:
    #        return (2*math.pi-d)*360/(2*math.pi)
    #else:
        #except NotImplemented()    
        #d = yi.diff_angle(yj)
    d = pgl.angle( yi, yj )
    return  d*360/(2*math.pi)
    
def standarize_angle( a ):
    """Angle standarisation.
    """
    if a > 180:
        return 360 - a 
    return a
