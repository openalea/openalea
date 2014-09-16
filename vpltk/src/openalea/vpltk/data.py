from openalea.core.path import path as Path


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

