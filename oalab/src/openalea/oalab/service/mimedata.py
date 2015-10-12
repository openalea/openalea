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

__all__ = ['encode', 'decode', 'qtencode', 'qtdecode',
           'possible_conv', 'compatible_mime', 'quick_check',
           'decode_function', 'decode_plugin',
           'reload_drag_and_drop_plugins']


from openalea.oalab.mimedata import MimeCodecManager

_drag_handler = {
}

_drop_handler = {
}

mm = MimeCodecManager()
mm.init()


def encode(data, mimetype_in, mimetype_out):
    return mm.encode(data, mimetype_in, mimetype_out)


def decode(raw_data, mimetype_in, mimetype_out):
    return mm.decode(raw_data, mimetype_in, mimetype_out)


def reload_drag_and_drop_plugins():
    mm.init()


possible_conv = mm.possible_conv
qtencode = mm.qtencode
qtdecode = mm.qtdecode
compatible_mime = mm.compatible_mime
quick_check = mm.quick_check


def decode_function(mimetype_out):
    for conv in mm._registry_decode:
        if conv[1].startswith(mimetype_out):
            return conv[1]


def decode_plugin(conv):
    return mm._registry_decode_plugin[conv]
