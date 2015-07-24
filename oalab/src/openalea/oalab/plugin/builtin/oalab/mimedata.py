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
from openalea.oalab.mimedata import QMimeCodecPlugin


@PluginDef
class UrlCodecPlugin(QMimeCodecPlugin):
    qtdecode = [
        ('text/uri-list', 'openalea/interface.IPath'),
    ]

    def __call__(self):
        from openalea.oalab.mimedata.codec import UrlCodec
        return UrlCodec


@PluginDef
class BuiltinControlCodecPlugin(QMimeCodecPlugin):
    qtdecode = [
        ('openalealab/control', 'openalealab/control'),
        ('openalealab/control', 'openalea/identifier'),
        ('openalealab/control', 'openalea/code.oalab.get'),
        ('openalealab/control', 'openalea/code.oalab.create'),
    ]

    qtencode = [
        ('openalealab/control', 'openalealab/control')
    ]

    mimetype_desc = {
        'openalea/code.oalab.get': dict(title='Python code (Get existing control)'),
        'openalea/code.oalab.create': dict(title='Python code (Create new control)'),
        'openalea/identifier': dict(title='Name')
    }

    def __call__(self):
        from openalea.oalab.mimedata.builtin import BuiltinControlCodec
        return BuiltinControlCodec


@PluginDef
class BuiltinDataCodecPlugin(QMimeCodecPlugin):
    qtdecode = [
        ('openalealab/data', 'openalealab/data'),
        ('openalealab/data', 'openalea/identifier'),
        ('openalealab/data', 'openalea/code.oalab.get'),
    ]
    qtencode = [
        ('openalealab/data', 'openalealab/data')
    ]

    mimetype_desc = {
        'openalea/code.oalab.get': dict(title='Python Code (Data path)'),
        'openalea/identifier': dict(title='Data Name'),
    }

    def __call__(self):
        from openalea.oalab.mimedata.builtin import BuiltinDataCodec
        return BuiltinDataCodec


@PluginDef
class BuiltinModelCodecPlugin(QMimeCodecPlugin):
    qtdecode = [
        ('openalealab/model', 'openalealab/model'),
        ('openalealab/model', 'openalea/identifier'),
        ('openalealab/model', 'openalea/code.oalab.get'),
    ]
    qtencode = [
        ('openalealab/model', 'openalealab/model')
    ]

    mimetype_desc = {
        'openalea/code.oalab.get': dict(title='Python Code (get model)'),
        'openalea/identifier': dict(title='Model Name'),
    }

    def __call__(self):
        from openalea.oalab.mimedata.builtin import BuiltinModelCodec
        return BuiltinModelCodec
