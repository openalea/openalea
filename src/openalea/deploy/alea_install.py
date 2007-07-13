# Script which wrap easy install with some post-processing

__requires__ = 'setuptools'
import sys
from pkg_resources import load_entry_point
from openalea.deploy import get_all_lib_dirs
from openalea.deploy.environ_var import set_lsb_env, set_win_env

def main():
    # Call easy install
    load_entry_point('setuptools', 'console_scripts', 'easy_install')()

    # Do post_processing


    # Set environment
    print "Setting environment variables"
    
    dirs = list(get_all_lib_dirs('openalea'))
    print "The following directories contains shared library :", '\n'.join(dirs), '\n'

    set_win_env(['OPENALEA_LIBS=%s'%(';'.join(dirs)), 'PATH=%OPENALEA_LIBS%'])
    set_lsb_env('openalea',
                ['OPENALEA_LIBS=%s'%(':'.join(dirs)), 'LD_LIBRARY_PATH=$OPENALEA_LIBS'])
