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

from openalea.core.formatting.html import html_section
from openalea.core.formatting.util import obj_icon_path, icon_path, pretty_print


def html_item_summary(project):
    excluded_categories = ['cache', 'world']

    html = ''
    # Loop on all categories available in this project
    for category, desc in project.categories.items():
        if category in excluded_categories:
            continue
        title = desc['title']
        items = project.items(category)
        if not items:
            continue

        html_items = []
        for item_name in sorted(items):
            model = items[item_name]
            html_items.append(
                '<span class="item"><span class="item-namebase">%s</span><span class="item-ext">%s</span></span>\n' % (
                    model.filename.namebase, model.filename.ext))
        html += html_section(category, title, html_items)
    return html


def html_metainfo_summary(project):
    items = [
        '<span class="key">Name</span>: <span class="value">%s</span>\n' % (project.name),
        '<span class="key">Path</span>: <span class="value">%s</span>\n' % (project.path)
    ]
    for label, value in project.metadata.items():
        if label in ('icon', 'alias') or not value:
            continue
        value = pretty_print(getattr(project, label))
        items.append(
            '<span class="key">%s</span>: <span class="value">%s</span>\n' %
            (label.capitalize(), value))
    return html_section('meta-information', 'Meta-information', items)


def html_project_summary(project):
    icon = obj_icon_path(project, paths=[project.path])
    if icon_path:
        image = '<img style="vertical-align:middle;" src="file://%s" width="128" />' % icon
    else:
        image = ''
    args = dict(image=image, title=project.title, name=project.name)
    html = '<div class="summary">%(image)s<p class="title">%(title)s</p>' % args
    html += '\n<hr>'
    html += html_metainfo_summary(project)
    html += html_item_summary(project)
    html += '</div>'
    return html
