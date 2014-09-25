# -*- python -*-
#
#       OpenAlea.Core
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
"""Data management classes"""

__license__ = "Cecill-C"
__revision__ = " $Id$ "

from openalea.core.node import AbstractFactory, Node, NodeFactory
from openalea.core.interface import IData
from openalea.core.path import path as Path

import os
import string


class PackageData(object):
    """ String representing a package data """

    # if __local__ is True, then PackageData point to a
    # local data (i.e in the currrent directory)
    __local__ = False

    def __init__(self, pkg_name, filename, package=None):
        """
        pkg_name : package name
        name : data name
        package : Package object
        """
        self.pkg_name = pkg_name
        self.name = filename

        if(not package):
            from openalea.core.pkgmanager import PackageManager
            path = PackageManager()[self.pkg_name].path
        else:
            path = package.path

        if(PackageData.__local__):
            self.repr = self.name
        else:
            self.repr = os.path.join(path, self.name)

    def __repr__(self):
        return "PackageData(%s, %s)" % (self.pkg_name, self.name)

    def __str__(self):
        return self.repr


class DataFactory(AbstractFactory):
    """ Data representation as factory """

    #mimetype = "openalea/datafactory"

    def __init__(self,
                 name,
                 description = '',
                 editors = None,
                 includes = None,
                 **kargs):
        """
        name : filename
        description : file description
        editors : dictionnary listing external command to execute
        includes : List of data files that are included in the file.
        """

        AbstractFactory.__init__(self, name, description,
            category='data', **kargs)
        self.pkgdata_cache = None

        self.editors = editors
        self.includes = includes

    def is_data(self):
        return True
    def is_valid(self):
        """
        Return True if the factory has associated data.
        Else raise an exception
        """
        if(not os.path.exists(str(self.get_pkg_data()))):
            raise Exception("%s does'nt exists. Ignoring" % \
                (str(self.get_pkg_data())))

    def get_pkg_data(self):
        """ Return the associated PackageData object """

        if(not self.pkgdata_cache):
            self.pkgdata_cache = \
                PackageData(self.package.name, self.name, self.package)

        return self.pkgdata_cache

    def instantiate(self, call_stack=[]):
        """ Return a node instance

        :param call_stack: the list of NodeFactory id already in call stack
            (in order to avoid infinite recursion)
        """

        node = DataNode(self.get_pkg_data(), self.editors, self.includes)
        node.factory = self
        return node

    def instantiate_widget(self, node=None, parent=None, \
            edit=False, autonomous=False):
        """ Return the corresponding widget initialized with node """

        if(node):
            editors = node.get_input(1)
        else:
            editors = self.editors

        # single command
        if(editors and isinstance(editors, str)):
            editors = {'edit': editors}

        # multiple command
        # Add systematically a text editor.
        if(not isinstance(editors, dict)):
            editors = {}

        # Add a text editor
        _edit = [x for x in editors if x.lower() == 'edit']
        if not _edit:
            editors['edit'] = None


        from openalea.visualea.code_editor import EditorSelector
        return EditorSelector(parent, editors, (self.get_pkg_data(), ))

    def get_writer(self):
        """ Return the writer class """
        return PyDataFactoryWriter(self)

    def clean_files(self):
        """ Remove files depending of factory """
        os.remove(str(self.get_pkg_data()))


class DataNode(Node):
    """ Node representing a Data """

    __color__ = (200, 200, 200)

    def __init__(self, packagedata, editors=None, includes= []):
        """
        @packagedata : A file contained in a defined package.
        @editors : A dictionary of commands which act on the file.
        @includes : Other files that are included in the data file.
        """
        Node.__init__(self, inputs=\
            (dict(name='data', interface=IData, value=packagedata),
             dict(name='editors', interface=None, value=editors),
             dict(name='includes', interface=None, value=includes)),
             outputs=(dict(name='data', interface=IData), ), )
        self.caption = '%s' % (packagedata.name)
        self.watch = None
        self.monitor_file(str(packagedata))

        if not includes:
            self.set_port_hidden(2, True)

    def __del__(self):
        del(self.watch)

    def __call__(self, args):
        return str(args[0]),

    def monitor_file(self, filename):
        """ Enable file monitoring """
        try:
            # TODO : Try to remove qt dependencie here
            from openalea.vpltk.qt import QtCore

            self.watch = QtCore.QFileSystemWatcher()
            QtCore.QCoreApplication.instance().connect(\
                self.watch, QtCore.SIGNAL("fileChanged(const QString&)"),\
                self.changed)

            self.watch.addPath(filename)

        except:
            print "File monitoring is not available"

    def changed(self, path):
        """ Call listeners """
        self.continuous_eval.notify_listeners(("node_modified", ))
    
    def to_script (self):
        return "\n"


class PyDataFactoryWriter(object):
    """ DataFactory python Writer """

    datafactory_template = """
$NAME = DataFactory(name=$PNAME,
                    description=$DESCRIPTION,
                    editors=$EDITORS,
                    includes=$INCLUDES,
                    )
"""

    def __init__(self, factory):
        self.factory = factory

    def __repr__(self):
        """ Return the python string representation """
        f = self.factory
        fstr = string.Template(self.datafactory_template)
        result = fstr.safe_substitute(NAME=f.get_python_name(),
                                      PNAME=repr(f.name),
                                      DESCRIPTION=repr(f.description),
                                      EDITORS=repr(f.editors),
                                      INCLUDES=repr(f.includes),
                                      )
        return result


class Data(object):
    mimetype = None
    default_name = 'Data'
    extension = None

    def __init__(self, **kwargs):
        """
        Classical use : *path* exists. Nothing is loaded in memory.
        Use :meth:`~Data.read` to get content
        """
        # TODO: document args
        self.path = Path(kwargs['path']) if 'path' in kwargs else None
        self._filename = Path(kwargs['filename']).name if 'filename' in kwargs else None

        if self._filename is None and self.path is None:
            raise ValueError('path or filename required')
        if self._filename and self.path and self.path.name != self._filename:
            raise ValueError("path '%s'  and filename '%s' are not compatible" % (self.path, self._filename))

        self.dtype = kwargs['dtype'] if 'dtype' in kwargs else None
        self._content = kwargs['content'] if 'content' in kwargs else None

    def get_documentation(self):
        return "No documentation for %s" % self.filename

    def is_same_data(self, other):
        if self.exists() and other.exists():
            return self.path == other.path
        elif not self.exists() and not other.exists():
            return self._content == other._content
        else:
            return False

    def save(self):
        if self.path is None:
            raise ValueError('You must specify a path to be able to save data')
        if self._content is not None:
            with open(self.path, 'wb') as f:
                f.write(self._content)
            self._content = None

    def read(self):
        if self.exists():
            with open(self.path, 'rb') as f:
                return f.read()
        else:
            return self._content

    def rename(self, new):
        pnew = Path(new)
        if pnew.isabs() or pnew.name != new :
            raise ValueError('You must give filename only, not path')
        new_path = self.path.parent / new
        self.move(new_path)

    def move(self, new_path):
        new_path = Path(new_path)
        if self._filename is not None:
            self._filename = new_path.name

        if self.path.isfile():
            self.path.move(new_path)

        self.path = new_path

    def exists(self):
        if self.path:
            return self.path.exists()
        else:
            return False

    @property
    def filename(self):
        if self._filename is None:
            return self.path.name
        else:
            return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value
