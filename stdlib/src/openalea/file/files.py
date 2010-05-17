# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006-2009 INRIA - CIRAD - INRA
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################
""" File manipulation """

__license__ = "Cecill-C"
__revision__ = " $Id$ "

import sys, os, subprocess
import tempfile
from openalea.core import *
from openalea.core.path import path

# File name manipulation


class FileName(object):
    """
    A file path
    :param object:
    :returns:  the filename path string
    """

    def __call__(self, input):
        """ inputs is the list of input values """

        fname = input
        return (str(fname), )


class DirName(object):
    """a file path"""

    def __call__(self, input):
        """
        :param input: list of input values 
        :returns: the path string
        """

        fname = input
        return (str(fname), )


class PackageDir(Node):
    """Package dir"""

    def __call__(self, inputs):
        """ inputs is the list of input values
        :param inputs: a package name
        :returns:  path of the package wralea
        """

        pname = str(inputs[0])

        from openalea.core.pkgmanager import PackageManager
        pm = PackageManager()
        pkg = pm.get(pname)
        path = ''

        if pkg:
            path = pkg.path

        return (path, )

# Path
import openalea.core.path as path


def glob(pattern):
    """Return a list of path that math the pattern

    :param pattern: a pattern to glob
    :return: a list of paths that match the pattern
    """
    ret = path.glob.glob(pattern)
    return (ret, )


def joinpath(pathlist):
    """Join several strings to form a path"""

    p = path.path(pathlist[0])
    ret = p.joinpath(*pathlist[1:])
    return (ret, )

# File contents


def py_write(x="", filename="", mode="w"):
    """ Write to a file """

    f = open(filename, mode)
    f.write(x)
    f.close()
    return filename,


class FileRead(object):
    """ Read a file as a string """

    def __init__(self):
        self.mtime = 0 # modification time
        self.filename = ''
        self.s = ''

    def read_contents(self, f):
        self.s = f.read()

    def __call__(self, filename=""):

        if(not isinstance(filename, basestring)):
            filename = str(filename)

        try:
            mtime = os.stat(filename).st_mtime
        except:
            mtime = 0

        if(filename != self.filename or
           mtime != self.mtime):

            self.filename = filename
            self.mtime = mtime
            f = open(filename, 'r')
            self.read_contents(f)
            f.close()

        return self.s


class FileReadlines(FileRead):
    """ Read a file as a list of strings """

    def __init__(self):

        FileRead.__init__(self)
        self.s = []

    def read_contents(self, f):
        self.s = f.readlines()


def py_tmpnam():
    return tempfile.mktemp(),

def parentdir(filename='.'):
    return os.path.dirname(filename),

def listdir(dir='.', pattern=None):
    return [str(x) for x in path(dir).listdir(pattern)],


def start(path):
    if hasattr(os, 'startfile'): # Windows
        os.startfile(path)
    else:
        if sys.platform.startswith('darwin'): # Mac OS X
            command = 'open'
        else: # Linux
            command = 'xdg-open'
        subprocess.call([command, path])

