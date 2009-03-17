""" clean up tool

The reST files are automatically generated using sphinx_tools.

However, there are known issus which require cleaning.

This code is intended at cleaning these issues until a neat 
solution is found.

:known problem:

- the misc package is not distributed under openalea namespace for now.
  Yet, project is openalea and therefore, openalea. namespace are included
  in the automodule string. They should be removed.
- Removing the "openalea." string , tha name of the automodule is identical to
  the module directive name so .. module:: and .. automodule :: are in conflict

:solution: remove "openalea." in the automodule and remove the module directive

"""
import os
import sys
sys.path.append(os.path.abspath('../'))
from openalea.misc import sphinx_tools

print 'Fixing the module and automodule conflict.'

files = [
    './misc/path_ref.rst',
    './misc/download_ref.rst',
    './misc/sphinx_tools_ref.rst',
    './misc/gendoc_ref.rst',
    './misc/upload_dist_ref.rst',
    './misc/make_develop_ref.rst',
    './misc/openalea_distrib_ref.rst',]
 

for file in files: 
    process = sphinx_tools.PostProcess(file)
    process.no_namespace_in_automodule()
    process.remove_header(nline=2, start=4)
    
print 'Try python setup.py build_sphinx now.'

