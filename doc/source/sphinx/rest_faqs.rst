Sphinx and resT faqs
======================


The link do not appear correctly when using :class: directive
-------------------------------------------------------------


For simplcity, let us consider the case of the function `openalea.stat_too.output.Display`.

The first reason may be that you are using :class: whereas you should use :func:  or another directive.

The second reason is that within all your reST files, you have not defined the module openalea.stat_tool.output: Another reason is that you defined it with the wrong namespace. For instance vplants.stat_tool.output and later on you try to refer to openalea.stat_tool.output.



.. _how_to_create_an_internal_reference:

how to create an internal reference
-----------------------------------

First, you need to create a label in the text wherever you want the reference to jump to. Here, we place such a label just before the title (see source file) using this syntax::

    .. _how_to_create_an_internal_reference:


Then, use the :ref: keyword and reference name as follows::

    :ref:`how_to_create_an_internal_reference`


So, in the text, it will simply appears like that: :ref:`how_to_create_an_internal_reference`.


This is not satisfactory because the name is not great. So, you can replace it as follows::


    :ref:`nicer reference <how_to_create_an_internal_reference>`

    
which render indeed nicer: :ref:`nicer reference <how_to_create_an_internal_reference>`


get section numbers
-------------------

Give a :numbered: option to the toctree directive where you want to start numbering.::

    .. toctree::
       :numbered: 1
