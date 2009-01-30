################################################################################
# -*- python -*-
#
#       OpenAlea.Deploy : OpenAlea setuptools extension
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA  
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#                       Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################
"""Install dynamic library.

The egm file describes the directory the dynamic library is originated from.
"""

__license__ = "Cecill-C"
__revision__ = " $Id$"

import os
import sys
import shutil
import glob
from os.path import join

EGG_MARKER_EXTENSION = ".egm"

from openalea.deploy.util import get_all_lib_dirs, get_base_dir, INSTALL_DIST
from openalea.deploy.util import is_virtual_env
from distutils.dir_util import mkpath
from distutils.sysconfig import get_python_lib


def get_default_dyn_lib():
    """ Return the default path for dynamic library """

    basedir = get_python_lib()

    # Virtual environment
    if(is_virtual_env()):
        if("posix" in os.name):
            return os.path.abspath( 
                os.path.join(basedir, '../../lib') )
        else:
            return os.path.join(basedir, "shared_libs")

    # Standard environment
    if("posix" in os.name):
        return "/usr/local/lib"
    else:
        basedir = get_python_lib()
        return os.path.join(basedir, "shared_libs")


def get_dyn_lib_dir(use_default=True):
    """ 
    Return the shared lib directory 
    if use_default : return default directory if not defined
    """

    bdir = get_base_dir("openalea.deploy")
    up_dir = os.path.abspath(join(bdir, os.path.pardir))

    try:
        f = open(join(up_dir, "shared-lib.pth"), 'r')
        lib_dir = f.read()
        print 'Reading shared-lib.pth found in %s' % lib_dir
        f.close()

    except Exception, e:

        if(use_default):
            lib_dir = get_default_dyn_lib()
        else:
            lib_dir = None
        
    return lib_dir



def set_dyn_lib_dir(path):
    """ Set the shared lib directory """
    
    path = os.path.abspath(path)
    bdir = get_base_dir("openalea.deploy")
    dir = os.path.abspath(join(bdir, os.path.pardir))
    dst = join(dir, "shared-lib.pth")
    try:
        f = open(dst, 'w')
        f.write(path)
        print "Write ", dst
        f.close()
    except Exception, e:
        print e


def is_lib(filename):
    """ Return true if filename is a library """

    for pat in (".dll", ".so", ".a", ".lib", ".dylib"):
        if filename.endswith(pat):
            return True

    return False


def link_lib(src, dst):
    """ 
    Symlink/copy library if necessary
    and create a marker file (egm) if it is absent
    src : source lib file
    dst : destination lib file
    """

    mark_file = dst + EGG_MARKER_EXTENSION

    # Test if there is a marker
    try:
        f = open(mark_file, 'r')
        mark = f.read()
        f.close()

        # File is identical : return
        if(mark == src and os.path.exists(dst)):
            return False

    except:
        pass
    
    # copy
    print "Installing %s -> %s"%(src, dst)
    if(os.path.exists(dst)):
        os.unlink(dst)

    if(hasattr(os, 'symlink')):
        os.symlink(src, dst)
    else:
        shutil.copy2(src, dst)

    # create an egm file
    print "Installing ", mark_file
    f = open(mark_file, 'w')
    f.write(src)
    f.close()

    return True


    
def clean_lib(lib_dir, clean_all=False):
    """ Remove lib if source has been removed
    If clean_all is True, remove all library with egm
    """

    for egm in glob.glob(join(lib_dir, "*" + EGG_MARKER_EXTENSION)):
        f = open(egm, 'r')
        srcfile = f.read()
        f.close()

        if(not os.path.exists(srcfile) or clean_all):
            libfile = egm[:- len(EGG_MARKER_EXTENSION)]

            try:
                print "Removing ", libfile
                os.remove(libfile)
            except Exception, e:
                print "Cannot remove %s : %s"%(libfile, e)
            
            try:
                print "Removing ", egm
                os.remove(egm)
            except Exception, e:
                print "Cannot remove %s : %s"%(egm, e)



def install_lib(lib_dir):
    """
    Install dynamic library in lib_dir
    if None, use previous dir or default
    Return real lib_dir
    """
    if(not lib_dir):
        lib_dir = get_dyn_lib_dir()

    # Create directory
    if(not os.path.exists(lib_dir)):
        mkpath(lib_dir)

    old_lib_dir = get_dyn_lib_dir(False)
    changed = (old_lib_dir != lib_dir)
    clean_all = (changed and old_lib_dir)

    # remove unused lib
    if(old_lib_dir):
        clean_lib(old_lib_dir, clean_all)

    if(changed):
        set_dyn_lib_dir(lib_dir)
    
    # get all the intial package lib_dirs before the copy of the sh lib.
    # Copy only libraries of the installed eggs.
    egglibdirs = set(get_all_lib_dirs(precedence=INSTALL_DIST))

    # install lib
    for d in egglibdirs:

        try:
            src_dir = os.path.abspath(d)
            dst_dir = os.path.abspath(lib_dir)
    
            for f in os.listdir(src_dir):

                if( is_lib(f) ):
                    src = join(src_dir, f)
                    dst = join(dst_dir, f)
                    link_lib(src, dst)
                    
        except Exception, e:
            print e
            


    return lib_dir
                




    


