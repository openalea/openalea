
class Info(object):
    pass

class XyzHandler(object):
    def read(self, filepath):
        print 'read %s' % filepath
        return 'repr(%s)' % filepath

    def write(self, filepath, data):
        print 'save %s into %s' % (data, filepath)
