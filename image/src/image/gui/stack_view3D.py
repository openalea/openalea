#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
# -*- python -*-
#
#       openalea.image.analysis.gui.stack_view3D
#
#       Copyright 2010-2011 INRIA - CIRAD - INRA - ENS-Lyon
#
#       File author(s): Vincent Mirabet - Frederic Boudon
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
from openalea.image.serial.basics import imread
from openalea.image.spatial_image import SpatialImage
from openalea.image.algo.analysis import SpatialImageAnalysis
#compatibility
try:
	from tvtk.tools import ivtk
	from tvtk.api import tvtk
except ImportError:
	from enthought.tvtk.tools import ivtk
	from enthought.tvtk.api import tvtk
except:
	print "import impossible dans stack_view3D"
	sys.exit(0)

from colormaps import black_and_white, rainbow_full, rainbow_green2red, rainbow_red2blue

def img2polydata(image, list_remove=[], sc=None, verbose=False):
	"""
	Convert a |SpatialImage| to a PolyData object with cells surface
	
	: Parameters :
	list_remove : a list of cells to be removed from the tissue before putting it on screen
	sc : if you give a paramter here, it will use it as scalar. you need to give a
	cell->scalar dictionnary
	
	"""
	
	labels_provi = list(np.unique(image))
	#ici on filtre déjà les listes
	labels= [i for i in labels_provi if i not in list_remove]
	
	try:      labels.remove(0)
	except:   pass
	try:      labels.remove(1)
	except:   pass
	
	#print image.shape
	
	xyz = {}
	if verbose:print "on récupère les bounding box"
	bbox = ndimage.find_objects(image)
	#print labels
	for label in xrange(2,max(labels)+1):
		if not label in labels: continue
		if verbose:print "% until cells are built", label/float(max(labels))*100
		slices = bbox[label-1]
		label_image = (image[slices] == label)
		#here we could add a laplacian function to only have the external shape
		mask = ndimage.laplace(label_image)
		label_image[mask!=0] = 0
		mask = ndimage.laplace(label_image)
		label_image[mask==0]=0
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
	k=0.0
	for c in filtre:
		if verbose: print "% until polydata is built", k/float(len(filtre))*100
		k+=1.
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
	

def rootSpI(img, list_remove=[], verbose=False):
	"""
	case where the data is a spatialimage
	"""
	#cells are positionned inside a structure, the polydata, and assigned a scalar value
	polydata = img2polydata(img, list_remove=list_remove, verbose=verbose)
	m = tvtk.PolyDataMapper(input=polydata.output)
	#definition of the scalar range (default : min to max of the scalar value)
	m.scalar_range=np.min(img), np.max(img)
	#actor that manage different views if memory is short
	a = tvtk.QuadricLODActor(mapper=m)
	a.property.point_size=8
	#scalebar
	sc=tvtk.ScalarBarActor(orientation='vertical',lookup_table=m.lookup_table)
	return a, sc, m
	
def rootSpIA(img, list_remove=[], sc=None, verbose=False):
	"""
	case where the data is a spatialimageanalysis
	"""	
	#cells are positionned inside a structure, the polydata, and assigned a scalar value
	polydata = img2polydata(img.image, list_remove=list_remove, sc=sc, verbose=verbose)
	m = tvtk.PolyDataMapper(input=polydata.output)
	#definition of the scalar range (default : min to max of the scalar value)
	if sc:
		ran=[sc[i] for i in sc.keys() if i not in list_remove]
		m.scalar_range=np.min(ran), np.max(ran)
	#actor that manage different views if memory is short
	a = tvtk.QuadricLODActor(mapper=m)
	a.property.point_size=8
	#scalebar
	sc=tvtk.ScalarBarActor(orientation='vertical',lookup_table=m.lookup_table)
	return a, sc, m
	


def display3D(img, list_remove=[], dictionnary=None, lut=black_and_white, verbose=False):
	"""
	paramètres :
	img : SpatialImage ou SpatialImageAnalysis
	list_remove : une liste des cellules à enlever lors de l'affichage
	dictionnary : dictionnaire cells->scalar
	lut : disponibles dans colormaps
	verbose : pour afficher ou non les progressions
	ex : 
	im1 = imread('../../../test/segmentation.inr.gz')
	im1a=SpatialImageAnalysis(im1)	
	dictionnary=dict(zip(im1a.labels(), im1a.volume()))
	display3D(im1,range(100), dictionnary, rainbow_full)
	
	fonction maitre en deux parties :
	la première partie gère le format de l'objet donné en paramètre	
	la seconde partie gère l'affichage
	
	"""
	#management of file format
	if isinstance(img,SpatialImageAnalysis):
		a, sc, m=rootSpIA(img, list_remove=list_remove,sc=dictionnary, verbose=verbose)
	elif isinstance(img,SpatialImage):
		a, sc, m=rootSpI(img, list_remove=list_remove, verbose=verbose)
	else:
		print "for now this file format is not managed by display3D)"
		return
	#choice of colormap
	m.lookup_table=lut(m.lookup_table)
	#switching on the viewer and loading the object and the scalarbar
	viewer = ivtk.viewer()
	viewer.scene.add_actor(a)
	viewer.scene.add_actor(sc)
	


if __name__ == '__main__':
	im1 = imread('../../../test/segmentation.inr.gz')
	im1a=SpatialImageAnalysis(im1)
	dictionnary=dict(zip(im1a.labels(), im1a.volume()))
	labs=im1a.labels()
	L1=im1a.L1()[1]
	filtre=[i for i in labs if i not in L1]
	display3D(im1,filtre, dictionnary, rainbow_full)
	
