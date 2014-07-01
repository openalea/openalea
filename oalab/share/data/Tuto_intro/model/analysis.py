from openalea.mtg.io import lpy2mtg, mtg2lpy, axialtree2mtg, mtg2axialtree
def to_mtg(model):
    scales = {}
    scales['P'] = 1
    scales['A'] =1
    scales['I'] = 1
    scales['B'] = 1

    params ={}
    params['P'] = ['age']
    params['A'] = ['age']
    params['I'] = ['age']
	
    g = axialtree2mtg(m.axialtree, scales, None, params)
    return g
    
    
m = Model("06-simple-differentiation")

def step():
	m.step()
	g = to_mtg(m)
	print count(g,'A')
	#g.display()

def count(g, label):
    return len([v for v in g if g.label(v) == label])

