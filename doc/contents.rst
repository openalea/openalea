#################################
Welcome to OpenAlea documentation
#################################

.. module:: main
    :synopsis: how to manage the sphinx documentation in OpenAlea and related projects

.. sidebar:: Summary

    :Version: |version|
    :Release: |release|
    :Date: |today|
    :Author: See `Authors`_ section
    :ChangeLog: See `ChangeLog`_ section

.. topic:: Overview

    * Commands to create sphinx documentation `Compiling the documentation`_
    * How to put a new package under Sphinx `How to initialise a new package`_
    * Explains how the sphinx documentation works `Sphinx and reST syntax`_
    * how to `Upload the documentation`_ of a package on thr gforge

Introduction
============

We have decided to use Sphinx to document the entire OpenAlea project. The proposal that justifies this choice is available on our WIKI `Sphinx proposal <http://openalea.gforge.inria.fr/dokuwiki/doku.php?id=documentation:doctests:sphinx_proposal>`_.

Using Sphinx is not as straightforward as using a tool such as Epydoc but brings a much more flexible and powerful tool:  we can combine Reference guide, user guide and tutorials all together, we can use LaTeX for equations, and structure a document exactly as we want.
 
Here below we hope that you will find some helps to start with Sphinx. 


Compiling the documentation
===========================

Witin OpenAlea/VPlants/Alinea, if you are working on a package that has already been setup for you and if you want to compile the documentation yourself (e.g., you want to update it), then simply go the root directory of the package and type::
    
    python setup.py build_sphinx

The HTML outputs should be ready in **./doc/html**.

.. note:: Exception: if you are in **openalea/doc**, which is not a package, just type **make html**.

How to initialise a new package
===============================

In principle the administrator should initialise the sphinx documentation once for all when the developers decide to release their package.

Therefore, the following link is intended at administrators. However, it could be interesting for developers who are willing to help.


.. toctree::
    :maxdepth: 1

    source/howto_init_package.rst


Upload the documentation
========================

If the build is successful and if you have an SSH key on the GForge, you may even upload the documentation to the wiki::

    python setup.py sphinx_upload   


Sphinx and reST syntax
======================

It's time to start writting documentation. Well, with Sphinx you will need to learn a new language, that is called **reST** for **restructuredText**. No worries, it is quite simple and you will get plenty of examples. Indeed, all those pages contains a link to the source code (see in the right sidebar), so it will be a good starting point. 

If you want to know more, here are two links. The quickstart allows you to start a sphinx project from scrach outisde OpenAlea so that you can test yourself reST. The second link is a summary of useful syntax used in reST and/or Sphinx.

.. toctree::
    :maxdepth: 1
    
    source/tutorial/quickstart
    source/tutorial/rest_syntax
    source/tutorial/sphinx_python_docstring

..    tutorial/rst_tutorial
..    tutorial/sphinx_tutorial


Once you are familiar with reST, you can jump to your code to add documenation either directly in the docstrings of your python modules or inside the **doc/user** directory of your package using reST.

Concerning the docstring, here below you can find links showing how to fill them. 

.. toctree::
    :maxdepth: 1

    Example, how to fill your docstrings<tutorial/template>

Extra information
=================

Here below, you will find some extra information related to Sphinx (e.g., all the possible commands) and more generally, information related to docstrings and code conventions.

.. toctree::
    :maxdepth: 2

    source/administrator.rst
    source/developer.rst
  

.. _OpenAlea: http://openalea.gforge.inria.fr
.. _visualea: ../visualea.html



Authors
=======

This documentation was written by 

.. include:: source/AUTHORS.txt

ChangeLog
=========

.. include:: source/ChangeLog.txt

