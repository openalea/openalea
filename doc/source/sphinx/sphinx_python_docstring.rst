How to document your docstrings
###############################



.. sidebar:: Summary

    :Release: |release|
    :Date: |today|
    :Authors: **Thomas Cokelaer**
    :Target: developers and administrators
    :status: mature


.. topic:: Overview

    This example shows how to document your docstrings and how to interpret it 
    within your reST document.


The docstring
-------------

Let us suppose that you have such a docstring:

.. literalinclude:: docstring.py
    :language: python

Autodocument your module
-------------------------

Then, you can use the **automodule** directive as follows::

    .. automodule:: docstring.py

which gives the following interpretation:

.. automodule:: docstring
