# -*- python -*-
#
#       OpenAlea.StdLib
#
#       Copyright 2006 - 2008 INRIA - CIRAD - INRA  
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#
################################################################################


__doc__ = """ OpenAlea.Data Structure."""
__license__ = "Cecill-C"
__revision__ =" $Id$ "


from openalea.core import *
from openalea.core.pkgdict import protected


__name__ = "openalea.data structure"
__alias__ = ['catalog.data', 'openalea.data']

__version__ = '0.0.2'
__license__ = "Cecill-C"
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'Nodes for standard data structure creation, edition and visualisation.'
__url__ = 'http://openalea.gforge.inria.fr'

               

__all__ = []

var_ = Factory( name="variable", 
               description="Variable", 
               category="datatype", 
               nodemodule="data",
               nodeclass="Variable",
               
               inputs=(dict(name='Caption', interface=IStr, value='Variable'),
                       dict(name='Object', interface=None, value=None),
                       ),
               outputs=(dict(name='Object', interface=None),)
               )

__all__.append('var_')

str_ = Factory( name=protected("string"), 
              description="String", 
              category="datatype", 
              nodemodule="data",
              nodeclass="String",
              
              inputs=(dict(name="String", interface=IStr, value=''),),
              outputs=(dict(name="String", interface=IStr),),
              )

__all__.append('str_')


text = Factory( name=protected("text"), 
              description="Text", 
              category="datatype", 
              nodemodule="data",
              nodeclass="Text",
              
              inputs=(dict(name="Text", interface=ITextStr, value=''),),
              outputs=(dict(name="Text", interface=ITextStr),),
              )


__all__.append('text')

datetime_ = Factory( name="datetime", 
              description="DateTime", 
              category="datatype", 
              nodemodule="data",
              nodeclass="DateTime",
              
              inputs=(dict(name="DateTime", interface=IDateTime, value=''),),
              outputs=(dict(name="DateTime", interface=IDateTime),),
              )

__all__.append('datetime_')


bool_ = Factory( name="bool", 
              description="boolean", 
              category="datatype", 
              nodemodule="data",
              nodeclass="Bool",
              
              inputs=(dict(name="Bool", interface=IBool, value=False),),
              outputs=(dict(name="Bool", interface=IBool),),
              )


__all__.append('bool_')


float_ = Factory( name="float",
              description="Float Value",
              category="datatype",
              nodemodule="data",
              nodeclass="Float",
              
              inputs=(dict(name="Float", interface=IFloat, value=0.0),),
              outputs=(dict(name="Float", interface=IFloat),),
              )


__all__.append('float_')


floatscy = Factory( name="float scy",
              description="Float Value",
              category="datatype",
              nodemodule="data",
              nodeclass="FloatScy",
              
              inputs=(dict(name="str", interface=IStr, value="0.0"),),
              outputs=(dict(name="Float", interface=IFloat),),
              )


__all__.append('floatscy')


int_ = Factory( name="int",
              description="Int Value",
              category="datatype",
              nodemodule="data",
              nodeclass="Int",
              
              inputs=(dict(name="Int", interface=IInt, value=0),),
              outputs=(dict(name="Int", interface=IInt),),
              )

__all__.append('int_')


rgb_ = Factory( name=protected("rgb"),
              description="RGB tuple",
              category="Color,datatype",
              nodemodule="data",
              nodeclass="RGB",
              
              inputs=(dict(name="RGB", interface=IRGBColor, value=(0,0,0), desc='3 uples RGB color'),),
              outputs=(dict(name="RGB", interface = ISequence, desc='3 uples RGB color'),),
              )


__all__.append('rgb_')
Alias(rgb_, 'rgb')

list_ = Factory( name=protected("list"),
              description="Python list",
              category="datatype",
              nodemodule="data",
              nodeclass="List",
              
              inputs=(dict(name="List", interface=ISequence),),
              outputs=(dict(name="List", interface=ISequence),),
              )


__all__.append('list_')


dict_ = Factory( name=protected("dict"),
              description="Python dictionary",
              category="datatype",
              nodemodule="data",
              nodeclass="Dict",
              
              inputs=(dict(name="Dict", interface=IDict),),
              outputs=(dict(name="Dict", interface=IDict),),
              )


__all__.append('dict_')


pair = Factory( name=protected("pair"),
              description="Python 2-uples",
              category="datatype",
              nodemodule="data",
              nodeclass="Pair",
              inputs=(dict(name="IN0", interface=None,),
                      dict(name="IN1", interface=None,),),
              outputs=(dict(name="OUT", interface = ISequence),),
              )

__all__.append('pair')

tuple3 = Factory( name=protected("tuple3"),
              description="Python 3-uples",
              category="datatype",
              nodemodule="data",
              nodeclass="Tuple3",
              inputs=(dict(name="IN0", interface=None,),
                      dict(name="IN1", interface=None,),
                      dict(name="IN1", interface=None,),
                      ),
              outputs=(dict(name="OUT", interface = ISequence),),
              )

__all__.append('tuple3')

# DEPRECATED
fname = Factory( name=protected("filename"), 
              description="File name", 
              category="datatype", 
              nodemodule="data",
              nodeclass="FileName",
              
              inputs=(dict(name='FileStr', interface=IFileStr, value=''),
                      dict(name='cwd', interface=IDirStr, value='', hide=True),),
              outputs=(dict(name='FileStr', interface=IFileStr),)
              )


__all__.append('fname')


dname = Factory( name=protected("dirname"), 
              description="Directory name", 
              category="datatype", 
              nodemodule="data",
              nodeclass="DirName",
              
              inputs=(dict(name='DirStr', interface=IDirStr, value=''),
                      dict(name='cwd', interface=IDirStr, value='', hide=True)),
              outputs=(dict(name='DirStr', interface=IDirStr),)
              )


__all__.append('dname')


pdir = Factory( name=protected("packagedir"), 
              description="Package Directory", 
              category="datatype", 
              nodemodule="data",
              nodeclass="PackageDir",
              
              inputs=(dict(name='PackageStr', interface=IStr, value=''),),
              outputs=(dict(name='DirStr', interface=IDirStr),)
              )

__all__.append('pdir')
