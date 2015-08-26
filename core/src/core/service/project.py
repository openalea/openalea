# -*- coding: utf-8 -*-
# -*- python -*-
#
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2015 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Baty <guillaume.baty@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

from openalea.core.project.manager import ProjectManager
PM = ProjectManager()


def set_active_project(project):
    PM.cproject = project


def active_project():
    return PM.cproject


def projects():
    PM.discover()
    return PM.items()


def project_item(project_name, category, name):
    data = PM.cproject.get_item(category, name)
    return data


def add_project_directory(projectdir):
    PM.repositories.append(projectdir)

create_project = PM.create

write_project_settings = PM.write_settings
default_project = PM.load_default
load_project = PM.load
discover_projects = PM.discover


def default_project_manager():
    return PM
