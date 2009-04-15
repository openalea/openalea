Developer Guidelines
####################


.. note:: When committing significant changes or fix bug, please update the Changelog.txt of the package(s) concerned.

Use spaces instead of tabs
==========================

tabs drawbacks
--------------
  * people mix tabs and spaces without knowing it or taking care of it.
  * people may use tabs for spaces (e.g., in strings)

tabs advantages
---------------
  * avoid to type a lot of spaces BUT most of the editors have options to replace the effect of pressing the tab key by the relevant number of spaces.
  * people can dynamically change the indentation.

Sphinx documentation
====================

If you read the previous page, you probably know by now that how to generate the HTML documentation::

    python setup.py build_sphinx 

In fact you could have typed::
    
    python setup.py build_sphinx -b html 

Similarly, you can replace the builder (here, html) by *latex*::

    python setup.py build_sphinx --builder latex  

or *doctest* ::

    python setup.py build_sphinx --builders doctest  

doctest
=======

To be able to parse the examples/test in your docstrings use the following syntax:

.. doctest::

    >>> #any comments and usual python code are accepted
    >>> for i in range(2):
    ...     print i,
    0 1
    >>> def dummy(): a=1
    >>> print dummy  # doctest: +SKIP
    <function dummy at 0x8f40f0c> 

Follow those rules:

  * If you have normal text, use '>>>' and a space.
  * If there is an indentation, you should use the '...'  and a space
  * If a statement returns text on the standard output, it should be there as well and should be exactly what is expected. 
  * You cannot always foreseen the expected output (for instance id of a function), then add the ``#doctest: +SKIP`` string after the statement you do not want to test.
