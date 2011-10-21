from openalea.image.serial.all import read_inrimage,write_inrimage
from openalea.image.spatial_image import SpatialImage,checkerboard,random_vector_field_like
import os
import numpy


def attenuation(x):
    return 1-x


def test_generate_write_read():
    """Tests if a scalar and a vector image are written and read back correctly.
    Can't test if they are compatible with other Inrimage tools here, use ZViewer!"""
    # create a checkerboard that fades to black in depth
    cb = checkerboard(vs=(0.5,0.5,0.2))
    coeffs = attenuation(numpy.linspace(0,1, cb.shape[2])).reshape(1,1,cb.shape[2])
    cb = SpatialImage(cb*coeffs, voxelsize=cb.voxelsize, dtype=cb.dtype)
    f = "test_inri_0.inr.gz"
    write_inrimage(f, cb)
    read_cb = read_inrimage(f)
    numpy.testing.assert_array_equal(cb, read_cb)
    os.remove(f)

    # create a random vector field
    ff = "test_inri_0_tr.inr.gz"
    field = random_vector_field_like(cb, 4.0,20)
    write_inrimage(ff, field)
    read_field = read_inrimage(ff)
    numpy.testing.assert_array_equal(field, read_field)
    os.remove(ff)

def test_read_write_read():
    """Tests if a scalar and a vector image are written and read back correctly.
    Can't test if they are compatible with other Inrimage tools here, use ZViewer!"""

    # load a file, write it and reread it:
    f = "SAM.inr.gz"
    f_p = "SAM_prime.inr.gz"
    read_im = read_inrimage(f)
    write_inrimage(f_p, read_im)
    reread_im = read_inrimage(f_p)
    numpy.testing.assert_array_equal(read_im, reread_im)



