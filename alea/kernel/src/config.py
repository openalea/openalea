"""
This module define the path for
 - prefix
 - test
 - widget
 - doc
 - examples
"""
import os

pj = os.path.join

version="0.0.1"
prefix = r"D:\pradal\devlp\alea"
pkg_dir = prefix
doc_dir = pj(prefix, 'doc')
test_dir = pj(prefix, 'test')
example_dir = pj(prefix, 'example')
lib_dir = pj(prefix, 'lib')
bin_dir = pj(prefix, 'bin')
setting_dir = pj(prefix, '.alea')
