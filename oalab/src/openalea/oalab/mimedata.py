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

from openalea.core.customexception import CustomException
from openalea.core.singleton import Singleton


class MimeConversionError(CustomException):
    title = u'Error: this data cannot be dropped here'
    message = u'%(data)s (%(mimetype_in)s) cannot be converted to %(mimetype_out)s'
    desc = "\n".join([
        "This error is raised because the data format dropped ",
        "is not supported by application or not completely supported",
        "System raised: \n%(exception)s"
    ])

    def _kargs(self):
        return dict(
            data=unicode(self._args[0].__class__.__name__),
            mimetype_in=self._args[1],
            mimetype_out=unicode(self._args[2]),
            exception=self._args[3]
        )


class MimeCodec(object):

    def quick_check(self, mimedata, mimetype_in, mimetype_out):
        return True

    def encode(self, data, mimetype_in, mimetype_out):
        return ('openalealab/control', '%s;%s' % (data.identifier, data.name))

    def decode(self, rawdata, mimetype_in, mimetype_out):
        """
        NO Qt HERE !
        """
        pass


from openalea.vpltk.qt import QtCore


class QMimeCodec(MimeCodec):

    def _raw_data(self, mimedata, mimetype_in, mimetype_out):
        return str(mimedata.data(mimetype_in))

    def qtdecode(self, mimedata, mimetype_in, mimetype_out):
        """
        QMimeData -> data
        """
        raw_data = self._raw_data(mimedata, mimetype_in, mimetype_out)
        if raw_data is None:
            return None, {}
        else:
            return self.decode(raw_data, mimetype_in, mimetype_out)

    def qtencode(self, data, qmimedata, mimetype_in, mimetype_out):
        """
        data -> QMimeData
        """
        mimetype, mimedata = self.encode(data, mimetype_in, mimetype_out)
        qmimedata.setData(mimetype, mimedata)
        return qmimedata


class MimeCodecPlugin(object):
    decode = {}
    encode = {}


class QMimeCodecPlugin(object):
    qtdecode = {}
    qtencode = {}


class MimeCodecManager(object):
    __metaclass__ = Singleton

    def __init__(self):
        self._registry_decode = set()
        self._registry_decode_plugin = {}

        self._registry_encode = set()
        self._registry_encode_plugin = {}

    def init(self):
        from openalea.core.plugin.manager import PluginManager
        pm = PluginManager()
        pm.discover('openalea.plugin')
        for plugin in pm.plugins('openalea.codec.mimetype'):
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

    def is_compatible(self, mimetype_in_list=None, mimetype_out_list=None):
        return bool(self.compatible_mime(mimetype_in_list, mimetype_out_list))

    def _decode(self, funcname, mimedata, mimetype_in, mimetype_out):
        try:
            plugin = self._registry_decode_plugin[(mimetype_in, mimetype_out)]
        except KeyError:
            return None, {}
        else:
            klass = plugin()()
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
            klass = plugin()()
            decoder = klass()
            # decoder.decode(mimedata, ...)
            return getattr(decoder, 'encode')(data, mimetype_in, mimetype_out)

    def qtencode(self, data, qmimedata, mimetype_in, mimetype_out):
        try:
            plugin = self._registry_encode_plugin[(mimetype_in, mimetype_out)]
        except KeyError:
            return None, {}
        else:
            klass = plugin()()
            decoder = klass()
            # decoder.decode(mimedata, ...)
            return getattr(decoder, 'qtencode')(data, qmimedata, mimetype_in, mimetype_out)
