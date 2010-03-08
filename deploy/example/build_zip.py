import zipfile
from openalea.core.path import path
import os

def qt4(directory = path('qt4'), name='qt4'):

    zip_name = path('..')/name + '.zip'

    patterns = ['*2.5.dylib', '*.py', '*.api', '*.so',  '*.txt', '*safe', '*INFO',  '*.4.dylib'] 

    curdir = path(os.curdir).abspath()
    os.chdir(directory)

    zf=zipfile.ZipFile(zip_name,compression=zipfile.ZIP_DEFLATED,mode='w')

    d = path('.')
    for pattern in patterns:
        for fn in d.walkfiles(pattern):
            print 'add ', fn
            zf.write(fn)

    zf.close()
    os.chdir(curdir)

def qt4_dev (directory=path('qt4-dev'), name='qt4_dev'):

    zip_name = path('..')/name + '.zip'
    curdir = path(os.curdir).abspath()
    os.chdir(directory)

    zf=zipfile.ZipFile(zip_name,compression=zipfile.ZIP_DEFLATED,mode='w')

    dirs = {}
    dirs['EGG-INFO'] = ['*']
    dirs['include'] = ['*']
    dirs['bin'] = ['*']
    dirs['sip'] = ['*']
    dirs['lib'] = ['*.4.dylib', '*2.5.dylib']

    for dir, patterns in dirs.iteritems():
        d = path(dir)
        for pattern in patterns:
            for fn in d.walkfiles(pattern):
                print 'add ', fn
                zf.write(fn)

    zf.close()
    os.chdir(curdir)

