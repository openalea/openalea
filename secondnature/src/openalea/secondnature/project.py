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


from PyQt4 import QtCore, QtGui
from openalea.core.singleton import ProxySingleton
from openalea.core.metaclass import make_metaclass
import cPickle
import zipfile
import io
import traceback



class Project(QtCore.QObject):

    # -- SIGNALS --
    closed                = QtCore.pyqtSignal(object)
    saved                 = QtCore.pyqtSignal(object)
    modified              = QtCore.pyqtSignal(object)
    data_added        = QtCore.pyqtSignal(object, object)
    data_name_changed = QtCore.pyqtSignal(object, object, str)
    project_name_changed  = QtCore.pyqtSignal(object, str)

    # -- PROPERTIES --
    name = property(lambda x:x.__name, lambda x,y:x.set_name(y))

    def __init__(self, name):
        QtCore.QObject.__init__(self)
        self.__name     = name
        self.__modified = False
        self.__names    = set()
        self.__docIdCtr = 0
        self.__docs     = {}
        self.__docToIds = {}
        self.__docprops = {}

    def set_name(self, value):
        self.__name = value
        self.project_name_changed.emit(self, value)

    def __fix_name(self, name):
        i = 1
        original = name
        candidate = name
        while candidate in self.__names:
            candidate = name + " (%i)"%i
            i += 1
        self.__names.add(candidate)
        return candidate

    def add_data(self, doc):

        name = self.__fix_name(doc.name)
        doc.name = name
        self.__docs[self.__docIdCtr] = doc
        self.__docToIds[doc] = self.__docIdCtr
        self.__docIdCtr += 1

        self.data_added.emit(self, doc)
        self.mark_as_modified()

    def get_data_id(self, data):
        return self.__docToIds.get(data, -1)

    def get_data(self, doc_id):
        return self.__docs.get(doc_id)

    def get_data_by_name(self, name):
        for datum in self.__docs.itervalues():
            if name==datum.name:
                return datum
        return None

    def del_data(self, doc_id):
        self.mark_as_modified()

    def has_data(self, doc):
        return doc in self.__docs.itervalues()

    def is_modified(self):
        return self.__modified

    def __iter__(self):
        return self.__docs.iteritems()

    def set_data_name(self, doc, name):
        if not self.has_data(doc):
            return #raise something
        oldName = doc.name
        self.__names.discard(oldName)
        fixedName = self.__fix_name(name)
        doc.name = fixedName
#        doc._set_name( fixedName )
        self.data_name_changed.emit(self, doc, fixedName)

    def set_data_property(self, doc, key, val):
        if doc not in self.__docToIds:
            raise Exception()
        self.__docprops.setdefault(doc, {})[key] = val

    def get_data_property(self, doc, key):
        if not self.has_data_property(doc, key):
            return None
        props = self.__docprops.get(doc)
        if props is not None:
            return props.get(key)

    def pop_data_property(self, doc, key):
        if not self.has_data_property(doc, key):
            return None
        props = self.__docprops.get(doc)
        if props is not None:
            return props.pop(key)

    def has_data_property(self, doc, key):
        props = self.__docprops.get(doc)
        if not props:
            return False #TODO : raise something dude
        return key in props


    def close(self):
        self.closed.emit(self)

        self.__names.clear()
        self.__docs.clear()
        self.__docToIds.clear()
        self.__docprops.clear()

        # self.closed.disconnect()
        # self.saved.disconnect()
        # self.modified.disconnect()


    def mark_as_modified(self):
        self.__modified = True
        self.modified.emit(self)

    def mark_as_saved(self):
        self.__modified = False
        self.saved.emit(self)


    ############
    # Pickling #
    ############

    def save_to(self, filepath):
        docnames = [doc.name+":"+doc.factory_name+":"+doc.type \
                    for doc in self.__docs.itervalues()]
        manifest = reduce(lambda x,y:x+"\n"+y, docnames, "name="+self.name)
        print manifest
        with zipfile.ZipFile(filepath, "w") as z:
            z.writestr("manifest.txt", manifest)
            for d in self.__docs.itervalues():
                try:
                    stream = io.BytesIO()
                    d.to_stream(stream)
                except Exception, e:
                    print "couldn't write", f, " : ", e
                else:
                    z.writestr(d.name,stream.getvalue())

    @classmethod
    def load_from(cls, filepath):
        from openalea.secondnature.data import DataFactoryManager
        dataMgr = DataFactoryManager()
        dataFactories = dataMgr.gather_items()
        docs = dict()
        name = ""
        with zipfile.ZipFile(filepath, "r") as z:
            manifest = z.read("manifest.txt")
            print manifest
            lines = manifest.split("\n")
            name = lines[0].split("=")[1]
            filesAndFactories = [f.split(":") for f in lines[1:]]
            ctr = 0
            for f, facName, type_ in filesAndFactories:
                df = dataFactories.get(facName)
                if not df:
                    continue

                bytes = z.read(f)
                stream = io.BytesIO(initial_bytes=bytes)
                try:
                    upk = df.data_from_stream(f, stream, type_)
                except Exception, e:
                    print "couldn't read", f, " : ", e
                    traceback.print_exc()
                else:
                    docs[ctr] = upk
                ctr+=1
        print docs
        proj = Project(name)
        proj.__docs = docs
        proj.__docIdCtr = len(proj.__docs)

        for k, v in proj.__docs.iteritems():
            proj.__docToIds[v] = k
            proj.__names.add(v.name)
        return proj





class ProjectManager(QtCore.QObject):

    __metaclass__ = make_metaclass((ProxySingleton,),
                                   (QtCore.pyqtWrapperType,))

    active_project_changed = QtCore.pyqtSignal(Project, Project)
    data_added             = QtCore.pyqtSignal(object, object)

    mimeformat   = "application/secondnature-project-data-id"

    def __init__(self):
        QtCore.QObject.__init__(self)
        self.__activeProject = None

    def new_active_project(self, name):
        proj = Project(name)
        return self.set_active_project(proj)

    def has_active_project(self):
        return self.__activeProject is not None

    def set_active_project(self, project):
        if self.has_active_project() and self.get_active_project().is_modified():
            return False# raise something
        old = self.__activeProject
        self.__activeProject = project
        self.__activeProject.data_added.connect(self.data_added)
        self.active_project_changed.emit(self.__activeProject, old)
        return True

    def get_active_project(self):
        return self.__activeProject

    def close_active_project(self):
        if self.__activeProject:
            self.__activeProject.close()
        self.__activeProject = None

    def save_active_project(self, filepath):
        self.__activeProject.save_to(filepath)

    def add_data_to_active_project(self, data):
        if data and data.registerable and self.__activeProject:
            self.__activeProject.add_data(data)

    def set_property_to_active_project(self, data, key, value):
        if data and self.__activeProject:
            self.__activeProject.set_data_property(data, key, value)


import os.path
from os.path import join as pj
class QActiveProjectManager(QtCore.QObject):

    __metaclass__ = make_metaclass((ProxySingleton,),
                                   (QtCore.pyqtWrapperType,))

    def __init__(self):
        QtCore.QObject.__init__(self)
        self.__pm = ProjectManager()

    #############
    # Shortcuts #
    #############
    def get_active_project(self):
        return self.__pm.get_active_project()

    def has_active_project(self):
        return self.__pm.has_active_project()


    #########################################
    # Methods that return prebound QActions #
    #########################################
    def get_action_new(self):
        action = QtGui.QAction("&New project...", self)
        action.triggered.connect(self.new_active_project)
        return action

    def get_action_open(self):
        action = QtGui.QAction("&Open project...", self)
        action.triggered.connect(self.open_project)
        return action

    def get_action_save(self):
        action = QtGui.QAction("&Save project...", self)
        action.triggered.connect(self.save_active_project)
        return action

    def get_action_close(self):
        action = QtGui.QAction("&Close project...", self)
        action.triggered.connect(self.close_active_project)
        return action

    ################################################
    # Gui wrappers around the Project Manager with #
    # nice questions to the user                   #
    ################################################
    def set_active_project(self, project):
        if self.has_active_project() and self.get_active_project().is_modified():
            if self.__ask_close_active():
                self.close_active_project()
        self.__pm.set_active_project(project)

    def new_active_project(self):
        proj = self.get_active_project()
        if proj and proj.is_modified():
            if not self.__ask_close_active():
                return None
            else:
                self.close_active_project()

        name, ok = QtGui.QInputDialog.getText(None,
                                              "New project...",
                                              "Please give a new to your project")
        if ok:
            self.__pm.new_active_project(name)
        else:
            return None

    def __ask_close_active(self):
        but = QtGui.QMessageBox.question(None,
                                         "Close current project?",
                                         "The current project has not been saved.\n\n"+\
                                         "Do you really want to close it?""",
                                         QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                                         QtGui.QMessageBox.No)
        return but == QtGui.QMessageBox.Yes

    def close_active_project(self):
        proj = self.get_active_project()
        projectClosed = False
        if proj and proj.is_modified():
            but = QtGui.QMessageBox.question(None,
                                             "Unsaved modifications!",
                                             "The current project has not been saved.\n"+\
                                             "All changes will be lost.\n\n"+\
                                             "Do you want to save it before closing it?",
                                             QtGui.QMessageBox.Yes|QtGui.QMessageBox.No,
                                             QtGui.QMessageBox.Yes)

            if but == QtGui.QMessageBox.Yes:
                self.save_active_project()
        self.__pm.close_active_project()


    def save_active_project(self):
        proj = self.get_active_project()
        if proj:
            pth = QtGui.QFileDialog.getSaveFileName(None,
                                                    "Save project to...",
                                                    pj(os.path.expanduser("~"),proj.name+".oas"),
                                                    "OpenAlea project (*.oas)",
                                                    "OpenAlea project (*.oas)",
                                                    QtGui.QFileDialog.DontResolveSymlinks)
            if pth == "":
                return
            else:
                self.__pm.save_active_project(str(pth))

    def open_project(self):
        proj = self.get_active_project()
        if proj and proj.is_modified():
                if not self.__ask_close_active():
                    return None
                else:
                    self.close_active_project()

        proj = None
        pth = QtGui.QFileDialog.getOpenFileName(None,
                                                "Open project from...",
                                                os.path.expanduser("~"),
                                                "OpenAlea project (*.oas)",
                                                "OpenAlea project (*.oas)",
                                                QtGui.QFileDialog.DontResolveSymlinks)
        if pth == "":
            return
        else:
            proj = Project.load_from(str(pth))
            if proj:
                self.set_active_project(proj)




