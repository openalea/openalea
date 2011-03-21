# -*- python -*-
#
#       image.serial: read/write images
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Eric Moscardi <eric.moscardi@inria.fr>
#                       Jerome Chopard <jerome.chopard@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
"""
This module redefine load and save to account for spatial images
"""

__license__= "Cecill-C"
__revision__=" $Id: $ "

from os.path import exists
import Image,ImageOps
import os, fnmatch
from pylab import imread as _imread
from struct import pack,unpack,calcsize
from pickle import dumps,loads
import numpy as np
from inrimage import *
from lsm import *
from ..spatial_image import SpatialImage  

def save (file, img) :
	"""Save an array to a binary file in numpy format
	
	:Parameters:
	 - `file` (file or str) - File or filename to which the data is saved.
	                          If the filename does not already have a ".npy"
	                          extension, it is added.
	 - `img` (array)
	"""
	if isinstance(img,SpatialImage) :
		if isinstance(file,str) :
			if file.endswith(".npy") :
				file = open(file,'wb')
			else :
				file = open("%s.npy" % file,'wb')
		
		file.write("SpatialImage")
		header = dumps( (img.resolution,img.info) )
		file.write(pack('i',len(header) ) )
		file.write(header)
		
		np.save(file,img)
	else :
		np.save(file,img)

def load (file, mmap_mode=None) :
	"""Load a pickled, ``.npy``, or ``.npz`` binary file.
	
	:Parameters:
	 - `file` (file or str)
	 - `mmap_mode` (None, 'r+', 'r', 'w+', 'c') - optional
	    If not None, then memory-map the file, using the given mode
	    (see `numpy.memmap`).  The mode has no effect for pickled or
	    zipped files.
	    A memory-mapped array is stored on disk, and not directly loaded
	    into memory.  However, it can be accessed and sliced like any
	    ndarray.  Memory mapping is especially useful for accessing
	    small fragments of large files without reading the entire file
	    into memory.
	
	:Returns Type: array, tuple, dict, etc.
	"""
	if isinstance(file,str) :
		file = open(file,'rb')
	
	header = file.read(12)
	
	if header == "SpatialImage" :
		nb, = unpack('i',file.read(calcsize('i') ) )
		res,info = loads(file.read(nb) )
		data = np.load(file,mmap_mode)
		
		if len(res) == len(data.shape) :
			vdim = 1
		else :
			vdim = data.shape[-1]
		
		return SpatialImage(data,res,vdim,info)
	else :
		file.seek(0)
		return np.load(file,mmap_mode)

##################################################
# TODO : Read voxels size in xlm file if provided #
##################################################
def read_sequence ( directory, grayscale=True, number_images=None, start=0, increment=1, filename_contains="", voxels_size=None, verbose=True) :
    """
    Convert a sequence of images in a folder as a numpy array.
    The images must all be the same size and type.
    They can be in TIFF, .... format.

    - `grayscale` (bool) - convert the image to grayscale
    - `number_images` (int) - specify how many images to open
    - `start` (int) - used to start with the nth image in the folder (default = 0 for the first image)
    - `increment` (int) - set to "n" to open every "n" image (default = 1 for opening all images)
    - `filename_contains` (str) - only files whose name contains that string are opened
    - `voxels_size (tuple) - specify voxels size
    - `verbose` (bool) - verbose mode
    """
    
    _images = []
    _files = []

    if verbose : print "Loading : "
    for f in os.listdir(directory):
        if fnmatch.fnmatch(f, '*%s*' %filename_contains):
            try :
                im = Image.open(os.path.join(directory, f))
                _files.append(f)
                if grayscale is True :
                    _images.append(ImageOps.grayscale(im))
                else: 
                    _images.append(im)
            except :
                if verbose : print "\t warning : cannot open %s" %f
            
    if len(_images) == 0 :
        if verbose : print "\t no images loaded"
        return -1
        
    xdim, ydim = _images[0].size

    if number_images is None :
        zdim = round(float(len(_images) - start)/ increment)
        _nmax = len(_images) - start
    else :
        zdim = number_images
        _nmax = number_images * increment

    if _images[0].mode == 'RGB':
        nd_image = np.zeros((xdim,ydim,zdim, 3), dtype=np.uint8)

    nd_image = np.zeros((xdim,ydim,zdim))

    j = 0
    for i in _images[start:_nmax+start:increment] :
        if i.size == _images[start].size :
            nd_image[:,:,j] = i
            if verbose : print "\t ./%s" %_files[_images.index(i)]
            j += 1
        else :
            if verbose : print "%s : wrong size - %s expected, %s found" %(_files[_images.index(i)], _images[start].size, i.size)
    result = nd_image.transpose(1,0,2)

    if voxels_size is None :  
        return SpatialImage(result)
    else :
        return SpatialImage(result, voxels_size)


def imread (filename) :
    """Read an image file
	
    .. warning:: supported format are either the classical format for images
	         like png and jpg or lsm and inrimage format for spatial nd images
	
    :Parameters:
    - `filename` (str)
	
    :Returns Type: array
    """
    if not exists(filename) :
	raise IOError("The requested file do not exist: %s" % filename)
        
    if filename.endswith(".lsm"):
        try :
            return read_lsm(filename)
	except :
            pass

    if filename.endswith("inr.gz") | filename.endswith("inr"):
        try:
            return read_inrimage(filename)
        except :
            pass

    return _imread(filename)
