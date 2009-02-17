Material to generate the sphinx documentation
=============================================

Building the documentation
==========================

You need to make sure that the directories containing te python files are
included within your PYTHONPATH. Concerning the OpenAlea packages, if you did

>>> python setup.py install 

or used the **ez_alea_setup**, you should not do anything more. However, to
include the examples in ./doc/source/tutorial/, you'll need to do

>>> export PYTHONPATH=$PYTHONPATH:$OPENALEA/doc/source/tutorial

Then, start the compilation of the HTML documentation:

>>> make html

This command will search for a Makefile, and build the HTML directory in ./build/html.

It will look inside the 'source' directory for any configuration file.

.. note:: if you wnat to compile a package on its own, go to irs directory and
type 'python setup.py build_sphinx' instead of 'make install'
 

.static directory
=================

the sphinx extension inheritance-diagram search for a .static directory either
in the current directory (where the Makefile is run) or the doc/ directory, which does not exists. This is why the .static exists. We put the CSS and common images inside this directory. 

source directory 
----------------

Contains:
 - the configuraton file 'conf.py'
 - the modules sources (1 directory for 1 modules)
 - static files (css and images)
 - ini file (metadata information such as the version)
 - a rst file that will be the main page

sphinxext directory
-------------------

This directory contains sphinx extension that are needed to compile the documentation. 

Those extensions were taken from the standard sphinx extension, and numpy/scipy and matplotlib

Note, that there were taken from sphinx release 0.5.1

Because, at the present time (feb 2009), I am using Sphinx 0.6, some
extensions failed to import modules that have moved.

List of changes
^^^^^^^^^^^^^^^
- only_directives: the import LaTeXTranslator is deprecated. The correct one
  is::

    from sphinx.writers.latex import LaTeXTranslator
- inheritance-diagram: quite common that imports fail. I changed the code:

  >>> try:
  >>>    module = __import__(path, None, None, [])
  >>> except ImportError:
  >>>    raise ValueError(

  to:

  >>>    try:
  >>>      module = __import__(fullname, None, None, [])
  >>>  except ImportError:
  >>>      raise ValueError(

 
