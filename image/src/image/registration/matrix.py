# -*- python -*-
# -*- coding: latin-1 -*-
#
#       vplants.asclepios.matrix
#
#       Copyright 2006 - 2011 INRIA - CIRAD - INRA
#
#       File author(s): Eric MOSCARDI <eric.moscardi@gmail.com>
#                       Daniel BARBEAU <daniel.barbeau@inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#       http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
################################################################################

__license__= "Cecill-C"
__revision__ = " $Id$ "

from ctypes import *

import numpy as np

def compute_rank( mat) :
    """
    Compute the rank of a matrix
    """
    u, s, v = np.linalg.svd(mat)
    rank = np.sum(s > 1e-10)
    return rank


def read_matrix(filename):
    """Reads 4x4 matrices either written by numpy or 
    Baladin matrices"""
    try:
        return np.loadtxt(filename)
    except ValueError:
        txt = ""
        with open(filename) as f:
            txt = f.read()
        if "O8" in txt:
            mat = []
            for l in txt.split("\n"):
                if "(" in l or "O8" in l:
                    continue
                if ")" in l:
                    break
                mat.append( [float(f) for f in l.split()] )
            return np.array(mat)
        else:
            raise Exception("Cannot read %s"%filename)
    
def numpy_4x4_mat_to_c_array( numpy_matrix ) :
    """
    """
    assert numpy_matrix.shape == (4,4)
    mat = c_double * 16
    return mat( *list(numpy_matrix.flatten()) )


def inverse_matrix( numpy_matrix ) :
    """
    """
    assert numpy_matrix.shape == (4,4)
    return np.linalg.inv(numpy_matrix)

def identity(target_res=None, source_res=None):
    mat = np.identity(4)
    if target_res is not None and source_res is not None:
        mat = matrix_real2voxels(mat, target_res, source_res)
    return mat
     
def matrix_voxels2real( matrix, target_res, source_res ) :
    """ Converts a transform matrix (M') expressed in voxel coordinates
    (from space_s to space_t) into a matrix M from space_r to space_r
    where space_s is the voxel space from which M' comes from and space_t
    the one where it will end, and space_r is the real common space.

    :Parameters:
     * matrix : a 4x4 numpy.array.
     * target_res : a 3-uple of unit vectors for the space_t (eg: (1.,2.,1)
     * source_res : a 3-uple of unit vectors for the space_s (eg: (2.,1.,3)

    :Returns:
     * The matrix in "real" coordinates (M mapping space_r to space_r ,
     instead of space_r to space_r).
    """
    assert matrix.shape == (4,4)
    vx_t, vy_t, vz_t = target_res
    vx_s, vy_s, vz_s = source_res

    return np.array( [ [matrix[0,0]* vx_t /vx_s, matrix[0,1]* vx_t /vy_s, matrix[0,2]* vx_t /vz_s, matrix[0,3]* vx_t],
                       [matrix[1,0]* vy_t /vx_s, matrix[1,1]* vy_t /vy_s, matrix[1,2]* vy_t /vz_s, matrix[1,3]* vy_t],
                       [matrix[2,0]* vz_t /vx_s, matrix[2,1]* vz_t /vy_s, matrix[2,2]* vz_t /vz_s, matrix[2,3]* vz_t],
                       [0.,                      0.,                      0.,                                  1.] ] )


def matrix_real2voxels( matrix, target_res, source_res ) :
    """ Converts a transform matrix (M) expressed in real coordinates
    (a transform from space_r to space_r) into a matrix M' from space_1 to space_2
    where space_s is the voxel space from which M comes from and space_t the
    one where it will end, and space_r is the real common space.

    :Parameters:
     * matrix : a 4x4 numpy.array.
     * target_res : a 3-uple of unit vectors for the space_2 (eg: (1.,2.,1)
     * source_res : a 3-uple of unit vectors for the space_1 (eg: (2.,1.,3)

    :Returns:
     * The matrix in "voxel" coordinates (M' mapping space_1 to space_2 ,
     instead of space_r to space_r).
    """
    assert matrix.shape == (4,4)
    # vx_t, vy_t, vz_t = target_res
    # vx_s, vy_s, vz_s = source_res

    # --this is wrong, no time to check why just now --
    # return np.array( [ [matrix[0,0]* vx_s /vx_t, matrix[0,1]* vx_s /vy_t, matrix[0,2]* vx_s /vz_t, matrix[0,3]/ vx_t],
    #                    [matrix[1,0]* vy_s /vx_t, matrix[1,1]* vy_s /vy_t, matrix[1,2]* vy_s /vz_t, matrix[1,3]/ vy_t],
    #                    [matrix[2,0]* vz_s /vx_t, matrix[2,1]* vz_s /vy_t, matrix[2,2]* vz_s /vz_t, matrix[2,3]/ vz_t],
    #                    [0.,                      0.,                      0.,                                  1.] ] )

    res = matrix.copy()
    h_out = np.diag(source_res)
    res[0:3,0:3] = np.dot(res[0:3,0:3],h_out)
    
    size_in = map(lambda x:1./x, target_res)
    h_in = np.diag(size_in)
    res[0:3,:] = np.dot(h_in, res[0:3,:])
    assert (res[3,0:3] == (0,0,0)).all()
    assert res[3,3]   == 1
    return res

