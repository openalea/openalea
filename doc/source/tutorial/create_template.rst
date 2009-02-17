.. _create_template:

Create a template for your package documentation
================================================

One drawback with sphinx documenation, which is also an advantage is 
that you have to create reST for each class or module that you want
to document. 

For instance, each module requires a piece of code similar to 

.. code-block:: rest

    .. automodule:: MainClass
       :members: 
       :undoc-members:
       :inherited-members:
       :show-inheritance:

In order to uniformize the documentation between the different packages,
we provide a script that we create a starting set of reST to be completed.

The script is called sphinx_tools, located in openalea/misc directory, and
can be called using such a command:

   python sphinx_tools --verbose --package core --project /home/user/openalea core
