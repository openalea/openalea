# -*- python -*-
#
#       OpenAlea.Visualea
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


__license__ = "Cecill-C"
__revision__ = " $Id$ "

from os.path import splitext
import urlparse
from urlparse import urlparse as uparse



from PyQt4 import QtCore, QtGui

class Extension(type):
    """ The application registry (also behaves as a metaclass
    for Extensions but that is a detail."""
    class Notifier(QtCore.QObject):
        applicationListChanged = QtCore.pyqtSignal()

    q = Notifier()
    appdict = {}
    urlSchemeHandlers = {}
    mimeHandlers = {}

    def __init__(cls, name, base, dic):
        ret = super(Extension, cls).__init__(name, base, dic)
        return ret

    def __call__(cls, *args, **kwargs):
        name = cls.__name__
        if name not in Extension.appdict:
            inst = super(Extension, cls).__call__(*args, **kwargs)
            Extension.appdict[name] = inst

            # -- give the instance an automatic name attribute --
            inst.name = name

            # -- register URL schemes for application, if any --
            hUrl = inst.handled_url_schemes()
            if hUrl is not None:
                for sc in hUrl:
                    Extension.urlSchemeHandlers[sc] = inst
            cls.q.applicationListChanged.emit()
            return inst
        else:
            return Extension.appdict.get(name)

    @classmethod
    def entry_point_init(self):
        import pkg_resources
        layouts = {}
        widgets = {}
        editors = {}
        schemes = {}

        for l in pkg_resources.iter_entry_points("openalea.app.layout"):
            try:
                layout = l.load()
                layouts.setdefault(layout.namespace, []).append(layout)
            except Exception, e:
                print e
                continue

        for sv in pkg_resources.iter_entry_points("openalea.app.singleton_view"):
            try:
                sview = sv.load()
                widgets.setdefault(sview.namespace, []).append(sview)
            except Exception, e:
                print e
                continue

        for ed in pkg_resources.iter_entry_points("openalea.app.data_editor"):
            try:
                editor = ed.load()
                editors.setdefault(editor.namespace, []).append(editor)
                ns, scheme = ed.name.split(".")
                schemes.setdefault(ns, set()).add(scheme)
            except Exception, e:
                print e
                continue


        namepaces = list(layouts.iterkeys())# | set(widgets.iterkeys()) | set(editors.iterkeys())

        for ns in namepaces:
            app = make_derived_application(ns,
                                           schemes[ns],
                                           layouts[ns],
                                           widgets[ns],
                                           editors[ns])
            print app


    @classmethod
    def get_application_names(cls):
        return list(cls.appdict)

    @classmethod
    def get_application(cls, name):
        return cls.appdict.get(name)

    @classmethod
    def get_applications(cls):
        return list(cls.appdict.itervalues())

    @classmethod
    def get_layout_names(cls):
        apps     = cls.get_applications()
        layouts  = []
        for app in apps:
            layoutNames = app.layouts()
            for ln in layoutNames:
                layouts.append(".".join((app.name, ln)))
        return layouts

    @classmethod
    def get_widget_names(cls):
        apps     = cls.get_applications()
        widgets  = []
        for app in apps:
            wids = app.widgets()
            for wid in wids:
                widgets.append(".".join((app.name, wid)))
        return widgets

    @classmethod
    def create_editor_for(self, url, parent=None):
        parsedUrl = uparse(url)
        handler  = Extension.urlSchemeHandlers.get(parsedUrl.scheme)
        instance, widget = None, None
        if handler:
            instance, widget = handler.create_editor_for(parsedUrl, parent)
        return instance, widget

    @classmethod
    def has_url_handler(self, url):
        parsedUrl = uparse(url)
        return parsedUrl.scheme in Extension.urlSchemeHandlers





class Namespaced(object):
    def __init__(self, ns):
        self.__ns = ns

    @property
    def namespace(self):
        return self.__ns


class WidgetFactory(Namespaced):
    __name__ = ""

    def __init__(self, ns):
        Namespaced.__init__(self, ns)

    def __call__(self, parsedUrl, parent):
        return self._make_instance(parsedUrl, parent)

    @property
    def name(self):
        return self.__name__

    @property
    def full_name(self):
        return ".".join((self.namespace, self.__name__))

    def _make_instance(self, parsedUrl, parent):
        raise NotImplementedError

    def handles(self, *args, **kwargs):
        raise NotImplementedError



class SingletonWidgetFactory(WidgetFactory):
    def __init__(self, ns):
        WidgetFactory.__init__(self, ns)
        self.__instance = None

    def __call__(self, *args, **kwargs):
        if self.__instance is not None:
            return self.__instance
        self.__instance = self._make_instance(*args, **kwargs)
        return self.__instance



class Layout(Namespaced):
    """A layout definition"""
    def __init__(self, ns, name, skeleton, widgetmap):
        """Create a layout description.
        :Parameters:
         - name (str) - a name for the layout
         - skeleton (str) - the reseult of splitterui.Splittable.toString()
         - widgetmap (dict<int:str>) - map splitter paneIds to widgetnames
        """
        Namespaced.__init__(self, ns)
        self.name = name
        self.skeleton  = skeleton
        self.widgetmap = widgetmap




class PaneGroup(object):
    """This one is I don't know for what yet"""
    def __init__(self, widget):
        self.widget  = widget
        self.menu    = None #QtGui.QMenu (or subclass) instance.






class ExtensionBase(object):

    __metaclass__ = Extension

    __layouts__   = None # dict<str:Layout>
    __widgets__   = None # set<str>
    __schemes__   = None # set<str>
    __mimetypes__ = None # set<str>

    def widgets(self):
        """Return a list of widget names for the given Extension"""
        return self.__widgets__.copy()

    def layouts(self):
        """Return a dictionnary of layout descriptions (applications.Layout type)"""
        return self.__layouts__.copy()

    def handled_url_schemes(self):
        """Return a set of url schemes names (protocols) handled by this application.
        {"http", "file", ...}."""
        return self.__schemes__.copy()

    def create_widget(self, name, **kwargs):
        """Return the widget named `name`"""
        raise NotImplementedError

    def create_editor_for(self, parsedUrl, parent=None):
        """Instantiate parsedUrl (type: urlparse.ParseResult) and return the
        instance and an editor for the instance"""
        raise NotImplementedError




# class ExtensionBase2(object):
#     def __init__(self):
#         # -- build layout dict --
#         self.__layouts = {}
#         for l in self.iter_layouts():
#             self.__layouts[l.name] = l

#         # -- build widget dict --
#         self.__widgets = {}
#         for wf in self.iter_widget_factories():
#             self.__widgets[wf.name] = wf

#     def layout_names(self):
#         return list(self.__layouts.iterkeys())

#     def layout(self, name):
#         return self.__layouts[name]

#     def widget_names(self):
#         return list(self.__widgets.iterkeys())

#     def create_widget(self, name=None, data=None):
#         if name is not None:
#             wf = self.__widgets[name]
#             return wf()
#         elif data is not None:
#             for wf in self.iter_widget_factories():
#                 if wf.handles(data):
#                     return wf(data)
#         else:
#             return None








def make_derived_application(ns, schemes, layouts, sing_widgets, editors):

    class DerivedExtension(ExtensionBase):
        __layouts__ = dict((lay.name, lay) for lay in layouts)
        __widgets__ = set(widFac.name for widFac in sing_widgets)
        __schemes__  = schemes

        __widFactoryMap__ = dict((widFac.name, widFac) for widFac in sing_widgets)
        __editors__ = editors[:]

        def create_widget(self, name, **kwargs):
            print self.__class__.__name__, "create_widget", name, self.__widFactoryMap__
            if name in self.__widFactoryMap__:
                return self.__widFactoryMap__[name]()

        def create_editor_for(self, parsedUrl, parent):
            for ed in self.__editors__:
                if ed.handles(parsedUrl):
                    return ed.__call__(parsedUrl, parent)

    DerivedExtension.__name__ = ns
    app = DerivedExtension()
    return app

