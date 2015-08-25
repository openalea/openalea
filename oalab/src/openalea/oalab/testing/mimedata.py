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


from openalea.core.service.plugin import register_plugin
from openalea.oalab.mimedata import QMimeCodecPlugin
from openalea.oalab.mimedata.qcodec import QMimeCodec
from openalea.oalab.service.mimedata import reload_drag_and_drop_plugins


class SampleCustomData(object):

    def __init__(self, num, letter):
        self.num = num
        self.letter = letter

    def __repr__(self, ):
        return '%s(num=%r, letter=%r)' % (self.__class__.__name__, self.num, self.letter)


class SampleCustomDataCodec(QMimeCodec):

    def decode(self, raw_data, mimetype_in, mimetype_out):
        num, letter = raw_data.split(';')
        num = int(num)
        if mimetype_out == 'custom/data':
            data = SampleCustomData(num, letter)
        elif mimetype_out == 'openalealab/control':
            from openalea.core.control import Control
            data = Control(letter, 'IInt', num)
        elif mimetype_out == 'text/plain':
            data = 'customdata: %s, %s' % (letter, num)
        elif mimetype_out == 'text/plain.verbose':
            data = 'Custom data define these values:\n  - letter: %s\n  - num: %s' % (letter, num)
        return data, {}

    def encode(self, data, mimetype_in, mimetype_out):
        return mimetype_out, '%s;%s' % (data.num, data.letter)


class SampleCustomDataCodecPlugin(QMimeCodecPlugin):
    qtencode = [
        ("custom/data", "custom/data"),
    ]
    qtdecode = [
        ("custom/data", "custom/data"),
        ("custom/data", "openalealab/control"),
        ("custom/data", "text/plain"),
        ("custom/data", "text/plain.verbose"),
    ]

    mimetype_desc = {
        'text/plain': dict(title='Short Text'),
        'text/plain.verbose': dict(title='Long Text'),
        'custom/data': dict(title='Custom data'),
        'openalealab/control': dict(title='Control'),
    }

    def __call__(self):
        return SampleCustomDataCodec


register_plugin('oalab.plugin', SampleCustomDataCodecPlugin)
reload_drag_and_drop_plugins()
