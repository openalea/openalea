# -*- python -*-
#
#       OpenAlea.Catalog
#
#       Copyright 2006 - 2007 INRIA - CIRAD - INRA  
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################

__doc__ = """ catalog.file """
__revision__ = " $Id$ "


from openalea.core import *


__name__ = "openalea.file"
__alias__ = ['catalog.file']

__version__ = '0.0.1'
__license__ ='CECILL-C'
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'File manimulation library.'
__url__ = 'http://openalea.gforge.inria.fr'


__all__ = []


filename = Factory( name="filename", 
                  description="File name", 
                  category="File", 
                  nodemodule="files",
                  nodeclass="FileName",

                  inputs=(dict(name='FileStr', interface=IFileStr, value=''),),
                  outputs=(dict(name='FileStr', interface=IFileStr),),
                  )

__all__.append('filename')

dirname = Factory( name="dirname", 
                   description="Directory name", 
                   category="File", 
                   nodemodule="files",
                   nodeclass="DirName",
                   
                   inputs=(dict(name='DirStr', interface=IDirStr, value=''),),
                   outputs=(dict(name='DirStr', interface=IDirStr),)
                   )


__all__.append('dirname')


pkgdir = Factory( name="packagedir", 
                  description="Package Directory", 
                  category="File", 
                  nodemodule="files",
                  nodeclass="PackageDir",

                  inputs=(dict(name='PackageStr', interface=IStr, value=''),),
                  outputs=(dict(name='DirStr', interface=IDirStr),)
                  )


__all__.append('pkgdir')

# Path
joinpath = Factory( name="joinpath", 
                    description="Join several strings to form a path", 
                    category="File", 
                    nodemodule="files",
                    nodeclass="joinpath",
                    
                    inputs=(dict(name='a', interface=ISequence, value=[]),
                            ),
                    outputs=(dict(name='path', interface=IStr),)
                  )

__all__.append('joinpath')


glob = Factory( name="glob", 
                description="Return a list of path that math the pattern", 
                category="File", 
                nodemodule="files",
                nodeclass="glob",

                inputs=(dict(name='pattern', interface=IStr, value="*"), ),
                outputs=(dict(name='path_list', interface=ISequence),)
                  )


__all__.append('glob')

# IO
read = Factory(name="read", 
               description="read a file", 
               category="File", 
               inputs=(dict(name="filename", interface=IFileStr),  ),
               outputs=(dict(name="string", interface=IStr),),
               
               nodemodule="files",
               nodeclass="FileRead",
               lazy = False,
               )


__all__.append('read')


readlines = Factory(name="readlines", 
                    description="read a file as a sequence of lines", 
                    category="File", 
                    inputs=(dict(name="filename", interface=IFileStr),
                            ),
                    outputs=(dict(name="string", interface=ISequence),),
                    nodemodule="files",
                    nodeclass="FileReadlines",
                    )

__all__.append('readlines')



write = Factory( name="write",
              description="write to a file",
              category="File",
              inputs=(dict(name="x", interface=IStr),
                      dict(name="filename", interface=IFileStr),
                      dict(name="mode", interface=IStr, value="w"),
                      ),
              outputs=(dict(name="filename", interface=IFileStr),),
              nodemodule="files",
              nodeclass="py_write",
              
              )


__all__.append('write')

tmpnam = Factory( name="tmpnam",
              description="return a unique name for a temporary file.",
              category="File",
              inputs=(),
              outputs=(dict(name="filename", interface=IStr),),
              nodemodule="files",
              nodeclass="py_tmpnam",
              
              )


__all__.append('tmpnam')

viewfile = CompositeNodeFactory(name='viewfile', 
                             description='View the content of a file.', 
                             category='File',
                             doc='',
                             inputs=[{'interface': IFileStr, 'name': 'filename(read)', 'value': ''}],
                             outputs=[{'interface': ITextStr, 'name': 'Text(text)'}],
                             elt_factory={2: ('catalog.file', 'read'), 3: ('catalog.data', 'text')},
                             elt_connections={  135946380: (2, 0, 3, 0),
   135946392: (3, 0, '__out__', 0),
   135946404: ('__in__', 0, 2, 0)},
                             elt_data={  2: {  'caption': 'read',
         'hide': True,
         'lazy': False,
         'minimal': False,
         'port_hide_changed': set([]),
         'posx': 246.25,
         'posy': 111.25,
         'priority': 0},
   3: {  'caption': 'text',
         'hide': False,
         'lazy': True,
         'minimal': False,
         'port_hide_changed': set([]),
         'posx': 246.25,
         'posy': 166.25,
         'priority': 0},
   '__in__': {  'caption': 'In',
                'hide': True,
                'lazy': True,
                'minimal': False,
                'port_hide_changed': set([]),
                'posx': 20.0,
                'posy': 5.0,
                'priority': 0},
   '__out__': {  'caption': 'Out',
                 'hide': True,
                 'lazy': True,
                 'minimal': False,
                 'port_hide_changed': set([]),
                 'posx': 20.0,
                 'posy': 250.0,
                 'priority': 0}},
                             elt_value={2: [], 3: [], '__in__': [], '__out__': []},
                             lazy=True,
                             )

__all__.append('viewfile')
