"""
This module define the path for
 - prefix
 - test
 - widget 
 - doc
 - examples
 - includes 
"""
from path import path
import os

try:
    prefix= path(os.environ['ALEA'])
except:
    raise 'Please define the ALEA environment variable to the location of the OpenAlea directory.'

version="0.0.1"
pkg_dir = prefix / 'packages'
doc_dir = prefix / 'documentation'
test_dir = prefix / 'tests'
example_dir = prefix / 'examples'
lib_dir = prefix / 'lib'
bin_dir = prefix / 'bin'
include_dir = prefix / 'include' 
rsrc_dir= prefix / 'resources'
setting_dir = prefix 

