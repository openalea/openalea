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


from openalea.core.interface import IInterface


class IQMimeCodecPlugin(IInterface):

    """
    An encoder should define:
    1 TYPE -> n out mimetype
    """
    implements = ['IQMimeCodec']

    def qtdecode(self, mimedata, mimetype_in, mimetype_out):
        """

        """


class IQMimeDecoder(IInterface):

    """
    Convert a QMimeData to a python object

    A decoder should define:
    1 TYPE -> n out mimetype
    """

    def qtdecode(self, mimedata, mimetype_in, mimetype_out):
        """

        """

    def quick_check(self, mimedata, mimetype_in, mimetype_out):
        """
        Proceed to a quick check: return True if mimedata can be decoded to mimetype_out else return False

        For example, a Decoder "text/uri-list -> openalea/interface.IImage" 
        can create an array by reading path content if path is an image file.
        But if path is not image, user do not want to see it. In this case, quick_check can just check file extension,
        if extension is a valid image extension (.jpg, .png, ...) quick_check return True, else False
        """


class IQMimeEncoder(IInterface):

    """
    Convert a python object to a QMimeData
    """

    def qtencode(self, data, qmimedata, mimetype_in, mimetype_out):
        """
        :param data: Data (python object) you want to encode
        :param qmimedata: QtCore.QMimeData to populate. Can be not empty. This qmimedata is generated from DragManager. Trust it.
        """


class IQMimeCodec(IQMimeEncoder, IQMimeDecoder):
    pass