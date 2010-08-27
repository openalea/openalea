# -*- python -*-
#
#       OpenAlea.Deploy: OpenAlea setuptools extension
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA  
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
"""Deployment utilities"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

import pkg_resources
import os, sys
from os.path import join as pj

OPENALEA_PI = "http://openalea.gforge.inria.fr/pi"
OPENALEA_REPOLIST = "http://openalea.gforge.inria.fr/repolist"
OPENALEA_RECOMMENDED_PKG = "http://openalea.gforge.inria.fr/pkg_prefix"


# Precedence
INSTALL_DIST = [pkg_resources.EGG_DIST, 
                pkg_resources.BINARY_DIST, 
                pkg_resources.SOURCE_DIST, 
                pkg_resources.CHECKOUT_DIST,]

DEV_DIST = [pkg_resources.DEVELOP_DIST]
ALL_DIST = DEV_DIST + INSTALL_DIST

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


def get_metainfo(pkg_name, info):
    """ Return the metainfo of a package named pkg_name
    
    Available info are:
      - name
      - version
      - summary
      - home-page
      - author
      - author-email
      - license
      - description
      - platform
    """
    dist = pkg_resources.get_distribution(pkg_name)

    for line in dist._get_metadata('PKG-INFO'):
        if line.lower().startswith(info.lower() + ':'):
            val = line.split(':',1)[1].strip()
            return val

    raise ValueError("Unknown info %s"%(info,))


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


def get_eggs(namespace=None, precedence=ALL_DIST):
    """ Return as a generator the list of the name of all EGGS in
    a particular namespace (optional) 
    select only egg with a particular precedence
    """

    env = pkg_resources.Environment()

    for project_name in env: 
        
        if(precedence):
            pkg = pkg_resources.get_distribution(project_name)
            if(pkg.precedence not in precedence):
                continue

        if(namespace and namespace+'.' in project_name):
            yield project_name

        elif(not namespace):
            yield project_name


def get_all_lib_dirs(namespace=None, precedence=ALL_DIST):
    """ 
    Return the iterator of the directories corresponding to the shared lib 
    Select only egg with a particular precedence
    """

    egg_names = get_eggs(namespace, precedence)
    for e in egg_names:

        location = get_base_dir(e)

        for sh in get_lib_dirs(e):
            if(os.path.isabs(sh)):
                full_location = sh
            else:
                full_location = pj(location, sh)
            yield os.path.normpath(full_location)


def get_all_bin_dirs(namespace=None, precedence=ALL_DIST):
    """ 
    Return the iterator of the directories corresponding to the shared lib 
    Select only egg with a particular precedence
    """

    egg_names = get_eggs(namespace, precedence)
    for e in egg_names:

        location = get_base_dir(e)

        for sh in get_bin_dirs(e):
            if(os.path.isabs(sh)):
                full_location = sh
            else:
                full_location = pj(location, sh)
            yield os.path.normpath(full_location)



# System config

def merge_uniq(list1, list2):
    """
    Merge two lists into one with only uniq elements.
    """

    full_list = list(list1)
    full_list.extend([elt for elt in list2 if elt not in list1])
    return full_list

def check_system():
    """
    Check system configuration and 

    Return a dictionnary containing environment variables to be set.
    """

    from install_lib import get_dyn_lib_dir

    in_env = dict(os.environ)
    out_env = {}

    try:

        # Linux
        if ("posix" in os.name) and ("linux" in sys.platform.lower()):

            paths = list(get_all_bin_dirs())
            paths = merge_uniq(paths, in_env['PATH'].split(':'))
            
            libs = [get_dyn_lib_dir()]
            libs = merge_uniq(libs, in_env['LD_LIBRARY_PATH'].split(':'))

            # update the environment
            out_env['LD_LIBRARY_PATH'] = ':'.join(libs)
            out_env['PATH'] = ':'.join(paths)

        # Windows
        elif sys.platform.lower().startswith('win'):

            bin = [d.lower() for d in get_all_bin_dirs()]
            lib = get_dyn_lib_dir().lower()
            if lib not in bin:
                bin.append(lib)

            paths = [d.lower() for d in in_env['PATH'].split(';')]
            libs = merge_uniq(bin, paths) 

            out_env['PATH'] = ';'.join(libs)
        # Mac 
        elif "darwin" in sys.platform.lower():

            paths = list(get_all_bin_dirs())
            paths = merge_uniq(paths, in_env['PATH'].split(':'))
            
            libs = [get_dyn_lib_dir()]

            #The environment variable ("DYLD_FRAMEWORK_PATH") is not set with the sudo commands.
            #If "DYLD_LIBRARY_PATH" is in os.environ, we try to run the merge 
            try:
                libs = merge_uniq(libs, in_env['DYLD_FRAMEWORK_PATH'].split(':'))
                libs = merge_uniq(libs, in_env['DYLD_LIBRARY_PATH'].split(':'))

            except:
                pass 
            # update the environment
            out_env['DYLD_LIBRARY_PATH'] = ':'.join(libs)
            out_env['DYLD_FRAMEWORK_PATH'] = ':'.join(libs)
            out_env['PATH'] = ':'.join(paths)


    except Exception, e:
        print e

    return out_env


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
        prefixes = urllib.urlopen(OPENALEA_RECOMMENDED_PKG)
        for i in prefixes:
            ret.append(i.strip())
        return ret

    except Exception, e:
        print e
        return ["openalea"]


def is_virtual_env():
    """ Return True if we are in a virtual env"""

    import site
    return hasattr(site, "virtual_addsitepackages")

   


def get_metadata(name):
    """return metadata of an egg

    :param name: string of a valid namespace

    return generator containing PKGINFO

    >>> dist = get_metadata('openalea.core')
    >>> list(dist)
    :author: Thomas Cokelaer
    """
    import pkg_resources
    dist = pkg_resources.get_distribution(name)
    return dist._get_metadata('PKG-INFO')
 
