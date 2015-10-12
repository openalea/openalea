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
from openalea.core.service.plugin import plugin


def node_factory(plugin_name, group=None, name=None, category=None):
    _plugin = plugin(plugin_name, group=group)
    name = name if name else _plugin.name
    factory = Factory(name=name, category=category,
                      inputs=_plugin.inputs, outputs=_plugin.outputs,
                      nodemodule=_plugin.modulename,
                      nodeclass=_plugin.objectname,
                      )
    return factory
