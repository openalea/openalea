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

from openalea.vpltk.qt import QtGui
from openalea.oalab.pluginwidget.explorer import PluginExplorer

from openalea.deploy.shared_data import shared_data
from openalea.core.formatting.util import icon_path
from openalea.core.formatting.html import html_section, html_list

from openalea.vpltk.qt import QT_API
from openalea.vpltk.qt import QtGui


if QT_API == 'pyqt':
    try:
        from PyQt4.QtWebKit import QWebView
        VIEW = "webkit"
    except ImportError:
        QWebView = QtGui.QTextEdit
        VIEW = "basic"
elif QT_API == 'pyside':
    try:
        from PySide.QtWebKit import QWebView
        VIEW = "webkit"
    except ImportError:
        QWebView = QtGui.QTextEdit
        VIEW = "basic"
else:
    QWebView = QtGui.QTextEdit
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


dep_order = 'python qt pyqt ipython pyqode numpy matplotlib scipy pandas git'.split()


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


class OpenAleaLabAbout(QtGui.QWidget):

    def __init__(self):
        QtGui.QWidget.__init__(self)

        self._lay = QtGui.QVBoxLayout(self)

        p = QtGui.QSizePolicy

        self._banner = QtGui.QLabel()
        banner = QtGui.QPixmap(shared_data(openalea.oalab, 'icons/logo/banner.png'))
        size = banner.size()
        self._banner.setPixmap(banner)
        self._banner.setSizePolicy(p(p.Maximum, p.Maximum))
        self._banner.setMaximumHeight(size.height())
        self._banner.setMaximumWidth(size.width())

        self._content = QWebView()
        if hasattr(self._content, "setReadOnly"):
            self._content.setReadOnly(True)
        self._content.setHtml(WELCOME)

        self._footer = QtGui.QLabel()
        self._footer.setStyleSheet("QLabel { background-color : #459454;}")

        self._lay.addWidget(self._banner)
        self._lay.addWidget(self._content)
        self._lay.addWidget(self._footer)
        self._lay.setContentsMargins(0, 0, 0, 0)
        self._lay.setSpacing(0)


class About(QtGui.QTabWidget):

    def __init__(self):
        QtGui.QTabWidget.__init__(self)

        self._welcome = OpenAleaLabAbout()
        self._plugin = PluginExplorer()
        self._plugin.groupby(filter_name="dist")

        self._credits = QtGui.QLabel('Credits')

        self.addTab(self._welcome, "About")
        self.addTab(self._plugin, "Plugins")
        self.addTab(self._credits, "Credits")

        size = self._welcome.size()
        self.resize(size.width(), 775)
        self.setMaximumWidth(size.width())
        self.setContentsMargins(10, 10, 10, 10)


if __name__ == '__main__':

    instance = QtGui.QApplication.instance()

    if instance is None:
        app = QtGui.QApplication([])
    else:
        app = instance

    from openalea.oalab.utils import ModalDialog

    about = About()
    dialog = ModalDialog(about)
    dialog.show()

    if instance is None:
        app.exec_()
