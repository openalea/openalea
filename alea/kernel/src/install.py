"""
Code for installing modules.
"""

from path import path

def install_tree( src, dest, exclude=['.svn']):

    src= path(src)
    if src.exists():
        # check if dest don't exists
        if not dest.exists():
            dest.mkdir()
        files= src.listdir()
        exception_files= []
        for f in files:
            dest= dest/f.basename()
            print 'Copy %s in %s'%(f,dest)
            if f.isdir():
                f.copytree(dest)
            elif f.isfile():
                f.copy(dest)
            else:
                exception_files.append(f)

        if exception_files:
            raise Warning("Could not copy " + ' , '.join(l))
    else:
        return False



