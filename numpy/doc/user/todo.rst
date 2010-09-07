List of Numpy functionalities available as VisuAlea nodes
#########################################################

Array creation routines
***********************

.. currentmodule:: numpy

Ones and zeros
--------------
.. autosummary::
   :toctree: generated/

   empty
   empty_like
   eye
   identity
   ones
   ones_like
   zeros
   zeros_like

From existing data
------------------
.. autosummary::
   :toctree: generated/

   array
   fromfunction
   loadtxt

.. todo:: asarray, asanyarray, ascontiguousarray, asmatrix, copy, frombuffer, fromfile, fromiter, fromstring

Numerical ranges
----------------
.. autosummary::
   :toctree: generated/

   arange
   linspace
   logspace

.. todo:: meshgrid, mgrid, ogrid

Building matrices
-----------------
.. autosummary::
   :toctree: generated/

   diag
   diagflat
   tri
   tril
   triu
   vander

The Matrix class
----------------
.. autosummary::
   :toctree: generated/

.. todo:: mat, bmat

Mathematical functions
**********************

.. currentmodule:: numpy

Trigonometric functions
-----------------------
.. autosummary::
   :toctree: generated/

   sin
   cos
   tan
   arcsin
   arccos
   arctan
   degrees
   radians
   deg2rad
   rad2deg

.. todo:: arctan2, hypot, unwrap

Hyperbolic functions
--------------------
.. autosummary::
   :toctree: generated/

   sinh
   cosh
   tanh
   arcsinh
   arccosh
   arctanh

Rounding
--------
.. autosummary::
   :toctree: generated/

   rint
   floor
   ceil
   trunc

.. todo:: around, round_, fix

Sums, products, differences
---------------------------
.. autosummary::
   :toctree: generated/

   sum
   cumprod
   cumsum
   diff
   cross

.. todo:: prod, nansum, ediff1d, gradient, trapz

Exponents and logarithms
------------------------
.. autosummary::
   :toctree: generated/

   exp
   expm1
   exp2
   log
   log10

.. todo:: log2, log1p, logaddexp, logaddexp2

Other special functions
-----------------------
.. autosummary::
   :toctree: generated/

.. todo:: i0, sinc

Floating point routines
-----------------------
.. autosummary::
   :toctree: generated/

.. todo:: signbit, copysign, frexp, ldexp

Arithmetic operations
---------------------
.. autosummary::
   :toctree: generated/

   add
   
.. todo:: reciprocal, negative, multiply, divide, power, subtract, true_divide, floor_divide, fmod, mod, modf, remainder

Handling complex numbers
------------------------
.. autosummary::
   :toctree: generated/

.. todo:: angle, real, imag, conj

Miscellaneous
-------------
.. autosummary::
   :toctree: generated/

   convolve
   clip
   sqrt
   square
   absolute
   fabs

.. todo:: sign, maximum, minimum, nan_to_num, real_if_close, interp

Array manipulation routines
***************************

This is the list of nodes available within VisuAlea in the **numpy.manipulation** package.

.. currentmodule:: numpy

Changing array shape
--------------------
.. autosummary::
   :toctree: generated/


   reshape
   ravel
   ndarray.flatten

.. todo:: ndarray.flat

Transpose-like operations
-------------------------

.. autosummary::
   :toctree: generated/

   transpose

.. todo:: rollaxis, swapaxes, ndarray.T

Changing number of dimensions
-----------------------------
.. autosummary::
   :toctree: generated/

.. todo:: atleast_1d, atleast_2d, atleast_3d, broadcast, broadcast_arrays, expand_dims, squeeze

Changing kind of array
----------------------
.. autosummary::
   :toctree: generated/

.. todo:: asarray, asanyarray, asmatrix, asfarray, asfortranarray, asscalar, require

Joining arrays
--------------
.. autosummary::
   :toctree: generated/

   hstack
   vstack

.. todo:: column_stack, concatenate, dstack

Splitting arrays
----------------
.. autosummary::
   :toctree: generated/

.. todo:: array_split, dsplit, hsplit, split, vsplit

Tiling arrays
-------------
.. autosummary::
   :toctree: generated/

.. todo:: tile, repeat

Adding and removing elements
----------------------------
.. autosummary::
   :toctree: generated/

   unique

.. todo:: delete, insert, append, resize, trim_zeros

Rearranging elements
--------------------
.. autosummary::
   :toctree: generated/

   reshape

.. todo:: fliplr, flipud, roll, rot90
