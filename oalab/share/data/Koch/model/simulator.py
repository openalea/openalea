koch_curve = Model("koch_curve")

CURVE = True

if CURVE:
    lstring_curve = koch_curve()
    world["koch_curve"] = lstring_curve
else:
    lstring_flake = koch_curve("_(0.001)F(1)-(90)F(1)-(90)F(1)-(90)F(1)")
    world["koch_flake"] = lstring_flake
