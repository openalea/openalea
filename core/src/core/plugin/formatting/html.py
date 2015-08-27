# -*- coding: utf-8 -*-
# -*- python -*-
#
#       OpenAleaLab
#
#       Copyright 2015 INRIA-CIRAD-INRA
#
#       File author(s): Guillaume Baty <guillaume.baty@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.github.io
#
###############################################################################
import openalea.core

from openalea.deploy.shared_data import shared_data
from openalea.core.formatting.util import icon_path
from openalea.core.formatting.html import html_section, html_list
from openalea.core.plugin.formatting.util import DEFAULT_ICON
from openalea.core.plugin.formatting.text import format_str, format_author
stylesheet_path = shared_data(openalea.core, 'stylesheet.css')

html_header = u'\n'.join([
    u'<html>',
    u'<head>',
    u'  <link rel="stylesheet" type="text/css" href="%s">' % stylesheet_path,
    u'  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">',
    u'</head>'])

html_footer = u'</html>'


def format_html(value, key=None):
    return format_str(value)


def html_summary(item):
    if hasattr(item, 'icon'):
        p = icon_path(item.icon, default=DEFAULT_ICON, packages=[openalea.core, openalea.oalab])
        image = u'<img style="vertical-align:middle;" src="%s" width="128" />'
    else:
        image = u''
    args = dict(image=image, title=format_html(item.label), name=format_html(item.name))
    html = u'<div class="summary"><p class="title"> %(image)s' % args
    html += u'%(title)s</p>' % args
    html += u'\n<hr>'

    criteria = item.criteria

    # Crédits
    items = []
    for label in ('author', 'authors'):
        value = criteria.get(label, 'None')
        if not value:
            continue
        if not isinstance(value, (list, tuple, set)):
            value = [value]
        for author in value:
            if author and author != "None":
                items.append(format_author(author, key=label))

    items.sort()
    html += html_section(u'credits', u'Credits', items)

    # Criteria
    items = []
    for label, value in item.criteria.items():
        if label in ('icon', 'author', 'authors') or not value:
            continue
        items.append(
            u'<span class="key">%s</span>: <span class="value">%s</span>\n' %
            (format_html(label).capitalize(), format_html(value, key=label)))
    html += html_section(u'criteria', u'Criteria', items)

    # Tags
    items = []
    for tag in item.tags:
        items.append(u'<span class="key">%s</span>\n' % tag)
    html += html_section(u'tags', u'Tags', items)

    html += u'</div>'
    return html
