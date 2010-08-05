"""

This is a copy and paste of some of pkginfo while pkginfo is a standard or while
another solution is found


"""

import os
import zipfile


import glob
import os
import sys
import warnings

from types import ModuleType
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO


try:
    from email.parser import Parser
except ImportError:
    import rfc822
    def parse(fp):
        return rfc822.Message(fp)
    def get(msg, header):
        return _collapse_leading_ws(msg.getheader(header))
    def get_all(msg, header):
        return [_collapse_leading_ws(x) for x in msg.getheaders(header)]
else:
    def parse(fp):
        return Parser().parse(fp)
    def get(msg, header):
        return _collapse_leading_ws(msg.get(header))
    def get_all(msg, header):
        return [_collapse_leading_ws(x) for x in msg.get_all(header)]

def _collapse_leading_ws(txt):
    return ' '.join([x.strip() for x in txt.splitlines()])

HEADER_ATTRS_1_0 = ( # PEP 241
    ('Metadata-Version', 'metadata_version', False),
    ('Name', 'name', False),
    ('Version', 'version', False),
    ('Platform', 'platforms', True),
    ('Supported-Platform', 'supported_platforms', True),
    ('Summary', 'summary', False),
    ('Description', 'description', False),
    ('Keywords', 'keywords', False),
    ('Home-Page', 'home_page', False),
    ('Author', 'author', False),
    ('Author-email', 'author_email', False),
    ('License', 'license', False),
)

HEADER_ATTRS_1_1 = HEADER_ATTRS_1_0 + ( # PEP 314
    ('Classifier', 'classifiers', True),
    ('Download-URL', 'download_url', False),
    ('Requires', 'requires', True),
    ('Provides', 'provides', True),
    ('Obsoletes', 'obsoletes', True),
)

HEADER_ATTRS_1_2 = HEADER_ATTRS_1_1 + ( # PEP 345
    ('Maintainer', 'maintainer', False),
    ('Maintainer-email', 'maintainer_email', False),
    ('Requires-Python', 'requires_python', False),
    ('Requires-External', 'requires_external', True),
    ('Requires-Dist', 'requires_dist', True),
    ('Provides-Dist', 'provides_dist', True),
    ('Obsoletes-Dist', 'obsoletes_dist', True),
    ('Project-URL', 'project_urls', True),
)

HEADER_ATTRS = {
    '1.0': HEADER_ATTRS_1_0,
    '1.1': HEADER_ATTRS_1_1,
    '1.2': HEADER_ATTRS_1_2,
}

class Distribution(object):
    metadata_version = None
    # version 1.0
    name = None
    version = None
    platforms = ()
    supported_platforms = ()
    summary = None
    description = None
    keywords = None
    home_page = None
    download_url = None
    author = None
    author_email = None
    license = None
    # version 1.1
    classifiers = ()
    requires = ()
    provides = ()
    obsoletes = ()
    # version 1.2
    maintainer = None
    maintainer_email = None
    requires_python = None
    requires_external = ()
    requires_dist = ()
    provides_dist = ()
    obsoletes_dist = ()
    project_urls = ()

    def extractMetadata(self):
        data = self.read()
        self.parse(data)

    def read(self):
        raise NotImplementedError

    def _getHeaderAttrs(self):
        return HEADER_ATTRS.get(self.metadata_version, [])

    def parse(self, data):
        fp = StringIO(data)
        msg = parse(fp)

        if 'Metadata-Version' in msg and self.metadata_version is None:
            value = get(msg, 'Metadata-Version')
            metadata_version = self.metadata_version = value

        for header_name, attr_name, multiple in self._getHeaderAttrs():

            if attr_name == 'metadata_version':
                continue

            if header_name in msg:
                if multiple:
                    values = get_all(msg, header_name)
                    setattr(self, attr_name, values)
                else:
                    value = get(msg, header_name)
                    if value != 'UNKNOWN':
                        setattr(self, attr_name, value)

    def __iter__(self):
        for header_name, attr_name, multiple in self._getHeaderAttrs():
            yield attr_name

    iterkeys = __iter__

class Develop(Distribution):

    def __init__(self, path, metadata_version=None):
        self.path = os.path.abspath(
                        os.path.normpath(
                            os.path.expanduser(path)))
        self.metadata_version = metadata_version
        self.extractMetadata()

    def read(self):
        candidates = [self.path]
        candidates.extend(glob.glob(os.path.join(self.path, '*.egg-info')))
        candidates.extend(glob.glob(os.path.join(self.path, 'EGG-INFO')))
        for candidate in candidates:
            if os.path.isdir(candidate):
                path = os.path.join(candidate, 'PKG-INFO')
                if os.path.exists(path):
                    return open(path).read()
        warnings.warn('No PKG-INFO found for path (develop mode): %s' % self.path)

class Installed(Distribution):

    def __init__(self, package, metadata_version=None):
        if isinstance(package, basestring):
            self.package_name = package
            try:
                __import__(package)
            except ImportError:
                package = None
            else:
                package = sys.modules[package]
        else:
            self.package_name = package.__name__
        self.package = package
        self.metadata_version = metadata_version
        self.extractMetadata()

    def read(self):
        if self.package is not None:
            package = self.package.__package__
            pattern = '%s*.egg-info' % package
            file = getattr(self.package, '__file__', None)
            if file is not None:
                dir, name = os.path.split(self.package.__file__)
                candidates = glob.glob(os.path.join(dir, pattern))
                candidates.extend(glob.glob(os.path.join(dir, '..', pattern)))
                for candidate in candidates:
                    if os.path.isdir(candidate):
                        path = os.path.join(candidate, 'PKG-INFO')
                    else:
                        path = candidate
                    if os.path.exists(path):
                        return open(path).read()
        warnings.warn('No PKG-INFO found for package (install mode) %s' % self.package_name)


def get_metadata(path_or_module, metadata_version=None):
    """ Try to create a Distribution 'path_or_module'.

    o 'path_or_module' may be a module object.

    o If a string, 'path_or_module' may point to an sdist file, a bdist
      file, an installed package, or a working checkout (if it contains
      PKG-INFO).

    o Return None if 'path_or_module' can't be parsed.
    """
    if isinstance(path_or_module, ModuleType):
        try:
            #print 'trying install mode'
            return Installed(path_or_module, metadata_version)
        except (ValueError, IOError):
            pass

    try:
        __import__(path_or_module)
    except ImportError:
        pass
    else:
        try:
            #print 'trying install mode 2'
            return Installed(path_or_module, metadata_version)
        except (ValueError, IOError):
            pass

    if os.path.isdir(path_or_module):
        try:
            #print 'trying develop mode  '
            return Develop(path_or_module, metadata_version)
        except (ValueError, IOError):
            pass
