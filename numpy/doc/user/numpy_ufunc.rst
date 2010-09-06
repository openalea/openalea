Universal functions 
*******************

This is the list of nodes available within VisuAlea in the **numpy.ufunc** package.

Math operations
===============

.. autosummary::

    add
    subtract
    multiply
    divide
    logaddexp
    logaddexp2
    true_divide
    floor_divide
    negative
    power
    remainder
    mod
    fmod
    absolute
    rint
    sign
    conj
    exp
    exp2
    log
    log2
    log10
    expm1
    log1p
    sqrt
    square
    reciprocal
    ones_like


Trigonometric functions
-----------------------
All trigonometric functions use radians when an angle is called for.
The ratio of degrees to radians is :math:`180^{\circ}/\pi.`

.. autosummary::

    sin
    cos
    tan
    arcsin
    arccos
    arctan
    arctan2
    hypot
    sinh
    cosh
    tanh
    arcsinh
    arccosh
    arctanh
    deg2rad
    rad2deg

Bit-twiddling functions
-----------------------

These function all require integer arguments and they manipulate the
bit-pattern of those arguments.

.. autosummary::

    bitwise_and
    bitwise_or
    bitwise_xor
    invert
    left_shift
    right_shift

Comparison functions
--------------------

.. autosummary::

    greater
    greater_equal
    less
    less_equal
    not_equal
    equal

.. warning::

    Do not use the Python keywords ``and`` and ``or`` to combine
    logical array expressions. These keywords will test the truth
    value of the entire array (not element-by-element as you might
    expect). Use the bitwise operators & and \| instead.

.. autosummary::

    logical_and
    logical_or
    logical_xor
    logical_not

.. warning::

    The bit-wise operators & and \| are the proper way to perform
    element-by-element array comparisons. Be sure you understand the
    operator precedence: ``(a > 2) & (a < 5)`` is the proper syntax because
    ``a > 2 & a < 5`` will result in an error due to the fact that ``2 & a``
    is evaluated first.

.. autosummary::

    maximum

.. tip::

    The Python function ``max()`` will find the maximum over a one-dimensional
    array, but it will do so using a slower sequence interface. The reduce
    method of the maximum ufunc is much faster. Also, the ``max()`` method
    will not give answers you might expect for arrays with greater than
    one dimension. The reduce method of minimum also allows you to compute
    a total minimum over an array.

.. autosummary::

    minimum

.. warning::

    the behavior of ``maximum(a, b)`` is different than that of ``max(a, b)``.
    As a ufunc, ``maximum(a, b)`` performs an element-by-element comparison
    of `a` and `b` and chooses each element of the result according to which
    element in the two arrays is larger. In contrast, ``max(a, b)`` treats
    the objects `a` and `b` as a whole, looks at the (total) truth value of
    ``a > b`` and uses it to return either `a` or `b` (as a whole). A similar
    difference exists between ``minimum(a, b)`` and ``min(a, b)``.


Floating functions
------------------

Recall that all of these functions work element-by-element over an
array, returning an array output. The description details only a
single operation.

.. autosummary::

    isreal
    iscomplex
    isfinite
    isinf
    isnan
    signbit
    copysign
    nextafter
    modf
    ldexp
    frexp
    fmod
    floor
    ceil
    trunc

