################################################################################
# -*- python -*-
#
#       OpenAlea.Deploy : OpenAlea setuptools extension
#
#       Copyright 2006-2007 INRIA - CIRAD - INRA  
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

__license__ = "Cecill-C"
__revision__ =" $Id: environ_var.py 847 2007-10-04 11:53:07Z dufourko $"

__doc__ = """ Install dynamic library """


import os
import sys
import shutil
import glob
from os.path import join

egg_marker_extension = ".egm"

from util import get_all_lib_dirs



def is_lib(filename):
    """ Return true if filename is a library """

    for pat in (".dll", ".so", ".a", ".lib"):
        if filename.endswith(pat):
            return True

    return False


def link_lib(src, dst):
    
    """ Create a symlink/copy library if necessary
    And create a marker file if it is absent
    """

    mark_file = dst + egg_marker_extension

    # test if there is a marker

    try:
        f = open(mark_file, 'r')
        mark = f.read()
        f.close()

        # file is identical : return
        if(mark == src):
            return False

    except Exception, e:
        print e
    
    # copy
    print "Installing %s -> %s"%(src, dst)
    if(os.path.exists(dst)):
        os.unlink(dst)

    if(hasattr(os, 'symlink')):
        os.symlink(src, dst)
    else:
        shutil.copy2(src, dst)

    # create a mark file
    print "Installing ", mark_file
    f = open(mark_file, 'w')
    f.write(src)
    f.close()

    return True


    
def clean_lib(lib_dir):
    """ Remove lib if source has been remvoved """

    for egm in glob.iglob(join(lib_dir, "*" + egg_marker_extension)):
        f = open(egm, 'r')
        srcfile = f.read()
        f.close()

        if(not os.path.exists(srcfile)):
            libfile = egm[:- len(egg_marker_extension)]
            print "Removing ", libfile
            os.remove(libfile)
            print "Removing ", egm
            os.remove(egm) 
        

def install_lib(lib_dir):

    # remove unused lib
    clean_lib(lib_dir)
    
    # get all lib_dir
    egglibdirs = set(get_all_lib_dirs())

    # install lib
    for d in egglibdirs:

        src_dir = os.path.abspath(d)
        dst_dir = os.path.abspath(lib_dir)
    
        for f in os.listdir(src_dir):

            if( is_lib(f) ):
                src = join(src_dir, f)
                dst = join(dst_dir, f)
                link_lib(src, dst)


    
                




    


