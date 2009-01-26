import sys
sys.path.append("core/src/")
from core import Node,GUINode

n=GUINode(Node())
print n.title()
print n.string_representation()
