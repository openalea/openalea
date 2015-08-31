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

from openalea.core.plugin.plugin import plugin_name


def format_author(author, key=None, **kwds):

    show_all = kwds.get('show_all', False)
    fmt_author = ''
    if isinstance(author, dict):
        name = author.get('name')

        # Case only team is defined. Means author is a team
        team = author.get('team')
        if name is None and team:
            name = '[Team] %s' % team

        # Email
        if kwds.get('show_email', show_all) is True:
            email = author.get('email')
        else:
            email = None

        if email:
            fmt_author = u'%s <%s>' % (name, email)
        else:
            fmt_author = name

        # Employer / Team
        employer = author.get('employer', None)
        team = author.get('team', None)
        if (employer and kwds.get('show_employerl', show_all)) or (team and kwds.get('show_team', show_all)):
            fmt_author += '['
            if employer and kwds.get('show_employer', show_all):
                fmt_author += 'Employer: %s' % (', '.join(employer))
            if team and kwds.get('show_team', show_all):
                fmt_author += ' Team: %s' % ', '.join(team)
            fmt_author += ']'

        # Note
        note = author.get('note')
        if note and kwds.get('show_note', show_all):
            fmt_author += ' (%s)' % note

    else:
        fmt_author = unicode(author)
    return fmt_author


def format_str(value, encoding='utf-8'):
    if isinstance(value, list):
        return u', '.join([format_str(v) for v in value])

    if isinstance(value, str):
        return value.decode(encoding)
    else:
        return unicode(value)


def can_display_criterion(criterion, value):
    if criterion.startswith('_'):
        return False
    elif criterion in ('implementation', 'name', 'name_conversion', 'identifier', 'tags', 'implement', 'criteria'):
        return False
    return True


def format_criterion(criterion, value, indent=0):
    istr = ' ' * indent
    if criterion == 'authors':
        s = '%sauthors:\n' % istr
        for author in value:
            s += istr + ' - %s (insitute: %s)\n' % (author.get('name', 'Anonymous'),
                                                    author.get('institute', 'not defined'))
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
        prefixes = ['openalea', 'oalab', 'vpltk']
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
                for plugin in pm.items(group):
                    interface = getattr(plugin, 'implement', None)
                    if interface:
                        plugin_groups.setdefault(interface, []).append(plugin)
                    else:
                        plugin_groups[UNDEF].append(plugin)
                for group, plugins in plugin_groups.items():
                    if not plugins:
                        continue
                    print '  implements: \033[91m%s\033[0m' % group
                    plugin_names = {}
                    for plugin in plugins:
                        plugin_names[plugin.name] = plugin
                    for pl_name in sorted(plugin_names):
                        plugin = plugin_names[pl_name]
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
