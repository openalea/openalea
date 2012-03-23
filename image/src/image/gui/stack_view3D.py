#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
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
import sys
import numpy as np
from scipy import ndimage
import math
from openalea.image.all import imread, display, SpatialImage
from openalea.image.algo.analysis import SpatialImageAnalysis
#compatibility
try:
	from tvtk.tools import ivtk
	from tvtk.api import tvtk
	from mayavi import mlab 
	from pyface.api import GUI
except ImportError:
	from enthought.tvtk.tools import ivtk
	from enthought.tvtk.api import tvtk
	from enthought.mayavi import mlab
	from enthought.pyface.api import GUI
except:
	print "import impossible dans stack_view3D"
	sys.exit(0)


def img2polydata(image, list_remove=[], sc=None):
	"""
	Convert a |SpatialImage| to a PolyData object with cells surface
	
	: Parameters :
	sc : if you give a paramter here, it will use it as scalar. you need to give a
	cell->scalar disctionnary
	
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
		a+=[slices[0].start, slices[1].start, slices[2].start ]
		#print a.shape
		if a.shape[1] == 4:
			#print a
			pass
		else:
			xyz[label] = a
    

	vx,vy,vz = image.resolution
	
	polydata = tvtk.AppendPolyData()
	polys = {}
	filtre=[i for i in xyz.keys() if i not in list_remove]
	for c in filtre:
		p=xyz[c]
		p=p.astype(np.float)
		pd = tvtk.PolyData(points=xyz[c].astype(np.float))
		if sc:
			try:
				pd.point_data.scalars = [sc[c] for i in xrange(len(xyz[c]))]
			except:
				pd.point_data.scalars = [c for i in xrange(len(xyz[c]))]
		else:
			pd.point_data.scalars = [c for i in xrange(len(xyz[c]))]
	
		f=tvtk.VertexGlyphFilter(input=pd)
		f2=tvtk.PointDataToCellData(input=f.output)
		polys[c]=f2.output
		polydata.add_input(polys[c])
		polydata.set_input_array_to_process(0,0,0,0,0)
	
	
	return polydata
	

def rootSpI(img, list_remove=[]):
	"""
	case where the data is a spatialimage
	"""
	polydata = img2polydata(img, list_remove=[])
	m = tvtk.PolyDataMapper(input=polydata.output)
	m.scalar_range=np.min(img), np.max(img)
	#m.lookup_table.table = colormap
	
	a = tvtk.QuadricLODActor(mapper=m)
	a.property.point_size=4
	
	sc=tvtk.ScalarBarActor(orientation='vertical',lookup_table=m.lookup_table)
	#sc.position_coordinate.coordinate_system='normalized_viewport'
	#sc.position_coordinate.value=0.1,0.01,0.0
	#scalar_bar.orientation="horizontal"
	return a, sc, m
	
def rootSpIA(img, list_remove=[], sc=None):
	"""
	case where the data is a spatialimageanalysis
	"""	
	polydata = img2polydata(img.image, list_remove, sc)
	m = tvtk.PolyDataMapper(input=polydata.output)
	if sc:
		ran=[sc[i] for i in sc.keys() if i not in list_remove]
		m.scalar_range=np.min(ran), np.max(ran)
	a = tvtk.QuadricLODActor(mapper=m)
	a.property.point_size=4
	sc=tvtk.ScalarBarActor(orientation='vertical',lookup_table=m.lookup_table)
	return a, sc, m
	


def display3D(img, list_remove=[], label=None):
	if type(img)==type(SpatialImage(np.zeros((0,0,0)))):
		a, sc, m=rootSpI(img)
	elif type(img)==type(SpatialImageAnalysis(np.zeros((0,0,0)))):
		a, sc, m=rootSpIA(img, list_remove,label)
	mapper1=m
	viewer = ivtk.viewer()
	viewer.scene.add_actor(a)
	viewer.scene.add_actor(sc)
	


if __name__ == '__main__':
	im1 = imread('../../../test/segmentation.inr.gz')
	im1a=SpatialImageAnalysis(im1)
	sc=dict(zip(im1a.labels(), im1a.volume()))
	display3D(im1a,range(100), sc)
	
	


#j'en suis à devoir choisir si sc sera un dico ou une liste, je pense partir sur le dico
