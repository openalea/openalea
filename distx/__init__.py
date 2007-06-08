# -*- python -*-
from distx import *


"""Extensions to the 'distutils' for large or complex distributions"""

# This code is inspired from setuptools 

from distutils.util import convert_path
import os.path


def find_packages(where='.', namespace = '', exclude=()):
    """Return a list all Python packages found within directory 'where'

    'where' should be supplied as a "cross-platform" (i.e. URL-style) path; it
    will be converted to the appropriate local path syntax.
    'namespace' is a string containing the namespace to prepend to package names.
    'exclude' is a sequence of package names to exclude; '*' can be used as
    a wildcard in the names, such that 'foo.*' will exclude all subpackages
    of 'foo' (but not 'foo' itself).
    """
    if (namespace) : namespace += ('.')
    else : namespace = ''
    
    out = []
    stack=[(convert_path(where), namespace)]
    while stack:
        where,prefix = stack.pop(0)
        for name in os.listdir(where):
            fn = os.path.join(where,name)
            if (os.path.isdir(fn) and
                os.path.isfile(os.path.join(fn,'__init__.py'))
            ):
                out.append(prefix+name); stack.append((fn,prefix+name+'.'))
    for pat in exclude:
        from fnmatch import fnmatchcase
        out = [item for item in out if not fnmatchcase(item,pat)]
    return out


def find_package_dir(where='.', namespace = '', exclude=()):
    """Return a dictionary { package_name : src_dir, ... }
    for all Python packages found within directory 'where'

    'where' should be supplied as a "cross-platform" (i.e. URL-style) path; it
    will be converted to the appropriate local path syntax.
    'namespace' is a string containing the namespace to prepend to package names.
    'exclude' is a sequence of package names to exclude; '*' can be used as a
    wildcard in the names, such that 'foo.*' will exclude all subpackages
    of 'foo' (but not     'foo' itself).
    """

    out = {}
    package_list = find_packages(where = where, namespace = namespace, exclude = exclude)
    for p in package_list:
        
        # remove namespace
        if(namespace):
            srcdir = p[ len(namespace)+1 :]
        else : srcdir = p[:]
        
        srcdir = os.path.join(where, *srcdir.split('.'))
        out[p] = srcdir
    return out


class Shortcut :
    """ class regrouping shortcut infos """

    def __init__ (self, name ='', target = '', arguments ='', 
                  group = '', description = '', icon=''):

        self.name = name
        self.target = target
        self.arguments = arguments
        self.group = group
        self.description = description
        self.icon = icon
        self.version = None


    def fill_with_metadata(self, metadata):
        """ Fill blank field with package metadata """

        if(not self.name) : self.name = metadata.get_name()
        if(not self.version) : self.version = metadata.get_version()
        if(not self.description) : self.description = metadata.get_description()
        

        
