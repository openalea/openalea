Include test in your docstrings
================================
.. warning:: **in progress**

To be able to parse the examples/test in your docstrings use the following syntax:

.. doctest::

    >>> #any comments and usual python code are accepted
    >>> for i in range(2):
    ...     print i,
    0 1
    >>> def dummy(): a=1
    >>> print dummy  # doctest: +SKIP
    <function dummy at 0x8f40f0c> 

then, in you doc directory type::

    make doctests

Rules to follow
---------------

  * If you have normal text, use '>>>' and a space.
  * If there is an indentation, you should use the '...'  and a space
  * If a statement returns text on the standard output, it should be there as well and should be exactly what is expected. 
  * You cannot always foreseen the expected output (for instance id of a function), then add the ``#doctest: +SKIP`` string after the statement you do not want to test.

