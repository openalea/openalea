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
"""todo"""

__license__ = "Cecill-C"
__revision__ =" $Id$"

import os, sys
import shutil

from pkg_resources import Environment, parse_version, EGG_DIST

def remove_egg(project_name, dist):
    """ Remove an egg from the system (use rm) """

    if(dist.precedence != EGG_DIST):
        return

    version = dist.version
    location = dist.location

    try:
        print "Remove ", project_name, version, location
        if(os.path.isdir(location)):
            print "Remove directory : %s"%(location,)
            shutil.rmtree(location)
        else:
            print "Remove file %s"%(location)
            os.remove(location)
            return True

    except Exception, e:
        print e
        return False

    except :
        print "Unexpected error:", sys.exc_info()[0]
        print "Please check you have permission to remove packages. "
        return False
  


def clean_version():
    """ Keep only most recent version of each package """

    env = Environment()

    for project_name in env._distmap.keys():

        installed_version = [d.version for d in env[project_name]]
        if(installed_version):
            max_version = max(installed_version, key=parse_version)

            for dist in env[project_name]:
                if parse_version(dist.version) < parse_version(max_version): 
                    remove_egg(project_name, dist)



def update_all():
    """ Update all packages """

    env = Environment()

    for project_name in env._distmap.keys():
        print "Update %s"%(project_name)
        alea_install_U(project_name)



def alea_install_U(project_name):
    """ Call alea_install -U project_name """

    from setuptools import setup
   
    setup(
        script_args = ['-q','alea_install', '-v', '-U', project_name],
        )
