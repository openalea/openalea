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

from openalea.core.path import path
from openalea.core.service.data import get_data

from openalea.oalab.mimedata import QMimeCodec


class UrlCodec(QMimeCodec):

    def qtdecode(self, mimedata, mimetype_in, mimetype_out):
        kwds = {}
        if mimetype_in == 'text/uri-list':
            raw_data = [url.toLocalFile() for url in mimedata.urls()]
        else:
            return None, {}
        return self.decode(raw_data, mimetype_in, mimetype_out, **kwds)

    def decode(self, raw_data, mimetype_in, mimetype_out, **kwds):
        """
        raw_data: list of urls
        """
        if mimetype_in == 'text/uri-list':
            for url in raw_data:
                local_file = path(url)
                return local_file, dict(path=local_file, name=local_file.namebase)
        else:
            return None, {}


class BuiltinControlCodec(QMimeCodec):

    """
    Decode: openalealab/control (mime) -> Control, name, identifier, code oalab, ...
    Encode: openalealab/control (Control) -> openalealab/control (mime)
    """

    def _decode_control(self, raw_data):
        """
        raw_data: str id;name
        """
        from openalea.core.service.control import get_control_by_id
        identifier, name = raw_data.data().split(';')
        control = get_control_by_id(identifier)
        if control.name != name:
            return None
        else:
            return control

    def encode(self, data, mimetype_in, mimetype_out):
        return ('openalealab/control', '%s;%s' % (data.identifier, data.name))

    def decode(self, raw_data, mimetype_in, mimetype_out):
        if mimetype_in != 'openalealab/control':
            return None, {}

        control = self._decode_control(raw_data)

        if control is None:
            return None, {}

        if mimetype_out == "openalealab/control":
            return control, {}
        elif mimetype_out == "openalea/identifier":
            return control.name, {}
        elif mimetype_out == "openalea/code.oalab":
            varname = '_'.join(control.name.split())
            pycode = '%s = get_control(%r) #%s' % (varname, control.name, control.interface)
            return pycode, {}
        else:
            return control, {}


class BuiltinDataCodec(QMimeCodec):

    def decode(self, raw_data, mimetype_in, mimetype_out):
        if mimetype_in != 'openalealab/data':
            return None, {}

        print repr(raw_data)
        data = get_data(raw_data.name)

        if mimetype_out == "openalealab/data":
            return data, {}
        elif mimetype_out == "openalea/identifier":
            return data.name, {}
        elif mimetype_out == "openalea/code.oalab":
            varname = '_'.join(data.name.split())
            pycode = '%s = get_data(%r)' % (varname, data.name)
            return pycode, {}
        else:
            return data, {}


#-        elif source.hasFormat('openalealab/omero'):
#-            data = decode('openalealab/omero', source.data('openalealab/omero'))
#-            if data is None:
#-                return
#-            name = data.split('=')[0]
#-            uri = '='.join(data.split('=')[1:])
