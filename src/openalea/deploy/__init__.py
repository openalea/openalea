# -*- python -*-
#
#       OpenAlea.Deploy: OpenAlea Deploy
#
#       Copyright 2006 INRIA - CIRAD - INRA  
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
__revision__=" $Id: node.py 622 2007-07-06 08:14:43Z dufourko $ "



import pkg_resources
from os.path import join as pj


OPENALEA_PI = "http://openalea.gforge.inria.fr/pi"



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

            full_location = pj(location, sh)
            yield full_location




        
