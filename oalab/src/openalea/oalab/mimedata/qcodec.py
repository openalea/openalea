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

from openalea.vpltk.qt import QtCore
from openalea.oalab.mimedata.codec import MimeCodec


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
