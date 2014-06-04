koch_curve = Model("koch_curve")

axialtree, = koch_curve()
world["koch_axialtree"] = axialtree

axialtree2, = koch_curve("_(0.001)-(90)/ (45)F(1)")
world["koch_axialtree2"] = axialtree2