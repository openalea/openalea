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

    This function uses docutils. Ideally it should use Sphinx. Consequently
    many directives are notunderstood and even rise many error messages.
    In order to prevent such messages, the cleanup method remove them.


    :param text: the docstring

    :returns: text in HTML format

    .. todo:: implement conversion with Sphinx to have all SPhinx's directives interpreted.
    """
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



class HelpWidget( QtGui.QTextBrowser ):

    def __init__(self, parent=None):
        QtGui.QTextBrowser.__init__(self, parent)
        self.setTextInteractionFlags(QtCore.Qt.TextBrowserInteraction)
        self.setOpenExternalLinks(True)
        self.css = None

    def set_rst(self, txt):
        if self.css:
            print "I have a css!"
            self.document().setDefaultStyleSheet(self.css)
        txt = rst2alea(txt)
        self.setHtml(txt)

    def set_stylesheet_file(self, file):
        try:
            f = open(file)
            self.css = f.read()
            f.close()
        except Exception, e:
            print e


