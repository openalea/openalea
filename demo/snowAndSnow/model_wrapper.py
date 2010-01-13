__license__ = "Cecill-C"
__revision__ = " $Id$ "


	
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


from openalea.core import Node
from openalea.core.interface import IBool, IFloat, IInt, IStr, IDict
from openalea.core.traitsui import View, Item, Group
import model as m
import phyllotaxis as phyllotaxis
import openalea.plotools.plotable as plotable


class NodeModel(object):
    def __init__( self, **kargs ):
        self.model = m.DiscInhibitorPhyllotaxisModel(visualisation=True)#None
        
    def __call__( self, gamma, nbr_prims, discretisation, visualisation, cont_sim, prim_inh ):
        if not cont_sim:
            self.model = m.DiscInhibitorPhyllotaxisModel(visualisation=visualisation)
        self.model.c_prim_size = gamma
        self.model.c_discretization = discretisation
        if prim_inh:
            self.model.c_show_inhibition_fields = True
            self.model.c_show_primordia = False
        else:
            self.model.c_show_inhibition_fields = False
            self.model.c_show_primordia = True
            
        self.model.run(nbr_prims)
        print  "current_prim: ",self.model.current_prim
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
    
