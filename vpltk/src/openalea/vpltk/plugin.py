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
            yield ep.load()
        else:
            try:
                yield ep.load()
            except Exception, err:
                print err

class Plugin(object):
    """ Define a Plugin from an entry point. """

    def __init__(self, epoint):
        self.ep = epoint

    @property
    def name(self):
        return self.ep.name

    @property
    def module_name(self):
        return self.ep.module_name

    @property
    def dist(self):
        return self.ep.dist

    def load(self, *args, **kwds):
        return self.ep.load(*args, **kwds)


