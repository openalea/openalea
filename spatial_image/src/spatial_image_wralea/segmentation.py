import numpy as np
import scipy
import pylab
from scipy import ndimage


def loadimage(filename):
    data = scipy.misc.pilutil.imread(filename)
    data = np.uint8(data[:,:,0])
    return data
    

def invert(matrix):
    data = 255 - matrix
    return data

def show(data):
    pylab.imshow(data)
    pylab.jet()
    pylab.show()


def set_seeds(markers, n, seeds):

    if seeds:
        for seed in seeds:
            markers [seed[1], seed[0]] = n
            n += 1

    markers = np.int8(markers)
    return markers


def get_seeds(matrix):

    markers = np.zeros(matrix.shape)
    labels, n = ndimage.label(matrix)
    
    for i in xrange(1,n):
        barycenter_label = ndimage.center_of_mass(matrix,labels,i)
        markers [ int(barycenter_label[0]) , int(barycenter_label[1])] = i

    markers = np.int8(markers)
    return markers, n

    
def threshold(matrix,threshold):
    matrix = np.where(matrix < threshold, 0, 255)               
    return matrix

