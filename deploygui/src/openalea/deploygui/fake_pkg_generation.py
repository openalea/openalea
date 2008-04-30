import os

def split_all_path(src):
    """ split a path into dir name lists """
    res = []
    head, tail = os.path.split(src)
    while len(tail) > 0:
        res.append(tail)
    res.append(head)
    res.reverse()
    return res
    
def relative_path(origin,dest):
        """ return the relative path between 2 path """
        origin = os.path.normpath(os.path.abspath(origin))
        dest = os.path.normpath(os.path.abspath(dest))

        dest_list = split_all_path(dest)
        orig_list = split_all_path(dest)

        
        # Find the location where the two paths start to differ.
        i = 0
        for start_seg, dest_seg in zip(orig_list, dest_list):
            if start_seg != dest_seg:
                break
            i += 1

        # Now i is the point where the two paths diverge.
        # Need a certain number of "os.pardir"s to work up
        # from the origin to the point of divergence.
        segments = [os.pardir] * (len(orig_list) - i)
        # Need to add the diverging part of dest_list.
        segments += dest_list[i:]
        if len(segments) == 0:
            # If they happen to be identical, use os.curdir.
            relpath = os.curdir
        else:
            relpath = os.path.join(*segments)
        return relpath


setup_dev_template = """
from setuptools import setup
# Setup script
setup(
    name='%s',
    version='%s',
    zip_safe = False,
    lib_dirs = {'lib' : '%s',},
    inc_dirs = { 'include' : '%s' },
   )
"""

def generate_setup_dev(pkg_name,pkg_version,pkg_dir,pkg_lib,pkg_inc):
    """ generate a setup.py for fake egg to install a local package """
    setup_dev_txt = setup_dev_template % (pkg_name,pkg_version,pkg_lib,pkg_inc)
    setup_dev_basename ='setup-fake-egg.py'
    setup_dev_fname = os.path.join(pkg_dir,setup_dev_basename)
    fstream = file(setup_dev_fname,'w')
    fstream.write(setup_dev_txt)
    fstream.close()
    return setup_dev_basename