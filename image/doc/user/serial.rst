Serial Package
##############

Reading images
==============

The :func:`imread <openalea.image.serial.basics.imread>` reads a grayscale or color image from the file specified by a filename.
Return value is a |SpatialImage|. All images are returned as 3D images. Images
that are only 2D are upgraded to 3D images (with only one slice). 3D images are returned as SX*SY*SZ images. RGB or RGBA images add
a fourth dimension (of size 3 or 4) to the returned array.

Supported formats are Inrimage (.inr), TIFF (.tif), LSM (.lsm) and more common formats like PNG, JPG, BMP...

The reader tries to retreive voxel sizes data from image files and it is stored in the "resolution" attribute of the returned SpatialImage.

.. code-block:: python
    :linenos:

    from openalea.image.serial.all import imread
    im = imread("lena.bmp")

.. dataflow:: openalea.image.demo imread


Saving images
=============

:func:`openalea.image.serial.basics.imsave` writes exclusively |SpatialImage| instances.
The writer is selected by looking at the extension. The directory where the file is written must exist.


.. code-block:: python
    :linenos:

    from openalea.image.serial.all import imread, imsave
    im = imread("lena.bmp")
    # -- process im as much as you want --
    imsave("lena_2.png", im)

.. dataflow:: openalea.image.demo imsave


