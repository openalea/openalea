# -*- python -*-
#
#       Plugin System for vpltk
#
#       OpenAlea.VPLTk: Virtual Plants Lab Toolkit
#
#       Copyright 2013 INRIA - CIRAD - INRA
#
#       File author(s): Christophe Pradal <christophe.pradal@inria.fr>
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
__revision__ = ""

"""
Plugin fundamentals are:
  - Dicovery
  - Registration
  - EntryPoint


"""

import pkg_resources
import site
import sys

from openalea.core.factory import AbstractFactory

def plugin_name(plugin):
    return plugin.name if hasattr(plugin, 'name') else plugin.__name__


def discover(group, name=None):
    """
    Return all Plugin objects from group.

    :Parameters:
        - group : the name of a plugin group

    :Returns:
        - plugins : dict of name:plugin

    :todo: check that the same name is not used by several plugins
    """

    plugin_map = {ep.name:ep for ep in pkg_resources.iter_entry_points(group, name)}
    return plugin_map

def iter_groups():
    groups = set()
    paths = site.getsitepackages()
    usersite = site.getusersitepackages()
    if isinstance(usersite, basestring):
        paths.append(usersite)
    elif isinstance(usersite, (tuple, list)):
        paths += list(usersite)
    paths += sys.path
    # scan all entry_point and list different groups
    for path in set(paths):
        distribs = pkg_resources.find_distributions(path)
        for distrib in distribs :
            for group in distrib.get_entry_map():
                groups.add(group)
    for group in groups:
        yield group


def iter_plugins(group, name=None, debug=False):
    for ep in pkg_resources.iter_entry_points(group, name):
        if debug is True or debug == 'all' or debug == group:
            ep = ep.load()
            if isinstance(ep, (list, tuple)):
                for item in ep:
                    yield item
            else:
                yield ep
        else:
            try:
                ep = ep.load()
            except Exception, err:
                print err
            else:
                if isinstance(ep, (list, tuple)):
                    for item in ep:
                        yield item
                else:
                    yield ep

class IPlugin(object):
    """ Define a Plugin from an entry point. """

    @property
    def identifier(self):
        """
        Unique identifier. By default, identifier is pluginmodule:PluginClass
        """

    @property
    def name(self):
        """
        Short name to identify plugin. Different plugin may have same name.
        """

    @property
    def alias(self):
        """
        Human readable name
        """

    @property
    def modulename(self):
        """
        Python module path containing implementation
        """

    @property
    def objectname(self):
        """
        Name of implementation
        """

    @property
    def distribution(self):
        """
        Current python distribution
        """

    @property
    def module(self):
        """
        Module containing implementation
        """

    @property
    def implementation(self):
        """
        Real implementation
        """

class Plugin(object):
    pass

class PluginDef(object):
  UNCHANGED =0
  DROP_PLUGIN = 1
  LOWER_CASE = 2

  def __new__(self, klass):
    klass.__plugin__ = True
    return klass
