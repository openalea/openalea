# -*- python -*-
#
#       OpenAleaLab
#
#       Copyright 2015 INRIA
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
import openalea.oalab
import random

from Qt import QtGui, QtWidgets, QtCompat

from openalea.oalab.pluginwidget.explorer import PluginExplorer

from openalea.deploy.shared_data import shared_data
from openalea.core.formatting.util import icon_path
from openalea.core.formatting.html import html_section, html_list
from openalea.core.plugin.formatting.text import format_author
from openalea.core import authors as auth

if QtCompat.__binding__ == 'pyqt':
    try:
        from PyQt4.QtWebKit import QWebView
        VIEW = "webkit"
    except ImportError:
        QWebView = QtWidgets.QTextEdit
        VIEW = "basic"
elif QtCompat.__binding__ == 'pyside':
    try:
        from PySide.QtWebKit import QWebView
        VIEW = "webkit"
    except ImportError:
        QWebView = QtWidgets.QTextEdit
        VIEW = "basic"
else:
    QWebView = QtWidgets.QTextEdit
    VIEW = "basic"

stylesheet_path = shared_data(openalea.core, 'stylesheet.css')

if VIEW == "webkit":
    stylesheet_path = 'file://' + stylesheet_path

dependencies = dict(
    vtk=dict(
        team=u'VTK',
        icon=u'vtk.png',
        website=u'http://vtk.org'
    ),

    pyqode=dict(
        authors=[u'Colin Duquesnoy'],
        team=u'PyQode',
        icon=u'pyqode.png',
        website=u'http://github.com/pyQode/pyQode',
        license=u'MIT',
    ),

    qt=dict(
        team=u'Qt',
        icon=u'qt.png',
        website=u'http://qt.io'
    ),

    pyqt=dict(
        team=u'PyQt',
        icon=u'pyqt.png',
        website=u'http://www.riverbankcomputing.com'
    ),

    git=dict(
        team=u'Git',
        icon=u'git.png',
        website=u'https://git-scm.com'
    ),

)

scientific = ['ipython', 'matplotlib', 'numpy', 'pandas', 'scipy', 'python']
for lib in scientific:
    dependencies[lib] = dict(team=lib.capitalize(), icon=u'%s.png' % lib, website=u'http://%s.org' % lib)

dep_order = 'python qt pyqt ipython pyqode numpy matplotlib scipy pandas git vtk'.split()

lst = [
    'openalea',
    'caribu'
    'PlantGL',
]

submodules = html_list('submodule', lst)

if VIEW == "webkit":
    html_dep = '<br />'
    width = 70
    for i, dep_name in enumerate(dep_order):
        dep = dependencies[dep_name]
        args = {}
        args.update(dep)
        icon_path = 'file://' + shared_data(openalea.oalab, 'icons/logo/%s' % dep["icon"])
        args.update(dict(x=i * width, icon=icon_path, width=width))
        html_dep += '<div style="width:%(width)dpx; float:left; text-align:center; padding-bottom:10px;">\n' % args
        html_dep += '  <img height="32px" src="%(icon)s" alt="%(team)s">\n' % args
        html_dep += '  <br /><span class="logo-label"><a href="%(website)s">%(team)s</a></span>\n' % args
        html_dep += '</div>\n' % args
else:
    html_dep = ''
    width = 70
    deps = []
    for i, dep_name in enumerate(dep_order):
        dep = dependencies[dep_name]
        args = {}
        args.update(dep)
        icon_path = shared_data(openalea.oalab, 'icons/logo/%s' % dep["icon"])
        args.update(dict(x=i * width, icon=icon_path, width=width))
        deps.append('<span class="logo-label"><a href="%(website)s">%(team)s</a></span>\n' % args)
    html_dep += html_list('dependencies', deps)

args = dict(
    stylesheet=stylesheet_path,
    dependencies=html_dep,
    submodules=submodules,
)

WELCOME = """
<html>
<head>
    <link rel="stylesheet" type="text/css" href="%(stylesheet)s">
</head>

<body>
<h2 class="subtitle">OpenAleaLab</h2>
<p class="introduction">
The OpenAleaLab is an opensource integrated software platform for numerical simulation and especially plant modeling.
It makes it possible to upload plant models, manipulate them, or create new models by simulation.

<br />
Different labs are available, each one responding to scientific field:
<br />
<b>PlantLab</b> is designed for whole plant modeling. It embeds various tools like MTG standard plant format, L-system programming (L-Py),
light models (Caribu, muSlim, etc.), ...
<br />

<b>TissueLab</b> is designed for tissue modeling. It embeds various tools like 3D image viewer, mars-alt pipeline, ...
<br />

</p>

<h2 class="subtitle">OpenAlea</h2>
<p class="introduction">
OpenAlea is a distributed collaborative effort to develop Python libraries and tools that address the needs of current
and future works primarily designed for the plant architecture modeling.
</p>

<br />

<div class="section-title">Code is powered by</div>
%(dependencies)s

</body>

</html>
""" % args

author_lst = [
    auth.gbaty,
    auth.fboudon,
    auth.jchopard,
    auth.tcokelaer,
    auth.dbarbeau,
    auth.sdufourko,
    auth.gcerutti,
    auth.cgodin,
    auth.jcoste,
    auth.emoscardi,
    auth.pfernique,
    auth.cpradal,
]

random.shuffle(author_lst)

authors = ', '.join([format_author(author) for author in author_lst])
args['authors'] = authors

CREDITS = """
<html>
<head>
    <link rel="stylesheet" type="text/css" href="%(stylesheet)s">
</head>

<body>
<h2 class="subtitle">OpenAleaLab</h2>
<p class="introduction">Platform is written by (random order) ... </p>

%(authors)s

<p class="introduction">Components are written by numerous authors, see "Plugins" tab for more information</p>

</body>

</html>

""" % args

class AboutPage(QtWidgets.QWidget):

    def __init__(self, banner_path=None, content=None):
        QtWidgets.QWidget.__init__(self)

        if banner_path is None:
            banner_path = shared_data(openalea.oalab, 'icons/logo/banner.png')

        self._lay = QtWidgets.QVBoxLayout(self)

        p = QtWidgets.QSizePolicy

        self._banner = QtWidgets.QLabel()
        self._banner.setStyleSheet("QLabel { background-color : #ffffff;}")
        banner = QtGui.QPixmap(banner_path)
        size = banner.size()
        self._banner.setPixmap(banner)

        self._content = QWebView()
        if hasattr(self._content, "setReadOnly"):
            self._content.setReadOnly(True)
        self._content.setHtml(content)

        self._footer = QtWidgets.QLabel()
        self._footer.setStyleSheet("QLabel { background-color : #459454;}")

        self._lay.addWidget(self._banner)
        self._lay.addWidget(self._content)
        self._lay.addWidget(self._footer)
        self._lay.setContentsMargins(0, 0, 0, 0)
        self._lay.setSpacing(0)


class OpenAleaLabSummary(AboutPage):

    def __init__(self):
        AboutPage.__init__(self, content=WELCOME)


class OpenAleaLabCredits(AboutPage):

    def __init__(self):
        AboutPage.__init__(self, content=CREDITS)


class About(QtWidgets.QTabWidget):

    def __init__(self):
        QtWidgets.QTabWidget.__init__(self)

        self._welcome = OpenAleaLabSummary()
        self._plugin = PluginExplorer()
        self._plugin.groupby(filter_name="dist")

        self._credits = OpenAleaLabCredits()

        self.addTab(self._welcome, "About")
        self.addTab(self._credits, "Credits")
        self.addTab(self._plugin, "Plugins")

        size = self._welcome.size()
        self._credits.resize(size.width(), 600)
        self.resize(size.width(), 600)
        self.setContentsMargins(10, 10, 10, 10)


if __name__ == '__main__':

    instance = QtWidgets.QApplication.instance()

    if instance is None:
        app = QtWidgets.QApplication([])
    else:
        app = instance

    from openalea.oalab.utils import ModalDialog

    about = About()
    dialog = ModalDialog(about)
    dialog.show()

    if instance is None:
        app.exec_()
