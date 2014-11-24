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


import os
from os.path import expanduser, join, exists
from openalea.core.singleton import Singleton
import openalea.misc

import sphinx.application
from sphinx.application import Sphinx
from sphinx.domains.python import PythonDomain
from sphinx.builders.html import StandaloneHTMLBuilder
from sphinx.writers.html import HTMLWriter
from sphinx.util.osutil import SEP, relative_uri

from docutils.readers.doctree import Reader as DoctreeReader
from docutils.writers.html4css1 import Writer
from docutils.core import Publisher
from docutils.io import StringInput, StringOutput, DocTreeInput
from docutils.readers.doctree import Reader
from docutils import frontend
from docutils import languages
from docutils import parsers
from docutils import utils, nodes
from docutils.parsers.rst import roles

sphinx.application.CONFIG_FILENAME="sphinx_configuration.py"

class Builder(StandaloneHTMLBuilder):
    def write_doc(self, docname, doctree):
        destination = StringOutput(encoding='utf-8')

        doctree.settings = self.docsettings

        self.secnumbers = self.env.toc_secnumbers.get(docname, {})
        self.imgpath = relative_uri(self.get_target_uri(docname), '_images')
        self.post_process_images(doctree)
        self.dlpath = relative_uri(self.get_target_uri(docname), '_downloads')
        self.docwriter.write(doctree, destination)
        self.docwriter.assemble_parts()
        body = self.docwriter.parts['fragment']
        metatags = self.docwriter.clean_meta
        return destination

class App(Sphinx):
    on_the_fly_doc_dir = expanduser(join("~",
                                         ".openalea",
                                         "otfDoc"))
    def __init__(self):
        if not exists(self.on_the_fly_doc_dir):
            os.mkdir(self.on_the_fly_doc_dir)

        Sphinx.__init__(self,
                        srcdir      = self.on_the_fly_doc_dir,
                        confdir     = openalea.misc.__path__[0],
                        outdir      = self.on_the_fly_doc_dir,
                        doctreedir  = self.on_the_fly_doc_dir,
                        buildername = None,
                        freshenv    = True)


    def warn(self, *args, **kwargs):
        pass
    info = warn

    def _init_env(self, freshenv):
        from sphinx.environment import BuildEnvironment
        if freshenv:
            self.env = BuildEnvironment(self.srcdir, self.doctreedir,
                                        self.config)
            for domain in self.domains.keys():
                self.env.domains[domain] = self.domains[domain](self.env)

    def _init_builder(self, bname):
        self.builder = Builder(self)
        self.emit('builder-inited')



__app = App()
__app.env.set_warnfunc = __app.warn
for k, v in PythonDomain.roles.iteritems():
    roles.register_local_role(k, v)

def aFunction(string):
    source  = StringInput(string, encoding='utf-8')
    docname = "fake"
    __app.env.temp_data['docname'] = docname

    settings = frontend.OptionParser((Writer,)).get_default_values()
    settings.tab_width = 8
    settings.pep_references = False
    settings.rfc_references = False
    settings.env = __app.env

    reader = DoctreeReader()
    parser = parsers.get_parser_class("rst")()

    docu   = utils.new_document(source.source_path, settings)
    parser.parse(source.read(), docu)
    __app.builder.prepare_writing((docname,))
    return __app.builder.write_doc(docname, docu).destination

