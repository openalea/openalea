from algo import *

m = Model("06-simple-differentiation")

def step():
	m.step()
	g = to_mtg(m)
	print count(g,'A')
	#g.display()

def init():
    m.init()