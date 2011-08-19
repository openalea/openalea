# -*- python -*-
# -*- coding: latin-1 -*-
#
#    creation : numpy package
#
#    Copyright 2006 - 2010 INRIA - CIRAD - INRA
#
#    File author(s): Eric MOSCARDI <eric.moscardi@sophia.inria.fr>
#
#    Distributed under the Cecill-C License.
#    See accompanying file LICENSE.txt or copy at
#        http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#    OpenAlea WebSite : http://openalea.gforge.inria.fr
################################################################################


__doc__ = """ openalea.numpy """
__revision__ = " $Id: $ "

from openalea.core import Factory
from openalea.core.interface import *

__name__ = "openalea.numpy.creation"
__alias__ = []

__version__ = '0.0.1'
__license__ = 'CECILL-C'
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'Numpy wrapping and utils module.'
__url__ = 'http://openalea.gforge.inria.fr'

__all__ = []


list_type = ['bool', 'uint8', 'uint16', 'uint32', 'uint64', 'int8', 'int16', 'int32', 'int64', 'float32', 'float64', 'float96', 'complex64', 'complex128', 'complex192']

array = Factory(name= "array",
        description= "Create an array",
        category = "numpy",
        inputs = ( dict(name='object', interface=None),
        dict(name='dtype',
        interface=IEnumStr(list_type),
        value='float64'),
        dict(name='copy', interface= IBool,
        value=True),
        dict(name='order', interface=IEnumStr(['C', 'F', 'A']),
        value='C'),
        dict(name='subok', interface= IBool,
        value=False),
        dict(name='ndmin', interface= IInt,
        value=0),),
        outputs = (dict(name='array', interface=None),),
        nodemodule = "basics",
        nodeclass = "wra_array",
            )

__all__.append("array")

zeros = Factory(name= "zeros",
               description= "Return a new array of given shape and type, filled with zeros",
               category = "numpy",
        inputs = ( dict(name='shape', interface=ITuple),
                dict(name='dtype', interface=IEnumStr(list_type),
                            value='float64'),
            dict(name='order', interface=IEnumStr(['C', 'F']),
                value='C'),),
         outputs = (dict(name='array', interface=None),),
               nodemodule = "numpy",
               nodeclass = "zeros",
            )

__all__.append("zeros")

zeros_like = Factory(name= "zeros_like",
           	     description= "Return an array of zeros with the same shape and type as a given array",
           	     category = "numpy",
		     inputs = ( dict(name='a', interface=None),),
     	             outputs = (dict(name='array', interface=None),),
           	     nodemodule = "numpy",
           	     nodeclass = "zeros_like",
                    )

__all__.append("zeros_like")

ones = Factory(name= "ones",
           	description= "Return a new array of given shape and type, filled with ones",
           	category = "numpy",
		inputs = ( dict(name='shape', interface=ITuple),
     		   dict(name='dtype', interface=IEnumStr(list_type),
                    		value='float64'),
			dict(name='order', interface=IEnumStr(['C', 'F']),
				value='C'),),
     	outputs = (dict(name='array', interface=ISequence),),
           	nodemodule = "numpy",
           	nodeclass = "ones",
            )

__all__.append("ones")

ones_like = Factory(name= "ones_like",
           	     description= "Returns an array of ones with the same shape and type as a given array",
           	     category = "numpy",
		     inputs = ( dict(name='x', interface=None),),
     	             outputs = (dict(name='array', interface=None),),
           	     nodemodule = "numpy",
           	     nodeclass = "ones_like",
                    )

__all__.append("ones_like")

empty = Factory(name= "empty",
           	description= "Return a new array of given shape and type, without initializing entries",
           	category = "numpy",
		inputs = ( dict(name='shape', interface=ISequence),
     		   dict(name='dtype', interface=IEnumStr(list_type),
                    		value='float64'),
			dict(name='order', interface=IEnumStr(['C', 'F']),
				value='C'),),
     	outputs = (dict(name='array', interface=ISequence),),
           	nodemodule = "numpy",
           	nodeclass = "empty",
            )

__all__.append("empty")

empty_like = Factory(name= "empty_like",
           	     description= "Return a new array with the same shape and type as a given array",
           	     category = "numpy",
		     inputs = ( dict(name='a', interface=None),),
     	             outputs = (dict(name='array', interface=None),),
           	     nodemodule = "numpy",
           	     nodeclass = "empty_like",
                    )

__all__.append("empty_like")

arange = Factory(name= "arange",
               description= "Return evenly spaced values within a given interval",
               category = "numpy",
        inputs = ( dict(name='start', interface=IFloat,
                value=0),
                dict(name='stop', interface=IFloat,
                value=0),
                dict(name='step', interface=IFloat,
                value=1),
            dict(name='dtype', interface=IEnumStr(list_type),
                            value='float64'),),
         outputs = (dict(name='array', interface=ISequence),),
               nodemodule = "numpy",
               nodeclass = "arange",
            )

__all__.append("arange")

linspace = Factory(name= "linspace",
           	description= "Return evenly spaced numbers over a specified interval",
           	category = "numpy",
		inputs = ( dict(name='start', interface=IFloat,value=0),
     		           dict(name='stop', interface=IFloat,value=0),
     		           dict(name='num', interface=IFloat,value=50),
     		           dict(name='endpoint', interface=IBool,value=True),
     		           dict(name='retstep', interface=IBool,value=True),),
     	        outputs = (dict(name='samples', interface=None),
                           dict(name='step', interface=IFloat),),
           	nodemodule = "numpy",
           	nodeclass = "linspace",
            )

__all__.append("linspace")

logspace = Factory(name= "logspace",
               description= "Return numbers spaced evenly on a log scale.",
               category = "numpy",
        inputs = ( dict(name='start', interface=IFloat,    value=0),
                dict(name='stop', interface=IFloat,value=4),
                dict(name='num', interface=IFloat,value=5),
                dict(name='endpoint', interface=IBool,value=True),
                dict(name='base', interface=IBool, value=10.0),),
         outputs = (dict(name='samples', interface=ISequence),
                dict(name='step', interface=IFloat),),
               nodemodule = "numpy",
               nodeclass = "logspace",
            )

__all__.append("logspace")



meshgrid = Factory(name="meshgrid",
                authors="Thomas Cokelaer",
                description="Return coordinate matrices from two coordinate vectors.",
                category= "numpy",
                inputs = (dict(name='x', interface=ISequence, value=[]),
                        dict(name='y', interface=ISequence, value=[])),
                outputs = (dict(name='X', interface=ISequence, value=[]),
                        dict(name='Y', interface=ISequence, value=[])),
               nodemodule = "numpy",
               nodeclass = "meshgrid",
                )

__all__.append("meshgrid")





eye = Factory(name= "eye",
               description= "Return a 2-D array with ones on the diagonal and zeros elsewhere",
               category = "numpy",
        inputs = ( dict(name='N', interface=IInt),
                dict(name='M', interface=IInt, value=None),
                dict(name='k', interface=IInt, value=0),
                        dict(name='dtype', interface=IEnumStr(list_type),
                            value='float64'),),
         outputs = (dict(name='array', interface=ISequence),),
               nodemodule = "numpy",
               nodeclass = "eye",
            )

__all__.append("eye")


tri = Factory(name= "tri",
               description= "Construct an array filled with ones at and below the given diagonal",
               category = "numpy",
        inputs = ( dict(name='N', interface=IInt),
                dict(name='M', interface=IInt, value=None),
                dict(name='k', interface=IInt, value=0),
                        dict(name='dtype', interface=IEnumStr(list_type),
                            value='float64'),),
         outputs = (dict(name='array', interface=ISequence),),
               nodemodule = "numpy",
               nodeclass = "tri",
            )

__all__.append("tri")

tril = Factory(name= "tril",
               description= "Lower triangular.     Return a copy of an array with elements above the k-th diagonal zeroed.",
               category = "numpy",
        inputs = ( dict(name='m'),   dict(name='k', interface=IInt, value=0)),
         outputs = (dict(name='array', interface=ISequence),),
               nodemodule = "numpy",
               nodeclass = "tril",
            )

__all__.append("tril")

triu = Factory(name= "triu",
               description= "Upper triangular.  Return a copy of an array with elements below the k-th diagonal zeroed.",
               category = "numpy",
        inputs = ( dict(name='m'),   dict(name='k', interface=IInt, value=0)),
         outputs = (dict(name='array', interface=ISequence),),
               nodemodule = "numpy",
               nodeclass = "triu",
            )

__all__.append("triu")


diag = Factory(name= "diag",
           	description= "Create a two-dimensional array with the flattened input as a diagonal",
           	category = "numpy",
		inputs = ( dict(name='v', interface=None),
     		           dict(name='k', interface=IInt, value=0),),
            	outputs = (dict(name='array', interface=None),),
           	nodemodule = "numpy",
           	nodeclass = "diag",
            )

__all__.append("diag")

diagflat = Factory(name= "diagflat",
           	description= "Extract a diagonal or construct a diagonal array",
           	category = "numpy",
		inputs = ( dict(name='v', interface=None),
     		           dict(name='k', interface=IInt, value=0),),
     	        outputs = (dict(name='array', interface=None),),
           	nodemodule = "numpy",
           	nodeclass = "diagflat",
            )

__all__.append("diagflat")

vander = Factory(name= "vander",
           	description= "Generate a Van der Monde matrix",
           	category = "numpy",
		inputs = ( dict(name='x', interface=ITuple),
     		           dict(name='N', interface=IInt, value=None),),
     	        outputs = (dict(name='array', interface=None),),
           	nodemodule = "numpy",
           	nodeclass = "vander",
            )

__all__.append("vander")

fromfunction = Factory(name= "fromfunction",
           	description= "Construct an array by executing a function over each coordinate",
           	category = "numpy",
		inputs = ( dict(name="func_str", interface=None),
                           dict(name='shape', interface=ITuple),
                           dict(name='dtype', interface=IEnumStr(list_type), value='float64'),),
     	        outputs = (dict(name='array', interface=None),),
           	nodemodule = "basics",
           	nodeclass = "wra_fromfunction",
            )

__all__.append("fromfunction")

identity = Factory(name= "identity",
           	description= "Return the identity array",
           	category = "numpy",
		inputs = ( dict(name='n', interface=IInt),
                           dict(name='dtype', interface=IEnumStr(list_type),value='float64'),),
     	        outputs = (dict(name='array', interface=ISequence),),
           	nodemodule = "numpy",
           	nodeclass = "identity",
                )

__all__.append("identity")

loadtxt = Factory(name = "loadtxt",
    description = "Load data from a text file.",
    category = "numpy",
    inputs = (dict(name='filename', interface= IFileStr),),
    outputs = (dict(name='array', interface= None),),
    nodemodule = "numpy",
    nodeclass = "loadtxt",
)
__all__.append("loadtxt")


axis_rotation = Factory(name= "axis_rotation_matrix",
                        description= "Create a 4x4 matrix that represents a rotation around one axis",
                        category = "numpy",
                        inputs = ( dict(name='axis', interface=IEnumStr(["X", "Y", "Z"]), value="Z"),
                                   dict(name='angle (degree)', interface=IFloat, value=0.0),
                                   dict(name='min_space', interface=ITuple3, value=None),
                                   dict(name='angle (degree)', interface=ITuple3, value=None),),
                                   outputs = (dict(name='rotation_matrix', interface=ISequence),),
                                   nodemodule = "numpy_utils",
                                   nodeclass = "axis_rotation_matrix",
                                   )

__all__.append("axis_rotation")
