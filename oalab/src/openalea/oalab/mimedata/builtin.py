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
from openalea.core.service.project import project_item
from urlparse import urlparse

from openalea.oalab.mimedata import QMimeCodec


def pyname(name):
    for sym in ["-", "+", "*", "/", "\"", "."]:
        name = name.replace(sym, '_')
    return str(name)


class UrlCodec(QMimeCodec):

    """
    decoding: text/uri-list -> path
    encoding: path -> text/uri-list
    """

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


def encode_project_item(category, data, mimetype_in, mimetype_out):
    # openalea://user@localhost:/project/projectname/data/dataname
    uri = 'openalea://user@localhost:/%s/%s/%s' % (None, category, data.name)
    return ('openalealab/%s' % category, uri)


def decode_project_item(raw_data, mimetype_in, mimetype_out):
    pkg_type, pkg_name, category, name = urlparse(raw_data).path.split('/')
    return project_item(None, category, name)


class BuiltinModelCodec(QMimeCodec):

    def encode(self, data, mimetype_in, mimetype_out):
        return encode_project_item('model', data, mimetype_in, mimetype_out)

    def decode(self, raw_data, mimetype_in, mimetype_out):
        if mimetype_in != 'openalealab/model':
            return None, {}

        data = decode_project_item(raw_data, mimetype_in, mimetype_out)
        kwds = dict(name=str(data.name), path=(data.path))

        if mimetype_out == "openalealab/model":
            return data, kwds
        elif mimetype_out == "openalea/identifier":
            return data.name, kwds
        elif mimetype_out == "openalea/code.oalab.get":
            pycode = '%s = get_model(%r)' % (pyname(data.name), str(data.name))
            return pycode, kwds
        else:
            raise NotImplementedError(mimetype_out)


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
        identifier, name = raw_data.split(';')
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
        elif mimetype_out == "openalea/code.oalab.get":
            varname = '_'.join(control.name.split())
            pycode = '%s = get_control(%r) #%s' % (varname, control.name, control.interface)
            return pycode, {}
        elif mimetype_out == "openalea/code.oalab.create":
            varname = '_'.join(control.name.split())
            pycode = '%s = new_control(%s, %s, %s)' % (varname, control.name, control.interface, control.value)
            return pycode, {}
        else:
            return control, {}


class BuiltinDataCodec(QMimeCodec):

    def encode(self, data, mimetype_in, mimetype_out):
        return encode_project_item("data", data, mimetype_in, mimetype_out)

    def decode(self, raw_data, mimetype_in, mimetype_out):
        if mimetype_in != 'openalealab/data':
            return None, {}

        data = decode_project_item(raw_data, mimetype_in, mimetype_out)
        kwds = dict(name=str(data.name), path=(data.path))

        if mimetype_out == "openalealab/data":
            return data, kwds
        elif mimetype_out == "openalea/identifier":
            return data.name, kwds
        elif mimetype_out == "openalea/code.oalab.get":
            pycode = '%s = data / %r' % (pyname(data.name), str(data.name))
            return pycode, kwds
        else:
            return data, kwds
