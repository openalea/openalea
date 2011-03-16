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
from openalea.secondnature.data import DataType


class AppletBase(HasName):

    __name__ = ""

    def __init__(self):
        HasName.__init__(self, self.__name__)
        self.__datatypes       = []
        self.__mimemap         = {}
        self.__defaultDataType = None

    def set_default_data_type(self, dt):
        assert dt in self.__datatypes
        self.__defaultDataType = dt

    def get_default_data_type(self):
        if self.__defaultDataType:
            return self.__defaultDataType
        elif len(self.__datatypes):
            return self.__datatypes[0]
        return None

    def get_mimetypes(self):
        return list(self.__mimemap.iterkeys())

    def get_icon(self):
        return NotImplementedError

    def get_applet_space(self, data):
        raise NotImplementedError

    def __call__(self, *args, **kwargs):
        return self.get_applet_space(*args, **kwargs)

    #############
    # DataTypes #
    #############
    def add_data_type(self, dt):
        assert isinstance(dt, DataType)
        self.__datatypes.append(dt)
        mimetypes = dt.mimetypes
        for mt in mimetypes:
            self.__mimemap[mt] = dt

    if __debug__:
        def add_data_types(self, dts):
            assert isinstance(dts, list)
            for dt in dts:
                self.add_data_type(dt)
    else:
        def add_data_types(self, dts):
            self.__datatypes.extend(dts)
            d = dict( (dt.mimetype, dt) for dt in dts )
            self.__mimemap.update(d)


    def get_data_types(self):
        return self.__datatypes[:]
