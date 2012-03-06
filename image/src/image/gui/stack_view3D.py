# -*- python -*-
#
#       vplants.mars_alt.alt.lineage_editor
#
#       Copyright 2010-2011 INRIA - CIRAD - INRA - ENS-Lyon
#
#       File author(s): Vincent Mirabet - Eric Moscardi, Manuel Forero
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#       http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################


__license__= "Cecill-C"
__revision__=" $Id$ "

# import libraries
import numpy as np
from scipy import ndimage
import math


def img2polydata(image):
    """
    Convert a |SpatialImage| to a PolyData object with cells surface

    : Parameters :

    """

    labels = list(np.unique(image))
    
    try:      labels.remove(0)
    except:   pass
    try:      labels.remove(1)
    except:   pass
    
    print image.shape
    
    xyz = {}
    bbox = ndimage.find_objects(image)
    print labels
    for label in xrange(2,max(labels)+1):
        if not label in labels: continue
        print label
        slices = bbox[label-1]
        label_image = (image[slices] == label)
        # compute the indices of voxel with adequate label
        a = np.array(label_image.nonzero()).T
        print a.shape
        if a.shape[1] == 4: print a
        else:               xyz[label] = a
    

    vx,vy,vz = image.resolution

    polydata = tvtk.AppendPolyData()
    polys = {}
    for c in xyz:
        pd = tvtk.PolyData(points=xyz[c])
        pd.point_data.scalars = [c for i in xrange(len(xyz[c]))]

        f=tvtk.VertexGlyphFilter(input=pd)
        f2=tvtk.PointDataToCellData(input=f.output)
        polys[c]=f2.output
        polydata.add_input(polys[c])
        polydata.set_input_array_to_process(0,0,0,0,0)


    return polydata


from tvtk.tools import ivtk
from tvtk.api import tvtk

def display3D(img, colormap = 'jet'):
    polydata = img2polydata(img)
    m = tvtk.PolyDataMapper(input=polydata.output)
    #m.lookup_table.table = colormap


    a = tvtk.QuadricLODActor(mapper=m)
    a.property.point_size=4

    mapper1=m
    viewer = ivtk.viewer()
    viewer.scene.add_actor(a)
    


if __name__ == '__main__':
    from openalea.image import *
    im1 = imread('../../../test/segmentation.inr.gz')

    display3D(im1)

