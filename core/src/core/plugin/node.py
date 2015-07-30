# -*- coding: utf-8 -*-
# -*- python -*-
#
#
#       Copyright 2015 INRIA - CIRAD - INRA
#
#       File author(s): Guillaume Baty <guillaume.baty@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
###############################################################################

from openalea.core.node import Factory
from openalea.core.plugin.manager import generate_plugin_name


def node_factory(plugin_class, name=None, category=None):
    plugin = plugin_class()
    if name is None:
        name = generate_plugin_name(plugin)
    return Factory(name=name, category=category,
                   inputs=plugin.inputs, outputs=plugin.outputs,
                   nodemodule=plugin.modulename,
                   nodeclass=plugin.objectname,
                   )
