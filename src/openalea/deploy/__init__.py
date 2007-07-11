

import pkg_resources
from os.path import join as pj


def get_base_dir(pkg_name):
    """ Return the base directory of a pkg """
    return pkg_resources.get_distribution(pkg_name).location

        
def get_shared_lib(pkg_name):
    """ Return a generator wich list the shared lib directory """

    dist = pkg_resources.get_distribution(pkg_name)
    try:
        lstr = dist.get_metadata('shared_lib.txt')
    except:
        lstr = ""
        
    return pkg_resources.yield_lines(lstr)


def get_shared_include(pkg_name):
    """ Return a generator wich list the shared lib directory """

    dist = pkg_resources.get_distribution(pkg_name)
    lstr = dist.get_metadata('shared_include.txt')
    return pkg_resources.yield_lines(lstr)



def get_eggs(namespace=None):
    """ Return as an iterator the list of the name of all EGGS in
    a particular namespace (optional) """

    env = pkg_resources.Environment()

    for project_name in env:
        if(namespace and namespace+'.' in project_name):
            yield project_name


def get_shared_lib_dirs(namespace=None):
    """ Return the iterator of the directories corresponding to the shared lib """

    egg_names = get_eggs(namespace)
    for e in egg_names:

        location = get_base_dir(e)

        for sh in get_shared_lib(e):

            full_location = pj(location, sh)
            yield full_location
        
    
    
