# -*- coding: utf-8 -*-
# -*- python -*-
#
#
#       OpenAlea.OALab: Multi-Paradigm GUI
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
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################


from openalea.core.plugin import PluginDef


@PluginDef
class RFile(object):
    implement = 'IData'

    default_name = "R"
    default_file_name = "script.r"
    pattern = "*.r"
    extension = "r"
    icon = ":/images/resources/RLogo.png"
    mimetype = "text/x-r"

    def __call__(self):
        from openalea.oalab.model.r import RFile
        return RFile


@PluginDef
class RModel(object):
    implement = 'IModel'

    default_name = "R"
    icon = ":/images/resources/RLogo.png"
    mimetype = "text/x-r"
    dtype = default_name

    def __call__(self):
        from openalea.oalab.model.r import RModel
        return RModel


@PluginDef
class VisualeaFile(object):
    implement = 'IData'

    default_name = "Workflow"
    default_file_name = "workflow.wpy"
    pattern = "*.wpy"
    extension = "wpy"
    icon = ":/images/resources/openalealogo.png"
    dtype = default_name
    mimetype = "text/x-visualea"

    def __call__(self):
        from openalea.oalab.model.visualea import VisualeaFile
        return VisualeaFile


@PluginDef
class VisualeaModel(object):
    implement = 'IModel'

    default_name = "Workflow"
    icon = ":/images/resources/openalealogo.png"
    mimetype = "text/x-visualea"
    dtype = default_name

    def __call__(self):
        from openalea.oalab.model.visualea import VisualeaModel
        return VisualeaModel
