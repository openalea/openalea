#################################
How to use sphinx ? 
#################################

.. module:: main
    :synopsis: how to manage the sphinx documentation in OpenAlea and related projects

.. sidebar:: Summary

    :Release: |release|
    :Date: |today|
    :Authors: **Thomas Cokelaer**
    :Target: developers and administrators
    :status: mature

.. topic:: Overview

    * `ReSt and Sphinx syntax <rest_syntax.html>`_
    * `How to document your docstrings <sphinx_python_docstring.html>`_
    * `Compiling the documentation`_ with Sphinx
    * `How to initialise a new package`_
    * How to `Upload the documentation`_ of a package on the web




Introduction
============

Using Sphinx to generate Reference guide is not as straightforward as using a tool such as Epydoc but brings a much more flexible and powerful tool that allows us to create user guide and tutorials as well.

It uses the reST syntax, that is quite simple to learn and has the advantagse to be human readable (useful for the docstrings !) . Moreover, it comes with many plugins such as LaTeX that can be used for equations.

Here below we hope that you will find some helps to start with Sphinx.

First, you will need to install Sphinx, which is done very easily using easy_install::

    easy_install -U sphinx

Quick Start
=============

.. toctree::
    :maxdepth: 1

    quickstart.rst

Compiling the documentation
===========================

Within OpenAlea/VPlants/Alinea, **if you are working on a package that has already been setup for you** and if you want to compile the documentation yourself (e.g., you want to update it), you have two methods:

From the package directory using setuptools
-------------------------------------------

Go the root directory of the package and type::

    python setup.py build_sphinx

The HTML outputs should be ready in **./doc/html**. Similarly, you can have a LaTeX output as follows::

    python setup.py build_sphinx -b latex

.. note:: Sphinx takes care to parse only the files that have changed. You may want to force the building using the -E option as follows:

::

    python setup.py build_sphinx -E

From the ./doc directory using Makefile
-----------------------------------------

Alternately, go in the ./doc/ directory and just type::

    make html

or::

    make latex

.. warning:: Exception, the openalea/doc directory is not yet a package, so only **make html** will work

Upload the documentation
========================

If the build is successful and if you have an SSH key on the GForge, you may even upload the documentation to the wiki::
    
    python setup.py sphinx_upload --username <your gforge username> 

.. note:: setuptools will look in the setup.cfg file looking for **project** and **package** in the [upload_sphinx] section. (see next section)

.. warning:: Exception, the openalea/doc directory is not yet a package; In order to upload the documentation, use the script sphinx_upload.py that is present in ./openalea/doc.

How to initialise a new package
===============================

In principle the administrator should initialise the sphinx documentation once for all when the developers decide to release their package. If you still want to do it yourself, check this link:


.. toctree::
    :maxdepth: 1

    howto_init_package.rst



Sphinx and reST syntax
======================

It's time to start writting documentation. Well, with Sphinx you will need to learn a new language, that is called **reST** for **restructuredText**. No worries, it is quite simple and you will get plenty of examples. Indeed, all those pages contains a link to the source code (see in the right sidebar), so it will be a good starting point. 

Here are some links related to the sphinx syntax

.. toctree::
    :maxdepth: 1

    rest_syntax
    sphinx_python_docstring
    doctest
    rest_faqs.rst


Once you are familiar with reST, you can jump to your code to add documenation either directly in the docstrings of your python modules or inside the **doc/user** directory of your package using reST.

.. note:: Administrators may be interested in the following link that was used to test different type of doctring syntax 

Administrators usage
====================
Here below, you will find some extra information explaining the structures of the documentation on the wiki (administrator usage)

.. toctree::
    :maxdepth: 1

    Different methods to fill the docstrings (admin usage)<template>
    administrator.rst
  

.. _OpenAlea: http://openalea.gforge.inria.fr
   .. _visualea: ../visualea.html


.. _authors:

Authors
=======

.. include:: ../AUTHORS.txt

ChangeLog
=========

.. include:: ../ChangeLog.txt



