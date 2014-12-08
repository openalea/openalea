# -*- coding: utf-8 -*-
# -*- python -*-
#
#
#       OpenAlea.OALab: Multi-Paradigm GUI
#
#       Copyright 2014 INRIA - CIRAD - INRA
#
#       File author(s):
#           Julien Coste <julien.coste@inria.fr>
#           Christophe Pradal<christophe.pradal@inria.fr>
#           Guillaume Baty <guillaume.baty@inria.fr>
#
#       File contributor(s):
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
#
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
###############################################################################

from openalea.core.path import path as Path
import warnings


class ISaver(object):

    """
    Generic interface class for savers
    """
    mimetype = unicode
    fmts = []

    def save(self, obj, path, fmt=None, **kwds):
        raise NotImplementedError


class ILoader(object):
    mimetype = unicode
    fmts = []

    def load(self, path, fmt=None, **kwds):
        raise NotImplementedError


class ISerializer(object):

    """
    Generic interface class for savers
    """
    dtype = unicode
    fmts = []

    def serialize(self, obj, fmt=None, **kwds):
        """
        This method must return an iterable object, ideally an iterator
        """
        return 'iterator'


class IDeserializer(object):

    """
    Generic interface class for savers
    """
    dtype = unicode
    fmts = []

    def deserialize(self, lines, fmt=None, **kwds):
        return 'data'


class AbstractSaver(object):

    def _open_file(self, path):
        filename = Path(path)
        if filename.isdir():
            print 'BUG: filename is a dir'
            return

        try:
            file_ = open(filename, "w")
        except IOError:
            newdir, fn = filename.splitpath()
            if not Path(newdir).isdir():
                newdir.makedirs()
            file_ = open(filename, "w")
        return file_

    def _write(self, lines, file_):
        for line in lines:
            file_.write(line)
        file_.close()

    def save(self, obj, path, fmt=None, **kwds):
        lines = self._serialize(obj, fmt=fmt, **kwds)
        file_ = self._open_file(path)
        self._write(lines, file_)

    def _serialize(self, obj, fmt, **kwds):
        raise NotImplementedError


class AbstractLoader(object):

    def _iter_file(self, file_):
        for line in file_:
            yield line
        file_.close()

    def load(self, path, fmt=None, **kwds):
        try:
            file_ = open(path, 'r')
        except IOError:
            lines = []
        else:
            lines = self._iter_file(file_)
        return self._deserialize(lines, fmt=fmt, **kwds)

    def _deserialize(self, lines, fmt=None, **kwds):
        raise NotImplementedError


class GenericTextSaver(AbstractSaver):

    """
    Classical saver that write str(obj) into file
    """
    default_name = "GenericSaver"
    output_format = "*.py"

    def _serialize(self, obj):
        code = str(obj).encode("utf8", "ignore")
        yield code


class BinarySaver(AbstractSaver):
    default_name = "BinarySaver"
    output_format = "*"

    def save(self, obj, filename):
        if isinstance(obj, Path):
            if obj.abspath() != Path(filename).abspath():
                obj.copyfile(filename)


class CPickleSaver(AbstractSaver):

    """
    Specific saver that use cPickle.dump
    """
    default_name = "CPickleSaver"
    output_format = "*"

    def save(self, obj, path):
        """
        Store obj into filename
        """
        file_ = self._open_file(path)
        try:
            import cPickle
            cPickle.dumps(obj, file_)
        except ImportError:
            warnings.warn("You must install cPickle.")


class BGEOMSaver(object):

    """
    Specific loader that is used to manipulate PlantGL objects
    """
    default_name = "BGEOMSaver"
    output_format = "*.BGEOM"

    def save(self, obj, filename):
        """
        Store obj into filename
        """
        filename = Path(filename)
        try:
            from openalea.plantgl.all import Scene
            sc = Scene()
            sc.add(obj)
            return sc.save(str(filename), "BGEOM")
        except ImportError:
            warnings.warn("You must install PlantGL if you want to load a BGEOM object.")
        except Exception, e:
            print e
            warnings.warn("Impossible to save the scene for object %s into %s" % (obj, filename))


class GenericLoader(object):

    """
    Classical loader that read file
    """
    default_name = "GenericLoader"
    input_format = "*.py"

    def load(self, filename):
        """
        :param filename: filename to convert into python object
        :return: a python object interpreted from string "text"
        """
        filename = Path(filename)
        if filename.exists():
            obj = open(filename, 'rU').read()
            return obj


class BinaryLoader(object):
    default_name = "BinaryLoader"
    input_format = "*"

    def load(self, filename):
        return Path(filename)


class PythonLoader(object):

    """
    Classical loader that read file and try to eval object
    """
    default_name = "PythonLoader"
    input_format = "*.py"

    def load(self, filename):
        """
        :param filename: filename to convert into python object
        :return: a python object interpreted from string "text"
        """
        filename = Path(filename)
        if filename.exists():
            obj = open(filename, 'rU').read()
            try:
                return eval(obj)
            except SyntaxError:
                return obj
            except NameError:
                return obj


class CPickleLoader(AbstractLoader):

    """
    Specific loader that use cPickle.loads
    """
    default_name = "CPickleLoader"
    input_format = "*"

    def load(self, filename):
        """
        :param filename: filename to convert into python object
        :return: a python object interpreted from filename
        """
        filename = Path(filename)
        if filename.exists():
            cpik = "False"
            try:
                import cPickle
                cpik = "True"
            except ImportError:
                warnings.warn("You must install cPickle.")
            if cpik:
                try:
                    file_ = open(filename, "r")
                    ret = cPickle.load(file_)
                    file_.close()
                    return ret
                except Exception, e:
                    print "Can't load file " + filename + " with loader CPickleLoader. "
                    print e


class BGEOMLoader(AbstractLoader):

    """
    Specific loader that is used to manipulate PlantGL objects
    """
    default_name = "BGEOMLoader"
    input_format = "*.BGEOM"

    def load(self, filename):
        """
        :param filename: filename to convert into python object
        :return: a python object interpreted from string "text"
        """
        filename = Path(filename)
        if filename.exists():
            try:
                from openalea.plantgl.all import Scene
                sc = Scene()
                sc.clear()
                sc.read(str(filename), "BGEOM")
                return sc
            except ImportError:
                warnings.warn("You must install PlantGL if you want to load a BGEOM object.")
            except Exception, e:
                print e
                warnings.warn("Impossible to load the scene")
