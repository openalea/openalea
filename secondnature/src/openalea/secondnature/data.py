#
#       OpenAlea.SecondNature
#
#       Copyright 2006-2011 INRIA - CIRAD - INRA
#
#       File author(s): Daniel Barbeau <daniel.barbeau@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

__license__ = "CeCILL v2"
__revision__ = " $Id$ "

from openalea.secondnature.base_mixins import HasName



class DataType(HasName):
    __name__ = ""
    __mimetypes__ = []
    __supports_open__ = True

    def __init__(self):
        HasName.__init__(self, self.__name__)
        self.__mimetypes = self.__mimetypes__[:]

    def new_0(self):
        data = self.new()
        data._Data__set_data_type(self)
        return data

    def new(self):
        raise NotImplementedError

    def open_url(self, parsedUrl):
        raise NotImplementedError

    def get_icon(self):
        return NotImplementedError

    def supports_open(self):
        return self.__supports_open__

    mimetypes = property(lambda x:x.__mimetypes)

class DataTypeNoOpen(DataType):
    __supports_open__ = False


class Data(HasName):
    """"""
    def __init__(self, name, obj, mimetype, **kwargs):
        HasName.__init__(self, name)
        self.__obj     = obj
        self.__mimetype = mimetype
        self.__props    = kwargs.copy()
        self.__dt = None

    obj          = property(lambda x:x.__obj)
    registerable = property(lambda x:True)
    mimetype     = property(lambda x:x.__mimetype)

    def get_inner_property(self, key):
        return self.__props.get(key)

    def __set_data_type(self, dt):
        assert isinstance(dt, DataType)
        self.__dt = dt


class UnregisterableData(Data):
    registerable = property(lambda x:False)
