"""
This module define the path for
 - prefix
 - test
 - widget
 - doc
 - examples
"""
import alea
from alea.kernel import path

version="0.0.1"
prefix = path(r"D:/pradal/devlp/alea")
pkg_dir = prefix
doc_dir = prefix / 'doc'
test_dir = prefix / 'test'
example_dir = prefix / 'example'
lib_dir = prefix / 'lib'
bin_dir = prefix / 'bin'
setting_dir = prefix / '.alea'

def _prefix():
    import os
    
