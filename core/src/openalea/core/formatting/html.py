import openalea.core

from openalea.deploy.shared_data import shared_data
from openalea.core.path import path as Path


def html_list(identifier, items):
    html = '  <ul id="%s">\n' % identifier
    for item in items:
        html += '    <li>%s</li>\n' % item
    html += '  </ul>\n'
    return html


def html_section(identifier, title, items):
    html = ''
    html += '<div class="section" id="section-%s">\n' % identifier
    html += '<div class="section-title">%s</div>' % title
    html += html_list(identifier, items)
    html += "</div>"
    return html
