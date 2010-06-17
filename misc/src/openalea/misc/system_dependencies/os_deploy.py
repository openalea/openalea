# -*- python -*-
#
#       VirtualPlant's buildbot continuous integration scripts.
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Daniel Barbeau <daniel.barbeau@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
###############################################################################

"""
This module defines two easy methods to deploy system dependencies
either for runtime or for development purposes.
"""


from os_factory import OsFactory
import dependency, distributions

__all__ = ["deploy_runtime_dependencies", "deploy_development_dependencies"]

def deploy_runtime_dependencies(software, osname, fake):
    theOs = OsFactory().create(osname)
    dependencies = dependency.Dependency(software, osname)
    theOs.install_packages(dependencies.runtime_distribution_packages(), fake)

def deploy_development_dependencies(software, osname, fake):
    theOs = OsFactory().create(osname)
    dependencies = dependency.Dependency(software, osname)
    theOs.install_packages(dependencies.development_distribution_packages(), fake)



