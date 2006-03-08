"""
Code for installing modules.
"""

import path

def install_tree( src, dest, exclude=['.svn']):
    src= path(src)
    if src.exists():
        # check if dest don't exists
        src.copytree(dest)
    else:
        return False



