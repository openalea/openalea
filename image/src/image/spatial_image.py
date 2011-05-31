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
This module create the main SpatialImage object
"""

__license__= "Cecill-C"
__revision__=" $Id: $ "

import numpy as np

class SpatialImage (np.ndarray) :
	"""Associate meta data to np.ndarray
	"""
	def __new__ (cls, input_array, resolution = None,
	                               vdim = 1,
	                               info = None) :
		"""Instantiate a new SpatialImage

		if resolution is None, vdim will be used to infer space size and affect
		a resolution of 1 in each direction of space

		:Parameters:
		 - `cls` - internal python
		 - `input_array` (array) - data to put in the image
		 - `resolution` (tuple of float) - spatial extension in each direction
		                                   of space
		 - `vdim` (int) - size of data if vector data are used
		 - `info` (dict of str|any) - metainfo
		"""
		#initialize datas
                if input_array.flags.f_contiguous :
                        obj = np.asarray(input_array).view(cls)
		else :
                        obj = np.asarray(input_array,order='F').view(cls)

		#assert resolution
		if resolution is None :
			if vdim == 1 :
				resolution = (1.,) * len(obj.shape)
			else :
				resolution = (1.,) * (len(obj.shape) - 1)
		else :
			if vdim == 1 :
				if len(resolution) != len(obj.shape) :
					raise ValueError("data dimension and resolution mismatch")
			else :
				if len(resolution) != (len(obj.shape) - 1) :
					raise ValueError("data dimension and resolution mismatch")

		obj.resolution = tuple(resolution)

		#set metadata
		if info is None :
			obj.info = {}
		else :
			obj.info = dict(info)

		#return
		return obj

	def __array_finalize__ (self, obj) :
		if obj is None :
			return

		#assert resolution
		res = getattr(obj, 'resolution', None)
		if res is None :#assert vdim == 1
			res = (1.,) * len(obj.shape)

		self.resolution = tuple(res)

		#metadata
		self.info = dict(getattr(obj, 'info', {}) )

	def clone (self, data) :
		"""Clone the current image metadata
		on the given data.

		.. warning:: vdim is defined according to self.resolution and data.shape

		:Parameters:
		 - `data` - (array)

		:Returns Type: SpatialImage
		"""
		if len(data.shape) == len(self.resolution) :
			vdim = 1
		elif len(data.shape) - len(self.resolution) == 1 :
			vdim =data.shape[-1]
		else :
			raise UserWarning("unable to handle such data dimension")

		return SpatialImage(data,self.resolution,vdim,self.info)





def null_vector_field_like(spatial_image):
	array = np.zeros( list(spatial_image.shape)+[3], dtype=np.float32 )
	return SpatialImage(array, spatial_image.resolution, vdim=3)
