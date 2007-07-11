

import pkg_resources


def get_base_dir(pkg_name):
    """ Return the base directory of a pkg """
    return pkg_resources.get_distribution(pkg_name).egg_name

        
def get_shared_lib(pkg_name):
    """ Return a generator wich list the shared lib directory """

    dist = pkg_resources.get_distribution(pkg_name)
    lstr = dist.get_metadata('shared_lib.txt')
    return pkg_resources.yield_lines(lstr)


def get_shared_include(pkg_name):
    """ Return a generator wich list the shared lib directory """

    dist = pkg_resources.get_distribution(pkg_name)
    lstr = dist.get_metadata('shared_include.txt')
    return pkg_resources.yield_lines(lstr)
