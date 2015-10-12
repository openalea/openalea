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
