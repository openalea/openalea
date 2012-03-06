# -*- python -*-
# -*- coding: latin-1 -*-
#
#       image : registration
#
#       Copyright 2006 - 2010 INRIA - CIRAD - INRA
#
#       File author(s): Eric MOSCARDI <eric.moscardi@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
################################################################################

__license__= "Cecill-C"
__revision__=" $Id: $ "

__all__ = ["pts2transfo", "angles2transfo"]


import numpy as np
from math import radians,cos,sin
from scipy.ndimage import center_of_mass

def pts2transfo(x,y):
    """ Infer rigid transformation from control point pairs
        using quaternions.

        The quaternion representation is used to register two point sets with known correspondences.
        It computes the rigid transformation as a solution to a least squares formulation of the problem.

        The rigid transformation, defined by the rotation R and the translation t,
        is optimized by minimizing the following cost function :

            C(R,t) = sum ( |yi - R.xi - t|^2 )

        The optimal translation is given by :

            t_ = y_b - R.x_b

                with x_b and y_b the barycenters of two point sets

        The optimal rotation using quaternions is optimized by minimizing the following cost function :

            C(q) = sum ( |yi'*q - q*xi'|^2 )

                with yi' and xi' converted to barycentric coordinates and identified by quaternions

        With the matrix representations :

            yi'*q - q*xi' = Ai.q

            C(q) = q^T.|sum(A^T.A)|.q = q^T.B.q

                with A = array([ [       0       ,  (xn_i - yn_i) , (xn_j - yn_j)  ,  (xn_k - yn_k) ],
                                 [-(xn_i - yn_i) ,        0       , (-xn_k - yn_k) ,  (xn_j + yn_j) ],
                                 [-(xn_j - yn_j) , -(-xn_k - yn_k),      0         ,  (-xn_i - yn_i)],
                                 [-(xn_k - yn_k) , -(xn_j + yn_j) , -(-xn_i - yn_i),         0      ] ])

        The unit quaternion representing the best rotation is the unit eigenvector
        corresponding to the smallest eigenvalue of the matrix -B :

            v = a, b.i, c.j, d.k

        The orthogonal matrix corresponding to a rotation by the unit quaternion v = a + bi + cj + dk (with |z| = 1) is given by :

            R = array([ [a*a + b*b - c*c - d*d,       2bc - 2ad      ,       2bd + 2ac      ],
                        [      2bc + 2ad      , a*a - b*b + c*c - d*d,       2cd - 2ab      ],
                        [      2bd - 2ac      ,       2cd + 2ab      , a*a - b*b - c*c + d*d] ])


        :Parameters:
         - `x` (list) - list of points
         - `y` (list) - list of points

        :Returns:
            T : array_like (R,t) which correspond to the optimal rotation and translation
                T = | R t |
                    | 0 1 |

                T.shape(4,4)

        :Examples:

        >>> from openalea.image import pts2transfo

        >>> # x and y, two point sets with 7 known correspondences

        >>> x = [[238.*0.200320, 196.*0.200320, 9.],
                 [204.*0.200320, 182.*0.200320, 11.],
                 [180.*0.200320, 214.*0.200320, 12.],
                 [201.*0.200320, 274.*0.200320, 12.],
                 [148.*0.200320, 225.*0.200320, 18.],
                 [248.*0.200320, 252.*0.200320, 8.],
                 [305.*0.200320, 219.*0.200320, 10.]]

        >>> y = [[173.*0.200320, 151.*0.200320, 17.],
                 [147.*0.200320, 179.*0.200320, 16.],
                 [165.*0.200320, 208.*0.200320, 12.],
                 [226.*0.200320, 204.*0.200320, 9.],
                 [170.*0.200320, 254.*0.200320, 10.],
                 [223.*0.200320, 155.*0.200320, 13.],
                 [218.*0.200320, 109.*0.200320, 23.]]

        >>> cp2transfo(x,y)

        array([[  0.40710149,   0.89363883,   0.18888626, -22.0271968 ],
               [ -0.72459862,   0.19007589,   0.66244094,  51.59203463],
               [  0.55608022,  -0.40654742,   0.72490964,  -0.07837002],
               [  0.        ,   0.        ,   0.        ,   1.        ]])

    """
    #compute barycenters
    # nx vectors of dimension kx
    if not isinstance(x,np.ndarray):
        x = np.array(x)
    nx,kx = x.shape
    x_barycenter = x.sum(0)/float(nx)

    # nx vectors of dimension kx
    if not isinstance(y,np.ndarray):
        y = np.array(y)
    ny,ky = y.shape
    y_barycenter = y.sum(0)/float(ny)

    #Check there are the same number of vectors
    assert nx == ny

    #converting to barycentric coordinates
    x = x - x_barycenter
    y = y - y_barycenter

    #Change of basis (y -> x)
    #~ y = y - x_barycenter

    #compute of A = yi*q - q*xi
    #             = array([ [       0       ,  (xn_i - yn_i) , (xn_j - yn_j)  ,  (xn_k - yn_k) ],
    #                       [-(xn_i - yn_i) ,        0       , (-xn_k - yn_k) ,  (xn_j + yn_j) ],
    #                       [-(xn_j - yn_j) , -(-xn_k - yn_k),      0         ,  (-xn_i - yn_i)],
    #                       [-(xn_k - yn_k) , -(xn_j + yn_j) , -(-xn_i - yn_i),         0      ] ])
    #

    A = np.zeros([nx,4,4])

    A[:,0,1] = x[:,0] - y[:,0]
    A[:,0,2] = x[:,1] - y[:,1]
    A[:,0,3] = x[:,2] - y[:,2]

    A[:,1,0] = -A[:,0,1]
    A[:,1,2] = -x[:,2] - y[:,2]
    A[:,1,3] = x[:,1] + y[:,1]

    A[:,2,0] = -A[:,0,2]
    A[:,2,1] = -A[:,1,2]
    A[:,2,3] = -x[:,0] - y[:,0]

    A[:,3,0] = -A[:,0,3]
    A[:,3,1] = -A[:,1,3]
    A[:,3,2] = -A[:,2,3]

    #compute of B = Sum [A^T.A]
    B = np.zeros([nx,4,4])
    At = A.transpose(0,2,1)

    #Maybe there is an another way to do not the "FOR" loop
    for i in xrange(nx):
        B[i] = np.dot(At[i],A[i])

    B = B.sum(0)

    #The solution q minimizes the sum of the squares of the errors : C(R) = q^T.B.q is done by
    #the eigenvector corresponding to the biggest eigenvalue of the matrix -B

    W,V = np.linalg.eig(-B)
    max_ind = np.argmax(W)
    #The orthogonal matrix corresponding to a rotation by the unit quaternion q = a + bi + cj + dk (with |q| = 1) is given by
    #   R = array([ [a*a + b*b - c*c - d*d,       2bc - 2ad      ,       2bd + 2ac],
    #               [      2bc + 2ad      , a*a - b*b + c*c - d*d,       2cd - 2ab],
    #               [      2bd - 2ac      ,       2cd + 2ab      , a*a - b*b - c*c + d*d] ])
    #

    #eigenvector corresponding to the biggest eigenvalue
    v = V[:,max_ind]

    R = np.zeros([3,3])
    R[0,0] = v[0]*v[0] + v[1]*v[1] - v[2]*v[2] - v[3]*v[3]
    R[0,1] = 2*v[1]*v[2] - 2*v[0]*v[3]
    R[0,2] = 2*v[1]*v[3] + 2*v[0]*v[2]

    R[1,0] = 2*v[1]*v[2] + 2*v[0]*v[3]
    R[1,1] = v[0]*v[0] - v[1]*v[1] + v[2]*v[2] - v[3]*v[3]
    R[1,2] = 2*v[2]*v[3] - 2*v[0]*v[1]

    R[2,0] = 2*v[1]*v[3] - 2*v[0]*v[2]
    R[2,1] = 2*v[2]*v[3] + 2*v[0]*v[1]
    R[2,2] = v[0]*v[0] - v[1]*v[1] - v[2]*v[2] + v[3]*v[3]

    #Compute of the matrix (R,t) which correspond to the optimal rotation and translation
    #  M = | R t | = array(4,4)
    #      | 0 1 |
    #

    #compute the optimal translation
    t = y_barycenter - np.dot(R,x_barycenter)

    T = np.zeros([4,4])
    T[0:3,0:3] = R
    T[0:3,3] = t
    T[3,3] = 1.

    return T


def angles2transfo(image1, image2, angleX=0, angleY=0, angleZ=0) :
    """
    Compute transformation matrix between 2 images from the angles in each directions.

    :Parameters:
     - `image1` (|SpatialImage|) -
     - `image2` (|SpatialImage|) -
     - `angleX` (int) - Rotation through angleX (degree)
     - `angleY` (int) - Rotation through angleY (degree)
     - `angleZ` (int) - Rotation through angleZ (degree)

    :Returns:
     - matrix (numpy array) - Transformation matrix
    """
    x = np.array(center_of_mass(image1))
    y = np.array(center_of_mass(image2))

    # Rx rotates the y-axis towards the z-axis
    thetaX = radians(angleX)
    Rx = np.zeros((3,3))
    Rx[0,0] = 1.
    Rx[1,1] = Rx[2,2] = cos(thetaX)
    Rx[1,2] = -sin(thetaX)
    Rx[2,1] = sin(thetaX)

    # Ry rotates the z-axis towards the x-axis
    thetaY = radians(angleY)
    Ry = np.zeros((3,3))
    Ry[0,0] = Ry[2,2] = cos(thetaY)
    Ry[0,2] = sin(thetaY)
    Ry[2,0] = -sin(thetaY)
    Ry[1,1] = 1.

    # Rz rotates the x-axis towards the y-axis
    thetaZ = radians(angleZ)
    Rz = np.zeros((3,3))
    Rz[0,0] = Rz[1,1] = cos(thetaZ)
    Rz[1,0] = sin(thetaZ)
    Rz[0,1] = -sin(thetaZ)
    Rz[2,2] = 1.

    # General rotations
    R = np.dot(np.dot(Rx,Ry),Rz)

    t = y - np.dot(R,x)

    matrix = np.zeros((4,4))
    matrix[0:3,0:3] = R
    matrix[0:3,3] = t
    matrix[2,2] = matrix[3,3] = 1.

    return matrix
