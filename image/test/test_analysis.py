from openalea.image.spatial_image import *
from openalea.image.algo.all import *
from openalea.image.serial.all import *
from numpy import mean, array
from time import time


def show_result(txt,function):
    ctime = time()
    res = function()
    ctime = time() - ctime
    print txt,':',res,'(%f sec.)'%ctime
    return res

def time_result(txt,function):
    ctime = time()
    res = function()
    ctime = time() - ctime
    print txt,'(%f sec.)'%ctime
    return res

def test_on_segmentation():
    im = time_result('Read image',lambda : read_inrimage("segmentation.inr.gz"))
    analysis = SpatialImageAnalysis(im)
    show_result('Nb labels',analysis.nb_labels)
    time_result('Bounding Box',analysis.boundingbox)
    barycenters = time_result('Center of mass',analysis.center_of_mass)
    labels = list(analysis.labels())
    labels.remove(1)
    time_result('Inertia Axis',lambda: analysis.inertia_axis(center_of_mass=barycenters,labels=labels))
    show_result('Mean volume',lambda : mean(analysis.volume()))
    show_result('Neigbbors',lambda: len(analysis.neighbors(range(10,20))))
    show_result('All Neigbbors',lambda: len(analysis.neighbors()))
    show_result('All Wall Surface',lambda: len(analysis.wall_surfaces()))

def test_on_simple_array():
    import numpy as np
    a = np.array([[1, 2, 7, 7, 1, 1],
                  [1, 6, 5, 7, 3, 3],
                  [2, 2, 1, 7, 3, 3],
                  [1, 1, 1, 4, 1, 1]])
    
    from openalea.image.algo.analysis import SpatialImageAnalysis, LIST, DICT
    analysis = SpatialImageAnalysis(a, return_type=LIST)

    res = analysis.neighbors(7)
    assert res == [1, 2, 3, 4, 5]

    res = analysis.neighbors([7,2])
    assert res == { 7: [1, 2, 3, 4, 5], 2: [1, 6, 7] }

    neighbors = analysis.neighbors()
    assert neighbors == { 1: [2, 3, 4, 5, 6, 7], 2: [1, 6, 7], 3: [1, 7], 4: [1, 7], 5: [1, 6, 7], 6: [1, 2, 5], 7: [1, 2, 3, 4, 5] }
    
    assert analysis.boundingbox(7) == (slice(0, 3), slice(2, 4))

    assert analysis.boundingbox([7,2]) == [(slice(0, 3), slice(2, 4)), (slice(0, 3), slice(0, 2))]

    assert analysis.boundingbox() == [(slice(0, 4), slice(0, 6)), 
                                      (slice(0, 3), slice(0, 2)), 
                                      (slice(1, 3), slice(4, 6)), 
                                      (slice(3, 4), slice(3, 4)), 
                                      (slice(1, 2), slice(2, 3)), 
                                      (slice(1, 2), slice(1, 2)), 
                                      (slice(0, 3), slice(2, 4))]

    #~ assert analysis.volume(7) == 4.0
    
    #~ assert analysis.volume([7,2]) == [4.0, 3.0]
    
    #~ assert analysis.volume() == [10.0, 3.0, 4.0, 1.0, 1.0, 1.0, 4.0]
    
    assert np.allclose(analysis.center_of_mass(7),array([.75, 2.75]))
    
    # print analysis.center_of_mass()
    assert np.allclose(analysis.center_of_mass([7,2]),[array([0.75, 2.75]), array([1.3333333333333333, 0.66666666666666663])])
    
    assert np.allclose(analysis.center_of_mass(),[array([1.8, 2.2999999999999998]),
                                         array([4/3., 2/3.]), 
                                         array([1.5, 4.5]), 
                                         array([3.0, 3.0]), 
                                         array([1.0, 2.0]), 
                                         array([1.0, 1.0]), 
                                         array([0.75, 2.75])])
     
    assert analysis.cell_wall_surface(7,2) ==  1
    
    assert analysis.cell_wall_surface(7,[2,5]) == {(2, 7): 1.0, (5, 7): 2.0}

    assert analysis.wall_surfaces({ 1 : [2, 3], 2 : [6] }) == {(1, 2): 5.0, (1, 3): 4.0, (2, 6): 2.0 }

    assert analysis.wall_surfaces() == {(1, 2): 5.0, (1, 3): 4.0, (1, 4): 2.0, (1, 5): 1.0, (1, 6): 1.0, (1, 7): 2.0, (2, 6): 2.0, (2, 7): 1.0, (3, 7): 2, (4, 7): 1, (5, 6): 1.0, (5, 7): 2.0 }
    
    inertia_axis, inertia_norm = analysis.inertia_axis(7)
    assert np.allclose(inertia_axis, [[ 0.9486833 , -0.31622777],[ 0.31622777,  0.9486833]])
    assert np.allclose(inertia_norm,[ 3.,  0.5 ])
    
if __name__ == '__main__':
    test_on_simple_array()
    test_on_segmentation()
    
