.. _template:

.. contents::

template
========

.. module:: template

The :mod:`template` module is aimed at illustrating the usage of 
docstring to create nice and useful documentation of your code.

.. seealso:: `rst_tutorial` and `sphinx_tutorial` 


.. note:: All reST files that are contained within those pages can be 
   visualized by clicking the link1_ link in the sidebar.

The :mod:`template` module contains a three classes :class:`MainClass1`, :class:`MainClass2` amf :class:`MainClass3` that are automatically parsed to provide 
the descriptions that follows. These classes also contain two functions: :func:`function1 <MainClass.function1>` and :func:`function2 <MainClass.function2>`.

The goal of these examples is to show that the HTML output may be equivalent even though the docstrings are different. However, there are small differences abd subtilities that we emphasize here below.

Note also, that you can easily add mathematical expressions and images outside of your python module so that the code remains small and readable.

.. math:: n_{\mathrm{offset}} = \sum_{k=0}^{N-1} s_k n_k

.. math:: 

   s_k^{\mathrm{column}} = \prod_{j=0}^{k-1} d_j , \quad  s_k^{\mathrm{row}} = \prod_{j=k+1}^{N-1} d_j .

.. image:: ../images/wiki_logo_openalea.png

-----

Here below is the resulting HTML code of the python file parsing 

----

Auto documented class (method 1)
--------------------------------

.. autoclass:: MainClass1
   :members: 
   :undoc-members:
   :inherited-members:
   :show-inheritance:

Auto documented class (method 2)
--------------------------------

.. autoclass:: MainClass2
   :members: 
   :undoc-members:
   :inherited-members:
   :show-inheritance:

Auto documented class (method 3)
--------------------------------

.. autoclass:: MainClass3
   :members: 
   :undoc-members:
   :inherited-members:
   :show-inheritance:







template.py source file
-----------------------

.. literalinclude:: template.py
   :linenos:
   :language: python


.. _link1: _sources/tutorial/template.txt
