"""
Code for installing modules.
"""

import shutil

def install_tree( src, dest, exclude=['.svn']):
    shutil.copytree(src,dest)

