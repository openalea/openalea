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
        self._name = name
        self.__ns = ns

    name      = property(lambda x: x._name)
    namespace = property(lambda x: x.__ns)
    fullname  = property(lambda x: ".".join([x.__ns, x._name]))



class Layout(Base):
    def __init__(self, name, ns, skeleton, resourcemap):
        Base.__init__(self, name, ns)
        self.__skeleton  = skeleton
        self.__resourcemap = resourcemap

    skeleton  = property(lambda x: x.__skeleton)
    resourcemap = property(lambda x: x.__resourcemap)



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

    def get_icon(self):
        return NotImplementedError

    def __call__(self, input):
        """returns ( (input|derived input), LayoutSpace)"""
        return self._instanciate_space(input)

    def _instanciate_space(self, input):
        """returns ( (input|derived input), LayoutSpace)"""
        raise NotImplementedError



class DocumentWidgetFactory(WidgetFactory):
    __mimeformats__ = []

    def get_mime_formats(self):
        return self.__mimeformats__[:]

    # def handles_mimetype(self, format):
        # raise NotImplementedError

    def new_document(self):
        raise NotImplementedError

    def open_document(self, parsedUrl):
        raise NotImplementedError

    def get_document_space(self, document):
        raise NotImplementedError



class ResourceWidgetFactory(WidgetFactory):
    def get_resource(self):
        raise NotImplementedError

    def _get_resource_space(self, resource):
        if not self.validate_resource(resource):
            raise Exception("resource "+resource.fullname+" is not handled by "+self.fullname)
        else:
            return self.get_resource_space(resource)

    def validate_resource(self, resource):
        raise NotImplementedError

    def get_resource_space(self, resource):
        raise NotImplementedError




class Document(Base):
    """"""
    def __init__(self, name, ns, source, obj, category="user"):
        Base.__init__(self, name, ns)
        self.__source = source
        self.__obj    = obj
        self.__cat    = category

    source    = property(lambda x:x.__source)
    obj       = property(lambda x:x.__obj)
    category  = property(lambda x:x.__cat)

    def _set_name(self, name):
        self._name = name


    def save(self):
        raise NotImplementedError

Resource = Document
