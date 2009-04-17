""" clean up tool

The reST files are automatically generated using sphinx_tools.

However, there are known issus which require cleaning.

This code is intended at cleaning these issues until a neat 
solution is found.
"""
import os
import sys
from openalea.misc import sphinx_tools


filenames = [   'visualea/openalea_visualea_postinstall_ref.rst',
                'visualea/openalea_visualea_postinstall_src.rst']

for file in filenames:
    process = sphinx_tools.PostProcess(file)
    process.remove_file()


print 'Try python setup.py build_sphinx now.'

