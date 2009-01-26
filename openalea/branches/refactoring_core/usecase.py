import sys
sys.path.append("core/src/")
from core import DataFlow,Node,GUINode,GUIEmptyNode,EmptyNode,DataNode

n=GUIEmptyNode()
print n.title()
print n.string_representation()

class AddNode (Node) :
	"""
	this node make the sum of all his inputs
	"""
	name="add"
	description="""add the two operands"""
	
	def __init__ (self) :
		Node.__init__(self)
		self.add_input("val1")
		self.add_input("val2")
		self.add_output("res")
	
	def __call__ (self, input_values) :
		return (sum(input_values),)
	
	def result (self) :
		return self.output(port_name="res")

#usecase
df=DataFlow()
v1=df.add_node(DataNode(15.))
v2=df.add_node(DataNode(3.))
add=df.add_node(AddNode())
e1=df.add_node(EmptyNode())

df.connect(v1,0,e1,0)
df.connect(e1,0,add,0)
df.connect(v2,0,add,1)

df.run()
print df.node(add).result()

