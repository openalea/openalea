# -*- coding: utf-8 -*-
# -*- python -*-
#
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
###############################################################################

from openalea.core.service.plugin import plugin_name


def can_display_criterion(criterion, value):
    if criterion.startswith('_'):
        return False
    elif criterion in ('implementation', 'name', 'name_conversion', 'identifier', 'tags', 'implement'):
        return False
    return True


def format_criterion(criterion, value, indent=0):
    istr = ' ' * indent
    if criterion == 'authors':
        s = '%sauthors:\n' % istr
        for author in value:
            s += istr + ' - %s (insitute: %s)\n' % (author.get('name', 'Anonymous'), author.get('institute', 'not defined'))
        return s
    elif criterion == 'inputs':
        s = istr + 'f('
        params = []
        for inp in value:
            name = inp.get('name', '??')
            interface = inp.get('interface', '??')
            default = inp.get('default', '??')
            params.append('%s:%s=%s' % (name, interface, default))
        return s + ', '.join(params) + ')'
    else:
        return '%s%s = %s' % (istr, criterion, value)


def list_plugins(lst, verbose=False):
    from openalea.core.plugin.manager import PluginManager
    pm = PluginManager()
    import pkg_resources
    from openalea.core.plugin import iter_groups

    if lst in ['summary', 'all']:
        prefixes = ['oalab', 'vpltk', 'openalea']
    else:
        prefixes = [lst]
    for group in sorted(iter_groups()):
        match = False
        for prefix in prefixes:
            if group.startswith(prefix):
                match = True
                break
        if match:
            eps = [ep for ep in pkg_resources.iter_entry_points(group)]
            if lst == 'summary':
                print '\n\033[91m%s\033[0m (%d plugins)' % (group, len(eps))
                for ep in eps:
                    parts = [str(s) for s in (ep.module_name, ep.name)]
                    identifier = ':'.join(parts)
                    print '  - %s \033[90m%s (%s)\033[0m' % (ep.name, identifier, ep.dist.egg_name())
            else:
                print '\033[44m%s\033[0m' % group
                UNDEF = 'Not defined'
                plugin_groups = {UNDEF: []}
                for plugin in pm.plugins(group):
                    interface = getattr(plugin, 'implement', None)
                    if interface:
                        plugin_groups.setdefault(interface, []).append(plugin)
                    else:
                        plugin_groups[UNDEF].append(plugin)
                for group, plugins in plugin_groups.items():
                    if not plugins:
                        continue
                    print '  implements: \033[91m%s\033[0m' % group
                    for plugin in plugins:
                        p_class = plugin.__class__
                        print '    - \033[93m%s \033[90m%s:%s\033[0m' % (plugin_name(plugin), p_class.__module__, p_class.__name__)
                        if verbose:
                            print '        tags: %s' % ', '.join(plugin.tags)
                            print '        plugin: %s, egg: %s\n        path: %s' % (
                                ep.name, ep.dist.egg_name(), ep.dist.location)
                            print '        criteria:'
                            for crit_name in sorted(dir(plugin)):
                                if crit_name in ('implementation', '__call__'):
                                    continue
                                crit = getattr(plugin, crit_name)
                                if can_display_criterion(crit_name, crit):
                                    print format_criterion(crit_name, crit, 10)

                print
                print
