# -*- python -*-
#
#       OpenAlea.Deploy: OpenAlea setuptools extension
#
#       Copyright 2006-2007 INRIA - CIRAD - INRA  
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#


__doc__="""
Deployment utilities
"""

__license__= "Cecill-C"
__revision__=" $Id$ "



import pkg_resources
import os, sys
from os.path import join as pj
from distutils.sysconfig import get_python_lib


OPENALEA_PI = "http://openalea.gforge.inria.fr/pi"
OPENALEA_REPOLIST = "http://openalea.gforge.inria.fr/repolist"
OPENALEA_RECOMMENDED_PKG = "http://openalea.gforge.inria.fr/pkg_prefix"

# EGG Management

def get_base_dir(pkg_name):
    """ Return the base directory of a pkg """
    return pkg_resources.get_distribution(pkg_name).location


def get_egg_info(pkg_name, info_key):
    """ Return as a generator the egg-infos contained in info_key"""
    
    dist = pkg_resources.get_distribution(pkg_name)
    try:
        lstr = dist.get_metadata(info_key)
    except:
        lstr = ""
        
    return pkg_resources.yield_lines(lstr)


def get_lib_dirs(pkg_name):
    """ Return a generator which lists the shared lib directory """

    return get_egg_info(pkg_name, 'lib_dirs.txt')


def get_bin_dirs(pkg_name):
    """ Return a generator which lists the shared lib directory """

    return get_egg_info(pkg_name, 'bin_dirs.txt')


def get_inc_dirs(pkg_name):
    """ Return a generator which lists the shared lib directory """

    return get_egg_info(pkg_name, 'inc_dirs.txt')


def get_postinstall_scripts(pkg_name):
    """ Return a generator which lists the post_install scripts (as string) """

    return get_egg_info(pkg_name, 'postinstall_scripts.txt')


def get_eggs(namespace=None):
    """ Return as a generator the list of the name of all EGGS in
    a particular namespace (optional) """

    env = pkg_resources.Environment()

    for project_name in env:
        if(namespace and namespace+'.' in project_name):
            yield project_name
        elif(not namespace):
            yield project_name


def get_all_lib_dirs(namespace=None):
    """ Return the iterator of the directories corresponding to the shared lib """

    egg_names = get_eggs(namespace)
    for e in egg_names:

        location = get_base_dir(e)

        for sh in get_lib_dirs(e):
            if(os.path.isabs(sh)):
                full_location = sh
            else:
                full_location = pj(location, sh)
            yield full_location


def get_all_bin_dirs(namespace=None):
    """ Return the iterator of the directories corresponding to the shared lib """

    egg_names = get_eggs(namespace)
    for e in egg_names:

        location = get_base_dir(e)

        for sh in get_bin_dirs(e):
            if(os.path.isabs(sh)):
                full_location = sh
            else:
                full_location = pj(location, sh)
            yield full_location


# System config

def check_system():
    """
    Check system configuration and return environment variables dictionary
    This function need OpenAlea.Deploy
    """
    from install_lib import get_dyn_lib_dir
    
    inenv = dict(os.environ)
    outenv = {}
    
    try:

        # Linux
        if(("posix" in os.name) and ("linux" in sys.platform.lower())):

            paths = set(get_all_bin_dirs())
            paths.update(set(inenv['PATH'].split(':')))
            
            libs = set([get_dyn_lib_dir()])
            libs.update(set(inenv['LD_LIBRARY_PATH'].split(':')))

            # libs
            outenv['LD_LIBRARY_PATH'] = ':'.join(libs)
            outenv['PATH'] = ':'.join(paths)

                

        # Windows
        elif("win" in sys.platform.lower()):

            libs = set(get_all_bin_dirs())
            libs.add(get_dyn_lib_dir())
            libs.update(set(inenv['PATH'].split(';')))
            
            outenv['PATH'] = ';'.join(libs)
                  
    except Exception, e:
        print e

    return outenv


# Repository management

def get_repo_list():
    """ Return the list of OpenAlea repository """
    import urllib
    try:
        ret = []
        u = urllib.urlopen(OPENALEA_REPOLIST)
        for i in u:
            ret.append(i.strip())
        return ret

    except Exception, e:
        print e
        return [OPENALEA_PI]



def get_recommended_prefix():
    """ Return the list of recommended package prefix """
    import urllib
    try:
        ret = []
        u = urllib.urlopen(OPENALEA_RECOMMENDED_PKG)
        for i in u:
            ret.append(i.strip())
        return ret

    except Exception, e:
        print e
        return ["openalea"]
