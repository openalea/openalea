Algo Package
###########


:mod:`openalea.image.end_margin` function
=========================================

A end margin is a inside black space that can be added into the end of array object.

Parameters: 

    - `img` ( NxMxP array)
    - `width` (int) - size of the margin
    - `axis` (int optional) - axis along which the margin is added. By default, add in all directions (see also stroke).


.. code-block:: python
    :linenos:
    
    from openalea.image import end_margin
    img = random.random((3,4,5))
    
    out = end_margin(img,1,0)
    assert out.shape == (3,4,5)

    assert (out[2,:,:] == zeros((4,5))).all()
    assert (out[1:2,:,:] == img[1:2,:,:]  ).all()

    out = end_margin(img,1,1)
    assert out.shape == (3,4,5)

    assert (out[:,3,:] == zeros((3,5))).all()
    assert (out[:,1:3,:] == img[:,1:3,:] ).all()

