# -*- python -*-
#
#       spatial_image: spatial nd images
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
This module create the main |SpatialImage| object
"""

__license__= "Cecill-C"
__revision__=" $Id: $ "

import numpy as np

# -- deprecation messages --
import warnings, exceptions
msg = "SpatialImage.resolution is deprecated, use SpatialImage.voxelsize"
rezexc = exceptions.PendingDeprecationWarning(msg)

class SpatialImage (np.ndarray) :
	"""Associate meta data to np.ndarray
	"""
	def __new__ (cls, input_array, voxelsize = None,
		     vdim = 1, info = None, dtype = None, **kwargs) :
		"""Instantiate a new |SpatialImage|

		if voxelsize is None, vdim will be used to infer space size and affect
		a voxelsize of 1 in each direction of space

		.. warning :: `resolution` keyword is deprecated. Use `voxelsize` instead.

		:Parameters:
		 - `cls` - internal python
		 - `input_array` (array) - data to put in the image
		 - `voxelsize` (tuple of float) - spatial extension in each direction
		                                   of space
		 - `vdim` (int) - size of data if vector data are used
		 - `info` (dict of str|any) - metainfo
		"""
		#initialize datas. For some obscure reason, we want the data
		#to be F-Contiguous in the NUMPY sense. I mean, if this is not
		#respected, we will have problems when communicating with
		#C-Code... yeah, that makes so much sense (fortran-contiguous
		#to be c-readable...).
		dtype = dtype if dtype is not None else input_array.dtype
                if input_array.flags.f_contiguous :
                        obj = np.asarray(input_array, dtype=dtype).view(cls)
		else :
                        obj = np.asarray(input_array, dtype=dtype, order='F').view(cls)
		
		voxelsize = kwargs.get("resolution", voxelsize) #to manage transition
		if voxelsize is None :
			if vdim == 1 :
				voxelsize = (1.,) * len(obj.shape)
			else :
				voxelsize = (1.,) * (len(obj.shape) - 1)
		else :
			if vdim == 1 :
				if len(voxelsize) != len(obj.shape) :
					raise ValueError("data dimension and voxelsize mismatch")
			else :
				if len(voxelsize) != (len(obj.shape) - 1) :
					raise ValueError("data dimension and voxelsize mismatch")

		obj.voxelsize = tuple(voxelsize)

		#set metadata
		if info is None :
			obj.info = {}
		else :
			obj.info = dict(info)

		#return
		return obj

	@property
	def resolution(self):
		warnings.warn(rezexc)
		return self.voxelsize

	def __array_finalize__ (self, obj) :
		if obj is None :
			return

		#assert resolution
		res = getattr(obj, 'voxelsize', None)
		if res is None :#assert vdim == 1
			res = (1.,) * len(obj.shape)

		self.voxelsize = tuple(res)

		#metadata
		self.info = dict(getattr(obj, 'info', {}) )

	def clone (self, data) :
		"""Clone the current image metadata
		on the given data.

		.. warning:: vdim is defined according to self.voxelsize and data.shape

		:Parameters:
		 - `data` - (array)

		:Returns Type: |SpatialImage|
		"""
		if len(data.shape) == len(self.voxelsize) :
			vdim = 1
		elif len(data.shape) - len(self.voxelsize) == 1 :
			vdim =data.shape[-1]
		else :
			raise UserWarning("unable to handle such data dimension")

		return SpatialImage(data,self.voxelsize,vdim,self.info)

	@classmethod
	def valid_array(cls, array_like):
		return isinstance(array_like, (np.ndarray, cls)) and \
		    array_like.flags.f_contiguous


def empty_image_like(spatial_image):
	array = np.zeros( spatial_image.shape, dtype=spatial_image.dtype )
	return SpatialImage(array, spatial_image.voxelsize, vdim=1)


def null_vector_field_like(spatial_image):
	array = np.zeros( list(spatial_image.shape)+[3], dtype=np.float32 )
	return SpatialImage(array, spatial_image.voxelsize, vdim=3)
