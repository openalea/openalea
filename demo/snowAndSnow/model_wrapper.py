

	
#class NodeGetSpecificResult(Node):
#    def __init__( self ):
#	Node.__init__( self )
#	self.add_input( name= "input_dict", interface=IDict())
#	self.add_input( name= "name", interface=IStr())
#	
#	self.add_output( name= "result_dict", interface=IDict() )
#	
#    def __call__( self, inputs ):
#	return (self.get_input("input_dict")[ self.get_input("name") ], )
#

#class NodeCreateVisualSequenceFromResult(Node):
#    def __init__( self ):
#	Node.__init__( self )
#	self.add_input( name= "input_dict", interface=IDict())
#	#self.add_input( name= "name", interface=IStr())
#	
#	self.add_output( name= "VisualSequence", interface=None )
#	
#    def __call__( self, inputs ):
#	return (  plotable.generate_VisualSequence_from_dict( self.get_input("input_dict") ), )


#def define_factory(package):
#    """ Defines the nodes for phyllotaxis model."""




#    nf = Factory( name= "Gets specific result from model output", 
#                      description= "Use to specify model output", 
#                      category = "Model", 
#                      nodemodule = "model_wrapper",
#                      nodeclass = "NodeGetSpecificResult",
#                      widgetmodule = None,
#                      widgetclass = None,
#		      parameters=["name", "input_dict"] 
#                      )
#
#    package.add_factory( nf )
#
#    nf = Factory( name= "Generates VisualSequence data", 
#                      description= "Use to plot data", 
#                      category = "Model", 
#                      nodemodule = "model_wrapper",
#                      nodeclass = "NodeCreateVisualSequenceFromResult",
#                      widgetmodule = None,
#                      widgetclass = None,
#		      parameters=["input_dict"] 
#                      )
#   package.add_factory( nf )


from openalea.core.core import Node
from openalea.core.interface import IBool, IFloat, IInt, IStr, IDict
import model as m
import phyllotaxis as phyllotaxis
import openalea.plotools.plotable as plotable


class NodeModel(Node):
    def __init__( self ):
	Node.__init__( self )
	self.add_input( name= "gamma", interface=IFloat, value=3.1)
	self.add_input( name= "nbr_prims", interface=IInt(min=2, max=2000), value=20)
	self.add_input( name= "discretisation", interface=IInt(min=4, max=1000), value=20)
	self.add_input( name= "visualisation", interface=IBool, value=True)
	self.add_input( name= "continueSimulation", interface=IBool, value=False)
	self.add_input( name= "Prims/InhibitionFields", interface=IBool, value=False)
        
	self.add_output( name= "result_dict", interface=None )
	
        self.model = m.DiscInhibitorPhyllotaxisModel(visualisation=self.get_input( "visualisation" ))#None
        
    def __call__( self, inputs ):
        if not self.get_input( "continueSimulation" ):
            self.model = m.DiscInhibitorPhyllotaxisModel(visualisation=self.get_input( "visualisation" ))
        self.model.c_prim_size = self.get_input( "gamma" )
        self.model.c_discretization = self.get_input( "discretisation" )
        if self.get_input( "Prims/InhibitionFields" ):
            self.model.c_show_inhibition_fields = True
            self.model.c_show_primordia = False
        else:
            self.model.c_show_inhibition_fields = False
            self.model.c_show_primordia = True
            
        self.model.run(self.get_input( "nbr_prims" ))
        return ({"prim2init_pos":self.model.i_prim2init_pos.copy(), "prim2time":self.model.i_prim2time.copy(), "current_prim":self.model.current_prim}, )
            
	
class NodeDivAngVisualisation( Node ):
    def __init__( self ):
	Node.__init__( self )
	self.add_input( name= "SnowAndSnowModelResult", interface=None)
        self.add_output( name="VisualSequence", interface=None)
        
    def __call__( self, inputs ):
	return ( phyllotaxis.generate_VisualSequence_prim_id2div_angle( self.get_input( "SnowAndSnowModelResult" )["prim2init_pos"]), )

class NodeAbsAngVisualisation( Node ):
    def __init__( self ):
	Node.__init__( self )
	self.add_input( name= "SnowAndSnowModelResult", interface=None)
        self.add_output( name="VisualSequence", interface=None)
        
    def __call__( self, inputs ):
	return ( phyllotaxis.generate_VisualSequence_prim_id2abs_angle( self.get_input( "SnowAndSnowModelResult" )["prim2init_pos"]), )


class NodeRelTimeVisualisation( Node ):
    def __init__( self ):
	Node.__init__( self )
	self.add_input( name= "SnowAndSnowModelResult", interface=None)

	self.add_output( name="VisualSequence", interface=None)
        
    def __call__( self, inputs ):
	return (  phyllotaxis.generate_VisualSequence_prim_id2rel_time( self.get_input( "SnowAndSnowModelResult" )["prim2time"]) , )

class NodeAbsTimeVisualisation( Node ):
    def __init__( self ):
	Node.__init__( self )
	self.add_input( name= "SnowAndSnowModelResult", interface=None)

	self.add_output( name="VisualSequence", interface=None)
        
    def __call__( self, inputs ):
	return (  phyllotaxis.generate_VisualSequence_prim_id2abs_time( self.get_input( "SnowAndSnowModelResult" )["prim2time"]) , )
    
