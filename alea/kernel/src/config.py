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

def _prefix():
    here= path(__file__)
    l= here.splitall()
    if 'alea' in l:
        i=l.index('alea')
        f= l[0]
        for s in l[1:i+1]:
            f= f/s
        return f
    else:
        return path('.')

version="0.0.1"
prefix = path("c:\\alea")
pkg_dir = prefix / 'packages'
doc_dir = prefix / 'doc'
test_dir = prefix / 'test'
example_dir = prefix / 'example'
lib_dir = prefix / 'lib'
bin_dir = prefix / 'bin'
include_dir = prefix / 'include' 
setting_dir = prefix

