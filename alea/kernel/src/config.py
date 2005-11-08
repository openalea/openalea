"""
This module define the path for
 - prefix
 - test
 - widget
 - doc
 - examples
"""
import alea, os

pj = os.path.join

prefix = os.path.dirname(alea.__file__)
pkg_dir = prefix
doc_dir = pj(prefix, 'doc')
test_dir = pj(prefix, 'test')
example_dir = pj(prefix, 'example')
lib_dir = pj(prefix, 'lib')
bin_dir = pj(prefix, 'bin')
setting_dir = pj(prefix, '.alea')

