.. _howto_init_package:


How to initialise a package to generate Sphinx documentation
############################################################

.. contents::


.. warning::

    Remember that you must have your package accessible in your Python environment to generate the sphinx documentation.

Sphinx configuration
====================
Sphinx installation
-------------------

First of all you need sphinx (latest version or at least 0.6.3). If not installed, use easy_install as follows in your environment::

    easy_install -U sphinx

sphinx and setuptools
---------------------

sphinx is include within setuptools, therefore you can use the following command to build the HTML documentation::

    python setup.py build_sphinx

However, you **must** tell where is the documentation, in particular the configuration file. This is done within the file **setup.cfg** where you will add those lines, if they are not present::

    [build_sphinx]
    source-dir = doc/
    build-dir = doc/_build
    all_files = 1

These options will tell Sphinx to look into the doc directory to search for a file called **conf.py** and to build the HTML outputs into the **./doc/_build/html** directory.

Sphinx configuration file
-------------------------

Go into the ./doc directory::

    cd doc

Here, you will need a configuration file **conf.py**::

    import os,sys
    from openalea.misc.sphinx_configuration import *
    from openalea.misc.sphinx_tools import sphinx_check_version
    from openalea.deploy.metainfo import read_metainfo

    sphinx_check_version()                      # check that sphinx version is recent
    metadata = read_metainfo('../metainfo.ini') # read metainfo from common file with setup.py
    for key in ['version','project','release','authors', 'name', 'package']:
        exec("%s = '%s'" % (key, metadata[key]))

    latex_documents = [('contents', 'main.tex', project + ' documentation', authors, 'manual')]

    project = project + '.' + package

This file looks for a common conf.py file to all OpenAlea package that can be found  in **./misc/src/openalea/misc/sphinx_configuration.py**

metainfo file
--------------

The file conf.py search for a metainfo file called metainfo.ini that should be at the same level as **`setup.py** and **setup.cfg** files. The metainfo must contains version, project, name, package and authors tags but may contain other metainfo to be used by the **setup.py** file ::

    [metainfo]
    version = 0.8.0
    release = 0.8
    project = openalea        ; must be in [openalea, vplants, alinea]; used to scp files and titles
    name = OpenAlea.Starter
    namespace = openalea
    package = starter         ; package is going to be used by Sphinx to create the title and scp the files
    description= whatever description you want
    long_description= whatever desription you want
    authors= your name
    authors_email = your emai
    url = http://openalea.gforge.inria.fr
    license = Cecill-C


Setup the source (ReST) files
-------------------------------


To finalise you sphinx setup, you should look into an already setup package and from the **doc** directory, copy the Makefile, make.bat, contents.rst, user/index.rst, user/overview.txt and user/autosum.rst to get an architecture as follows::


    |-- openalea
    |   |-- yourpackage
    |   |   |-- AUTHORS.txt
    |   |   |-- ChangeLog.txt
    |   |   |-- LICENSE.txt
    |   |   |-- doc
    |   |   |   |-- Makefile
    |   |   |   |-- _static
    |   |   |   |-- _build
    |   |   |   |-- conf.py
    |   |   |   |-- contents.rst
    |   |   |   |-- make.bat
    |   |   |   `-- user
    |   |   |       |-- autosum.rst
    |   |   |       |-- index.rst
    |   |   |       `-- overview.txt


Checking the configuration
==========================

the command should work without errors::

    make html

and your HTML files should be available in::

    ./doc/_build/html/contents.html


What are _static and _build directories
========================================

The **_static** directory is used by sphinx to store documents, images. 
The **_build** directory is used by sphinx to store html and other built documents.

They must be present bu can be empty. 

Where to start ?
================
**contents.rst** is the main entry point. You should not change it too much so, so as to keep a page very similar to the other packages. 



