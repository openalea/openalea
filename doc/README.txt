



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

 
