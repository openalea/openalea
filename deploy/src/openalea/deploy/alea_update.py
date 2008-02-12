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

import pkg_resources
import os
import shutil

def remove_egg(project_name, version, location):
    """ Remove an egg from the system (use rm) """

    try:
        print "Remove ", project_name, version, location
        if(os.path.isdir(location)):
            shutil.rmtree(location)
        else:
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

    env = pkg_resources.Environment()

    for project_name in env._distmap.keys():

        installed_version = [d.version for d in env[project_name]]
        if(installed_version):
            max_version = max(installed_version)

        for dist in env[project_name]:
            if(dist.version < max_version): remove_egg(project_name, dist.version, dist.location)


