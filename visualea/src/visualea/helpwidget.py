# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright 2006-2010 INRIA - CIRAD - INRA
#
#       File author(s): Daniel Barbeau <daniel.barbeau@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################


from PyQt4 import QtGui, QtCore


def rst2alea(text=""):
    """Convert docstring into HTML (assuming docstring is in reST format)

    This function uses docutils. Ideally it should use Sphinx

    :param text: the docstring

    :returns: text in HTML format

    .. todo:: implement conversion with Sphinx to have all SPhinx's directives interpreted.
    """
    try:
        from docutils import core
        from docutils.writers.html4css1 import Writer
        w = Writer()
        res = core.publish_parts(text, writer=w)['html_body']
        return res
    except:
        res = '<i>For a better rendering, install docutils or sphinx !</i><br/>'
        if text is not None:
            res += text
        for name in [':Parameters:', ':Returns:', ':Keywords:', ':Author:', ':Authors:']:
            res = res.replace(name, '<b>'+name.replace(':','') + '</b>')
        res = res.replace('\n','<br />')
        return res



class HelpWidget( QtGui.QTextBrowser ):

    def __init__(self, parent=None):
        QtGui.QTextBrowser.__init__(self, parent)
        self.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.setOpenExternalLinks(True)

    def set_rst(self, txt):
        txt = rst2alea(txt)
        self.setHtml(txt)
