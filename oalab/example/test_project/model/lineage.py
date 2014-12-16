
graph = applet('LineageViewer').graph
space = 30
n0 = graph.new_vertex(position=(-2*space,0))
n1 = graph.new_vertex(position=(-1*space,0))

branch1 = []
branch2 = []

prev=n1
for i in range(5):
    node = graph.new_vertex(position=(i*space,1*space))
    graph.new_edge(prev, node)
    prev = node
    branch1.append(node)

prev=n1
for i in range(5):
    node = graph.new_vertex(position=(i*space,-1*space))
    graph.new_edge(prev, node)
    prev = node
    branch2.append(node)

graph.new_edge(n0, n1)
graph.new_edge(n1, branch1[0])
graph.new_edge(n1, branch2[0])