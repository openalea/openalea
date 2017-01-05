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

from Qt import QtCore, QtGui, QtWidgets

#from openalea.visualea import lightsphinx

def rst2alea(text=""):
    """Convert docstring into HTML (assuming docstring is in reST format)

    This function uses docutils. Ideally it should use Sphinx. Consequently
    many directives are notunderstood and even rise many error messages.
    In order to prevent such messages, the cleanup method remove them.


    :param text: the docstring

    :returns: text in HTML format

    .. todo:: implement conversion with Sphinx to have all SPhinx's directives interpreted.
    """

    # res = lightsphinx.aFunction(text)
    # return res

    def cleanup(text):
        newtext = ''
        for line in text.splitlines():
            if line.find('System Message')>=0 or line.find('Unknown directive')>=0:
                pass
            else:
                newtext += line + '\n'
        return newtext
    try:
        from docutils import core
        import docutils.core2
        import docutils.parsers.rst
        from openalea.misc.sphinx_configuration import extensions
        #for ext in extensions:
        #    docutils.parsers.rst.directives.register_directive('TestDirective', ext)

        from docutils.writers.html4css1 import Writer
        w = Writer()
        res = core.publish_parts(text, writer=w)['html_body']
        return cleanup(res)
    except:
        res = ''
        if text is not None:
            res += text
        for name in [':Parameters:', ':Returns:', ':Keywords:', ':Author:', ':Authors:']:
            res = res.replace(name, '<b>'+name.replace(':','') + '</b>')
        res = res.replace('\n','<br />')
        return cleanup(res)



import re
line_re = re.compile(r"^(.*?)", re.MULTILINE)
bold_re = re.compile(r"\*\*(.*?)\*\*")
bold2_re = re.compile(r":(.*?):")
#bold3_re = re.compile(r"\*\*(.*?)\*\*")

def simple_rst_to_html(rst):
    if not isinstance(rst, str):
        return ""
    html = line_re.sub(r'\1<br/>', rst)
    html = bold_re.sub(r'<b>\1</b>', html)
    html = bold2_re.sub(r'<b>\1</b>', html)
    #html = bold3_re.sub(r'<b>\1</b>', html)
    return html


class HelpWidget(QtWidgets.QTextBrowser ):

    def __init__(self, parent=None):
        QtWidgets.QTextBrowser.__init__(self, parent)
        self.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.setOpenExternalLinks(True)
        self.css = None

    def set_rst(self, txt):
        if self.css:
            self.document().setDefaultStyleSheet(self.css)
        txt = simple_rst_to_html(txt)
        self.setHtml(txt)

    def set_stylesheet_file(self, file):
        try:
            f = open(file)
            self.css = f.read()
            f.close()
        except Exception, e:
            pass
