# -*- coding: utf-8 -*-
# -*- python -*-
#
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Baty <guillaume.baty@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

from openalea.core.path import path as Path


def get(uri, path=None, force=False):
    """
    If path is specified, save data to path if not yet exists.
    """
    protocol, uri = uri.split('://')
    from openalea.core.service.plugin import plugin_instance
    db = plugin_instance('oalab.db', protocol)
    if db:
        return db.get(uri, path, force)
