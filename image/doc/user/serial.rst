Serial Package
##############

Reading images
==============

:class:`openalea.serial.imread` reads a grayscale or color image from the file specified by a filename.
Return value is a numpy.array. 

For grayscale images, the return array is MxN. 

For RGB images, the return value is MxNx3. 

For RGBA images the return value is MxNx4.

For LSM or INR images, the return value is MxNxZ.

.. code-block:: python
    :linenos:
    
    from openalea.image import imread
    im = imread("lena.bmp")


