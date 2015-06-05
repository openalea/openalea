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

from openalea.oalab.mimedata import QMimeCodecPlugin


class UrlCodecPlugin(QMimeCodecPlugin):
    qtdecode = [
        ('text/uri-list', 'openalea/interface.IPath'),
    ]

    def __call__(self):
        from openalea.oalab.plugins.mimedata.codec import UrlCodec
        return UrlCodec


class BuiltinControlCodecPlugin(QMimeCodecPlugin):
    qtdecode = [
        ('openalealab/control', 'openalealab/control'),
        ('openalealab/control', 'openalea/code.oalab'),
        ('openalealab/control', 'openalea/identifier'),
    ]

    def __call__(self):
        from openalea.oalab.plugins.mimedata.codec import BuiltinControlCodec
        return BuiltinControlCodec


class BuiltinDataCodecPlugin(QMimeCodecPlugin):
    qtdecode = [
        ('openalealab/data', 'openalealab/data'),
        ('openalealab/data', 'openalea/code.oalab'),
        ('openalealab/data', 'openalea/identifier'),
    ]

    def __call__(self):
        from openalea.oalab.plugins.mimedata.codec import BuiltinDataCodec
        return BuiltinDataCodec


class BuiltinMimeDataCodecPlugin(object):
    category = 'openalea.codec.mimetype'
    plugins = [UrlCodecPlugin, BuiltinControlCodecPlugin, BuiltinDataCodecPlugin]
