.. _howto_init_package:

How to initialise a package to generate Sphinx documentation
############################################################


.. sidebar:: Target

    This document is intended to be a resource for developers, especially those who wish to
    generate the sphinx documentation from sratch; e.g., when a package is not yet under Sphinx.
    

This Howto is mainly for Administrators and possibly for developpers. It explained how to set up the sphinx documentation in a package, if not already done , and how to generate the sphinx output.

Before starting, you will need to install Sphinx (see below), OpenAlea main packages such as deploy and misc. And you will need to have your package accessible in your Python environment.


Sphinx configuration
====================

Sphinx installation
-------------------

First of all you need sphinx (latest version or at least 0.6.1). If not installed, use easy_install as follows in your environment::

    easy_install sphinx

Package setup
-------------

Then, go into your package directory (e.g, PlantGL in the vplants project). Look if a file called **setup.cfg** exists. If not create it. In any case, add those lines if they are not present::

    [build_sphinx]
    source-dir = doc/
    build-dir = doc/
    all_files = 1

These options will tell Sphinx to look into the doc directory to search for a file called **conf.py** and to build the HTML outputs into the **./doc/build** directory.


Then, go to the ./doc directory::

    cd doc

Here, you will need some configuration file. For now, the way the documentation is managed is not yet completely stabilised or frozen. For instance, we need to meta information such as the project name and package name. To be sure that those information are correct, we've decided to use an ini file called sphinx.ini to store some meta information. This fille looks like::

    [metadata]
    package=stat_tool
    project=vplants
    release=0.6.2
    version=0.6

.. note:: You can also add an extra line (**api=false**), to prevent the reference guide to be rebuilt each time you compile Sphinx documentation.

automatically create the reference guide and index file
-------------------------------------------------------

We suppose that you have installed OpenAlea and that the script **alea_init_sphinx** is installed. If not, look into the **misc** directory for **sphinx_tools.py**. If this is a brand new installation (no user directory, no rst files), type::

    alea_init_sphinx --configuration --contents --index --verbose

This command should create for you the reference guide files (in <package_name>, a contents.rst file and two index.rst files, one in the user directory and one in the reference directory. Finally, a conf.py file required by Sphinx is also created. You can now change those files and put them in the archive. Next time you use alea_init_sphinx, for instance to generate the reference guide only, do not use the options above, simply type::

    alea_init_sphinx --verbose

Your configuration file (conf.py) should be similar to::

    import sys
    import os
    sys.path.append(os.path.join(os.getcwd(), '../../../openalea/doc'))
    from common_conf import *
    # add whatever you want to override already defined parameters (none in principle)

Check you have everything ready
-------------------------------

Note that the third line assume that you have installed OpenAlea in a specific directory. Therefore, your architecture should look like::

    |-- openalea
    |   |-- core
    |   |   |-- AUTHORS.txt
    |   |   |-- ChangeLog.txt
    |   |   |-- LICENSE.txt
    |   |-- deploy
    |   |   |-- AUTHORS.txt
    |   |   |-- ChangeLog.txt
    |   |   |-- LICENSE.txt
    |   |   |-- doc
    `-- vplants
        |-- PlantGL
        |   |-- AUTHORS.txt
        |   |-- ChangeLog.txt

.. note:: in the future, we will get rid of this line. At the moment, the misc package is not yet released, so we need this statement. 

Building the documentation
==========================

Once done, go back to your package directory, in principle simply type::

    cd ..

and test the command to build the documentation::

    python setup.py build_sphinx -b html

Even though you have not yet written a single line of code, you should already have a few HTML pages generated for you. Check that you can access to them. 

By default, each time you launch the python setup.py build_sphinx, sphinx will regenerate the Reference guide input files. To prevent this option, edit the **sphinx_ini** file and add an option called 'api' and set it to the string 'false'




Architecture of the source file and how to add documentation
============================================================


Let us suppose that you work with the package **PlantGL**.


Then next step is to write/create some rest files. The architecture in the **doc** directory should be as follows::

    .
    |-- conf.py
    |-- contents.rst
    |-- sphinx.ini
    |-- .static
    |-- stat_tool
    |   |-- openalea_stat_tool_vectors_ref.rst
    |   |-- openalea_stat_tool_vectors_src.rst
        |-- index.rst
        |-- ....
    `-- user
        |-- index.rst
        |-- overview.txt
        |-- ...

The files **conf.py** and **sphinx.ini** have already been explained. 

The **.static** directory may be used to store documents, images. The sphinx extension inheritance-diagram search for a .static directory either in the current directory (where the Makefile is run) or the doc/ directory, which does not exists. This is why the .static exists. We put the CSS and common images inside this directory.


**contents.rst** is the main entry point. You should not change it too much so, so as to keep a page very similar to the other packages. 


Note that inside this rst files, two other reST files are included: **./user/index.rst** and **./stat_tool/index.rst**. The latter should not be touched, but the formet is you entry point, where you can edit and add whatever you want. 


