import os, glob
from openalea.misc.path import path

setup_cmd = '*/setup.py'

def list_packages(project_directory, exclude_list):
    '''    List of packages from openalea project
    '''
    packages = None
    # write the node code here.
    directory = path(project_directory).abspath()
    directories = '/'.join([directory, setup_cmd])
    ret = glob.glob(directories)
    packages = [os.path.basename(os.path.dirname(s)) for s in ret]
    for l in exclude_list:
        if l in packages:
            packages.remove(l)
    # return outputs
    return packages
