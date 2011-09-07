# -*- python -*-
#
#       image.serial: read/write images
#
#       Copyright 2006 - 2011 INRIA - CIRAD - INRA
#
#       File author(s): Eric Moscardi <eric.moscardi@inria.fr>
#                       Jerome Chopard <jerome.chopard@sophia.inria.fr>
#                       Daniel BARBEAU <daniel.barbeau@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
################################################################################
"""
This module redefine load and save to account for spatial images
"""

__license__= "Cecill-C"
__revision__=" $Id$ "

from os.path import exists, splitext, split as psplit
import Image,ImageOps
import os, fnmatch
#from pylab import imread as _imread, imsave as _imsave
from scipy.misc import imsave as _imsave
from struct import pack,unpack,calcsize
from pickle import dumps,loads
import numpy as np
from inrimage import *
from lsm import *
from tif import *
from openalea.image.spatial_image import SpatialImage

__all__ = ["save", "load", "read_sequence", "imread", "imsave", "lazy_image_or_path"]

def save (filename, img, is_vectorial=False) :
    """Save an array to a binary file in numpy format with a SpatialImage header.

    .. warning::

      There is no way to distinguish a 2D RGB[A] image from a 3D scalar image.
      If img is a 2D RGB[A] image, make sure its shape is similar to (SX,SY,1,3) for RGB or
      (SX,SY,1,4) for RGBA.

    :Parameters:
     - `filename` (file or str) - Filename to which the data is saved.
                                  If the filename does not already have a ".npy"
                                  extension, it is added.
     - `img` (array)
     - `is_vectorial` (bool) - specifically deal with img as if it was
        a 2D vectorial (RGB[A]) image so that it saves it as a 3D RGBA image
        and conforms to the contract.
    """
    if isinstance(filename,str) :
        if filename.endswith(".npy") :
            file_ = open(filename,'wb')
        else :
            file_ = open("%s.npy" % filename,'wb')
    file_.write("SpatialImage")


    lenShape = len(img.shape)
    if isinstance(img,SpatialImage) :
        resolution = img.resolution
        info       = img.info
    elif isinstance(img, np.ndarray):
        resolution = (1.,)*lenShape
        info       = {}

    # if the data is of shape 2 then
    # we can be sure it is a scalar 2D image
    # and we can reshape to a 3D scalar image.
    if lenShape==2:
        print "openalea.image.serial.basics.save: assuming 2D scalar image"
        img = img.reshape(img.shape+(1,))
        if len(resolution) == 2:
            resolution += (1.,)
    elif lenShape == 3 and not is_vectorial:
        print "openalea.image.serial.basics.save: assuming 3D scalar image"
    elif lenShape == 3 and  is_vectorial:
        print "openalea.image.serial.basics.save: interpreting as 2D scalar RGB[A] image"
        img = img.reshape( img.shape[:2] + (1, img.shape[2]) )
        if len(resolution) == 2:
            resolution += (1.,)
    elif lenShape == 4 and not is_vectorial:
        print "openalea.image.serial.basics.save: assuming 3D RGB[A] image"
    else:
        raise IOError("Unable to identify image shape and encoding")

    header = dumps( (resolution, info) )
    file_.write(pack('i',len(header) ) )
    file_.write(header)
    np.save(file_,img)


def load (file, mmap_mode=None, is_vectorial=False) :
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
     - `is_vectorial` (bool) - specifically deal with file as if it was
        a 2D vectorial (RGB[A]) image so that it returns a 3D RGBA image
        and conforms to the contract.
    :Returns Type: SpatialImage
    """
    if isinstance(file,str) :
        file = open(file,'rb')

    header = file.read(12)

    if header == "SpatialImage" :
        nb, = unpack('i',file.read(calcsize('i') ) )
        res,info = loads(file.read(nb) )
        data = np.load(file,mmap_mode)

        # if the read data is of shape 2 then
        # we can be sure it is a scalar 2D image
        # and we can reshape to a 3D scalar image.
        if len(data.shape) == 2:
            print "openalea.image.serial.basics.load: assuming 2D scalar image"
            data = data.reshape(data.shape+(1,))
            if len(res) == 2:
                res += (1.,)
        elif len(data.shape) == 3 and not is_vectorial:
            print "openalea.image.serial.basics.load: assuming 3D scalar image"
        elif len(data.shape) == 3 and  is_vectorial:
            print "openalea.image.serial.basics.load: interpreting as 2D scalar RGB[A] image"
            data = data.reshape( data.shape[:2] + (1, data.shape[2]) )
            if len(res) == 2:
                res += (1.,)
        elif len(data.shape) == 4 and not is_vectorial:
            print "openalea.image.serial.basics.load: assuming 3D RGB[A] image"
        else:
            raise IOError("Unable to identify image shape and encoding")

        if len(res) == len(data.shape) :
            vdim = 1
        else :
            vdim = data.shape[-1]

        return SpatialImage(data,res,vdim,info)
    else :
        file.seek(0)
        return SpatialImage(np.load(file,mmap_mode))

##################################################
# TODO : Read voxels size in xlm file if provided #
##################################################
def read_sequence ( directory, grayscale=True, number_images=None, start=0, increment=1, filename_contains="", voxels_size=None, verbose=True) :
    """
    Convert a sequence of images in a folder as a numpy array.
    The images must all be the same size and type.
    They can be in TIFF, .... format.

    :Parameters:
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
    """Reads an image file completely into memory.

    It uses the file extension to determine how to read the file. It first tries
    some specific readers for volume images (Inrimages, TIFFs, LSMs, NPY) or falls
    back on PIL readers for common formats if installed.

    In all cases the returned image is 3D (2D is upgraded to single slice 3D).
    If it has colour or is a vector field it is even 4D.

    :Parameters:
     - `filename` (str)

    :Returns Type:
        `openalea.image.all.SpatialImage`
    """
    if not exists(filename) :
        raise IOError("The requested file do not exist: %s" % filename)

    root, ext = splitext(filename)
    ext = ext.lower()
    if ext == ".gz":
        root, ext = splitext(root)
        ext = ext.lower()
    if ext == ".inr":
        return read_inrimage(filename)
    elif ext == ".lsm":
        return read_lsm(filename)
    elif ext in [".tif", ".tiff"]:
        return read_tif(filename)
    elif ext in [".npz", ".npy"]:
        return load(filename)
    else:
        # -- We use the normal numpy reader. It returns 2D images.
        # If len(shape) == 2 : scalar image.
        # If len(shape) == 3 and shape[2] == 3 : rgb image
        # If len(shape) == 3 and shape[3] == 4 : rgba image.
        # Return a SpatialImage please! --

        # Use the array protocol to convert a PIL image to an array.
        # Don't use pylab'es PIL_to_array conversion as it flips images vertically.
        im_array = np.array(Image.open(filename))
        shape    = im_array.shape
        if len(shape)==2:
            newShape = (shape[0], shape[1], 1, 1)
        elif len(shape) == 3:
            newShape = (shape[0], shape[1], 1, shape[2])
        else:
            raise IOError("unhandled image shape : %s, %s"%(filename, str(shape)))
        #newarr   = np.zeros(newShape, dtype=im_array.dtype, order="C")
        #newarr[:,:,0] = im_array[:,:]
        vdim     = 1 if( len(shape) < 3 ) else shape[2]
        return SpatialImage(im_array[..., np.newaxis], None, vdim)

def imsave(filename, img):
    """Save a `openalea.image.all.SpatialImage` to filename.

    .. note: `img` **must** be a SpatialImage.

    The filewriter is choosen according to the file extension. However all file extensions
    will not match the data held by img, in dimensionnality or encoding, and might raise `IOError`s.

    For real volume data, Inrimage and NPY are currently supported.
    For SpatialImages that are actually 2D, PNG, BMP, JPG among others are supported if PIL is installed.

    :Parameters:
     - `filename` (str)
     - `img` (openalea.image.all.SpatialImage)
    """

    assert isinstance(img, SpatialImage)
    # -- images are always at least 3D! If the size of dimension 3 (indexed 2) is 1, then it is actually
    # a 2D image. If it is 4D it has vectorial or RGB[A] data. --

    head, tail = psplit(filename)
    head = head or "."
    if not exists(head):
        raise IOError("The directory do not exist: %s" % head)

    root, ext = splitext(filename)

    is2D = img.shape[2] == 1
    ext = ext.lower()
    if ext == ".gz":
        root, ext = splitext(root)
        ext = ext.lower()
    if ext == ".inr":
        write_inrimage(filename, img)
    elif ext in [".npz", ".npy"]:
        save(filename, img)
    elif ext in [".tiff", ".tif"]:
        write_tif(filename, img)
    else:
        if not is2D:
            raise IOError("No writer found for format of 3D image %s"%filename)
        else:
            # -- fallback on Pylab.
            # WARNING: Careful, this can fail in many ways still!
            # For example, many formats wont support writing scalar floats, or
            # vector floats, or encodings different from uchar8 --
            if len(img.shape) == 4: # RGB[A] images
                _imsave(filename,img[:,:,0,:])
            elif len(img.shape) == 3: #scalar images
                _imsave(filename, img[:,:,0])
            else:
                raise IOError("Unhandled image shape %s"%str(img.shape))

###################
# UTILITY METHODS #
###################

def lazy_image_or_path(image):
    """ Takes an image or a path to an image and returns the image.

    Extensively used in other functions to make them accept images given as paths.
    If `image` is already a SpatialImage this method is a pass-thru. If it looks
    like a path, it will load the image at that path and return it.

    :Parameters:
     -`image` (openalea.image.spatial_image.SpatialImage, str) - [Path] or image.

    :Returns:
     - image or imread(image)

    :Returns Type:
        `openalea.image.all.SpatialImage`
    """
    wp = False
    if isinstance(image, (str, unicode)):
        image = imread(image)
        wp = True
    else:
        assert isinstance(image, SpatialImage)
    return image, wp
