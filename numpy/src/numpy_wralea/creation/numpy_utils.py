




import math
import numpy

I = numpy.linalg.inv
D = numpy.dot

def axis_rotation_matrix(axis, angle, min_space=None, max_space=None):
    if axis not in ["X", "Y", "Z"]:
        raise Exception("Unknown axis : "+ str(axis))
    rads = math.radians(angle)
    s = math.sin(rads)
    c = math.cos(rads)

    centering = numpy.identity(4)
    if min_space is None and max_space is not None:
        min_space = numpy.array([0.,0.,0.])

    if max_space is not None:
        space_center = (max_space-min_space)/2.
        offset = -1.*space_center
        centering[:3,3] = offset

    rot = numpy.identity(4)
    if axis=="X":
        rot = numpy.array([ [1., 0., 0., 0.],
                            [0., c, -s,  0.],
                            [0., s,  c,  0.],
                            [0., 0., 0., 1.] ])
    elif axis=="Y":
        rot = numpy.array([ [c,   0., s,  0.],
                            [0.,  1., 0., 0.],
                            [-s,  0., c,  0.],
                            [0.,  0., 0., 1.] ])

    elif axis=="Z":
        rot = numpy.array([ [c, -s,  0., 0.],
                            [s,  c,  0., 0.],
                            [0., 0., 1., 0.],
                            [0., 0., 0., 1.] ])

    return D(I(centering), D(rot, centering))


if __name__=="__main__":
    print axis_rotation_matrix("Z", 90., max_space=(145, 50, 40))

