# -*- python -*-
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


class Base(object):
    def __init__(self, name, ns):
        self.__name = name
        self.__ns = ns

    name      = property(lambda x: x.__name)
    namespace = property(lambda x: x.__ns)
    fullname  = property(lambda x: ".".join([x.__ns, x.__name]))



class Layout(Base):
    def __init__(self, name, ns, skeleton, widgetmap):
        Base.__init__(self, name, ns)
        self.__skeleton  = skeleton
        self.__widgetmap = widgetmap

    skeleton  = property(lambda x: x.__skeleton)
    widgetmap = property(lambda x: x.__widgetmap)



class LayoutSpace(Base):
    """returned by widget factories"""
    def __init__(self, name, ns, content, menu=None, toolbar=None):
        Base.__init__(self, name, ns)
        self.__content = content
        self.__menu    = menu
        self.__toolbar = toolbar

    menu    = property(lambda x:x.__menu)
    content = property(lambda x:x.__content)
    toolbar = property(lambda x:x.__toolbar)


class WidgetFactory(Base):
    __name__ = ""
    __namespace__ = ""
    def __init__(self):
        Base.__init__(self, self.__name__, self.__namespace__)

    def creates_without_data(self):
        return False

    def handles(self, input):
        """returns True or False"""
        raise NotImplementedError

    def __call__(self, input, parent):
        """returns ( (input|derived input), LayoutSpace)"""
        return self._instanciate_space(input, parent)

    def _instanciate_space(self, input, parent):
        """returns ( (input|derived input), LayoutSpace)"""
        raise NotImplementedError


class SingletonWidgetFactory(WidgetFactory):
    def __init__(self):
        WidgetFactory.__init__(self)
        self.__instance = None
        self.__data     = None

    def __call__(self, input, parent):
        if self.__instance is not None:
            return self.__data, self.__instance
        self.__data, self.__instance = self._instanciate_space(input, parent)
        return self.__data, self.__instance


