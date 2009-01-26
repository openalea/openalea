import os
from openalea.core import Node
from openalea.core.interface import *
from types import *

type_interface= { StringType : IStr,
		FloatType : IFloat,
		IntType: IInt,
		BooleanType : IBool }

def functionfactory( f, input_types, output_types ):
    def init(self):
      Node.__init__(self)
      self.f=f
      name= self.f.func_name
      varnames= self.f.func_code.co_varnames
      defaults=self.f.func_defaults
      
      nv= len(varnames)
      assert nv == len(input_types)
      nd= len(defaults)

      args= []
      for i,name in enumerate( varnames[:nv-nd] ):
        cur_type= input_types[i]
        cur_default= cur_type.__call__()
	interface= type_interface.get(cur_type,None)
        args.append((name, interface, cur_default))

      input_interfaces= map( lambda x: type_interface.get(x,None),input_types[nv-nd:])
      args.extend( zip( varnames[nv-nd:],input_interfaces, defaults ) )
      
      print "final args ",args

      for name, typ, default in args:
        self.add_input(name, typ, default)

      if len(output_types) >= 1:
        for i,typ in enumerate(output_types):
		self.add_output('out'+str(i),typ)

    def call(self, inputs):
      return self.f.__call__(*inputs)
      
    klass= type(f.func_name,(Node,), {'__init__':init, '__call__':call})

    return klass


        
        

