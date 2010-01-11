.. _template:

.. contents::

template
========

.. module:: template

The :mod:`template` module is aimed at illustrating the usage of 
docstring to create nice and useful documentation of your code.

.. warning :: make sure your modules are inside your PYTHONPATH otherwise Sphinx is not able to parse them.


The :mod:`template` module contains a three classes :class:`MainClass1`, :class:`MainClass2` amf :class:`MainClass3` that are automatically parsed to provide 
the descriptions that follows. These classes also contain two functions: :func:`function1 <MainClass1.function1>` and :func:`function2 <MainClass2.function2>`.

The goal of these examples is to show that the HTML output may be equivalent even though the docstrings are different. However, there are small differences abd subtilities that we emphasize here below.



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

Auto documented class (method 4) mix of 1 and 2
------------------------------------------------

.. autoclass:: MainClass4
   :members: 
   :undoc-members:
   :inherited-members:
   :show-inheritance:


.. module:: template_final

.. autoclass:: MainClass1
   :members: 
   :undoc-members:
   :inherited-members:
   :show-inheritance:

.. autoclass:: MainClass2
   :members: 
   :undoc-members:
   :inherited-members:
   :show-inheritance:

.. autoclass:: MainClass3
   :members: 
   :undoc-members:
   :inherited-members:
   :show-inheritance:




.. autoclass:: MainClass4
   :members: 
   :undoc-members:
   :inherited-members:
   :show-inheritance:



template.py source file
-----------------------

.. literalinclude:: template.py
   :linenos:
   :language: python


