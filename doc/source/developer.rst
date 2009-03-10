Developer Guidelines
####################


bookeeping for the releases
===========================

* When committing significant changes or fix bug, please update the Changelog.txt of the package(s) concerned.

Sphinx documentation
====================

html
----
Generally speaking, go to the package directory and type::

    python setup.py build_sphinx

latex
-----

Add an option::
    
    python setup.py build_sphinx --builders latex


test
----

You can include small test in your docstring must they should be validated using::
    
    python setup.py build_sphinx --builders doctest

To be able to parse the examples/test in your docstrings use the following syntax::

.. doctest::

    >>> # any comments and usual python code are accepted
    >>> for i in range(2)
    ...     print i,
    0,1
    >>> def dummy(): a=1
    >>> print dummy
    <function dummy at 0x8f40f0c> #doctest: +SKIP

Follow those rules:

  * If you have normal text, use '>>>' and a space.
  * If ithere is an indentation, you should use the '...'  and a space
  * If a statement returns text on the standard output, it should be there as well and should be exactly what is expected. 
  * You cannot always foreseen the expected output (for instance id of a function), then add the ``#doctest: +SKIP`` string after the statement you do not want to test.
