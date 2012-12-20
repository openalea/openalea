# -*- python -*-
#
#       image.serial: read tif
#
#       Copyright 2011 INRIA - CIRAD - INRA
#
#       File author(s): Christophe Pradal <christophe.pradal@cirad.fr>
#                       Daniel Barbeau    <daniel.barbeau@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
################################################################################
"""
This module reads 3D tiff format
"""

from __future__ import division

__license__ = "Cecill-C"
__revision__ = " $Id$ "

import numpy as np
from openalea.image.spatial_image import SpatialImage


__all__ = []

try:
    import decimal
    import libtiff
    from libtiff import TIFFfile
    from libtiff.tiff_image import TIFFimage, TIFFentry
    from libtiff import tif_lzw
    from libtiff.utils import bytes2str, VERBOSE
    import os, os.path, sys, time
    __all__ += ["read_tif", "write_tif","mantissa"]
except ImportError, e :
    pass

def read_tif(filename,channel=0):
    """Read a tif image

    :Parameters:
    - `filename` (str) - name of the file to read
    """

    # TIF reader
    tif = libtiff.TIFF.open(filename)
    
    if tif.GetField('ImageDescription'):
        tif = TIFFfile(filename)
        arr = tif.get_tiff_array()
        _data = arr[:].T
        info_str = tif.get_info()
    else:
        i = 1
        while not tif.LastDirectory():
            i+=1
            tif.ReadDirectory()
        tif.SetDirectory(0)
        _data = np.zeros((i,)+tif.read_image().shape,dtype=tif.read_image().dtype)
        for ii,i in enumerate(tif.iter_images()):
            _data[ii] = i
        _data = _data.transpose(2, 1, 0)
        info_str = tif.info()

    nx, ny, nz = _data.shape

    # -- prepare metadata dictionnary --
    
    info_dict = dict( filter( lambda x: len(x)==2,
                              (inf.split(':') for inf in info_str.split("\n"))
                              ) )
    for k,v in info_dict.iteritems():
        info_dict[k] = v.strip()

    print info_dict

    # -- getting the voxelsizes from the tiff image: sometimes
    # there is a BoundingBox attribute, sometimes there are
    # XResolution, YResolution, ZResolution or spacing.
    # the object returned by get_tiff_array has a "get_voxel_sizes()"
    # method but it fails, so here we go. --
    if "BoundingBox" in info_dict:
        bbox = info_dict["BoundingBox"]
        xm, xM, ym, yM, zm, zM = map(float,bbox.split())
        _vx = (xM-xm)/nx
        _vy = (yM-ym)/ny
        _vz = (zM-zm)/nz
    else:
        # -- When we have [XYZ]Resolution fields, it describes the
        # number of voxels per real unit. In SpatialImage we want the
        # voxelsizes, which is the number of real units per voxels.
        # So we must invert the result. --
        if "XResolution" in info_dict:
            # --resolution is stored in a [(values, precision)] list-of-one-tuple, or
            # sometimes as a single number --
            xres_str = eval(info_dict["XResolution"])
            if isinstance(xres_str, list) and isinstance(xres_str[0], tuple):
                xres_str = xres_str[0]
                _vx = float(xres_str[0])/xres_str[1]
            elif isinstance(xres_str, (int, float)):
                _vx = float(xres_str)
            else:
                _vx = 1.
            _vx = 1./_vx if _vx != 0 else 1.
        else:
            _vx = 1.0 # dumb fallback, maybe we will find something smarter later on
        if "YResolution" in info_dict:
            # --resolution is stored in a [(values, precision)] list-of-one-tuple, or
            # sometimes as a single number --
            yres_str = eval(info_dict["YResolution"])
            if isinstance(yres_str, list) and isinstance(yres_str[0], tuple):
                yres_str = yres_str[0]
                _vy = float(yres_str[0])/yres_str[1]
            elif isinstance(yres_str, (int, float)):
                _vy = float(yres_str)
            else:
                _vy = 1.
            _vy = 1./_vy if _vy != 0 else 1.
        else:
            _vy = 1.0 # dumb fallback, maybe we will find something smarter later on

        if "ZResolution" in info_dict:
            # --resolution is stored in a [(values, precision)] list-of-one-tuple, or
            # sometimes as a single number --
            zres_str = eval(info_dict["ZResolution"])
            if isinstance(zres_str, list) and isinstance(zres_str[0], tuple):
                zres_str = zres_str[0]
                _vz = float(zres_str[0])/zres_str[1]
            elif isinstance(zres_str, (int, float)):
                _vz = float(zres_str)
            else:
                _vz = 1.
            _vz = 1./_vz if _vz != 0 else 1.
        else:
            if "spacing" in info_dict:
                _vz = eval(info_dict["spacing"])
            else:
                _vz = 1.0 # dumb fallback, maybe we will find something smarter later on

    tif.close()
    # -- dtypes are not really stored in a compatible way (">u2" instead of uint16)
    # but we can convert those --
    dt = np.dtype(_data.dtype.name)
    # -- Return a SpatialImage please! --
    im = SpatialImage(_data, dtype=dt)
    im.resolution = _vx,_vy,_vz

    return im


def mantissa(value):
    """Convert value to [number, divisor] where divisor is power of 10"""
    # -- surely not the nicest thing around --
    d = decimal.Decimal(str(value)) # -- lovely...
    sign, digits, exp = d.as_tuple()
    n_digits = len(digits)
    dividend = int(sum( v*(10**(n_digits-1-i)) for i, v in enumerate(digits) ) * \
                        (1 if sign == 0 else -1))
    divisor  = int(10**-exp)
    return dividend, divisor


def write_tif(filename, obj):
    if len(obj.shape) > 3:
        raise IOError("Vectorial images are currently unsupported by tif writer")

    obj = obj.T
    image = TIFFimage(obj)
    vsx, vsy, vsz = obj.resolution

    extra_info = {"XResolution": vsx,
                  "YResolution": vsy,
                  #"ZResolution": str(vsz), # : no way to save the spacing (no specific tag)
                  }
    print extra_info
    return pylibtiff_write_file(image, filename, info=extra_info)
    #return image.write_file(filename, compression='lzw')


def pylibtiff_write_file(tif, filename, compression="none",
                         strip_size = 2**13, planar_config = 1,
                         validate = False, verbose = None,
                         info = {}):
    """Write image data to TIFF file.

    This function is actually a reimplementation of pylibtiff.tiff_image.TIFFImage.write_image
    so that I can pass extra header information. Thanks to the pylibtiff developers.

    Parameters
    ----------
    filename : str
    compression : {'none', 'lzw'}
    strip_size : int
    Specify the size of uncompressed strip.
    validate : bool
    When True then check compression by decompression.
    verbose : {bool, None}
    When True then write progress information to stdout. When None
    then verbose is assumed for data that has size over 1MB.

    Returns
    -------
    compression : float
    Compression factor.
    """
    if verbose is None:
        nbytes = tif.depth*tif.length*tif.width*tif.dtype.itemsize
        verbose = nbytes >= 1024**2

        if os.path.splitext (filename)[1].lower () not in ['.tif', '.tiff']:
            filename = filename + '.tif'

        if verbose:
            sys.stdout.write('Writing TIFF records to %s\n' % (filename))
            sys.stdout.flush()

        compression_map = dict(packbits=32773, none=1, lzw=5, jpeg=6, ccitt1d=2,
                               group3fax = 3, group4fax = 4
                               )
        compress_map = dict(none=lambda data: data,
                            lzw = tif_lzw.encode)
        decompress_map = dict(none=lambda data, bytes: data,
                              lzw = tif_lzw.decode)
        compress = compress_map.get(compression or 'none', None)
        if compress is None:
            raise NotImplementedError (`compression`)
        decompress = decompress_map.get(compression or 'none', None)
        # compute tif file size and create image file directories data
        image_directories = []
        total_size = 8
        data_size = 0
        image_data_size = 0
        for i,image in enumerate(tif.data):
            if verbose:
                sys.stdout.write('\r  creating records: %5s%% done  ' % (int(100.0*i/len(tif.data))))
                sys.stdout.flush ()
            if image.dtype.kind=='V' and len(image.dtype.names)==3: # RGB image
                sample_format = dict(u=1,i=2,f=3,c=6).get(image.dtype.fields[image.dtype.names[0]][0].kind)
                bits_per_sample = [image.dtype.fields[f][0].itemsize*8 for f in image.dtype.names]
                samples_per_pixel = 3
                photometric_interpretation = 2
            else: # gray scale image
                sample_format = dict(u=1,i=2,f=3,c=6).get(image.dtype.kind)
                bits_per_sample = image.dtype.itemsize * 8
                samples_per_pixel = 1
                photometric_interpretation = 1
            if sample_format is None:
                print 'Warning(TIFFimage.write_file): unknown data kind %r, mapping to void' % (image.dtype.kind)
                sample_format = 4
            length, width = image.shape
            bytes_per_row = width * image.dtype.itemsize
            rows_per_strip = min(length, int(np.ceil(strip_size / bytes_per_row)))
            strips_per_image = int(np.floor((length + rows_per_strip - 1) / rows_per_strip))
            assert bytes_per_row * rows_per_strip * strips_per_image >= image.nbytes
            d = dict(ImageWidth=width,
                     ImageLength=length,
                     Compression=compression_map.get(compression, 1),
                     PhotometricInterpretation=photometric_interpretation,
                     PlanarConfiguration=planar_config,
                     Orientation=1,
                     ResolutionUnit = 1,
                     XResolution = 1,
                     YResolution = 1,
                     SamplesPerPixel = samples_per_pixel,
                     RowsPerStrip = rows_per_strip,
                     BitsPerSample = bits_per_sample,
                     SampleFormat = sample_format,
                     )
            d.update(info)
            if i==0:
                d.update(dict(
                        ImageDescription = tif.description,
                        Software = 'http://code.google.com/p/pylibtiff/'))

            entries = []
            for tagname, value in d.items ():
                entry = TIFFentry(tagname)
                entry.add_value(value)
                entries.append(entry)
                total_size += 12 + entry.nbytes
                data_size  += entry.nbytes

            strip_byte_counts = TIFFentry('StripByteCounts')
            strip_offsets = TIFFentry('StripOffsets')
            entries.append(strip_byte_counts)
            entries.append(strip_offsets)
            # strip_offsets and strip_byte_counts will be filled in the next loop
            if strips_per_image==1:
                assert strip_byte_counts.type_nbytes <= 4
                assert strip_offsets.type_nbytes <= 4
                total_size += 2*12
            else:
                total_size += 2*12 + strips_per_image*(strip_byte_counts.type_nbytes + strip_offsets.type_nbytes)
                data_size += strips_per_image * (strip_byte_counts.type_nbytes + strip_offsets.type_nbytes)

            # image data:
            total_size += image.nbytes
            data_size += image.nbytes
            image_data_size += image.nbytes

            # records for nof IFD entries and offset to the next IFD:
            total_size += 2 + 4

            # entries must be sorted by tag number
            entries.sort(cmp=lambda x,y: cmp(x.tag, y.tag))

            strip_info = strip_offsets, strip_byte_counts, strips_per_image, rows_per_strip, bytes_per_row
            image_directories.append((entries, strip_info, image))

        tif = np.memmap(filename, dtype=np.ubyte, mode='w+', shape=(total_size,))
        def tif_write(tif, offset, data, tifs=[]):
            end = offset + data.nbytes
            if end > tif.size:
                size_incr = int((end - tif.size)/1024**2 + 1)*1024**2
                new_size = tif.size + size_incr
                assert end <= new_size, `end, tif.size, size_incr, new_size`
                #sys.stdout.write('resizing: %s -> %s\n' % (tif.size, new_size))
                #tif.resize(end, refcheck=False)
                tif._mmap.resize(new_size)
                new_tif = np.ndarray.__new__(np.memmap, (tif._mmap.size(), ),
                                                dtype = tif.dtype, buffer=tif._mmap)
                new_tif._parent = tif
                new_tif.__array_finalize__(tif)
                tif = new_tif
            tif[offset:end] = data
            return tif
        # write TIFF header
        tif[:2].view(dtype=np.uint16)[0] = 0x4949 # low-endian
        tif[2:4].view (dtype=np.uint16)[0] = 42   # magic number
        tif[4:8].view (dtype=np.uint32)[0] = 8    # offset to the first IFD

        offset = 8
        data_offset = total_size - data_size
        image_data_offset = total_size - image_data_size
        first_data_offset = data_offset
        first_image_data_offset = image_data_offset
        start_time = time.time ()
        compressed_data_size = 0
        for i, (entries, strip_info, image) in enumerate(image_directories):
            strip_offsets, strip_byte_counts, strips_per_image, rows_per_strip, bytes_per_row = strip_info

            # write the nof IFD entries
            tif[offset:offset+2].view(dtype=np.uint16)[0] = len(entries)
            offset += 2
            assert offset <= first_data_offset,`offset, first_data_offset`

            # write image data
            data = image.view(dtype=np.ubyte).reshape((image.nbytes,))

            for j in range(strips_per_image):
                c = rows_per_strip * bytes_per_row
                k = j * c
                c -= max((j+1) * c - image.nbytes, 0)
                assert c>0,`c`
                orig_strip = data[k:k+c]
                strip = compress(orig_strip)
                if validate:
                    test_strip = decompress(strip, orig_strip.nbytes)
                    if (orig_strip!=test_strip).any():
                        raise RuntimeError('Compressed data is corrupted: cannot recover original data')
                compressed_data_size += strip.nbytes
                #print strip.size, strip.nbytes, strip.shape, tif[image_data_offset:image_data_offset+strip.nbytes].shape
                strip_offsets.add_value(image_data_offset)
                strip_byte_counts.add_value(strip.nbytes)

                tif = tif_write(tif, image_data_offset, strip)
                image_data_offset += strip.nbytes
                if j==0:
                    first = strip_offsets[0]
                last = strip_offsets[-1] + strip_byte_counts[-1]


            # write IFD entries
            for entry in entries:
                data_size = entry.nbytes
                if data_size:
                    entry.set_offset(data_offset)
                    assert data_offset+data_size <= total_size, `data_offset+data_size,total_size`
                    r = entry.toarray(tif[data_offset:data_offset + data_size])
                    assert r.nbytes==data_size
                    data_offset += data_size
                    assert data_offset <= first_image_data_offset,`data_offset, first_image_data_offset, i`
                tif[offset:offset+12] = entry.record
                offset += 12
                assert offset <= first_data_offset,`offset, first_data_offset, i`

            # write offset to the next IFD
            tif[offset:offset+4].view(dtype=np.uint32)[0] = offset + 4
            offset += 4
            assert offset <= first_data_offset,`offset, first_data_offset`

            if verbose:
                sys.stdout.write('\r  filling records: %5s%% done (%s/s)%s' \
                                     % (int(100.0*(i+1)/len(image_directories)),
                                        bytes2str(int((image_data_offset-first_image_data_offset)/(time.time ()-start_time))),
                                        ' '*2))
                if (i+1)==len (image_directories):
                    sys.stdout.write ('\n')
                sys.stdout.flush ()


        # last offset must be 0
        tif[offset-4:offset].view(dtype=np.uint32)[0] = 0

        compression = 1/(compressed_data_size/image_data_size)

        if compressed_data_size != image_data_size:
            sdiff = image_data_size - compressed_data_size
            total_size -= sdiff
            tif._mmap.resize(total_size)
            if verbose:
                sys.stdout.write('  resized records: %s -> %s (compression: %.2fx)\n' \
                                     % (bytes2str(total_size + sdiff), bytes2str(total_size),
                                        compression))
                sys.stdout.flush ()
        del tif # flushing
        return compression



