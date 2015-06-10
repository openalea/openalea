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

__all__ = ['add_drop_callback', 'add_drag_format', 'encode']

from openalea.oalab.gui.drag_and_drop import DragHandler, DropHandler, encode_to_qmimedata
from openalea.oalab.mimedata import MimeCodecManager

_drag_handler = {
}

_drop_handler = {
}

mm = MimeCodecManager()
mm.init()


def drop_handler(widget, **kwds):
    if widget not in _drop_handler:
        _drop_handler[widget] = DropHandler(widget, **kwds)

    return _drop_handler[widget]


def drag_handler(widget, **kwds):
    if widget not in _drag_handler:
        _drag_handler[widget] = DragHandler(widget, **kwds)

    return _drag_handler[widget]


def add_drop_callback(widget, mimetype, callback, **kwds):
    """
    :mimetype: a mimetype requested by widget
    """
    dnd = drop_handler(widget)
    dnd.add_drop_callback(mimetype, callback, **kwds)


def add_drag_format(widget, mimetype, **kwds):
    dnd = drag_handler(widget)
    dnd.add_drag_format(mimetype, **kwds)


def encode(data, mimetype_in, mimetype_out):
    return mm.encode(data, mimetype_in, mimetype_out)


def decode(raw_data, mimetype_in, mimetype_out):
    return mm.decode(raw_data, mimetype_in, mimetype_out)
