# -*- python -*-
#
#       image.serial: read/write images
#
#       Copyright 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Jerome Chopard <jerome.chopard@sophia.inria.fr>
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

from struct import pack,unpack,calcsize
from pickle import dumps,loads
import numpy as np
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

