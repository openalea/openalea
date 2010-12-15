# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2010 INRIA - CIRAD - INRA
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
"""Describes the component concept.

"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "


from openalea.core.singleton import Singleton
from openalea.core.settings import Settings
from openalea.core import logger

def abstract(f):
    def abstractM(*args, **kwargs):
        raise NotImplementedError
    return abstractM


class ComponentRegistry(dict):
    __metaclass__ = Singleton

    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__typeToComponentMap = {}

    def __setitem__(self, compoName, v):
        dict.__setitem__(self, compoName, v)
        for t in v.supported_types():
            self.__typeToComponentMap[t] = v

    def get_component_names(self):
        return list(self.iterkeys())

    def create_editor_for(self, obj, *args, **kwargs):
        t = type(obj)
        c = self.__typeToComponentMap.get(t)
        if c:
            return c.create_editor_for(obj, *args, **kwargs)
        else:
            raise Exception("No editor found for type "+str(t))



class Component(object):

    __metaclass__ = Singleton

    def __init__(self):
        name = self.__class__.__name__
        ComponentRegistry()[name] = self
        self._logger = logger.get_logger(__name__+"."+self.__class__.__name__)

    def supported_types(self, *args, **kwargs):
        return []

    @abstract
    def get_version(self): pass

    @abstract
    def create_editor_for(self, obj, *args, **kwargs): pass

    @abstract
    def close_editor_of(self, obj): pass



class ComponentWithSettings(Component):
    def __init__(self, *args, **kwargs):
        Component.__init__(self)
        self.register_within_settings()

    def register_within_settings(self):
        settings = Settings()
        name = self.__class__.__name__
        if not settings.exists(name):
            settings.add_section(name)
            settings.add_section_update_handler(name, self)
            settings.add_option(name, "version", self.get_version())
            if hasattr(self, "SettingsDesc"):
                for opt in self.SettingsDesc:
                    settings.add_option(name, opt[0])

        elif hasattr(self, "SettingsDesc"):
            items           = dict(settings.items(name))
            settingsVersion = items.get("version")
            unknownItems    = [] #items that are in the settings but not in the component's current description
            newItems        = [] #items that are in the component's current description but not in the settings
            ok              = [] #items that are correctly recognized

            optNames = map(lambda x: x[0].replace(" ", "_").lower(), self.SettingsDesc)
            for optName, opt in zip(optNames, self.SettingsDesc):
                if optName not in items:
                    newItems.append((optName, opt[1]))
                else:
                    v = items[optName]
                    v = v if v != Settings.__notset__ else opt[1]
                    ok.append((optName, v))

            for optName, opt in items.iteritems():
                if optName not in optNames:
                    unknownItems.append((optName, opt))

            self._solve_unknown_items(settingsVersion, unknownItems)
            self._solve_new_items(settingsVersion, newItems)
            self.update_settings(settingsVersion, ok)

    def _solve_unknown_items(self, version, items):
        if version <= self.get_version():
            settings = Settings()
            name = self.__class__.__name__
            for k, v in items:
                settings.remove_option(name, k)

    def _solve_new_items(self, version, items):
        if version <= self.get_version():
            settings = Settings()
            name = self.__class__.__name__
            for k, v in items:
                settings.add_option(name, k, v)

    def update_settings(self, version, items):
        if version <= self.get_version():
            for k, v in items:
                name = k.replace(" ", "_").lower()
                getattr(self, "set_setting_"+name)(v)


##########################################
# SOME EXAMPLE COMPONENT IMPLEMENTATIONS #
##########################################
from PyQt4 import QtCore, QtGui
from openalea.core.interface import IEnumStr, IFileStr, IInt

if logger.QT_LOGGING_MODEL_AVAILABLE:
    import logging

    class CompactTableView(QtGui.QTableView):
        def __init__(self, *args, **kwargs):
            QtGui.QTableView.__init__(self, *args, **kwargs)
            rowHeight = self.fontMetrics().height() + 2;
            self.verticalHeader().setDefaultSectionSize(rowHeight);
            self.verticalHeader().setStyleSheet(
                "QHeaderView::section {" + \
                "padding-bottom: 0px;" + \
                "padding-top: 0px;" + \
                "padding-left: 0px;" + \
                "padding-right: 1px;" + \
                "margin: 1px;" + \
                "}")


    class Logging(ComponentWithSettings):

        SettingsDesc = [("Level","DEBUG"),
                        ("Logging file", logger.LoggerOffice().get_handler("file").baseFilename),
                        ("Log view length", "1000")]

        def __init__(self, *args, **kwargs):
            ComponentWithSettings.__init__(self, *args, **kwargs)
            self.__view = None

        def get_version(self):
            return "0.9"

        def supported_types(self, *args, **kwargs):
            return (logger.QLogHandlerItemModel,)

        def create_editor_for(self, obj, *args, **kwargs):
            if self.__view is not None:
                return self.__view
            model = obj
            assert isinstance(model, self.supported_types())
            view = CompactTableView() #QtGui.QTableView()
            view.verticalHeader().hide()
            view.setAlternatingRowColors(True)
            view.setModel(model)
            view.resizeColumnsToContents()
            view.resizeRowsToContents()
            return view

        def set_setting_level(self, v):
            self._logger.debug("set_setting_level " + v)
            logger.LoggerOffice().set_global_handler_level(logging._levelNames[v])

        def set_setting_logging_file(self, v):
            self._logger.debug("set_setting_logging_file " + v)
            logger.LoggerOffice().get_handler("file").baseFilename = v

        def set_setting_log_view_length(self, v):
            self._logger.debug("set_setting_log_view_length " + v)
            logger.LoggerOffice().get_handler("qt").length = int(v)


    # -- !!! be sure to instantiate it or else it won't get registered --
    # -- !!! No worries: it IS a singleton, multiple imports won't reinstantiate it ---
    Logging()






from openalea.core.compositenode import CompositeNode
class Dataflow(ComponentWithSettings):

    SettingsDesc = [("Node doubleclick action","Open"),
                    ("Edge style", "Spline"),
                    ("Show evaluation cue", "False")]

    def __init__(self, *args, **kwargs):
        ComponentWithSettings.__init__(self, *args, **kwargs)
        self.__views = []

    def get_version(self):
        return "0.9"

    def supported_types(self, *args, **kwargs):
        return (CompositeNode,)

    def create_editor_for(self, obj, *args, **kwargs):
        assert isinstance(obj, self.supported_types())
        gwidget = dataflowview.GraphicalGraph.create_view(obj, parent=kwargs.get("parent"))
        return gwidget

    def set_setting_node_doubleclick_action(self, v):
        pass

    def set_setting_edge_style(self, v):
        pass

    def set_setting_show_evaluation_cue(self, v):
        pass


# -- !!! be sure to instantiate it or else it won't get registered --
# -- !!! No worries: it IS a singleton, multiple imports won't reinstantiate it ---
Dataflow()


#####################################################################################
# EXPERIMENTAL STUFF - EXPERIMENTAL STUFF - EXPERIMENTAL STUFF - EXPERIMENTAL STUFF #
#####################################################################################
import ui_components_pref
class ComponentPreferenceBrowser(QtGui.QDialog, ui_components_pref.Ui_Dialog):

    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        ui_components_pref.Ui_Dialog.__init__(self)
        self.setupUi(self)

        settings = Settings()
        for section in settings.sections():
            self.compoList.addItem(section)
            widget = QtGui.QGroupBox(section)
            lay = QtGui.QVBoxLayout()
            widget.setLayout(lay)
            items = settings.items(section)
            for k, v in items:
                sl = QtGui.QHBoxLayout()
                lay.addLayout(sl)
                sl.addWidget(QtGui.QLabel(k))
                sl.addWidget(QtGui.QLabel(v))
            lay.addStretch()
            self.stack.addWidget(widget)

        self.compoList.currentRowChanged.connect(self.stack.setCurrentIndex)
#####################################################################################
# EXPERIMENTAL STUFF - EXPERIMENTAL STUFF - EXPERIMENTAL STUFF - EXPERIMENTAL STUFF #
#####################################################################################

