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


__doc__ = """ Catalog.Data """
__license__ = "Cecill-C"
__revision__ =" $Id: data_wralea.py 997 2007-12-13 14:38:21Z dufourko $ "


from openalea.core import *


__name__ = "openalea.data"
__alias__ = ['catalog.data']

__version__ = '0.0.1'
__license__ = "Cecill-C"
__authors__ = 'OpenAlea Consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'Base library'
__url__ = 'http://openalea.gforge.inria.fr'

               

__all__ = []

var_ = Factory( name="variable", 
               description="Variable", 
               category="Type", 
               nodemodule="data",
               nodeclass="Variable",
               
               inputs=(dict(name='Caption', interface=IStr, value='Variable'),
                       dict(name='Object', interface=None, value=None),
                       ),
               outputs=(dict(name='Object', interface=None),)
               )

__all__.append('var_')

str_ = Factory( name="string", 
              description="String", 
              category="Type", 
              nodemodule="data",
              nodeclass="String",
              
              inputs=(dict(name="String", interface=IStr, value=''),),
              outputs=(dict(name="String", interface=IStr),),
              )

__all__.append('str_')


text = Factory( name="text", 
              description="Text", 
              category="Type", 
              nodemodule="data",
              nodeclass="Text",
              
              inputs=(dict(name="Text", interface=ITextStr, value=''),),
              outputs=(dict(name="Text", interface=ITextStr),),
              )


__all__.append('text')

datetime_ = Factory( name="datetime", 
              description="DateTime", 
              category="Type", 
              nodemodule="data",
              nodeclass="DateTime",
              
              inputs=(dict(name="DateTime", interface=IDateTime, value=''),),
              outputs=(dict(name="DateTime", interface=IDateTime),),
              )

__all__.append('datetime_')


bool_ = Factory( name="bool", 
              description="boolean", 
              category="Type", 
              nodemodule="data",
              nodeclass="Bool",
              
              inputs=(dict(name="Bool", interface=IBool, value=False),),
              outputs=(dict(name="Bool", interface=IBool),),
              )


__all__.append('bool_')


float_ = Factory( name="float",
              description="Float Value",
              category="Type",
              nodemodule="data",
              nodeclass="Float",
              
              inputs=(dict(name="Float", interface=IFloat, value=0.0),),
              outputs=(dict(name="Float", interface=IFloat),),
              )


__all__.append('float_')


floatscy = Factory( name="float scy",
              description="Float Value",
              category="Data Types",
              nodemodule="data",
              nodeclass="FloatScy",
              
              inputs=(dict(name="str", interface=IStr, value="0.0"),),
              outputs=(dict(name="Float", interface=IFloat),),
              )


__all__.append('floatscy')


int_ = Factory( name="int",
              description="Int Value",
              category="Type",
              nodemodule="data",
              nodeclass="Int",
              
              inputs=(dict(name="Int", interface=IInt, value=0),),
              outputs=(dict(name="Int", interface=IInt),),
              )

__all__.append('int_')


rgb_ = Factory( name="rgb",
              description="RGB tuple",
              category="Type,Color",
              nodemodule="data",
              nodeclass="RGB",
              
              inputs=(dict(name="RGB", interface=IRGBColor, value=(0,0,0), desc='3 uples RGB color'),),
              outputs=(dict(name="RGB", interface = ISequence, desc='3 uples RGB color'),),
              )


__all__.append('rgb_')


list_ = Factory( name="list",
              description="Python list",
              category="Type",
              nodemodule="data",
              nodeclass="List",
              
              inputs=(dict(name="List", interface=ISequence),),
              outputs=(dict(name="List", interface=ISequence),),
              )


__all__.append('list_')


dict_ = Factory( name="dict",
              description="Python dictionary",
              category="Type",
              nodemodule="data",
              nodeclass="Dict",
              
              inputs=(dict(name="Dict", interface=IDict),),
              outputs=(dict(name="Dict", interface=IDict),),
              )


__all__.append('dict_')


pair = Factory( name="pair",
              description="Python 2-uples",
              category="Type",
              nodemodule="data",
              nodeclass="Pair",
              inputs=(dict(name="IN0", interface=None,),
                      dict(name="IN1", interface=None,),),
              outputs=(dict(name="OUT", interface = ISequence),),
              )

__all__.append('pair')

tuple3 = Factory( name="tuple3",
              description="Python 3-uples",
              category="Type",
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
fname = Factory( name="filename", 
              description="File name", 
              category="Type", 
              nodemodule="data",
              nodeclass="FileName",
              
              inputs=(dict(name='FileStr', interface=IFileStr, value=''),
                      dict(name='cwd', interface=IDirStr, value='', hide=True),),
              outputs=(dict(name='FileStr', interface=IFileStr),)
              )


__all__.append('fname')


dname = Factory( name="dirname", 
              description="Directory name", 
              category="Type", 
              nodemodule="data",
              nodeclass="DirName",
              
              inputs=(dict(name='DirStr', interface=IDirStr, value=''),
                      dict(name='cwd', interface=IDirStr, value='', hide=True)),
              outputs=(dict(name='DirStr', interface=IDirStr),)
              )


__all__.append('dname')


pdir = Factory( name="packagedir", 
              description="Package Directory", 
              category="Type", 
              nodemodule="data",
              nodeclass="PackageDir",
              
              inputs=(dict(name='PackageStr', interface=IStr, value=''),),
              outputs=(dict(name='DirStr', interface=IDirStr),)
              )

__all__.append('pdir')
