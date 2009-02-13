# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#                       Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
"""Export application functions"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "


import os
import string


def export_app(name, filename, cn_factory):
    """Export application

    :param name: name of the application
    :param filename: python file to write$
    :param cn_factory:  composite node factory
    """

    # Read template
    dir = os.path.dirname(__file__)
    template_fn = os.path.join(dir, "template_app.txt")
    f = open(template_fn, "r")

    template = f.read()
    f.close()

    #todo replace this line so as to remove string import that is deprecated
    template_str = string.Template(template)

    import version as versionmodule
    import time

    try:
        info = cn_factory.package.metainfo
    except:
        info = {}

    authors = info.get('authors', "")
    license = info.get('license', "")
    version = info.get('version', "")
    doc = cn_factory.doc

    writer = code = cn_factory.get_writer()
    code = repr(writer)
    fname = cn_factory.get_python_name()

    # Replace value
    result = template_str.safe_substitute(
        OPENALEA_VERSION=versionmodule.version,
        DATE=time.asctime(time.localtime()),
        NAME=name,
        AUTHOR=authors,
        LICENSE=license,
        VERSION=version,
        DOC=doc,
        FACTORY_CODE=code,
        FACTORY_NAME=fname,
        )

    # write file
    f = open(filename, "w")
    f.write(result)
    f.close()
