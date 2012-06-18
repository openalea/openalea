
# This file has been generated at Wed Apr 21 17:24:35 2010

from openalea.core import *


__name__ = 'openalea.file'

__editable__ = True
__description__ = 'File manimulation library.'
__license__ = 'CECILL-C'
__url__ = 'http://openalea.gforge.inria.fr'
__alias__ = ['catalog.file']
__version__ = '0.0.1'
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__icon__ = ''


__all__ = ['files_DirName', 'files_joinpath', 'expand_user', 'files_FileReadlines', 'parentdir_parentdir', 'files_py_write', 'files_glob', 'viewfile', 'files_FileName', 'files_FileRead', 'files_py_tmpnam', 'files_PackageDir']



files_DirName = Factory(name='dirname',
                description='Directory name',
                category='File,IO',
                nodemodule='files',
                nodeclass='DirName',
                inputs=({'interface': IDirStr, 'name': 'DirStr', 'value': ''},),
                outputs=({'interface': IDirStr, 'name': 'DirStr'},),
                widgetmodule=None,
                widgetclass=None,
               )


files_joinpath = Factory(name='joinpath',
                description='Join several strings to form a path',
                category='File,IO',
                nodemodule='files',
                nodeclass='joinpath',
                inputs=({'interface': ISequence, 'name': 'a', 'value': []},),
                outputs=({'interface': IStr, 'name': 'path'},),
                widgetmodule=None,
                widgetclass=None,
               )

expand_user = Factory(name='expand_user_dir',
                description='Replaces tilde by user home dir',
                category='File,IO',
                nodemodule='files',
                nodeclass='expanduser',
                inputs=({'interface': IStr, 'name': 'path', 'value': ''},),
                outputs=({'interface': IStr, 'name': 'path'},),
                widgetmodule=None,
                widgetclass=None,
               )


files_FileReadlines = Factory(name='readlines',
                description='read a file as a sequence of lines',
                category='File,IO',
                nodemodule='files',
                nodeclass='FileReadlines',
                inputs=({'interface': IFileStr, 'name': 'filename'},),
                outputs=({'interface': ISequence, 'name': 'string'},),
                widgetmodule=None,
                widgetclass=None,
               )




parentdir_parentdir = Factory(name='parentdir',
                description='os.path.dirname method',
                category='data i/o',
                nodemodule='files',
                nodeclass='parentdir',
                inputs=[{'interface': IFileStr, 'name': 'path', 'value': '.', 'desc': 'file or path name'}],
                outputs=[{'interface': IDirStr, 'name': 'dirname', 'desc': ''}],
                widgetmodule=None,
                widgetclass=None,
               )




files_py_write = Factory(name='write',
                description='write to a file',
                category='File,IO',
                nodemodule='files',
                nodeclass='py_write',
                inputs=({'interface': IStr, 'name': 'x'}, {'interface': IFileStr, 'name': 'filename'}, {'interface': IStr, 'name': 'mode', 'value': 'w'}),
                outputs=({'interface': IFileStr, 'name': 'filename'},),
                widgetmodule=None,
                widgetclass=None,
               )




files_glob = Factory(name='glob',
                description='Return a list of path that math the pattern',
                category='File,IO',
                nodemodule='files',
                nodeclass='glob',
                inputs=({'interface': IDirStr, 'name': 'directory'}, {'interface': IStr, 'name': 'pattern', 'value': '*'},),
                outputs=({'interface': ISequence, 'name': 'path_list'},),
                #widgetmodule='widget',
                #widgetclass="ListSelectorWidget",
               )

files_copy = Factory(name='copy',
                description='Copy data and mode bits ("cp src dst")',
                category='File,IO',
                nodemodule='shutil',
                nodeclass='copy',
                inputs=({'interface': IFileStr, 'name': 'src'},{'interface': IFileStr, 'name': 'dest'},),
                outputs=({'name': 'status'},),
                widgetmodule=None,
                widgetclass=None,
               )
__all__.append('files_copy')


viewfile = CompositeNodeFactory(name='viewfile',
                             description='View the content of a file.',
                             category='File,IO,composite',
                             doc='',
                             inputs=[{  'interface': IFileStr, 'name': 'filename(read)', 'value': ''}],
                             outputs=[{  'interface': ITextStr, 'name': 'Text(text)'}],
                             elt_factory={  2: ('catalog.file', 'read'), 3: ('catalog.data', 'text')},
                             elt_connections={  135946380: (2, 0, 3, 0),
   135946392: (3, 0, '__out__', 0),
   135946404: ('__in__', 0, 2, 0)},
                             elt_data={  2: {  'caption': 'read',
         'hide': True,
         'lazy': False,
         'minimal': False,
         'port_hide_changed': set(),
         'posx': 246.25,
         'posy': 111.25,
         'priority': 0},
   3: {  'caption': 'text',
         'hide': False,
         'lazy': True,
         'minimal': False,
         'port_hide_changed': set(),
         'posx': 246.25,
         'posy': 166.25,
         'priority': 0},
   '__in__': {  'caption': 'In',
                'hide': True,
                'lazy': True,
                'minimal': False,
                'port_hide_changed': set(),
                'posx': 20.0,
                'posy': 5.0,
                'priority': 0},
   '__out__': {  'caption': 'Out',
                 'hide': True,
                 'lazy': True,
                 'minimal': False,
                 'port_hide_changed': set(),
                 'posx': 20.0,
                 'posy': 250.0,
                 'priority': 0}},
                             elt_value={  2: [], 3: [], '__in__': [], '__out__': []},
                             elt_ad_hoc={  },
                             lazy=True,
                             )




files_FileName = Factory(name='filename',
                description='Browser to select a file pathname',
                category='File,IO',
                nodemodule='files',
                nodeclass='FileName',
                inputs=({'interface': IFileStr, 'name': 'FileStr', 'value': ''},),
                outputs=({'interface': IFileStr, 'name': 'FileStr'},),
                widgetmodule=None,
                widgetclass=None,
               )




files_FileRead = Factory(name='read',
                description='read a file',
                category='File,IO',
                nodemodule='files',
                nodeclass='FileRead',
                inputs=({'interface': IFileStr, 'name': 'filename'},),
                outputs=({'interface': IStr, 'name': 'string'},),
                widgetmodule=None,
                widgetclass=None,
               )




files_py_tmpnam = Factory(name='tmpnam',
                description='return a unique name for a temporary file.',
                category='File,IO',
                nodemodule='files',
                nodeclass='py_tmpnam',
                inputs=(),
                outputs=({'interface': IStr, 'name': 'filename'},),
                widgetmodule=None,
                widgetclass=None,
               )




files_PackageDir = Factory(name='packagedir',
                description='Package Directory',
                category='File,IO',
                nodemodule='files',
                nodeclass='PackageDir',
                inputs=({'interface': IStr, 'name': 'PackageStr', 'value': ''},),
                outputs=({'interface': IDirStr, 'name': 'DirStr'},),
                widgetmodule=None,
                widgetclass=None,
               )

files_listdir =  Factory(name='listdir',
                description='ls',
                category='File,IO',
                nodemodule='files',
                nodeclass='listdir',
                inputs=({'interface': IDirStr, 'name': 'directory', 'value': '.'},
                        {'interface': IStr, 'name': 'pattern', 'value': '*'}),
                outputs=({'interface': IDirStr, 'name': 'DirStr'},),
               )

start =  Factory(name='start',
                description='Open a file with the default application',
                category='File,IO',
                nodemodule='files',
                nodeclass='start',
                inputs=({'interface': IFileStr, 'name': 'path', 'value': '.'},),
               )
__all__.append('start')

httpfile =  Factory(name='http file',
                description='Copy a network object denoted by a URL to a local file, if necessary. If the URL points to a local file, or a valid cached copy of the object exists, the object is not copied. ',
                category='File,IO, http',
                nodemodule='urllib',
                nodeclass='urlretrieve',
                inputs=({'interface': IStr, 'name': 'url'},),
                outputs=(dict(name='filename',interface=IFileStr),
                        dict(name='headers', interface=None)),
               )
__all__.append('httpfile')
