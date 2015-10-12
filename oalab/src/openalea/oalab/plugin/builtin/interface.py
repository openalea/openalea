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


from openalea.core.plugin import PluginDef


@PluginDef
class OpenAleaLabInterfacePlugin(object):
    implement = 'IInterface'

    def __call__(self):

        from openalea.oalab.plugin.applet import IApplet
        from openalea.oalab.interface import IColormap, IIntRange

        return [IColormap, IIntRange, IApplet]
