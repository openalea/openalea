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

import itertools

from openalea.core.service.plugin import plugins
from openalea.core.singleton import Singleton


class MimeCodecManager(object):
    __metaclass__ = Singleton

    def __init__(self):
        self._registry_decode = set()
        self._registry_decode_plugin = {}

        self._registry_encode = set()
        self._registry_encode_plugin = {}

    def init(self):
        self._registry_decode = set()
        self._registry_decode_plugin = {}

        self._registry_encode = set()
        self._registry_encode_plugin = {}

        for plugin in plugins('oalab.plugin', criteria=dict(implement='IQMimeCodec')):
            for k, v in plugin.qtdecode:
                codec = (unicode(k), unicode(v))
                self._registry_decode.add(codec)
                self._registry_decode_plugin[codec] = plugin
            for k, v in plugin.qtencode:
                codec = (unicode(k), unicode(v))
                self._registry_encode.add(codec)
                self._registry_encode_plugin[codec] = plugin

    def _mimelist(self, mimetype_list, keyidx):
        if mimetype_list is None:
            mimetype_list = [k[keyidx] for k in self._registry_decode]
        elif isinstance(mimetype_list, basestring):
            mimetype_list = [mimetype_list]
        else:
            mimetype_list = [mime for mime in mimetype_list]
        return mimetype_list

    def compatible_mime(self, mimetype_in_list, mimetype_out_list):
        mimetype_in_list = self._mimelist(mimetype_in_list, 0)
        mimetype_out_list = self._mimelist(mimetype_out_list, 1)
        wish = set(itertools.product(mimetype_in_list, mimetype_out_list))
        existing = set(self._registry_decode)
        res = []
        for wk, wv in wish:
            for ek, ev in existing:
                if wk == ek and wv.startswith(ev):
                    res.append((ek, ev))
        return res

    def possible_conv(self, data, mimetype):
        _possible_conv = {}
        for k, g in itertools.groupby(self._registry_encode, lambda data: data[0]):
            _possible_conv[k] = list(g)
        return _possible_conv

    def is_compatible(self, mimetype_in_list=None, mimetype_out_list=None):
        return bool(self.compatible_mime(mimetype_in_list, mimetype_out_list))

    def _decode(self, funcname, mimedata, mimetype_in, mimetype_out):
        try:
            plugin = self._registry_decode_plugin[(mimetype_in, mimetype_out)]
        except KeyError:
            return None, {}
        else:
            klass = plugin.implementation
            decoder = klass()
            # decoder.decode(mimedata, ...)
            return getattr(decoder, funcname)(mimedata, mimetype_in, mimetype_out)

    def decode(self, mimedata, mimetype_in, mimetype_out):
        return self._decode('decode', mimedata, mimetype_in, mimetype_out)

    def qtdecode(self, mimedata, mimetype_in, mimetype_out):
        return self._decode('qtdecode', mimedata, mimetype_in, mimetype_out)

    def quick_check(self, mimedata, mimetype_in, mimetype_out):
        return self._decode('quick_check', mimedata, mimetype_in, mimetype_out)

    def encode(self, data, mimetype_in, mimetype_out):
        try:
            plugin = self._registry_encode_plugin[(mimetype_in, mimetype_out)]
        except KeyError:
            return None, {}
        else:
            klass = plugin.implementation
            decoder = klass()
            # decoder.decode(mimedata, ...)
            return getattr(decoder, 'encode')(data, mimetype_in, mimetype_out)

    def qtencode(self, data, qmimedata, mimetype_in, mimetype_out):
        try:
            plugin = self._registry_encode_plugin[(mimetype_in, mimetype_out)]
        except KeyError:
            return None, {}
        else:
            klass = plugin.implementation
            decoder = klass()
            # decoder.decode(mimedata, ...)
            return getattr(decoder, 'qtencode')(data, qmimedata, mimetype_in, mimetype_out)
