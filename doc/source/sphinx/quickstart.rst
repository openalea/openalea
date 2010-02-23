.. sidebar:: Summary

    :Release: |release|
    :Date: |today|
    :Authors: **Thomas Cokelaer**
    :Target: developers and administrators
    :status: mature

.. topic:: Overview

    How to quickly start a new Sphinx project without OpenAlea framework.



Create your own sphinx project
------------------------------
If you want to start your own documentation with Sphinx, the simplest way is as follows.

First,you need to install **Sphinx** using easy_install::

    easy_install -U sphinx          # you may use sudo under Linux systems

Then, you need to initiate a new project. Type::

    sphinx-quickstart

and follow the instructions. Most of the time you simply need to press enter. You will have to enter the project name.

In principle you should now have a file called **conf.py**, a file called **index.rst** and some directories.

Edit **index.rst** and change it to your need.

Compilation
------------


In order to compile the documentation, under linux type::

    make html

or::

    make latex

and under windows, type::

    make.bat html

To build a PDF version, type the previous command and then::

    cd _build
    make all-pdf

No, it is time to edit your main file **index.rst**.

Edition
--------

The most important is to understand that tabulation is essential (like in python).

Title are made using unerlined strings as follows::

    main title
    ==========
    sub title
    ---------

bold text is done using::

    **bold text**

and you can include image using the so called **directives** image::

    .. image:: filename.png

Finally, to include code::

    .. code-block:: python

        import mymodule
        mymodule.test()
    
    then, you can comment this piece of code.

.. note:: note the tabulation, and you must then come back to the main indentation to carry on your reST document.



