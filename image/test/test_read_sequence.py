# -*- python -*-
#
#       image: image reading
#
#       Copyright 2006 INRIA - CIRAD - INRA
#
#       File author(s): Eric Moscardi <eric.moscardi@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
"""
Test image : reading
"""

__license__= "Cecill-C"
__revision__ = " $Id:  $ "

from openalea.image.all import read_sequence

def test_read_sequence():
    """
    Test of read_sequence function
    """
    directory = "../share/data/p60-tiff/"
    verbose = False

    # Test of read_sequence with "directory path"
    res = read_sequence(directory, verbose=verbose)
    assert res.shape == (460, 460, 59)
    assert res.resolution == (1,1,1)

    # Test of read_sequence with "voxels_size" parameter
    res = read_sequence(directory, voxels_size=(0.2, 0.2, 1.), verbose=verbose)
    assert res.shape == (460, 460, 59)
    assert res.resolution == (0.2, 0.2, 1.)

    # Test of read_sequence with "number_images" parameter
    res = read_sequence(directory, number_images=10, verbose=verbose)
    assert res.shape == (460, 460, 10)

    # Test of read_sequence with "start" parameter
    res = read_sequence ( directory, start=10, verbose=verbose)
    assert res.shape == (460, 460, 49)

    # Test of read_sequence with "increment" parameter
    res = read_sequence ( directory, increment=2, verbose=verbose)
    assert res.shape == (460, 460, 30)

    res = read_sequence ( directory, increment=3, verbose=verbose)
    assert res.shape == (460, 460, 20)

    # Test of read_sequence with "filename_contains" parameter
    res = read_sequence ( directory, filename_contains="zzzrrr...", verbose=verbose)
    assert res == -1

    # Test of read_sequence with "number_images" and "start" parameters
    res = read_sequence(directory, number_images=10, start=5, verbose=verbose)
    assert res.shape == (460, 460, 10)

    # Test of read_sequence with "number_images" and "increment" parameters
    res = read_sequence(directory, number_images=10, increment=2, verbose=verbose)
    assert res.shape == (460, 460, 10)

    # Test of read_sequence with "number_images", "start" and "increment" parameters
    res = read_sequence(directory, number_images=10, start=5, increment=2, verbose=verbose)
    assert res.shape == (460, 460, 10)
