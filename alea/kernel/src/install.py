"""
Code for installing modules.
"""

import shutil
import glob

def install_tree( src, dest, exclude=['.svn']):
    shutil.copytree(src,dest)

