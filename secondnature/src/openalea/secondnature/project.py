
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


from PyQt4 import QtCore
from openalea.core.singleton import ProxySingleton
from openalea.core.metaclass import make_metaclass


class RefPOD(object):
    def __init__(self, val):
        self.val = val

class Project(QtCore.QObject):

    closed                = QtCore.pyqtSignal(object)
    saved                 = QtCore.pyqtSignal(object)
    modified              = QtCore.pyqtSignal(object)
    document_added        = QtCore.pyqtSignal(object, object)
    document_name_changed = QtCore.pyqtSignal(object, object, str)
    project_name_changed  = QtCore.pyqtSignal(object, str)

    def __init__(self, name):
        QtCore.QObject.__init__(self)
        self.__name     = name
        self.__modified = False
        self.__names    = {}
        self.__docIdCtr = 0
        self.__docs     = {}
        self.__docprops = {}

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        print "new name:", value
        self.__name = value
        self.project_name_changed.emit(self, value)

    def __fix_name(self, name):
        nbName = self.__names.setdefault(name, 1)
        self.__names[name] += 1
        if nbName > 1:
            name += " (%i)"%nbName
        return name

    def add_document(self, doc):
        name = self.__fix_name(doc.name)
        doc._set_name( name )
        self.__docs[self.__docIdCtr] = doc
        self.__docIdCtr += 1

        self.document_added.emit(self, doc)
        self.mark_as_modified()

    def get_document(self, doc_id):
        pass

    def del_document(self, doc_id):
        self.mark_as_modified()

    def has_document(self, doc):
        return doc in self.__docs.itervalues()

    def is_modified(self):
        return self.__modified

    def __iter__(self):
        return self.__docs.iteritems()

    def set_document_name(self, doc, name):
        if not self.has_document(doc):
            return #raise something
        fixedName = self.__fix_name(name)
        doc._set_name( fixedName )
        self.document_name_changed.emit(self, doc, fixedName)

    def set_document_property(self, doc, key, val):
        self.__docprops.setdefault(doc, {})[key] = val

    def get_document_property(self, doc, key):
        if not self.has_document_property(doc, key):
            return None
        props = self.__docprops.get(doc)
        if props is not None:
            return props.get(key)

    def pop_document_property(self, doc, key):
        if not self.has_document_property(doc, key):
            return None
        props = self.__docprops.get(doc)
        if props is not None:
            return props.pop(key)

    def has_document_property(self, doc, key):
        props = self.__docprops.get(doc)
        if not props:
            return False #TODO : raise something dude
        return key in props



    def mark_as_modified(self):
        self.__modified = True
        self.modified.emit(self)

    def mark_as_saved(self):
        self.__modified = False
        self.saved.emit(self)

    def save_to(self, file):
        #...
        self.saved.emit(self)

    def close(self):
        #...
        self.closed.emit(self)
        self.closed.disconnect()
        self.saved.disconnect()
        self.modified.disconnect()
        self.doc_connected.disconnect()



class ProjectManager(QtCore.QObject):
    """An manager that references all projects on a user's system.
    Maybe an extension of PackageManager"""

    __metaclass__ = make_metaclass((ProxySingleton,),
                                   (QtCore.pyqtWrapperType,))

    activeProjectChanged       = QtCore.pyqtSignal(object)
    activeProjectClosed        = QtCore.pyqtSignal(object)
    activeProjectSaved         = QtCore.pyqtSignal(object)
    activeProjectModified      = QtCore.pyqtSignal(object)
    aboutToCloseActiveProject  = QtCore.pyqtSignal(object, RefPOD)

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
            return # raise something
        self.__activeProject = project
        self.__activeProject.closed.connect(self.activeProjectClosed)
        self.__activeProject.saved.connect(self.activeProjectSaved)
        self.__activeProject.modified.connect(self.activeProjectModified)
        self.activeProjectChanged.emit(self.__activeProject)

    def get_active_project(self):
        return self.__activeProject

    def close_active_project(self):
        save = RefPOD(False)
        self.aboutToCloseActiveProject.emit(self.__activeProject, save)
        if save.val == True:
            self.save_active_project()
        self.__activeProject.close()
        self.__activeProject = None

    def save_active_project(self):
        self.__activeProject.save()





